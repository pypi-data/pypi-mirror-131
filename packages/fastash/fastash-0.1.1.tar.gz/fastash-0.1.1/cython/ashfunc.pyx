# distutils: language = c++

cdef extern from "stdlib.h":
    ctypedef void const_void "const void"
    void qsort(void *base, int nmemb, int size,
            int(*compar)(const void *, const void *)) nogil

from libcpp.vector cimport vector
from libc.stdlib cimport malloc, free
from libcpp cimport bool

import cython

import numpy as np
cimport numpy as np

np.import_array()

from cpython cimport array
import array

DTYPE = np.intc

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
def compute_bins_P_shift(np.ndarray[double, ndim=2] X, 
                         int n,
                         int d,
                         np.ndarray[double, ndim=1] x_min,
                         np.ndarray[double, ndim=1] norm_inf_w,
                         np.ndarray[double, ndim=1] norm_2_w,
                         double h, 
                         double shift, 
                         np.ndarray[double, ndim=2] A,
                         np.ndarray[double, ndim=1] r,
                         int n_hyp,
                         np.ndarray[double, ndim=2] X_mc,
                         int n_mc,):
    cdef Py_ssize_t i, j, j_unique, i_hyp
        
    X_digit_uniques = np.zeros((n, d), dtype=DTYPE)
    cdef np.ndarray[int, ndim=2] X_digit_uniques_view = X_digit_uniques
        
    P = np.zeros(n, dtype=np.double)
    cdef np.ndarray[double, ndim=1] P_view = P
    
    cdef int **X_digit
            
    cdef bool trigger_unique, trigger_correction
    
    cdef int * last_x
    last_x = <int *> malloc(d * sizeof(int))
    
    cdef int i_last = 0
    cdef int i_unique = 0
        
    cdef double * center
    center = <double *> malloc(d * sizeof(double))
    
    cdef double hyp_correction
                
    cdef double * dist
    
    cdef bool * trigger_hyp
    trigger_hyp = <bool *> malloc(n_hyp * sizeof(bool))
    
    # discretize
    X_digit = discretize(X=X, 
                         x_min = x_min,
                         n = n,
                         d = d,
                         h = h,
                         shift = shift)
    
    # sort
    sort_according_d(X_digit, n, d)
    
    # count
    for j in range(d):
        last_x[j] = X_digit[0][j]
    i_unique = -1
    i_last = 0
    
    for i in range(1,n):
        trigger_unique = False
        for j in range(d):
            if X_digit[i][j] != last_x[j] or (i == n-1 and j == 0):
                # if it's the first column to change
                if trigger_unique == False:
                    # their is a new unique !
                    # increment
                    i_unique = i_unique + 1
                                            
                    # # for each column
                    for j_unique in range(d):
                        # save center for boundary correction below
                        center[j_unique] = x_min[j_unique] - 1.5 * h + shift + h * last_x[j_unique]
                        # save the unique x
                        X_digit_uniques_view[i_unique, j_unique] = last_x[j_unique]
                    
                    
                    dist = inf_distances_to_hyperplanes(h=h,
                                                        center=center,
                                                        d=d,
                                                        A = A,
                                                        r = r,
                                                        n_hyp=n_hyp,
                                                        norm_inf_w=norm_inf_w,
                                                        norm_2_w = norm_2_w)
                    
                    trigger_correction = False
                    
                    for i_hyp in range(n_hyp):
                        if dist[i_hyp] < h/2:
                            trigger_correction = True
                            trigger_hyp[i_hyp] = True
                        else:
                            trigger_hyp[i_hyp] = False
                    
                    hyp_correction = 1.0
                    if trigger_correction:
                        
                        hyp_correction = hyperplanes_clip_volume_monte_carlo(
                            center=center,
                            d=d,
                            X_mc=X_mc,
                            n_mc=n_mc,
                            A = A,
                            r = r,
                            n_hyp=n_hyp,
                            trigger_hyp=trigger_hyp)
                    
                    # save the proba
                    P_view[i_unique] = (i - i_last) / (n * hyp_correction)
                    i_last = i
                
                # finally save this new last unique
                last_x[j] = X_digit[i][j]
                # and set trigger True
                # to say that a unique is found
                trigger_unique = True
    
    i_to_keep = P>0
    X_digit_uniques = X_digit_uniques[i_to_keep,:]
    P = P[i_to_keep]
    
    free(X_digit)
    free(center)
    free(dist)
    free(trigger_hyp)
    
    return(X_digit_uniques, P, shift)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
def merge_predict_shift(np.ndarray[int, ndim=2] X_digit_uniques,
                        int n_X,
                        int d,
                  np.ndarray[double, ndim=1] P,
                  np.ndarray[double, ndim=2] Y,
                  int n_Y,
                  np.ndarray[double, ndim=1] x_min,
                  double h,
                  double shift):
        
    cdef Py_ssize_t j
        
    cdef int i_X
    
    cdef bool trigger_set_P, keep_search
    
    # Y_digit is [[y0, y1, 0], [y0, y1, 1], ... [y0, y1, n_y]]
    # by this way, the index is kept after the sort process
    cdef int **Y_digit
    
    
    f = np.zeros(n_Y, dtype=np.double)
    cdef np.ndarray[double, ndim=1] f_view = f
    
    cdef int last_j_success_level, j_success_level
    
    # discretize
    Y_digit = discretize(X = Y,
                     x_min = x_min,
                     n = n_Y,
                     d = d,
                     h = h,
                     shift = shift,
                     index_column = True)
    
    # sort
    sort_according_d(Y_digit, n_Y, d)
    
    i_X = -1
    
    for i_Y in range(n_Y):
        trigger_set_P = False
        
        keep_search = True
        
        while i_X < n_X and keep_search:
            i_X = i_X + 1
            
            for j in range(d):
                if Y_digit[i_Y][j] > X_digit_uniques[i_X, j]:
                    break
                elif Y_digit[i_Y][j] < X_digit_uniques[i_X, j]:
                    keep_search = False
                    break
                else:
                    if keep_search and j + 1 == d:
                        f_view[Y_digit[i_Y][d]] = f_view[Y_digit[i_Y][d]] + P[i_X]
                        keep_search = False
        
        i_X = i_X -1
        
    free(Y_digit)
    
    return(f)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef bool lower(int *a,
                int *b,
                int d):
    for j in range(d):
        if a[j] < b[j]:
            return(True)
    return(False)
    

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef int ** discretize(np.ndarray[double, ndim=2] X,
                       np.ndarray[double, ndim=1] x_min,
                       int n,
                       int d,
                       double h,
                       double shift,
                       bool index_column = False):
    cdef Py_ssize_t i, j
    
    cdef int **X_digit
    X_digit = <int **> malloc(n * sizeof(int*))
    
    cdef double *slide = <double *> malloc(d * sizeof(double))
    for j in range(d):
        slide[j] = x_min[j] - 2 * h + shift
    
    for i in range(n):
        if index_column:
            X_digit[i] = <int *> malloc((d + 1) * sizeof(int))
            for j in range(d):
                X_digit[i][j] = <int>((X[i,j] - slide[j]) / h)
            
            X_digit[i][d] = i
            
        else:
            X_digit[i] = <int *> malloc(d * sizeof(int))
            for j in range(d):
                X_digit[i][j] = <int>((X[i,j] - slide[j]) / h)
    return(X_digit)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double * inf_distances_to_hyperplanes(double h,
                                           double *center,
                                           int d,
                                           np.ndarray[double, ndim=2] A, 
                                           np.ndarray[double, ndim=1] r,
                                           int n_hyp,
                                           np.ndarray[double, ndim=1] norm_inf_w,
                                           np.ndarray[double, ndim=1] norm_2_w):
    
    cdef double * dist
    dist = <double *> malloc(n_hyp * sizeof(double))
    cdef Py_ssize_t i_hyp, j
    
    # initialize dist_min greater than the limit condition
    for i_hyp in range(n_hyp):
        # distance to hyperplan
        dist[i_hyp] = 0.0
        for j in range(d):
            dist[i_hyp] = dist[i_hyp] + center[j] * A[j, i_hyp]
        dist[i_hyp] = dist[i_hyp] + r[i_hyp]
        # dist[i_hyp] = abs(dist[i_hyp]) / norm_2_w[i_hyp]
        dist[i_hyp] = abs(dist[i_hyp]) / norm_2_w[i_hyp]**2 * norm_inf_w[i_hyp]
        
    return(dist)



@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double hyperplanes_clip_volume_monte_carlo(double *center,
                                    int d, 
                                    np.ndarray[double, ndim=2] X_mc,
                                    int n_mc, 
                                    np.ndarray[double, ndim=2] A,
                                    np.ndarray[double, ndim=1] r,
                                    int n_hyp, 
                                    bool * trigger_hyp):
    cdef double dot
    cdef double hyp_correction = 0.0
    cdef bool trigger_mc_inside
    
    cdef Py_ssize_t i_hyp, i_mc, j
    for i_mc in range(n_mc):
        trigger_mc_inside = True
        for i_hyp in range(n_hyp):
            if trigger_hyp[i_hyp]:
                dot = 0.0
                for j in range(d):
                    dot = dot + (center[j]+X_mc[i_mc, j]) * A[j, i_hyp]
                dot = dot + r[i_hyp]
                                                    
                if dot < 0.0:
                    trigger_mc_inside = False
        
        if trigger_mc_inside:
            hyp_correction = hyp_correction + 1
        
    hyp_correction = hyp_correction / n_mc
    
    return(hyp_correction)

cdef void sort_according_d(void *base, 
                           int n,
                           int d):
    
    if d == 1:
        qsort(base, n, sizeof(int*), compare_1d)
    elif d == 2:
        qsort(base, n, sizeof(int*), compare_2d)
    elif d == 3:
        qsort(base, n, sizeof(int*), compare_3d)
    elif d == 4:
        qsort(base, n, sizeof(int*), compare_4d)
    elif d == 5:
        qsort(base, n, sizeof(int*), compare_5d)
    elif d == 6:
        qsort(base, n, sizeof(int*), compare_6d)
    elif d == 7:
        qsort(base, n, sizeof(int*), compare_7d)
    elif d == 8:
        qsort(base, n, sizeof(int*), compare_8d)
    elif d == 9:
        qsort(base, n, sizeof(int*), compare_9d)
    elif d == 10:
        qsort(base, n, sizeof(int*), compare_10d)
    elif d == 11:
        qsort(base, n, sizeof(int*), compare_11d)
    elif d == 12:
        qsort(base, n, sizeof(int*), compare_12d)
    elif d == 13:
        qsort(base, n, sizeof(int*), compare_13d)
    elif d == 14:
        qsort(base, n, sizeof(int*), compare_14d)
    elif d == 15:
        qsort(base, n, sizeof(int*), compare_15d)
    elif d == 16:
        qsort(base, n, sizeof(int*), compare_16d)
    elif d == 17:
        qsort(base, n, sizeof(int*), compare_17d)
    elif d == 18:
        qsort(base, n, sizeof(int*), compare_18d)
    elif d == 19:
        qsort(base, n, sizeof(int*), compare_19d)
    elif d == 20:
        qsort(base, n, sizeof(int*), compare_20d)

# =============================================================================
# Compare functions
# =============================================================================

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_1d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(1):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_2d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(2):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_3d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(3):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_4d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(4):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_5d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(5):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_6d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(6):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_7d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(7):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_8d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(8):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_9d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(9):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_10d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(10):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_11d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(11):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_12d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(12):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_13d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(13):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_14d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(14):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_15d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(15):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_16d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(16):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_17d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(17):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_18d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(18):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_19d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(19):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_20d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(20):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

# @cython.boundscheck(False)  # Deactivate bounds checking.
# @cython.wraparound(False)   # Deactivate negative indexing.
# @cython.cdivision(True) # Deactivate zero division checking.
# def compute_bins_P(np.ndarray[double, ndim=2] X, 
#                     double h, 
#                     int q, 
#                     int n_mc,
#                     np.ndarray[double, ndim=2] A,
#                     np.ndarray[double, ndim=1] r,
#                     ):
#     cdef Py_ssize_t i_shift, i, j, j_unique, i_hyp
    
#     cdef int n = X.shape[0]
#     cdef int d = X.shape[1]
    
#     X_digit_uniques = np.zeros((q, n, d), dtype=DTYPE)
#     cdef np.ndarray[int, ndim=3] X_digit_uniques_view = X_digit_uniques
        
#     P = np.zeros((q, n), dtype=np.double)
#     cdef np.ndarray[double, ndim=2] P_view = P
    
#     cdef double dh = h / q
    
#     x_min = np.min(X, axis=0)
#     cdef np.ndarray[double, ndim = 1] x_min_view = x_min
    
#     cdef int **X_digit
            
#     cdef bool trigger_unique, trigger_correction
    
#     cdef int * last_x
#     last_x = <int *> malloc(d * sizeof(int))
    
#     cdef int i_last = 0
#     cdef int i_unique = 0
        
#     cdef double * center
#     center = <double *> malloc(d * sizeof(double))
    
#     X_mc = np.random.random((n_mc, d)) * h - h / 2
#     cdef np.ndarray[double, ndim=2] X_mc_view = X_mc
    
#     cdef int n_hyp = A.shape[1]
    
#     cdef double hyp_correction
    
#     norm_inf_w = np.linalg.norm(A, axis=0, ord=np.inf)
#     cdef np.ndarray[double, ndim = 1] norm_inf_w_view = norm_inf_w
    
#     norm_2_w = np.linalg.norm(A, axis=0, ord=2)
#     cdef np.ndarray[double, ndim = 1] norm_2_w_view = norm_2_w
                
#     cdef double * dist
    
#     cdef bool * trigger_hyp
#     trigger_hyp = <bool *> malloc(n_hyp * sizeof(bool))
    
#     for i_shift in range(q):
#         # discretize
#         X_digit = discretize(X=X, 
#                               x_min = x_min_view,
#                               n = n,
#                               d = d,
#                               h = h,
#                               shift = i_shift * dh)
        

        
#         # sort
#         sort_according_d(X_digit, n, d)
        
#         # count
#         for j in range(d):
#             last_x[j] = X_digit[0][j]
#         i_unique = -1
#         i_last = 0
        
#         for i in range(1,n):
#             trigger_unique = False
#             for j in range(d):
#                 if X_digit[i][j] != last_x[j] or (i == n-1 and j == 0):
#                     # if it's the first column to change
#                     if trigger_unique == False:
#                         # their is a new unique !
#                         # increment
#                         i_unique = i_unique + 1
                                                
#                         # # for each column
#                         for j_unique in range(d):
#                             # save center for boundary correction below
#                             center[j_unique] = x_min_view[j_unique] - 1.5 * h + i_shift * dh + h * last_x[j_unique]
#                             # save the unique x
#                             X_digit_uniques_view[i_shift, i_unique, j_unique] = last_x[j_unique]
                        
                        
#                         dist = inf_distances_to_hyperplanes(h=h,
#                                                             center=center,
#                                                             d=d,
#                                                             A = A,
#                                                             r = r,
#                                                             n_hyp=n_hyp,
#                                                             norm_inf_w=norm_inf_w_view,
#                                                             norm_2_w = norm_2_w_view)
                        
#                         trigger_correction = False
                        
#                         for i_hyp in range(n_hyp):
#                             if dist[i_hyp] < h/2:
#                                 trigger_correction = True
#                                 trigger_hyp[i_hyp] = True
#                             else:
#                                 trigger_hyp[i_hyp] = False
                        
#                         hyp_correction = 1.0
#                         if trigger_correction:
                            
#                             hyp_correction = hyperplanes_clip_volume_monte_carlo(
#                                 center=center,
#                                 d=d,
#                                 X_mc=X_mc_view,
#                                 n_mc=n_mc,
#                                 A = A,
#                                 r = r,
#                                 n_hyp=n_hyp,
#                                 trigger_hyp=trigger_hyp)
                        
#                         # save the proba
#                         P_view[i_shift, i_unique] = (i - i_last) / (n * hyp_correction)
#                         i_last = i
                    
#                     # finally save this new last unique
#                     last_x[j] = X_digit[i][j]
#                     # and set trigger True
#                     # to say that a unique is found
#                     trigger_unique = True
    
#     i_to_keep = np.max(P, axis=0)>0
#     X_digit_uniques = X_digit_uniques[:,i_to_keep,:]
#     P = P[:, i_to_keep]
    
#     free(X_digit)
#     free(center)
#     free(dist)
#     free(trigger_hyp)
    
#     return(X_digit_uniques, P)

#@cython.boundscheck(False)  # Deactivate bounds checking.
# @cython.wraparound(False)   # Deactivate negative indexing.
# @cython.cdivision(True)
# def merge_predict(np.ndarray[int, ndim=3] X_digit_uniques,
#                   np.ndarray[double, ndim=2] P,
#                   np.ndarray[double, ndim=2] Y,
#                   np.ndarray[double, ndim=1] x_min,
#                   double h,
#                   int q):
    
#     cdef int n_Y = Y.shape[0]
#     cdef int n_X = X_digit_uniques.shape[1]
#     cdef int d = Y.shape[1] 
    
#     cdef Py_ssize_t i_shift, j
    
#     cdef double dh = h / q
    
#     cdef int i_X
    
#     cdef bool trigger_set_P, keep_search
    
#     # Y_digit is [[y0, y1, 0], [y0, y1, 1], ... [y0, y1, n_y]]
#     # by this way, the index is kept after the sort process
#     cdef int **Y_digit
    
    
#     f = np.zeros(n_Y, dtype=np.double)
#     cdef np.ndarray[double, ndim=1] f_view = f
    
#     cdef int last_j_success_level, j_success_level
    
#     for i_shift in range(q):
#         # discretize
#         Y_digit = discretize(X = Y,
#                          x_min = x_min,
#                          n = n_Y,
#                          d = d,
#                          h = h,
#                          shift = i_shift * dh,
#                          index_column = True)
        
#         # sort
#         sort_according_d(Y_digit, n_Y, d)
        
#         i_X = -1
        
#         for i_Y in range(n_Y):
#             trigger_set_P = False
            
#             keep_search = True
            
#             while i_X < n_X and keep_search:
#                 i_X = i_X + 1
                
#                 for j in range(d):
#                     if Y_digit[i_Y][j] > X_digit_uniques[i_shift, i_X, j]:
#                         break
#                     elif Y_digit[i_Y][j] < X_digit_uniques[i_shift, i_X, j]:
#                         keep_search = False
#                         break
#                     else:
#                         if keep_search and j + 1 == d:
#                             f_view[Y_digit[i_Y][d]] = f_view[Y_digit[i_Y][d]] + P[i_shift, i_X]
#                             keep_search = False
            
#             i_X = i_X -1
    
#     f = f / (q * h ** d)
    
#     free(Y_digit)
#     return(f)