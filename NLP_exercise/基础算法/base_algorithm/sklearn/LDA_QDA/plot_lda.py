# -*- coding: utf-8 -*-


from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# samples for training 
n_train = 20

# samples for testing
n_test = 200

# how often to repeat classification
n_averages = 50

# maximum number of features
n_features_max = 75

# step size for the calculation
step = 4


def generate_data(n_samples, n_features):
	# generate random blob-ish data with noisy features. 
	# this returns an array of input data with shape (n_samples, n_features) and an array of 'n_samples' target labels
	# only one feature contains discriminative information, the other features contains only noise

	x, y = make_blobs(n_samples = n_samples, n_features = 1, centers = [[-2], [2]])

	# add non-discriminative features
	if n_features > 1:
		x = np.hstack([x, np.random.randn(n_samples, n_features - 1)])
	return x, y


acc_clf1, acc_clf2 = [], []
n_features_range = range(1, n_features_max + 1, step)

for n_features in n_features_range:
	score_clf1, score_clf2 = 0, 0
	for _ in range(n_averages):
		x, y = generate_data(n_train, n_features)

		clf1 = LinearDiscriminantAnalysis(solver = 'lsqr', shrinkage = 'auto').fit(x, y)
		clf2 = LinearDiscriminantAnalysis(solver = 'lsqr', shrinkage = None).fit(x, y)

		x, y = generate_data(n_test, n_features)
		score_clf1 += clf1.score(x, y)
		score_clf2 += clf2.score(x, y)
	
	acc_clf1.append(score_clf1 / n_averages)
	acc_clf2.append(score_clf2 / n_averages)

features_samples_ratio = np.array(n_features_range) / n_train

plt.plot(features_samples_ratio, acc_clf1, linewidth = 2, label = 'Linear Discriminant Analysis with shrinkage', color = 'r')

plt.plot(features_samples_ratio, acc_clf2, linewidth = 2, label = 'Linear Discriminant Analysis', color = 'g')


plt.xlabel('n_features / n_samples')
plt.ylabel("classification accuracy")

plt.legend(loc = 1, prop = {'size': 12})
plt.suptitle('Linear Discriminant Analysis vs shrinkage Linear Discrimminant Analysis (1 discriminant feature)')
plt.show()







