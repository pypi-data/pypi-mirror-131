import numpy as np

import fastash.ashfunc
from .whitening_transformer import WhiteningTransformer
from .hyperplane import Hyperplane
from joblib import Parallel, delayed

import os
from joblib import dump, load
import shutil

class ASH():
    def __init__(self,
                 h='scott',
                 q=100,
                 n_mc = 10000,
                 bounds = [],
                 n_jobs = 1,
                 verbose=0):

        self.h = h
        self._h = None
        self.q = q
        self.n_mc = n_mc
        self.bounds = bounds 
        self.n_jobs = n_jobs
        self.verbose = verbose

    def __repr__(self):
        if self._h is None:
            return('ASH(h='+str(self.h)+')')
        else:
            return('ASH(h='+str(self._h)+')')

    def fit(self, X):
        # preprocessing
        # self._set_data(X)
        
        self._real_X_min = np.min(X, axis=0)
        self._real_X_max = np.max(X, axis=0)
        
        # get data dimensions
        self._n, self._d = X.shape
        
        # preprocessing
        self._wt = WhiteningTransformer()
        X = self._wt.fit_transform(X)
        
        self._x_min = np.min(X, axis=0)
        
        # BOUNDARIES INFORMATIONS
        A, r = self._set_boundaries(x = X[0])

        # BANDWIDTH SELECTION
        self._compute_bandwidth(X)
        
        # MonteCarlo Set
        # used for the volume computation of hypercubes clipped by hyperplans
        X_mc = np.random.random((self.n_mc, self._d)) * self._h - self._h / 2
        
        # self._X_digit_uniques, self._P = fastash.ashfunc.compute_bins_P(X,
        #                                 self._h,
        #                                 self.q,
        #                                 self.n_mc,
        #                                 A,
        #                                 r)
        
        folder = './.temp_joblib_memmap'
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        
        X_filename_memmap = os.path.join(folder, 'X_memmap')
        dump(X, X_filename_memmap)
        X_memmap = load(X_filename_memmap, mmap_mode='r')

        self._fit_results = Parallel(n_jobs=self.n_jobs)(delayed(fastash.ashfunc.compute_bins_P_shift)(
            X_memmap, # X
            self._n, # n
            self._d, # d
            X.min(axis=0), # x_min
            np.linalg.norm(A, axis=0, ord=np.inf), #norm_2_w
            np.linalg.norm(A, axis=0, ord=2), # norm_inf_w
            self._h, # h
            i_shift * self._h / self.q, # shift
            A, # A
            r, # r
            A.shape[1], #n_hyp
            X_mc, # X_mc
            self.n_mc, #n_mc
            ) for i_shift in range(self.q))
        
        try:
            shutil.rmtree(folder)
        except:  # noqa
            print('Could not clean-up automatically.')

        return(self)

    def predict(self, X):
        X = self._wt.transform(X)
        
        id_out_of_bounds = np.zeros(X.shape[0]).astype(np.bool)
        for hyp in self._bounds_hyperplanes:
            id_out_of_bounds = np.any((id_out_of_bounds, ~hyp.side(X)), axis=0)
        
        # get indices outside bounds
        # it will be use to cut off the result later
            
        # f = fastash.ashfunc.merge_predict(X_digit_uniques = self._X_digit_uniques,
        #                           P = self._P,
        #                           Y = X,
        #                           x_min = self._x_min,
        #                           h = self._h,
        #                           q = self.q)
        
        folder = './.temp_joblib_memmap'
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        
        X_filename_memmap = os.path.join(folder, 'X_memmap')
        dump(X, X_filename_memmap)
        X_memmap = load(X_filename_memmap, mmap_mode='r')
        
        f = Parallel(n_jobs=self.n_jobs)(delayed(fastash.ashfunc.merge_predict_shift)(
            self._fit_results[i_shift][0], # X_digit_uniques
            self._fit_results[i_shift][0].shape[0], # n_X
            self._d, # d
            self._fit_results[i_shift][1], # P
            X_memmap, # Y
            X.shape[0], # n_Y
            self._x_min, # x_min
            self._h, # h
            self._fit_results[i_shift][2], # shift
            ) for i_shift in range(self.q))
        
        f = np.sum(f, axis=0)
        f = f / (self.q * self._h ** self._d)
        
        # outside bounds : equal to 0
        f[id_out_of_bounds] = 0

        # Preprocessing correction
        f /= self._wt.scale_
        
        try:
            shutil.rmtree(folder)
        except:  # noqa
            print('Could not clean-up automatically.')
        
        return(f)
    
    def _set_boundaries(self, x):
        self._bounds_hyperplanes = []

        for k, pos in self.bounds:
            if pos == 'left':
                self._add_boundary(k=k,
                                   value=self._real_X_min[k],
                                   x=x)
            elif pos == 'right':
                self._add_boundary(k=k,
                                   value=self._real_X_max[k],
                                   x=x)
            elif pos == 'both':
                self._add_boundary(k=k,
                                   value=self._real_X_min[k],
                                   x=x)
                self._add_boundary(k=k,
                                   value=self._real_X_max[k],
                                   x=x)
            else:
                raise(TypeError('Unexpected bounds parameters'))
        
        A = np.zeros((self._d, len(self._bounds_hyperplanes)))
        r = np.zeros(len(self._bounds_hyperplanes))
        
        for i_hyp, hyp in enumerate(self._bounds_hyperplanes):
            A[:, i_hyp] = hyp.w
            r[i_hyp] = hyp.b
        
        return(A, r)
    
    def _add_boundary(self, k, value, x):
        P = np.diag(np.ones(self._d))
        
        P[:, k] = value

        P_wt = self._wt.transform(P)

        hyp = Hyperplane().set_by_points(P_wt)
        hyp.set_positive_side(x)
        self._bounds_hyperplanes.append(hyp)
    
    def _compute_bandwidth(self, X):
        if type(self.h) is int or type(self.h) is float:
            self._h = float(self.h)

        elif type(self.h) is str:
            if self.h == 'scott' or self.h == 'silverman':
                # the scott rule is based on gaussian kernel
                # the support of the gaussian kernel to have 99%
                # of the density is 2.576
                self._h = 2.576 * scotts_rule(X)
            else:
                raise (ValueError("Unexpected bandwidth selection method."))
        else:
            raise (TypeError("Unexpected bandwidth type."))

        if self.verbose > 0:
            print('Bandwidth selection done : h=' + str(self._h))

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

def scotts_rule(X):
    """
    Scott's rule according to "Multivariate density estimation", Scott 2015, p.164.
    The Silverman's rule is exactly the same in "Density estimation for statistics and data analysis", Silverman 1986, p.87.
    Parameters
    ----------
    X : numpy array of shape (n_samples, n_features).

    Returns
    -------
    h : float
        Scotts rule bandwidth. The returned bandwidth should be then factored
        by the data variance.

    """
    n = X.shape[0]
    d = X.shape[1]
    return(n**(-1/(d + 4)))