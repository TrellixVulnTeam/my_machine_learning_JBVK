# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

n_neighbors = 15
iris = datasets.load_iris()
x = iris.data[:, :2]
y = iris.target

# step size in the mesh
h = 0.02

# create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

for weights in ['uniform', 'distance']:
	clf = neighbors.KNeighborsClassifier(n_neighbors, weights = weights)
	clf.fit(x, y)

	# plot the decision boundary, and assign a color to each
	x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
	y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
	z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

	# put the result into a color plot
	z = z.reshape(xx.shape)
	plt.figure()
	plt.pcolormesh(xx, yy, z, cmap = cmap_light)

	# plot the training points
	plt.scatter(x[:, 0], x[:, 1], c = y, cmap = cmap_bold)
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.title("3-class classification (k = %i, weights = %s)" %(n_neighbors, weights))

plt.show()



