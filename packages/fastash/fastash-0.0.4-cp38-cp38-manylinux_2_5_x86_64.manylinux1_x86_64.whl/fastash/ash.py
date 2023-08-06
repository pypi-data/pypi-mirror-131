import numpy as np
import pandas as pd

from .density_estimator import DensityEstimator
import ashfunc
from . import bandwidth_selection

class ASH(DensityEstimator):
    def __init__(self,
                 h='scott',
                 q=10,
                 n_mc = 10000,
                 bounds = [],
                 verbose=0):

        super().__init__(bounds = bounds,
                         verbose=verbose)

        self.h = h
        self._h = None
        self.q = q
        self.n_mc = n_mc

    def __repr__(self):
        if self._h is None:
            return('ASH(h='+str(self.h)+')')
        else:
            return('ASH(h='+str(self._h)+')')

    def fit(self, X):
        # preprocessing
        self._set_data(X)
        
        self._x_min = np.min(self._data, axis=0)
        
        # BOUNDARIES INFORMATIONS
        self._set_boundaries()

        # BANDWIDTH SELECTION
        if type(self.h) is int or type(self.h) is float:
            self._h = float(self.h)

        elif type(self.h) is str:
            if self.h == 'scott' or self.h == 'silverman':
                # the scott rule is based on gaussian kernel
                # the support of the gaussian kernel to have 99%
                # of the density is 2.576
                self._h = 2.576 * bandwidth_selection.scotts_rule(X)
                # self._h = bandwidth_selection.scotts_rule(X)
            else:
                raise (ValueError("Unexpected bandwidth selection method."))
        else:
            raise (TypeError("Unexpected bandwidth type."))

        if self.verbose > 0:
            print('Bandwidth selection done : h=' + str(self._h))
        
        A = np.zeros((self._d, len(self._bounds_hyperplanes)))
        r = np.zeros(len(self._bounds_hyperplanes))
        
        for i_hyp, hyp in enumerate(self._bounds_hyperplanes):
            A[:, i_hyp] = hyp.w
            r[i_hyp] = hyp.b
        
        self._X_digit_uniques, self._P, self._X_digit = ashfunc.histograms(self._data,
                                        self._h,
                                        self.q,
                                        self.n_mc,
                                        A,
                                        r)
        
        return(self)

    def predict(self, X):
        X = self._wt.transform(X)
        
        id_out_of_bounds = np.zeros(X.shape[0]).astype(np.bool)
        for hyp in self._bounds_hyperplanes:
            id_out_of_bounds = np.any((id_out_of_bounds, ~hyp.side(X)), axis=0)
        
        # get indices outside bounds
        # it will be use to cut off the result later
            
        f = ashfunc.merge_predict(X_digit_uniques = self._X_digit_uniques,
                                  P = self._P,
                                  Y = X,
                                  x_min = self._x_min,
                                  h = self._h,
                                  q = self.q)
        
        # outside bounds : equal to 0
        f[id_out_of_bounds] = 0
        # f[id_out_of_high_bounds] = 0

        # Preprocessing correction
        f /= self._wt.scale_
        
        return(f)
