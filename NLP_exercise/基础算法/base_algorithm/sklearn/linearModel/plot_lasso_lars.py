# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from sklearn import linear_model
from sklearn import datasets

diabetes = datasets.load_diabetes()
x = diabetes.data
y = diabetes.target

print("computing regularization path using the Lars...")
alphas, _, coefs = linear_model.lars_path(x, y, method = 'lasso', verbose = True)

xx = np.sum(np.abs(coefs.T), axis = 1)
xx /= xx[-1]

plt.plot(xx, coefs.T)
ymin, ymax = plt.ylim()

plt.vlines(xx, ymin, ymax, linestyle = 'dashed')
plt.xlabel("|coef| / max|coef|")
plt.ylabel("coefficients")

plt.title('Lasso path')
plt.axis('tight')
plt.show()












