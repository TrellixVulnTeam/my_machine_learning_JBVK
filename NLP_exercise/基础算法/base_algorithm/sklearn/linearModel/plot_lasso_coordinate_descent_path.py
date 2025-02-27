# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import lasso_path, enet_path
from sklearn import datasets

diabetes = datasets.load_diabetes()

x = diabetes.data
y = diabetes.target

# standardize data
x /= x.std(axis = 0)

# compute paths
# the smaller it is, the longer is the path, eps = alpha_min / alpha_max
eps = 5e-3

print("computing regularization path using the lasso...")
alphas_lasso, coefs_lasso, _ = lasso_path(x, y, eps, fit_intercept = False)

print("computing regularization path using the positive lasso...")
alphas_positive_lasso, coefs_positive_lasso, _ = lasso_path(x, y, eps, positive = True, fit_intercept = False)

print("computing regularization path using the elastic net...")
alphas_enet, coefs_enet, _ = enet_path(x, y, eps = eps, l1_ratio = 0.8, fit_intercept = False)

print("computing regularization path using the positive elastic net...")
alphas_positive_enet, coefs_positive_enet, _ = enet_path(x, y, eps = eps, l1_ratio = 0.8, positive = True, fit_intercept = False)



# display results
plt.figure(1)
ax = plt.gca()
ax.set_color_cycle(2 * ['b', 'r', 'g', 'c', 'k'])
l1 = plt.plot(-np.log10(alphas_lasso), coefs_lasso.T)
l2 = plt.plot(-np.log10(alphas_enet), coefs_enet.T, linestyle = '--')

plt.xlabel('-log(alpha)')
plt.ylabel('coefficients')
plt.title("Lasso and Elastic-Net Paths")
plt.legend()
plt.axis('tight')



plt.figure(2)
ax = plt.gca()
ax.set_color_cycle(2 * ['b', 'r', 'g', 'c', 'k'])
l1 = plt.plot(-np.log10(alphas_lasso), coefs_lasso.T)
l2 = plt.plot(-np.log10(alphas_positive_lasso), coefs_positive_lasso.T, linestyle = '--')

plt.xlabel('-log(alpha)')
plt.ylabel('coefficients')
plt.title("Lasso and positive Lasso")
plt.legend((l1[-1], l2[-1]), ('Lasso', 'positive Lasso'), loc = 'lower left')
plt.axis("tight")



plt.figure(3)
ax = plt.gca()
ax.set_color_cycle(2 * ['b', 'r', 'g', 'c', 'k'])
l1 = plt.plot(-np.log10(alphas_enet), coefs_enet.T)
l2 = plt.plot(-np.log10(alphas_positive_enet), coefs_positive_enet.T, linestyle = '--')

plt.xlabel("-log(alpha)")
plt.ylabel("coefficients")
plt.title("Elastic-Net and positive Elastic-Net")
plt.legend((l1[-1], l2[-1]), ('Elastic-Net', 'positive Elastic-Net'), loc = 'lower left')

plt.axis('tight')
plt.show()


















