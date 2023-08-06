# -*- coding: utf-8 -*-

from scipy import stats
import numpy as np
from matplotlib import pyplot as plt
import fastash
from time import time
#%% Dataset

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
    
    return(X, Y, pdf_Y, X_grid)
    

# %%
X, Y, pdf_Y, X_grid = bounded_set(100000, 42)

#%%
st = time()
ash = fastash.ASH(q=100,
        bounds=[
                (0, 'left'),
                (1, 'both')
                ],
        n_mc=10000,
        n_jobs=2)
ash.fit(X)
print('fit exec time : ', time()-st)

# st = time()
# n_X = np.max([ash._fit_results[i_shift][0].shape[0] for i_shift in range(ash.q)])

# ash._X_digit_uniques = np.zeros((ash.q, n_X, ash._d))
# ash._P = np.zeros((ash.q, n_X))
# for i_shift in range(ash.q):
#     n_X_i = ash._fit_results[i_shift][0].shape[0]
    
#     ash._X_digit_uniques[i_shift, :n_X_i, :] = ash._fit_results[i_shift][0]
#     ash._P[i_shift, :n_X_i] = ash._fit_results[i_shift][1]

# ash._X_digit_uniques = ash._X_digit_uniques.astype(np.int32)

# print('self process exec time :', time()-st)

# print(len(ash._ret))
# f = ash.predict(X_grid)

# I = np.sum(f) * np.product(X_grid.max(axis=0)-X_grid.min(axis=0)) / X_grid.shape[0]
# print(I)

#%%
# X_eval = np.vstack((np.ones(100)*0.5,
#                        np.linspace(0,2,100))).T

st = time()
f_grid = ash.predict(X_grid)
print('grid exec time :', time()-st)

# plt.plot(Y[:,1], pdf_Y)
# plt.plot(Y[:,1], f_eval)
# plt.show()




