# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelBinarizer
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA


def plot_hyperplane(clf, min_x, max_x, linestyle, label):
	# get the separating hyperplane
	w = clf.coef_[0]
	a = -w[0] / w[1]
	xx = np.linspace(min_x - 5, max_x + 5)
	yy = a * xx - (clf.intercept_[0]) / w[1]
	plt.plot(xx, yy, linestyle, label = label)


def plot_subfigure(x, y, subplot, title, transform):
	if transform == 'pca':
		x = PCA(n_components = 2).fit_transform(x)
	elif transform == 'cca':
		x = CCA(n_components = 2).fit(x, y).transform(x)
	else:
		raise ValueError

	min_x = np.min(x[:, 0])
	max_x = np.max(x[:, 0])
	min_y = np.min(x[:, 1])
	max_y = np.max(x[:, 1])

	classif = OneVsRestClassifier(SVC(kernel = 'linear'))
	classif.fit(x, y)
	plt.subplot(2, 2, subplot)
	plt.title(title)

	zero_class = np.where(y[:, 0])
	one_class = np.where(y[:, 1])
	plt.scatter(x[:, 0], x[:, 1], s = 40, c = 'gray')
	plt.scatter(x[zero_class, 0], x[zero_class, 1], s = 160, edgecolors = 'b', facecolors = 'none', linewidth = 2, label = 'Class 1')
	plt.scatter(x[one_class, 0], x[one_class, 1], s = 80, edgecolors = 'orange', facecolors = 'none', linewidth = 2, label = 'Class 2')
	

	plot_hyperplane(classif.estimators_[0], min_x, max_x, 'k--', 'Boundary\nfor class 1')
	plot_hyperplane(classif.estimators_[1], min_x, max_x, 'k-.', 'Boundary\nfor class 2')

	plt.xticks(())
	plt.yticks(())
	plt.xlim(min_x - 0.5 * max_x, max_x + 0.5 * max_x)
	plt.ylim(min_y - 0.5 * max_y, max_y + 0.5 * max_y)

	if subplot == 2:
		plt.xlabel('First principle component')
		plt.ylabel('Second principle component')
		plt.legend(loc = 'upper left')

plt.figure(figsize = (8, 6))
x, y = make_multilabel_classification(n_classes = 2, n_labels = 1, allow_unlabeled = True, random_state = 1)
plot_subfigure(x, y, 1, 'with unlabeled sample + CCA', 'cca')
plot_subfigure(x, y, 2, 'with unlabeled sample + PCA', 'pca')


x, y = make_multilabel_classification(n_classes = 2, n_labels = 1, allow_unlabeled = False, random_state = 1)
plot_subfigure(x, y, 3, 'without unlabeled sample + CCA', 'cca')
plot_subfigure(x, y, 4, 'without unlabeled sample + PCA', 'pca')

plt.subplots_adjust(0.04, 0.02, 0.97, 0.94, 0.09, 0.2)
plt.show()

