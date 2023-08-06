import os
import pathlib
import numpy as np
import pandas as pd

from py_neuromodulation import \
    (nm_projection,
    nm_rereference,
    nm_run_analysis,
    nm_features,
    nm_resample,
    nm_stream, nm_test_settings)


class RealTimePyNeuro(nm_stream.PNStream):

    def __init__(self,
        PATH_SETTINGS=...,
        PATH_NM_CHANNELS: str = ...,
        PATH_OUT: str = ...,
        PATH_GRIDS: str = ...,
        VERBOSE: bool = ...,
        fs: int = 128,
        line_noise: int = 50) -> None:

        super().__init__(PATH_SETTINGS=PATH_SETTINGS,
            PATH_NM_CHANNELS=PATH_NM_CHANNELS,
            PATH_OUT=PATH_OUT,
            PATH_GRIDS=PATH_GRIDS,
            VERBOSE=VERBOSE)

        self.set_fs(fs)
        self.set_linenoise(line_noise)
        self.set_channels(self.PATH_NM_CHANNELS)

        self.set_run()

    def run(self, ieeg_batch: np.array) -> pd.Series:
        self.run_analysis.run(ieeg_batch)

        # return last estimated data batch by run_analysis
        self.df_features.append(self.run_analysis.feature_arr.iloc[-1, :])

    def add_coordinates(self):
        """Lateron add here method for providing coordinates"""
        pass