# -*- coding: utf-8 -*-

"""
	将 digits（0~9）分为两类（0~4， 5~9），转化为二分类问题
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import datasets


digits = datasets.load_digits()

x, y = digits.data, digits.target
x = StandardScaler().fit_transform(x)

# classify small against large digits
y = (y > 4).astype(np.int)


# set regularization parmeter
for i, C in enumerate((100, 1, 0.01)):
	# turn down tolerance for short training time
	clf_L1_LR = LogisticRegression(C = C, penalty = 'l1', tol = 0.01)
	clf_L2_LR = LogisticRegression(C = C, penalty = 'l2', tol = 0.01)
	clf_L1_LR.fit(x, y)
	clf_L2_LR.fit(x, y)

	coef_L1_LR = clf_L1_LR.coef_.ravel()
	coef_L2_LR = clf_L2_LR.coef_.ravel()

	# coef_L1_LR contains zeros due to L1 sparsity inducing norm
	# compute the degree of sparsity
	sparsity_L1_LR = np.mean(coef_L1_LR == 0) * 100
	sparsity_L2_LR = np.mean(coef_L2_LR == 0) * 100

	print("C = %.2f" %C)
	print("sparsity with L1 penalty: %.2f%%" %sparsity_L1_LR)
	print("score with L1 penalty: %.4f" %clf_L1_LR.score(x, y))
	print("sparsity with L2 penalty: %.2f%%" %sparsity_L2_LR)
	print("score with L2 penalty: %.4f" %clf_L2_LR.score(x, y))

	L1_plot = plt.subplot(3, 2, 2 * i + 1)
	L2_plot = plt.subplot(3, 2, 2 * (i + 1))

	if i == 0:
		L1_plot.set_title("L1 penalty")
		L2_plot.set_title("L2 penalty")
	
	L1_plot.imshow(np.abs(coef_L1_LR.reshape(8, 8)), interpolation = 'nearest', cmap = 'binary', vmax = 1, vmin = 0)
	L2_plot.imshow(np.abs(coef_L2_LR.reshape(8, 8)), interpolation = 'nearest', cmap = 'binary', vmax = 1, vmin = 0)
	plt.text(-8, 3, "C = %.2f" %C)

	L1_plot.set_xticks(())
	L1_plot.set_yticks(())
	L2_plot.set_xticks(())
	L2_plot.set_yticks(())

plt.show()




