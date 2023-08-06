# -*- coding: utf-8 -*-

from scipy import stats
import numpy as np

X_min = np.array([-0.5, 0.3])
x1_max = 1.5

mean = np.array([0,0])
rho = 0.7
cov = np.array([[1,rho],[rho,1]])

def _pdf(X, X_min):
    f = stats.multivariate_normal.pdf(X, mean=mean, cov=cov) 

    f[np.any(X<X_min, axis=1)] = 0
    f[X[:,1]>=x1_max] = 0

    return(f)

def _rvs(X_min, n,seed=None):
    np.random.seed(seed)
    X = stats.multivariate_normal.rvs(mean=mean, cov=cov, size=n)
    np.random.seed(None)
    X = X[np.all(X >= X_min, axis=1)]
    X = X[X[:,1] < x1_max]

    return(X)

def bounded_set(n, seed):
    X = _rvs(X_min, n, seed=seed)
    
    xk = (np.linspace(X[:,0].min()-X[:,0].std(),X[:,0].max()+X[:,0].std(),300),
          np.linspace(X[:,1].min()-X[:,1].std(),X[:,1].max()+X[:,1].std(),300))
    X_grid = np.meshgrid(xk[0], xk[1])
    X_grid = np.vstack((X_grid[0].flat, X_grid[1].flat)).T
    
    pdf_grid = np.sum(_pdf(X_grid, X_min)) * np.product(X_grid.max(axis=0)-X_grid.min(axis=0)) / X_grid.shape[0]# -*- coding: utf-8 -*-
    
    Y = np.vstack((np.ones(100)*0.5,
                   np.linspace(0,2,100))).T
    
    pdf_Y = _pdf(Y, X_min) / pdf_grid
    
    return(X, Y, pdf_Y)
    

