import logging
import os
import shutil
import sys
from multiprocessing import Pool

import keras
import pandas as pd
import lightkurve as lk
import foldedleastsquares as tls
import matplotlib.pyplot as plt
import astropy.units as u
import requests
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astroquery.mast import Catalogs, Tesscut
from keras import Sequential
from keras.layers import Conv1D, Dropout, MaxPooling1D, Flatten, Dense, Embedding, LSTM

from sherlockpipe.ois.OisManager import OisManager

from lcbuilder.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from lcbuilder.objectinfo.preparer.MissionFfiLightcurveBuilder import MissionFfiLightcurveBuilder
from lcbuilder.objectinfo.MissionObjectInfo import MissionObjectInfo
from lcbuilder.objectinfo.preparer.MissionLightcurveBuilder import MissionLightcurveBuilder
from lcbuilder.eleanor import TargetData
from lcbuilder import eleanor
from lcbuilder.star.TicStarCatalog import TicStarCatalog
import numpy as np
import tsfresh
from tsfresh.utilities.dataframe_functions import impute

class MlTrainingSetPreparer:
    SECTOR_URL = "https://tess.mit.edu/wp-content/uploads/all_targets_S0{:02}_v1.csv"

    def __init__(self, dir, cache_dir):
        self.cache_dir = cache_dir
        self.cache_dir_eleanor = cache_dir + "/.eleanor/"
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        if not os.path.exists(self.cache_dir_eleanor):
            os.mkdir(cache_dir + ".eleanor")
        if not os.path.exists(self.cache_dir_eleanor + "/metadata"):
            os.mkdir(cache_dir + ".eleanor/metadata")
        self.dir = dir
        if not os.path.exists(dir):
            os.mkdir(dir)
        file_dir = dir + "/ml.log"
        if os.path.exists(file_dir):
            os.remove(file_dir)
        formatter = logging.Formatter('%(message)s')
        logger = logging.getLogger()
        while len(logger.handlers) > 0:
            logger.handlers.pop()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler(file_dir)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.positive_dir = dir + "/tp/"
        self.negative_dir = dir + "/ntp/"
        self.false_positive_dir = dir + "/fp/"
        if not os.path.isdir(dir):
            os.mkdir(dir)
        if not os.path.isdir(self.positive_dir):
            os.mkdir(self.positive_dir)
        if not os.path.isdir(self.negative_dir):
            os.mkdir(self.negative_dir)
        if not os.path.isdir(self.false_positive_dir):
            os.mkdir(self.false_positive_dir)
        for sector in range(1, 53):
            try:
                logging.info("Updating ELEANOR sector " + str(sector))
                eleanor.Update(sector, self.cache_dir_eleanor)
            except Exception as e:
                logging.warning("Could not update sector due to exception. Continuing...")
                logging.debug(e, exc_info=True)

    def download_neighbours(self, ID: int, sectors: np.ndarray, search_radius: int = 10):
        """
        Queries TIC for sources near the target and obtains a cutout
        of the pixels enclosing the target.
        Args:
            ID (int): TIC ID of the target.
            sectors (numpy array): Sectors in which the target
                                   has been observed.
            search_radius (int): Number of pixels from the target
                                 star to search.
        """
        ID = ID
        sectors = sectors
        search_radius = search_radius
        N_pix = 2 * search_radius + 2
        # query TIC for nearby stars
        pixel_size = 20.25 * u.arcsec
        df = Catalogs.query_object(
            str(ID),
            radius=search_radius * pixel_size,
            catalog="TIC"
        )
        new_df = df[
            "ID", "Tmag", "ra", "dec", "mass", "rad", "Teff", "plx"
        ]
        stars = new_df.to_pandas()

        TESS_images = []
        col0s, row0s = [], []
        pix_coords = []
        # for each sector, get FFI cutout and transform RA/Dec into
        # TESS pixel coordinates
        for j, sector in enumerate(sectors):
            Tmag = stars["Tmag"].values
            ra = stars["ra"].values
            dec = stars["dec"].values
            cutout_coord = SkyCoord(ra[0], dec[0], unit="deg")
            cutout_hdu = Tesscut.get_cutouts(cutout_coord, size=N_pix, sector=sector)[0]
            cutout_table = cutout_hdu[1].data
            hdu = cutout_hdu[2].header
            wcs = WCS(hdu)
            TESS_images.append(np.mean(cutout_table["FLUX"], axis=0))
            col0 = cutout_hdu[1].header["1CRV4P"]
            row0 = cutout_hdu[1].header["2CRV4P"]
            col0s.append(col0)
            row0s.append(row0)

            pix_coord = np.zeros([len(ra), 2])
            for i in range(len(ra)):
                RApix = np.asscalar(
                    wcs.all_world2pix(ra[i], dec[i], 0)[0]
                )
                Decpix = np.asscalar(
                    wcs.all_world2pix(ra[i], dec[i], 0)[1]
                )
                pix_coord[i, 0] = col0 + RApix
                pix_coord[i, 1] = row0 + Decpix
            pix_coords.append(pix_coord)

        # for each star, get the separation and position angle
        # from the targets star
        sep = [0]
        pa = [0]
        c_target = SkyCoord(
            stars["ra"].values[0],
            stars["dec"].values[0],
            unit="deg"
        )
        for i in range(1, len(stars)):
            c_star = SkyCoord(
                stars["ra"].values[i],
                stars["dec"].values[i],
                unit="deg"
            )
            sep.append(
                np.round(
                    c_star.separation(c_target).to(u.arcsec).value,
                    3
                )
            )
            pa.append(
                np.round(
                    c_star.position_angle(c_target).to(u.deg).value,
                    3
                )
            )
        stars["sep (arcsec)"] = sep
        stars["PA (E of N)"] = pa

        stars = stars
        TESS_images = TESS_images
        col0s = col0s
        row0s = row0s
        pix_coords = pix_coords
        return stars

    def prepare_tic(self, prepare_tic_input):
        tic_id = str(prepare_tic_input.tic)
        target_dir = prepare_tic_input.dir + tic_id + "/"
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        lc_short = None
        failed_target = None
        try:
            mission_lightcurve_builder = MissionLightcurveBuilder()
            mission_ffi_lightcurve_builder = MissionFfiLightcurveBuilder()
        except Exception as e:
            failed_target = tic_id
            logging.exception(e)
        try:
            logging.info("Trying to get short cadence info for " + str(prepare_tic_input.tic))
            lcbuild_short = \
                mission_lightcurve_builder.build(MissionObjectInfo(tic_id, 'all'), None, self.cache_dir)
            lc_short = lcbuild_short.lc
            lc_data = lcbuild_short.lc_data
            lc_data["centroids_x"] = lc_data["centroids_x"] - np.nanmedian(lc_data["centroids_x"])
            lc_data["centroids_y"] = lc_data["centroids_y"] - np.nanmedian(lc_data["centroids_y"])
            lc_data["motion_x"] = lc_data["motion_x"] - np.nanmedian(lc_data["motion_x"])
            lc_data["motion_y"] = lc_data["motion_y"] - np.nanmedian(lc_data["motion_y"])
            lc_data.to_csv(target_dir + "time_series_short.csv")
            tpf_short = lk.search_targetpixelfile(tic_id, cadence="short", author="spoc").download_all(
                download_dir=self.cache_dir + ".lightkurve-cache")
            short_periodogram = lc_short.to_periodogram(oversample_factor=5)
            periodogram_df = pd.DataFrame(columns=['period', 'power'])
            periodogram_df["period"] = short_periodogram.period.value
            periodogram_df["power"] = short_periodogram.power.value
            periodogram_df.to_csv(target_dir + "periodogram_short.csv")
        except Exception as e:
            logging.warning("No Short Cadence data for target " + str(prepare_tic_input.tic))
            logging.exception(e)
        logging.info("Trying to get long cadence info for " + str(prepare_tic_input.tic))
        try:
            lcbuild_long = \
                mission_ffi_lightcurve_builder.build(MissionFfiIdObjectInfo(tic_id, 'all'), None,
                                                     self.cache_dir)
            star_df = pd.DataFrame(columns=['obj_id', 'ra', 'dec', 'R_star', 'R_star_lerr', 'R_star_uerr', 'M_star',
                                                'M_star_lerr', 'M_star_uerr', 'Teff_star', 'Teff_star_lerr',
                                                'Teff_star_uerr', 'ld_a', 'ld_b'])
            ld_a = lcbuild_long.star_info.ld_coefficients[0] if lcbuild_long.star_info.ld_coefficients is not None else None
            ld_b = lcbuild_long.star_info.ld_coefficients[1] if lcbuild_long.star_info.ld_coefficients is not None else None
            star_df = star_df.append(
                {'obj_id': tic_id, 'ra': lcbuild_long.star_info.ra, 'dec': lcbuild_long.star_info.dec,
                 'R_star': lcbuild_long.star_info.radius,
                 'R_star_lerr': lcbuild_long.star_info.radius - lcbuild_long.star_info.radius_min,
                 'R_star_uerr': lcbuild_long.star_info.radius_max - lcbuild_long.star_info.radius,
                 'M_star': lcbuild_long.star_info.mass, 'M_star_lerr': lcbuild_long.star_info.mass - lcbuild_long.star_info.mass_min,
                 'M_star_uerr': lcbuild_long.star_info.mass_max - lcbuild_long.star_info.mass,
                 'Teff_star': lcbuild_long.star_info.teff, 'Teff_star_lerr': 200, 'Teff_star_uerr': 200,
                 'logg': lcbuild_long.star_info.logg, 'logg_err': lcbuild_long.star_info.logg_err,
                 'ld_a': ld_a, 'ld_b': ld_b,
                 'feh': lcbuild_long.star_info.feh,
                 'feh_err': lcbuild_long.star_info.feh_err, 'v': lcbuild_long.star_info.v, 'v_err': lcbuild_long.star_info.v_err,
                 'j': lcbuild_long.star_info.j, 'j_err': lcbuild_long.star_info.j_err,
                 'k': lcbuild_long.star_info.k, 'k_err': lcbuild_long.star_info.k_err,
                 'h': lcbuild_long.star_info.h, 'h_err': lcbuild_long.star_info.h_err,
                 'kp': lcbuild_long.star_info.kp},
                ignore_index=True)
            star_df.to_csv(target_dir + "params_star.csv", index=False)
            sectors = lcbuild_long.sectors
            lc_long = lcbuild_long.lc
            lc_data = lcbuild_long.lc_data
            lc_data["centroids_x"] = lc_data["centroids_x"] - np.nanmedian(lc_data["centroids_x"])
            lc_data["centroids_y"] = lc_data["centroids_y"] - np.nanmedian(lc_data["centroids_y"])
            lc_data["motion_x"] = lc_data["motion_x"] - np.nanmedian(lc_data["motion_x"])
            lc_data["motion_y"] = lc_data["motion_y"] - np.nanmedian(lc_data["motion_y"])
            lc_data.to_csv(target_dir + "time_series_long.csv")
            lcf_long = lc_long.remove_nans()
            tpf_long = lk.search_targetpixelfile(tic_id, cadence="long", author="tess-spoc")\
                .download_all(download_dir=self.cache_dir + ".lightkurve-cache")
            tpfs_dir = target_dir + "tpfs/"
            if not os.path.exists(tpfs_dir):
                os.mkdir(tpfs_dir)
            for tpf in tpf_long.data:
                shutil.copy(tpf.path, tpfs_dir + os.path.basename(tpf.path))
            long_periodogram = lc_long.to_periodogram(oversample_factor=5)
            periodogram_df = pd.DataFrame(columns=['period', 'power'])
            periodogram_df["period"] = long_periodogram.period.value
            periodogram_df["power"] = long_periodogram.power.value
            periodogram_df.to_csv(target_dir + "periodogram_long.csv")
            logging.info("Downloading neighbour stars for " + prepare_tic_input.tic)
            #TODO get neighbours light curves stars = self.download_neighbours(prepare_tic_input.tic, sectors)
            logging.info("Classifying candidate points for " + prepare_tic_input.tic)
            target_ois = prepare_tic_input.target_ois[
                (prepare_tic_input.target_ois["Disposition"] == "CP") |
                (prepare_tic_input.target_ois["Disposition"] == "KP")]
            target_ois_df = pd.DataFrame(
                columns=['id', 'name', 'period', 'period_err', 't0', 'to_err', 'depth', 'depth_err', 'duration',
                         'duration_err'])
            tags_series_short = np.full(len(lc_short.time), "BL")
            tags_series_long = np.full(len(lc_long.time), "BL")
            if prepare_tic_input.label is not None:
                for index, row in target_ois.iterrows():
                    if row["OI"] not in prepare_tic_input.excluded_ois:
                        logging.info("Classifying candidate points with OI %s, period %s, t0 %s and duration %s for " + prepare_tic_input.tic,
                                     row["OI"], row["Period (days)"], row["Epoch (BJD)"], row["Duration (hours)"])
                        target_ois_df = target_ois_df.append(
                            {"id": row["Object Id"], "name": row["OI"], "period": row["Period (days)"],
                             "period_err": row["Period (days) err"], "t0": row["Epoch (BJD)"] - 2457000.0,
                             "to_err": row["Epoch (BJD) err"], "depth": row["Depth (ppm)"],
                             "depth_err": row["Depth (ppm) err"], "duration": row["Duration (hours)"],
                             "duration_err": row["Duration (hours) err"]}, ignore_index=True)
                        if lc_short is not None:
                            mask_short = tls.transit_mask(lc_short.time.value, row["Period (days)"],
                                                          row["Duration (hours)"] / 24, row["Epoch (BJD)"] - 2457000.0)
                            tags_series_short[mask_short] = prepare_tic_input.label
                        mask_long = tls.transit_mask(lc_long.time.value, row["Period (days)"], row["Duration (hours)"] / 24,
                                                     row["Epoch (BJD)"] - 2457000.0)
                        tags_series_long[mask_long] = prepare_tic_input.label
                for index, row in prepare_tic_input.target_additional_ois_df.iterrows():
                    if row["OI"] not in prepare_tic_input.excluded_ois:
                        target_ois_df = target_ois_df.append(
                            {"id": row["Object Id"], "name": row["OI"], "period": row["Period (days)"],
                             "period_err": row["Period (days) err"], "t0": row["Epoch (BJD)"] - 2457000.0,
                             "to_err": row["Epoch (BJD) err"], "depth": row["Depth (ppm)"],
                             "depth_err": row["Depth (ppm) err"], "duration": row["Duration (hours)"],
                             "duration_err": row["Duration (hours) err"]}, ignore_index=True)
                        if lc_short is not None:
                            mask_short = tls.transit_mask(lc_short.time.value, row["Period (days)"],
                                                          row["Duration (hours)"] / 24, row["Epoch (BJD)"] - 2457000.0)
                            tags_series_short[mask_short] = prepare_tic_input.label
                        mask_long = tls.transit_mask(lc_long.time.value, row["Period (days)"], row["Duration (hours)"] / 24,
                                                     row["Epoch (BJD)"] - 2457000.0)
                        tags_series_long[mask_long] = prepare_tic_input.label
            if lc_short is not None:
                lc_classified_short = pd.DataFrame.from_dict(
                    {"time": lc_short.time.value, "flux": lc_short.flux.value, "tag": tags_series_short})
                lc_classified_short.to_csv(target_dir + "lc_classified_short.csv")
            lc_classified_long = pd.DataFrame.from_dict(
                {"time": lc_long.time.value, "flux": lc_long.flux.value, "tag": tags_series_long})
            lc_classified_long.to_csv(target_dir + "lc_classified_long.csv")
            # TODO store folded light curves -with local and global views-(masking previous candidates?)
        except Exception as e:
            failed_target = tic_id
            logging.exception(e)
        return failed_target

    def prepare_positive_tic(self, prepare_tic_input):
        return self.prepare_tic(prepare_tic_input)

    def prepare_false_positive_tic(self, prepare_tic_input):
        return self.prepare_tic(prepare_tic_input)

    def prepare_negative_tic(self, prepare_tic_input):
        return self.prepare_tic(prepare_tic_input)

    def prepare_positive_training_dataset(self, cpus):
        logging.info("Preparing positives")
        # TODO do the same for negative targets
        ois = OisManager(self.cache_dir).load_ois()
        ois = ois[(ois["Disposition"] == "CP") | (ois["Disposition"] == "KP")]
        # TODO fill excluded_ois from given csv file
        excluded_ois = {}
        # TODO fill additional_ois from given csv file with their ephemeris
        additional_ois_df = pd.DataFrame(columns=['Object Id', 'name', 'period', 'period_err', 't0', 'to_err', 'depth',
                                                  'depth_err', 'duration', 'duration_err'])
        failed_targets_df = pd.DataFrame(columns=["Object Id"])
        inputs = []
        for tic in ois["Object Id"].unique():
            logging.info("Preparing positive input data for " + str(tic))
            target_ois = ois[ois["Object Id"] == str(tic)]
            target_additional_ois_df = additional_ois_df[additional_ois_df["Object Id"] == str(tic)]
            inputs.append(PrepareTicInput(self.positive_dir, tic, target_ois,
                                          target_additional_ois_df, excluded_ois, "TP"))
        with Pool(processes=cpus) as pool:
            failed_targets = pool.map(self.prepare_tic, inputs)
        failed_targets = [failed_target for failed_target in failed_targets if failed_target]
        failed_targets_df['Object Id'] = failed_targets
        failed_targets_df.to_csv(self.dir + "failed_targets_positive.csv", index=False)

    def prepare_false_positive_training_dataset(self, cpus):
        # TODO do the same for negative targets
        logging.info("Preparing false positives")
        ois = OisManager(self.cache_dir).load_ois()
        ois = ois[(ois["Disposition"] == "FP")]
        # TODO fill excluded_ois from given csv file
        excluded_ois = {}
        # TODO fill additional_ois from given csv file with their ephemeris
        additional_ois_df = pd.DataFrame(columns=['Object Id', 'name', 'period', 'period_err', 't0', 'to_err', 'depth',
                                                  'depth_err', 'duration', 'duration_err'])
        failed_targets_df = pd.DataFrame(columns=["Object Id"])
        inputs = []
        for tic in ois["Object Id"].unique():
            logging.info("Preparing false positive input data for " + str(tic))
            target_ois = ois[ois["Object Id"] == str(tic)]
            target_additional_ois_df = additional_ois_df[additional_ois_df["Object Id"] == str(tic)]
            inputs.append(PrepareTicInput(self.false_positive_dir, tic, target_ois,
                                          target_additional_ois_df, excluded_ois, "FP"))
        with Pool(processes=cpus) as pool:
            failed_targets = pool.map(self.prepare_false_positive_tic, inputs)
        failed_targets = [failed_target for failed_target in failed_targets if failed_target]
        failed_targets_df['Object Id'] = failed_targets
        failed_targets_df.to_csv(self.dir + "failed_targets_false_positive.csv", index=False)

    def prepare_negative_training_dataset(self, first_sector, cpus):
        logging.info("Preparing negatives")
        # TODO do the same for negative targets
        ois = OisManager(self.cache_dir).load_ois()
        # TODO fill excluded_ois from given csv file
        excluded_ois = {}
        # TODO fill additional_ois from given csv file with their ephemeris
        additional_ois_df = pd.DataFrame(columns=['Object Id', 'name', 'period', 'period_err', 't0', 'to_err', 'depth',
                                                  'depth_err', 'duration', 'duration_err'])
        failed_targets_df = pd.DataFrame(columns=["Object Id"])
        inputs = []
        failed_targets = []
        for sector in np.arange(first_sector, 27, 1):
            self.negative_dir = self.dir + "/ntp/" + str(sector)
            if not os.path.exists(self.negative_dir):
                os.mkdir(self.negative_dir)
            sector_url = self.SECTOR_URL.format(sector)
            logging.info("Preparing negatives for sector from url " + sector_url)
            sector_file = "sector.csv"
            tic_csv = open(sector_file, 'wb')
            request = requests.get(sector_url)
            tic_csv.write(request.content)
            tic_csv.close()
            tics_sector_df = pd.read_csv(sector_file, comment='#', sep=',')
            tics_sector_df = tics_sector_df.sample(n=50, random_state=0)
            os.remove(sector_file)
            tics_sector_df["TICID"] = "TIC " + tics_sector_df["TICID"].map(str)
            for tic in tics_sector_df["TICID"].unique():
                logging.info("Preparing negative input data for " + str(tic))
                if tic in ois["Object Id"]:
                    logging.warning(str(tic) + " has official candidates!")
                    continue
                target_additional_ois_df = additional_ois_df[additional_ois_df["Object Id"] == str(tic)]
                inputs.append(PrepareTicInput(self.negative_dir, tic, ois,
                                              target_additional_ois_df, excluded_ois, None))
            with Pool(processes=cpus) as pool:
                failed_targets_sector = pool.map(self.prepare_negative_tic, inputs)
            failed_targets_sector = [failed_target for failed_target in failed_targets_sector if failed_target]
            failed_targets.extend(failed_targets_sector)
        failed_targets_df['Object Id'] = failed_targets
        failed_targets_df.to_csv(self.dir + "failed_targets_negative.csv", index=False)

    def prepare_tsfresh(self, positive_dir, negative_dir):
        tsfresh_short_df = pd.DataFrame(columns=['id', 'time', 'flux', 'flux_err', 'background_flux', 'quality', 'centroids_x',
                                           'centroids_y', 'motion_x', 'motion_y'])
        tsfresh_long_df = pd.DataFrame(columns=['id', 'time', 'flux', 'flux_err', 'background_flux', 'quality', 'centroids_x',
                                           'centroids_y', 'motion_x', 'motion_y'])
        tsfresh_tags_short = []
        tsfresh_tags_long = []
        for tic_dir in os.listdir(positive_dir):
            short_lc_dir = positive_dir + "/" + tic_dir + "/time_series_short.csv"
            if os.path.exists(short_lc_dir):
                lc_short_df = pd.read_csv(positive_dir + "/" + tic_dir + "/time_series_short.csv")
                lc_short_df['id'] = tic_dir
                tsfresh_short_df.append(lc_short_df)
                tsfresh_tags_short.append([tic_dir, 1])
            lc_long_df = pd.read_csv(positive_dir + "/" + tic_dir + "/time_series_long.csv")
            lc_long_df['id'] = tic_dir
            tsfresh_long_df.append(lc_long_df)
            tsfresh_tags_long.append([tic_dir, 1])
        for tic_dir in os.listdir(negative_dir):
            short_lc_dir = negative_dir + "/" + tic_dir + "/time_series_short.csv"
            if os.path.exists(short_lc_dir):
                lc_short_df = pd.read_csv(negative_dir + "/" + tic_dir + "/time_series_short.csv")
                lc_short_df['id'] = tic_dir
                tsfresh_short_df.append(lc_short_df)
                tsfresh_tags_short.append([tic_dir, 1])
            lc_long_df = pd.read_csv(negative_dir + "/" + tic_dir + "/time_series_long.csv")
            lc_long_df['id'] = tic_dir
            tsfresh_long_df.append(lc_long_df)
            tsfresh_tags_long.append([tic_dir, 0])
        tsfresh_tags_short = pd.Series(tsfresh_tags_short)
        tsfresh_tags_long = pd.Series(tsfresh_tags_long)
        # TODO tsfresh needs a dataframe with all the "time series" data (centroids, motion, flux, bck_flux...)
        # TODO with an id column specifying the target id and a "y" as a df containing the target ids and the classification
        # TODO tag. We need to check how to make this compatible with transit times tagging instead of entire curve
        # TODO classification. Maybe https://tsfresh.readthedocs.io/en/latest/text/forecasting.html is helpful.
        extracted_features_short = tsfresh.extract_relevant_features(tsfresh_short_df, tsfresh_tags_short, column_id='id',
                                                                     column_sort='time')
        extracted_features_long = tsfresh.extract_relevant_features(tsfresh_long_df, tsfresh_tags_long, column_id='id',
                                                                    column_sort='time')

def get_flux_branch(name):
    flux_input = keras.Input(shape=(2500, 7),
                             name=name)  # (flux, detrended_flux1... detrended_flux5, flux_model) flux model by transit params and stellar params
    flux_branch = keras.layers.SpatialDropout1D(rate=0.2)(flux_input)
    flux_branch = keras.layers.Conv1D(filters=128, kernel_size=9, activation="relu")(flux_branch)
    flux_branch = keras.layers.MaxPooling1D(pool_size=10, strides=6)(flux_branch)
    flux_branch = keras.layers.Dropout(rate=0.1)(flux_branch)
    flux_branch = keras.layers.Conv1D(filters=64, kernel_size=7, activation="relu")(flux_branch)
    flux_branch = keras.layers.MaxPooling1D(pool_size=4, strides=3)(flux_branch)
    flux_branch = keras.layers.Conv1D(filters=32, kernel_size=5, activation="relu")(flux_branch)
    flux_branch = keras.layers.MaxPooling1D(pool_size=3, strides=3)(flux_branch)
    flux_branch = keras.layers.Conv1D(filters=16, kernel_size=3, activation="relu")(flux_branch)
    flux_branch = keras.layers.MaxPooling1D(pool_size=2, strides=2)(flux_branch)
    return flux_input, flux_branch

def get_centroids_bck_branch(name):
    centroids_motion_bck_input = keras.Input(shape=(2500, 5), name=name)
    centroids_motion_bck_branch = keras.layers.SpatialDropout1D(rate=0.2)(centroids_motion_bck_input)
    centroids_motion_bck_branch = keras.layers.Conv1D(filters=128, kernel_size=9, activation="relu")(
        centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.MaxPooling1D(pool_size=10, strides=6)(centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.Dropout(rate=0.1)(centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.Conv1D(filters=64, kernel_size=7, activation="relu")(
        centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.MaxPooling1D(pool_size=4, strides=3)(centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.Conv1D(filters=32, kernel_size=5, activation="relu")(
        centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.MaxPooling1D(pool_size=3, strides=3)(centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.Conv1D(filters=16, kernel_size=3, activation="relu")(
        centroids_motion_bck_branch)
    centroids_motion_bck_branch = keras.layers.MaxPooling1D(pool_size=2, strides=2)(centroids_motion_bck_branch)
    return centroids_motion_bck_input, centroids_motion_bck_branch

def get_flux_model_branch():
    flux_input, flux_branch = get_flux_branch("global_flux_branch")
    centroids_input, centroids_branch = get_centroids_bck_branch("global_centroids_bck_branch")
    flux_centroids_branch = keras.layers.concatenate([flux_branch, centroids_branch])
    flux_centroids_branch = keras.layers.Dense(16, activation="relu")(flux_centroids_branch)
    flux_centroids_branch = keras.Model(inputs=[flux_input, centroids_input], outputs=flux_centroids_branch)
    return flux_centroids_branch

def get_focus_flux_branch(name):
    focus_flux_input = keras.Input(shape=(500, 7),
                                   name=name)  # (flux, detrended_flux1... detrended_flux5, flux_model) flux model by transit params and stellar params
    focus_flux_branch = keras.layers.SpatialDropout1D(rate=0.2)(focus_flux_input)
    focus_flux_branch = keras.layers.Conv1D(filters=64, kernel_size=5, activation="relu", use_bias=True)(focus_flux_branch)
    focus_flux_branch = keras.layers.MaxPooling1D(pool_size=5, strides=3)(focus_flux_branch)
    focus_flux_branch = keras.layers.Dropout(rate=0.1)(focus_flux_branch)
    focus_flux_branch = keras.layers.Conv1D(filters=32, kernel_size=3, activation="relu", use_bias=True)(focus_flux_branch)
    focus_flux_branch = keras.layers.MaxPooling1D(pool_size=3, strides=3)(focus_flux_branch)
    focus_flux_branch = keras.layers.Dense(16, activation="relu")(focus_flux_branch)
    return focus_flux_input, focus_flux_branch

def get_centroids_bck_focus_branch(name):
    focus_centroids_motion_bck_input = keras.Input(shape=(500, 5), name=name)
    focus_centroids_motion_bck_branch = keras.layers.SpatialDropout1D(rate=0.2)(focus_centroids_motion_bck_input)
    focus_centroids_motion_bck_branch = keras.layers.Conv1D(filters=64, kernel_size=3, activation="relu")(
        focus_centroids_motion_bck_branch)
    focus_centroids_motion_bck_branch = keras.layers.MaxPooling1D(pool_size=5, strides=3)(focus_centroids_motion_bck_branch)
    focus_centroids_motion_bck_branch = keras.layers.Dropout(rate=0.1)(focus_centroids_motion_bck_branch)
    focus_centroids_motion_bck_branch = keras.layers.Conv1D(filters=32, kernel_size=3, activation="relu")(
        focus_centroids_motion_bck_branch)
    focus_centroids_motion_bck_branch = keras.layers.MaxPooling1D(pool_size=3, strides=3)(focus_centroids_motion_bck_branch)
    return focus_centroids_motion_bck_input, focus_centroids_motion_bck_branch

def get_focus_flux_model_branch():
    odd_flux_input, odd_flux_branch = get_focus_flux_branch("focus_odd_flux_branch")
    even_flux_input, even_flux_branch = get_focus_flux_branch("focus_even_flux_branch")
    harmonic_odd_flux_input, harmonic_odd_flux_branch = get_focus_flux_branch("focus_harmnic_odd_flux_branch")
    harmonic_even_flux_input, harmonic_even_flux_branch = get_focus_flux_branch("focus_harmonic_even_flux_branch")
    subharmonic_odd_flux_input, subharmonic_odd_flux_branch = get_focus_flux_branch("focus_subharmonic_odd_flux_branch")
    subharmonic_even_flux_input, subharmonic_even_flux_branch = get_focus_flux_branch("focus_subharmonic_even_flux_branch")
    odd_centroids_input, odd_centroids_bck_branch = get_centroids_bck_focus_branch("focus_odd_centroids_bck_branch")
    even_centroids_input, even_centroids_bck_branch = get_centroids_bck_focus_branch("focus_even_centroids_bck_branch")
    odd_harmonic_centroids_input, odd_harmonic_centroids_bck_branch = get_centroids_bck_focus_branch("focus_odd_harmonic_centroids_bck_branch")
    even_harmonic_centroids_input, even_harmonic_centroids_bck_branch = get_centroids_bck_focus_branch("focus_even_harmonic_centroids_bck_branch")
    odd_subharmonic_centroids_input, odd_subharmonic_centroids_bck_branch = get_centroids_bck_focus_branch("focus_odd_subharmonic_centroids_bck_branch")
    even_subharmonic_centroids_input, even_subharmonic_centroids_bck_branch = get_centroids_bck_focus_branch("focus_even_subharmonic_centroids_bck_branch")
    odd_flux_branch = keras.layers.concatenate([odd_flux_branch, harmonic_odd_flux_branch, subharmonic_odd_flux_branch])
    even_flux_branch = keras.layers.concatenate([even_flux_branch, harmonic_even_flux_branch, subharmonic_even_flux_branch])
    odd_centroids_bck_branch = keras.layers.concatenate([odd_centroids_bck_branch, odd_harmonic_centroids_bck_branch, odd_subharmonic_centroids_bck_branch])
    even_centroids_bck_branch = keras.layers.concatenate([even_centroids_bck_branch, even_harmonic_centroids_bck_branch, even_subharmonic_centroids_bck_branch])
    odd_flux_branch = keras.layers.Dense(16, activation="relu")(odd_flux_branch)
    odd_flux_branch = keras.layers.Dropout(rate=0.1)(odd_flux_branch)
    even_flux_branch = keras.layers.Dense(16, activation="relu")(even_flux_branch)
    even_flux_branch = keras.layers.Dropout(rate=0.1)(even_flux_branch)
    odd_centroids_bck_branch = keras.layers.Dense(16, activation="relu")(odd_centroids_bck_branch)
    odd_centroids_bck_branch = keras.layers.Dropout(rate=0.1)(odd_centroids_bck_branch)
    even_centroids_bck_branch = keras.layers.Dense(16, activation="relu")(even_centroids_bck_branch)
    even_centroids_bck_branch = keras.layers.Dropout(rate=0.1)(even_centroids_bck_branch)
    odd_flux_branch = keras.layers.concatenate([odd_flux_branch, odd_centroids_bck_branch])
    even_flux_branch = keras.layers.concatenate([even_flux_branch, even_centroids_bck_branch])
    odd_flux_branch = keras.layers.Dense(32, activation="relu")(odd_flux_branch)
    even_flux_branch = keras.layers.Dense(32, activation="relu")(even_flux_branch)
    flux_branch = keras.layers.concatenate([odd_flux_branch, even_flux_branch])
    flux_branch = keras.layers.Dense(16, activation="relu")(flux_branch)
    input = [odd_flux_input, even_flux_input, harmonic_odd_flux_input, harmonic_even_flux_input,
             subharmonic_odd_flux_input, subharmonic_even_flux_input, odd_centroids_input, even_centroids_input,
             odd_harmonic_centroids_input, even_harmonic_centroids_input, odd_subharmonic_centroids_input,
             even_subharmonic_centroids_input]
    flux_branch = keras.Model(inputs=input, outputs=flux_branch)
    return flux_branch


def get_model():
    # model = Sequential()
    # model.add(Conv1D(filters=64, kernel_size=3, activation='relu', use_bias=True, input_shape=(n_timesteps, n_features)))
    # model.add(Conv1D(filters=64, kernel_size=3, activation='relu', use_bias=True))
    # model.add(Dropout(0.2))
    # model.add(MaxPooling1D(pool_size=2))
    # model.add(Flatten())
    # model.add(Dense(100, activation='relu'))
    # model.add(Dense(3, activation='softmax'))
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    stellar_model_input = keras.Input(shape=(6, 1), name="stellar_model") #TODO
    stellar_model_branch = keras.layers.Dense(16, activation="relu", name="stellar-first")(stellar_model_input)
    stellar_model_branch = keras.layers.Dropout(rate=0.1, name="stellar-first-dropout-0.1")(stellar_model_branch)
    stellar_model_branch = keras.layers.Dense(16, activation="relu", name="stellar-refinement")(stellar_model_branch)
    flux_model_branch = get_flux_model_branch()
    focus_flux_model_branch = get_focus_flux_model_branch()
    final_branch = keras.layers.concatenate([stellar_model_branch, flux_model_branch.output, focus_flux_model_branch.output], axis=1)
    final_branch = keras.layers.Dense(64, activation="relu", name="final-dense1")(final_branch)
    final_branch = keras.layers.Dense(16, activation="relu", name="final-dense2")(final_branch)
    final_branch = keras.layers.Dense(3, activation="softmax", name="final-dense-softmax")(final_branch)
    inputs = [stellar_model_input] + flux_model_branch.inputs + focus_flux_model_branch.inputs
    model = keras.Model(inputs=inputs, outputs=final_branch, name="mnist_model")
    keras.utils.vis_utils.plot_model(model, "multi_input_and_output_model.png", show_shapes=True)


class PrepareTicInput:
    def __init__(self, dir, tic, target_ois, target_additional_ois_df, excluded_ois, label):
        self.dir = dir
        self.tic = tic
        self.target_ois = target_ois
        self.target_additional_ois_df = target_additional_ois_df
        self.excluded_ois = excluded_ois
        self.label = label

# cpus = 1
# first_negative_sector = 1
# ml_training_set_preparer = MlTrainingSetPreparer("training_data/", "/home/martin/")
# #ml_training_set_preparer.prepare_positive_training_dataset(cpus)
# #ml_training_set_preparer.prepare_false_positive_training_dataset(cpus)
# ml_training_set_preparer.prepare_negative_training_dataset(first_negative_sector, cpus)
get_model()
#TODO prepare_negative_training_dataset(negative_dir)
