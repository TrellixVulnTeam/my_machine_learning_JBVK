# -*- coding: utf-8 -*-


from __future__ import print_function

import numpy as np
import logging
from optparse import OptionParser
import sys
from time import time
import matplotlib.pyplot as plt


from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics


# display progress logs on stdout
logging.basicConfig(level = logging.INFO, format = '%(asctime)s %(levelname)s')

# parse commandline arguments
op = OptionParser()

op.add_option("--report", action = "store_true", dest = "print_report", help = "Print a detailed classification report")

op.add_option("--chi2_select", action = "store", type = "int", dest = "select_chi2", help = "Select some number of features using a chi-squared test")

op.add_option("--confusion_matrix", action = "store_true", dest = "print_cm", help = "Print the confusion matrix.")

op.add_option("--top10", action="store_true", dest="print_top10", help="Print ten most discriminative terms per class for every classifier.")

op.add_option("--all_categories", action="store_true", dest="all_categories", help="Whether to use all categories or not.")

op.add_option("--use_hashing", action="store_true", help="Use a hashing vectorizer.")

op.add_option("--n_features", action="store", type=int, default=2 ** 16, help="n_features when using the hashing vectorizer.")

op.add_option("--filtered", action="store_true", help="Remove newsgroup information that is easily overfit: headers, signatures, and quoting.")


(opts, args) = op.parse_args()

if len(args) > 0:
	op.error("this script takes no arguments")
	sys.exit(1)

print(__doc__)
op.print_help()
print()

######################################################################################
# load some categories from the training set
if opts.all_categories:
	categories = None
else:
	categories = ['alt.atheism', 'talk.religion.misc', 'comp.graphics', 'sci.space']


if opts.filtered:
	remove = ('headers', 'footers', 'quotes')
else:
	remove = ()

print("loading 20 newsgroups dataset for categories: ")
print(categories if categories else "all")


data_train = fetch_20newsgroups(subset = 'train', categories = categories, shuffle = True, random_state = 42, remove = remove)

data_test = fetch_20newsgroups(subset = 'test', categories = categories, shuffle = True, random_state = 42, remove = remove)

print("data loaded......")

# for case categories == None
categories = data_train.target_names


def size_mb(docs):
	return sum(len(s.encode('utf-8')) for s in docs) / 1e6

data_train_size_mb = size_mb(data_train.data)
data_test_size_mb = size_mb(data_test.data)

print("%d documents - %0.3f MB (train set)" %(len(data_train.data), data_train_size_mb))
print("%d documents - %0.3f MB (test set)" %(len(data_test.data), data_test_size_mb))
print("%d categories" %len(categories))
print()


#split a train set and a test set
x_train, x_test = data_train.data, data_test.data
y_train, y_test = data_train.target, data_test.target

print("extracting features from the train set data using parser vectorizer")
t0 = time()
if opts.use_hashing:
	vectorizer = HashingVectorizer(stop_words = 'english', non_negative = True, n_features = opts.n_features)
	x_train = vectorizer.transform(data_train.data)
else:
	vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, stop_words = 'english')
	x_train = vectorizer.fit_transform(data_train.data)

duration = time() - t0
print("done in %fs at %0.3f MB/s" %(duration, data_train_size_mb / duration))
print("n_samples: %d, n_features: %d" %x_train.shape)
print()


print("extracting features from the test data using same vectorizer")
t0 = time()
x_test = vectorizer.transform(data_test.data)
duration = time() - t0
print("done in %fs at %0.3f MB/s" %(duration, data_test_size_mb / duration))
print("n_smaples: %d, n_features: %d" %x_test.shape)
print()


# mapping from integer feature name to original token string
if opts.use_hashing:
	feature_names = None
else:
	feature_names = vectorizer.get_feature_names()


if opts.select_chi2:
	print("extracting %d best features by a chi-squared test" %opts.select_chi2)
	t0 = time()
	ch2 = SelectKBest(chi2, k = opts.select_chi2)

	x_train = ch2.fit_transform(x_train, y_train)
	x_test = ch2.transform(x_test)

	if feature_names:
		# keep selected feature names
		feature_names = [feature_names[i] for i in ch2.get_support(indices = True)]
	print("done in %fs" %(time() - t0))
	print()


if feature_names:
	feature_names = np.asarray(feature_names)

def trim(s):
	# trim string to fit on terminal (assuming 80-colimn display)
	return s if len(s) <= 80 else s[:77] + "..."


####################################################################################
# benchmark classifiers
def benchmark(clf):
	print('_' * 80)
	print("training: ")
	print(clf)

	t0 = time()
	clf.fit(x_train, y_train)
	train_time = time() - t0
	print("train time: %0.3fs" %train_time)
	
	
	t0 = time()
	pred = clf.predict(x_test)
	test_time = time() - t0
	print("test time: %0.3f" %test_time)

	score = metrics.accuracy_score(y_test, pred)
	print("accuracy: %0.3f" %score)


	if hasattr(clf, 'coef_'):
		"""
		`coef_` : array, shape (n_features, ) or (n_targets, n_features)
        		Estimated coefficients for the linear regression problem.
        		If multiple targets are passed during the fit (y 2D), this
        		is a 2D array of shape (n_targets, n_features), while if only
        		one target is passed, this is a 1D array of length n_features
		"""
		print("dimensionality: %d" %clf.coef_.shape[1])
		print("density: %f" %density(clf.coef_))

		if opts.print_top10 and feature_names is not None:
			print("top 10 keywords per class: ")
			for i, category in enumerate(categories):
				top10 = np.argsort(clf.coef_[i])[-10:]
				print(trim("%s: %s" %(category, " ".join(feature_names[top10]))))
		print()
	
	if opts.print_report:
		print("classification report: ")
		print(metrics.classification_report(y_test, pred, target_names = categories))
	
	if opts.print_cm:
		print("confusion matrix: ")
		print(metrics.confusion_matrix(y_test, pred))
	
	print()
	clf_descr = str(clf).split('(')[0]
	
	return clf_descr, score, train_time, test_time


results = []
for clf, name in (
		(RidgeClassifier(tol = 1e-2, solver = "lsqr"), "Ridge Classifier"), 
		(Perceptron(n_iter = 50), "Perceptron"), 
		(PassiveAggressiveClassifier(n_iter = 50), "Passive-Aggressive"), 
		(KNeighborsClassifier(n_neighbors = 10), "kNN")):
	print("=" * 80)
	print(name)
	results.append(benchmark(clf))


for penalty in ["l2", "l1"]:
	print("=" * 80)
	print("%s penalty" %penalty.upper())

	# train LibLinear model
	results.append(benchmark(LinearSVC(loss = "l2", penalty = penalty, dual = False, tol = 1e-3)))

	# train SGD model
	results.append(benchmark(SGDClassifier(alpha = 0.0001, n_iter = 50, penalty = penalty)))


# train SGD with Elastic Net penalty
print("=" * 80)
print("Elastic-Net penalty")
results.append(benchmark(SGDClassifier(alpha = 0.0001, n_iter = 50, penalty = "elasticnet")))


# train NearestCentroid without threshold
print("=" * 80)
print("NearestCentroid (aka Rocchio classifer)")
results.append(benchmark(NearestCentroid()))

# train sparse Naive Bayes classifiers
print("=" * 80)
print("Naive Bayes")
results.append(benchmark(MultinomialNB(alpha = 0.01)))
results.append(benchmark(BernoulliNB(alpha = 0.01)))


print("=" * 80)
print("LinearSVC with L1-based feature selection")

# the smaller C, the stronger the regularization
# the more regularizetion, the more sparsity
results.append(benchmark(Pipeline([('feature_selection', LinearSVC(penalty = 'l1', dual = False, tol = 1e-3)), ('classification', LinearSVC())])))

print("results: ")
print(results)

# make the plot
indices = np.arange(len(results))
results = [[x[i] for x in results] for i in range(4)]

clf_names, score, train_time, test_time = results
train_time = np.array(train_time) / np.max(train_time)
test_time = np.array(test_time) / np.max(test_time)


plt.figure(figsize = (12, 8))
plt.title("score")

plt.barh(indices, score, 0.2, label = "score", color = 'r')
plt.barh(indices + 0.3, train_time, 0.2, label = "train time", color = 'g')
plt.barh(indices + 0.6, test_time, 0.2, label = "test time", color = 'b')

plt.yticks(())
plt.legend(loc = "best")

plt.subplots_adjust(left = 0.25)
plt.subplots_adjust(top = 0.95)
plt.subplots_adjust(bottom = 0.05)


for i, c in zip(indices, clf_names):
	plt.text(-0.3, i, c)

plt.show()





