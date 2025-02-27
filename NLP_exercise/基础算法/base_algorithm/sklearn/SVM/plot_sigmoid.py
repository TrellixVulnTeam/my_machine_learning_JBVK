# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm


gammas = [0.01, 0.03, 0.05, 0.07, 0.09, 0.12, 0.15]
r = -0.1

np.random.seed(0)
x = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
y = [0] * 20 + [1] * 20

for gamma in gammas:
	my_estimator = svm.SVR(kernel = 'sigmoid', gamma = gamma, coef0 = r)
	my_estimator.fit(x, y)

#	w = my_estimator.coef_[0]
#	a = -w[0] / w[1]
	x_lim = np.linspace(-5, 5)
	y_lim = np.linsapce(-5, 5)


#	b = my_estimator.support_vectors_[0]
#	y_lower = a * x_lim + (b[1] - a * b[0])

	b = my_estimator.support_vectors_[-1]
	y_upper = a * x_lim + (b[1] - a * b[0])

	plt.plot(x_lim, y_lim, 'k-*-')
	plt.plot(x_lim, y_lower, 'bo')
	plt.plot(x_lim, y_upper, 'r-')
	
	plt.scatter(my_estimator.support_vectors_[:, 0], my_estimator.support_vectors_[:, 1], s = 80, facecolors = 'none')
	plt.scatter(x[:, 0], x[:, 1], c = y, cmap = plt.cm.Paired)

plt.axis('tight')
plt.show()



