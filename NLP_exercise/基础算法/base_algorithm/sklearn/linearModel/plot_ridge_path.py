# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

# x is the 10 * 10 Hilbert matrix
# Hilbert matrix: H_ij = 1 / (i + j - 1)
x = 1.0 / (np.arange(1, 11) + np.arange(0, 10)[:, np.newaxis])
y = np.ones(10)

# compute the paths
n_alphas = 200
alphas = np.logspace(-10, -2, n_alphas)

clf = linear_model.Ridge(fit_intercept = False)

coefs = []

for a in alphas:
	clf.set_params(alpha = a)
	clf.fit(x, y)
	coefs.append(clf.coef_)


# display results
ax = plt.gca()
ax.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])

ax.plot(alphas, coefs)
ax.set_xscale('log')

# reverse axis
ax.set_xlim(ax.get_xlim()[::-1])

plt.xlabel('alpha')
plt.ylabel('weights')
plt.title('Ridge coefficients as a function of the regularization')

plt.axis('tight')
plt.show()




