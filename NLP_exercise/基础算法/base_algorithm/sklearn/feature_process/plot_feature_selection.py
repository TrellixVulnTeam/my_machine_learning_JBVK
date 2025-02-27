# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from sklearn.feature_selection import SelectPercentile, f_classif


iris = datasets.load_iris()
e = np.random.uniform(0, 0.1, size = (len(iris.data), 20))

x = np.hstack((iris.data, e))
y = iris.target

plt.figure(1)
plt.clf()
x_indices = np.arange(x.shape[-1])


# univariate feature selection with F-test for feature scoring, we use the default selection function: the 10% most significant features
selector = SelectPercentile(f_classif, percentile = 10)
selector.fit(x, y)
scores = -np.log10(selector.pvalues_)
scores /= scores.max()
plt.bar(x_indices - 0.45, scores, width = 0.2, label = r'Univariate score ($-Log(p_{value})$)', color = 'y')


# compare to the weights of SVM
clf = svm.SVC(kernel = 'linear')
clf.fit(x, y)
svm_weights = (clf.coef_**2).sum(axis = 0)
svm_weights /= svm_weights.max()
plt.bar(x_indices - 0.25, svm_weights, width = 0.2, label = 'SVM weight', color = 'r')


clf_selected = svm.SVC(kernel = 'linear')
clf_selected.fit(selector.transform(x), y)
svm_weights_selected = (clf_selected.coef_**2).sum(axis = 0)
svm_weights_selected /= svm_weights_selected.max()
plt.bar(x_indices[selector.get_support()] - 0.05, svm_weights_selected, width = 0.2, label = 'SVM weights after selection', color = 'b')

plt.title('comparing feature selection')
plt.xlabel('feature number')
plt.yticks(())
plt.axis('tight')
plt.legend(loc = 'upper right')
plt.show()

