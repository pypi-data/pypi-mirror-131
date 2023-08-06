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

"""Classifiers using a combination of different measures for class distances."""

import numpy as np
from typing import Union  # noqa F401  # flake8 issue
from geoarray import GeoArray

from .._baseclasses import _ImageClassifier, _kNN_ImageClassifier
from ..misc import normalize_endmembers_image, im2spectra
from ..similarity_measures import calc_sam


class FEDSA_Classifier(_ImageClassifier):
    def __init__(self, train_spectra, CPUs=1):
        # type: (np.ndarray, Union[int, None]) -> None
        super(FEDSA_Classifier, self).__init__(train_spectra, np.array(range(train_spectra.shape[0])), CPUs=CPUs)

        self.clf_name = 'fused euclidian distance / spectral angle (FEDSA)'

    @property
    def fedsa(self):
        return self._distance_metrics

    def _calc_fedsa(self, image, endmembers):
        if not image.shape[2] == self.train_spectra.shape[1]:
            raise RuntimeError('Matrix dimensions are not aligned. Input image has %d bands but input spectra '
                               'have %d.' % (image.shape[2], self.train_spectra.shape[1]))

        # normalize input data because SAM asserts only data between -1 and 1
        train_spectra_norm, tileimdata_norm = normalize_endmembers_image(endmembers, image)

        angles = np.zeros((image.shape[0], image.shape[1], self.n_samples), float)
        ed = np.zeros((image.shape[0], image.shape[1], self.n_samples), float)
        tileimspectra = im2spectra(image)
        # if np.std(tileimdata) == 0:  # skip tiles that only contain the same value

        # loop over all training spectra and compute spectral angle for each pixel
        for n_sample in range(self.n_samples):
            train_spectrum = train_spectra_norm[n_sample, :].reshape(1, 1, self.n_features)
            angles[:, :, n_sample] = calc_sam(tileimdata_norm, train_spectrum, axis=2)
            ed[:, :, n_sample] = np.sqrt(np.sum((tileimspectra.astype(float) -
                                                 train_spectrum.flatten().astype(float)) ** 2, axis=1))\
                .reshape(image.shape[:2])

        angles_norm = angles / angles.max()
        ed_norm = ed / ed.max()

        fedsa = (angles_norm + ed_norm) / 2

        return fedsa

    def _predict(self, imdata, endmembers):
        # type: (GeoArray, np.ndarray) -> (np.ndarray, Union[np.ndarray, None])
        fedsa = self._calc_fedsa(imdata, endmembers)
        fedsa_min = np.min(fedsa, axis=2).astype(np.float32)
        cmap = np.argmin(fedsa, axis=2).astype(np.int16)
        cmap = self.overwrite_cmap_at_nodata_positions(cmap, imdata)

        return cmap.astype(np.int16), fedsa_min

    def label_unclassified_pixels(self, label_unclassified, threshold):
        # type: (int, Union[str, int, float]) -> GeoArray
        return self._label_unclassified_pixels(
            self.cmap, label_unclassified, threshold, self.fedsa
        )

    def show_fedsa_histogram(self, figsize=(10, 5), bins=100, normed=False):
        self._show_distances_histogram(self.fedsa, self.cmap, figsize=figsize, bins=bins, normed=normed)

    def show_fedsa(self, **kwargs):
        self._show_distance_metrics(**kwargs)


class kNN_FEDSA_Classifier(FEDSA_Classifier, _kNN_ImageClassifier):
    def __init__(self, train_spectra, n_neighbors=3, CPUs=1):
        # type: (np.ndarray, int, Union[int, None]) -> None
        super(kNN_FEDSA_Classifier, self).__init__(train_spectra, CPUs=CPUs)

        self.clf_name = 'k-nearest neighbour fused euclidian distance / spectral angle (kNN_FEDSA; k=%d)' % n_neighbors
        self.n_neighbors = n_neighbors

    def _predict(self, imdata, endmembers):
        # type: (GeoArray, np.ndarray) -> (np.ndarray, Union[np.ndarray, None])
        fedsa = self._calc_fedsa(imdata, endmembers)
        fedsa_min_k, cmap = self.get_min_distances_and_corresponding_cmap(fedsa)
        cmap = self.overwrite_cmap_at_nodata_positions(cmap, imdata)

        return cmap.astype(np.int16), fedsa_min_k
