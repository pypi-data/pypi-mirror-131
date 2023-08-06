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

"""Classifiers using euclidian distance as measure for class distances."""

import numpy as np


def calc_sam(s1_norm, s2_norm, axis=0):
    """Compute spectral angle between two vectors or images (in radians)."""
    upper = np.sum(s1_norm * s2_norm, axis=axis)
    lower = \
        np.sqrt(np.sum(s1_norm * s1_norm, axis=axis)) * \
        np.sqrt(np.sum(s2_norm * s2_norm, axis=axis))

    if isinstance(lower, np.ndarray):
        lower[lower == 0] = 1e-10
    else:
        lower = lower or 1e-10

    quotient = upper / lower
    quotient[np.isclose(quotient, 1)] = 1  # in case of pixels that are equal to the endmember

    return np.arccos(quotient)


def calc_sid(s1_norm, s2_norm, axis=0):
    """Compute the spectral information divergence between two vectors or images."""
    def get_sum(x, axis=0):
        s = np.sum(x, axis=axis)
        s[s == 0] = 1e-10
        return s

    if s1_norm.ndim == 3 and s2_norm.ndim == 3:
        p = (s1_norm / get_sum(s1_norm, axis=axis)[:, :, np.newaxis]) + np.spacing(1)
        q = (s2_norm / get_sum(s1_norm, axis=axis)[:, :, np.newaxis]) + np.spacing(1)
    else:
        p = (s1_norm / get_sum(s1_norm, axis=axis)) + np.spacing(1)
        q = (s2_norm / get_sum(s1_norm, axis=axis)) + np.spacing(1)

    return np.sum(p * np.log(p / q) + q * np.log(q / p), axis=axis)
