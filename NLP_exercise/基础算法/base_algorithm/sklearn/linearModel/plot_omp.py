# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.linear_model import OrthogonalMatchingPursuitCV
from sklearn.datasets import make_sparse_coded_signal

n_components, n_features = 512, 100
n_nonzero_coefs = 17

# generate the data
# y = xw
# |x|_0 = n_nonzero_coefs

y, x, w = make_sparse_coded_signal(n_samples = 1, n_components = n_components, n_features = n_features, n_nonzero_coefs = n_nonzero_coefs, random_state = 0)

idx, = w.nonzero()

# distort the clean signal
y_noisy = y + 0.05 * np.random.randn(len(y))

# plot the sparse signal
plt.figure(figsize = (7, 7))
plt.subplot(4, 1, 1)
plt.xlim(0, 512)
plt.title("Sparse signal")
plt.stem(idx, w[idx])


# plot the noise-free reconstruction
omp = OrthogonalMatchingPursuit(n_nonzero_coefs = n_nonzero_coefs)

omp.fit(x, y)
coef = omp.coef_
idx_r, = coef.nonzero()

plt.subplot(4, 1, 2)
plt.xlim(0, 512)
plt.title("Recovered signal from noise-free measurements")
plt.stem(idx_r, coef[idx_r])


# plot the noisy reconstruction
omp.fit(x, y_noisy)
coef = omp.coef_
idx_r, = coef.nonzero()

plt.subplot(4, 1, 3)
plt.xlim(0, 512)
plt.title("Recovered signal from noisy measurements")
plt.stem(idx_r, coef[idx_r])


# plot the noisy reconstruction with number of non-zeros set by CV
omp_cv = OrthogonalMatchingPursuitCV()
omp_cv.fit(x, y_noisy)
coef = omp_cv.coef_
idx, = coef.nonzero()

plt.subplot(4, 1, 4)
plt.xlim(0, 512)
plt.title("Recovered signal from noisy measurements with cv")
plt.stem(idx_r, coef[idx_r])

plt.subplots_adjust(0.06, 0.04, 0.94, 0.90, 0.20, 0.38)
plt.suptitle('Sparse signal recovery with orthogonal matching pursuit', fontsize = 16)
plt.show()









