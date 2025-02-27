# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV

# utility function to move the midpoint of a colormap to be around the values of interest
class MidpointNormalize(Normalize):
	def __init__(self, vmin = None, vmax = None, midpoint = None, clip = False):
		self.midpoint = midpoint
		Normalize.__init__(self, vmin, vmax, clip)
	
	def __call__(self, value, clip = None):
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

# load and prepare dataset
iris = load_iris()
x = iris.data
y = iris.target

# dataset for decision function visualization: only keep the first two features in x and sub-sample the dataset to keep only 2 classes and made it a binary classification problem
x_2d = x[:, :2]
x_2d = x_2d[y > 0]
y_2d = y[y > 0]
y_2d -= 1

# scale the data, Standardize features by removing the mean and scaling to unit variance
scaler = StandardScaler()
x = scaler.fit_transform(x)
x_2d = scaler.fit_transform(x_2d)


# train classifiers
# for an initial search, a logarithmic grid with basis 10 is often helpful. using a basis of 2, a finer tuning can be achieved but at a much higher cost
C_range = np.logspace(-2, 10, 13)
gamma_range = np.logspace(-9, 3, 13)
param_grid = dict(gamma = gamma_range, C = C_range)
cv = StratifiedShuffleSplit(y, n_iter = 5, test_size = 0.2, random_state = 42)
grid = GridSearchCV(SVC(), param_grid = param_grid, cv = cv)
grid.fit(x, y)
print("the best parameters are %s with a score of %0.2f" %(grid.best_params_, grid.best_score_))


# fit a classifier for all parameters in the 2d version
C_2d_range = [1e-2, 1, 1e2]
gamma_2d_range = [1e-1, 1, 1e1]
classifiers = []
for C in C_2d_range:
	for gamma in gamma_2d_range:
		clf = SVC(C = C, gamma = gamma)
		clf.fit(x_2d, y_2d)
		classifiers.append((C, gamma, clf))

# visualization
# draw visualization of parameter effects
plt.figure(figsize = (8, 6))
xx, yy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
for (k, (C, gamma, clf)) in enumerate(classifiers):
	# evaluate decision function in a grid
	z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
	z = z.reshape(xx.shape)
	
	# visualization decision function for these parameters
	plt.subplot(len(C_2d_range), len(gamma_2d_range), k + 1)
	plt.title("gamma = 10^%d, C = 10^%d" %(np.log10(gamma), np.log10(C)), size = 'medium')

	# visualization parameter's effect an decision function
	plt.pcolormesh(xx, yy, -z, cmap = plt.cm.RdBu)
	plt.scatter(x_2d[:, 0], x_2d[:, 1], c = y_2d, cmap = plt.cm.RdBu_r)
	plt.xticks(())
	plt.yticks(())
	plt.axis('tight')


# plot the scores of th grid
# grid_scores_ contains parameter settings and scores
scores = [x[1] for x in grid.grid_scores_]
scores = np.array(scores).reshape(len(C_range), len(gamma_range))


# Draw heatmap of the validation accuracy as a function of gamma and C
# The score are encoded as colors with the hot colormap which varies from dark red to bright yellow. As the most interesting scores are all located in the 0.92 to 0.97 range we use a custom normalizer to set the mid-point to 0.92 so as to make it easier to visualize the small variations of score values in the interesting range while not brutally collapsing all the low score values to the same color.
plt.figure(figsize = (8, 6))
plt.subplots_adjust(left = 0.2, right = 0.95, bottom = 0.15, top = 0.95)
plt.imshow(scores, interpolation = 'nearest', cmap = plt.cm.hot, norm = MidpointNormalize(vmin = 0.2, midpoint = 0.92))

plt.xlabel('gamma')
plt.ylabel("C")
plt.colorbar()

plt.xticks(np.arange(len(gamma_range)), gamma_range, rotation = 45)
plt.yticks(np.arange(len(C_range)), C_range)
plt.title("Validation accuracy")
plt.show()
