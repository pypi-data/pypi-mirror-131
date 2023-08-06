#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 15:01:44 2021

@author: frem
"""

import numpy as np

from .whitening_transformer import WhiteningTransformer
from .hyperplane import Hyperplane

class DensityEstimator():
    def __init__(self,
                 bounds = [],
                 verbose=0):

        self.bounds = bounds
        self.verbose = verbose

    def _set_data(self, X):
        self._real_X_min = np.min(X, axis=0)
        self._real_X_max = np.max(X, axis=0)
        
        # preprocessing
        self._wt = WhiteningTransformer()
        self._data = self._wt.fit_transform(X)

        # get data dimensions
        self._n = self._data.shape[0]
        self._d = self._data.shape[1]

    def _set_boundaries(self):
        self._bounds_hyperplanes = []
        self._low_bound_trigger = []

        for k, pos in self.bounds:
            if pos == 'left':
                self._add_boundary(k=k,
                                   value=self._real_X_min[k])
            elif pos == 'right':
                self._add_boundary(k=k,
                                   value=self._real_X_max[k])
            elif pos == 'both':
                self._add_boundary(k=k,
                                   value=self._real_X_min[k])
                self._add_boundary(k=k,
                                   value=self._real_X_max[k])
            else:
                raise(TypeError('Unexpected bounds parameters'))
    
    def _add_boundary(self, k, value):
        A = np.diag(np.ones(self._d))
        
        A[:, k] = value

        A_wt = self._wt.transform(A)

        hyp = Hyperplane().set_by_points(A_wt)
        hyp.set_positive_side(self._data[0])
        self._bounds_hyperplanes.append(hyp)
                
        if hyp.positive_side_scalar == 1:
            self._low_bound_trigger.append(True)
        else:
            self._low_bound_trigger.append(False)

    def _forbid_null_values_process(self, f):
        if self.verbose > 0:
            print('Null value correction...')
        idx = f == 0.0

        m_0 = idx.sum()

        new_n = self._n + m_0

        f = f * self._n / new_n

        min_value = 1 / new_n * self._normalization * 1
        f[f == 0.0] = min_value

        # Warning flag
        # check the relative number of corrected probabilities
        if self.verbose > 0:
            print('m_0 = ' + str(m_0) + ', m = ' + str(self._n) + ', m_0 / m = ' + str(
                np.round(m_0 / self._n, 4)))

        # warning flag
        if m_0 / self._n > 0.01:
            print('WARNING : m_0/m > 0.01. The parameter `n_fit_max` should be higher.')

        if self.verbose > 0:
            print('Null value correction done for ' + str(m_0) + ' elements.')

        return(f)

    def set_params(self, **params):
        """
        Set parameters.

        Parameters
        ----------
        **params : kwargs
            Parameters et values to set.

        Returns
        -------
        self : DensityEstimator
            The self object.

        """
        for param, value in params.items():
            setattr(self, param, value)

class NullEstimator(DensityEstimator):
    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return (self)

    def predict(self, X):
        return (np.zeros(X.shape[0]))
