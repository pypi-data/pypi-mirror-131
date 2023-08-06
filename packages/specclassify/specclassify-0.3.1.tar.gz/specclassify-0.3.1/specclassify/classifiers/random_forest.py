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

"""Classifiers using random forest algorithms for class separation."""

import numpy as np
from typing import Union, List  # noqa F401  # flake8 issue
from geoarray import GeoArray

from .._baseclasses import _ImageClassifier
from ..misc import im2spectra


class RF_Classifier(_ImageClassifier):
    """Random forest classifier."""
    def __init__(self, train_spectra, train_labels, CPUs=1, **kwargs):
        # type: (np.ndarray, Union[np.ndarray, List[int]], Union[int, None], dict) -> None
        from sklearn.ensemble import RandomForestClassifier as _RandomForestClassifier  # avoids static TLS errors here

        # if CPUs is None or CPUs > 1:
        #     CPUs = 1  # The NearestCentroid seems to parallelize automatically. So using multiprocessing is slower.

        super(RF_Classifier, self).__init__(train_spectra, train_labels, CPUs=CPUs)

        self.clf_name = 'random forest'
        self.clf = _RandomForestClassifier(n_jobs=1, **kwargs)
        self.clf.fit(train_spectra, train_labels)

    def _predict(self, imdata, endmembers):
        # type: (GeoArray, np.ndarray) -> (np.ndarray, Union[np.ndarray, None])
        cmap = self.clf.predict(im2spectra(imdata)).reshape(*imdata.shape[:2])
        cmap = self.overwrite_cmap_at_nodata_positions(cmap, imdata)

        return cmap.astype(np.int16), None
