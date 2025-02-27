# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.datasets.samples_generator import make_blobs

# generate 50 separable points
x, y = make_blobs(n_samples = 50, centers = 2, random_state = 0, cluster_std = 0.6)

# fit the model
clf = SGDClassifier(loss = 'hinge', alpha = 0.01, n_iter = 200, fit_intercept = True)
clf.fit(x, y)

xx = np.linspace(-1, 5, 10)
yy = np.linspace(-1, 5, 10)

xx1, xx2 = np.meshgrid(xx, yy)
z = np.empty(xx1.shape)

for (i, j), val in np.ndenumerate(xx1):
	x1 = val
	x2 = xx2[i, j]
	p = clf.decision_function([[x1, x2]])
	z[i, j] = p[0]
levels = [-1.0, 0.0, 1.0]
linestyles = ['dashed', 'solid', 'dashed']
colors = 'k'

plt.contour(xx1, xx2, z, levels, colors = colors, linestyles = linestyles)
plt.scatter(x[:, 0], x[:, 1], c = y, cmap = plt.cm.Paired)
plt.axis('tight')
plt.show()





