# -*- coding: utf-8 -*-

# specclassify, A Python package for multi- or hyperspectral image classification.
#
# Copyright (C) 2019-2021
# - Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences Potsdam,
#   Germany (https://www.gfz-potsdam.de/)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functions commonly used by specclassify modules."""

import numpy as np
from typing import Union, Tuple  # noqa F401  # flake8 issue
from geoarray import GeoArray


def normalize_endmembers_image(endmembers, image):
    # type: (np.ndarray, np.ndarray) -> Tuple[np.ndarray, np.ndarray]
    from sklearn.preprocessing import MaxAbsScaler  # avoids static TLS errors here

    em = endmembers.astype(float)
    im = image.astype(float)

    # provide training values as 2D ROW (n samples x 1 feature),
    # because normalization should be applied globally, not band-by-band
    allVals = np.hstack([em.flat, im.flat]).reshape(-1, 1)

    if allVals.min() < -1 or allVals.max() > 1:
        max_abs_scaler = MaxAbsScaler()
        max_abs_scaler.fit(allVals)

        endmembers_norm = \
            max_abs_scaler \
            .transform(em.reshape(-1, 1)) \
            .reshape(em.shape)
        image_norm = \
            max_abs_scaler \
            .transform(im.reshape(-1, 1)) \
            .reshape(im.shape)

        return endmembers_norm, image_norm

    else:
        return em, im


def im2spectra(geoArr):
    # type: (Union[GeoArray, np.ndarray]) -> np.ndarray
    """Convert 3D images to array of spectra samples (rows: samples;  cols: spectral information)."""
    return geoArr.reshape((geoArr.shape[0] * geoArr.shape[1], geoArr.shape[2]))


def spectra2im(spectra, tgt_rows, tgt_cols):
    # type: (Union[GeoArray, np.ndarray], int, int) -> np.ndarray
    """Convert array of spectra samples (rows: samples;  cols: spectral information) to a 3D image.

    :param spectra:     2D array with rows: spectral samples / columns: spectral information (bands)
    :param tgt_rows:    number of target image rows
    :param tgt_cols:    number of target image rows
    :return:            3D array (rows x columns x spectral bands)
    """
    return spectra.reshape(tgt_rows, tgt_cols, spectra.shape[1])
