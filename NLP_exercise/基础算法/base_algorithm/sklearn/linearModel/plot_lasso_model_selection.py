# -*- coding: utf-8 -*-

import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LassoCV, LassoLarsCV, LassoLarsIC
from sklearn import datasets

diabetes = datasets.load_diabetes()
x = diabetes.data
y = diabetes.target

rng = np.random.RandomState(42)

# add some bad features
x = np.c_[x, rng.randn(x.shape[0], 14)]

# normalize data as done by Lars to allow for comparison
x /= np.sqrt(np.sum(x ** 2, axis = 0))

###################################################################

# LassoLarsIC: Least angle regression with BIC/AIC criterion
model_bic = LassoLarsIC(criterion = 'bic')
t1 = time.time()
model_bic.fit(x, y)
t_bic = time.time() - t1
alpha_bic_ = model_bic.alpha_


model_aic = LassoLarsIC(criterion = 'aic')
model_aic.fit(x, y)
alpha_aic_ = model_aic.alpha_


def plot_ic_criterion(model, name, color):
	alpha_ = model.alpha_
	alphas_ = model.alphas_

	criterion_ = model.criterion_
	plt.plot(-np.log10(alphas_), criterion_, '--', color = color, linewidth = 3, label = '%s estimate' %name)
	plt.axvline(-np.log10(alpha_), color = color, linewidth = 3, label = 'alpha: %sestimate' %name)

	plt.xlabel("-log(alpha)")
	plt.ylabel("criterion")


plt.figure()
plot_ic_criterion(model_aic, "AIC", 'b')
plot_ic_criterion(model_bic, "BIC", 'r')

plt.legend()
plt.title("Information-criterion for model selection (training time %0.3fs)" % t_bic)

###################################################################

# LassoCV: coordinate descent
# compute path
print("computing regularization path using the coordinate descent lasso...")

t1 = time.time()

# parameter:
# cv: int
# 	cross-validation generator or an iterable
model = LassoCV(cv = 20).fit(x, y)
t_lasso_cv = time.time() - t1

# display the results
m_log_alphas = -np.log10(model.alphas_)

plt.figure()

ymin, ymax = 2300, 3800
plt.plot(m_log_alphas, model.mse_path_, ":")
plt.plot(m_log_alphas, model.mse_path_.mean(axis = -1), 'k', label = "Average across the folds", linewidth = 2)
plt.axvline(-np.log10(model.alpha_), linestyle = '--', color = 'k', label = 'alpha: CV estimate')

plt.legend()
plt.xlabel('-log(alpha)')
plt.ylabel('mean square error')
plt.title('mean square error on each fold: coordinate descent (train time: %0.2fs)' %t_lasso_cv)

plt.axis('tight')
plt.ylim(ymin, ymax)

###############################################################

# LassoLarsCV: least angle regression
# compute paths
print("computing regularization path using the Lars lasso...")
t1 = time.time()
model = LassoLarsCV(cv = 20).fit(x, y)
t_lasso_lars_cv = time.time() - t1


# display results
m_log_alphas = -np.log10(model.cv_alphas_)

plt.figure()
plt.plot(m_log_alphas, model.cv_mse_path_, ":")
plt.plot(m_log_alphas, model.cv_mse_path_.mean(axis = -1), 'k', label = 'Average across the folds', linewidth = 2)
plt.axvline(-np.log10(model.alpha_), linestyle = '--', color = 'k', label = 'alpha CV')

plt.legend()
plt.xlabel('-log(alpha)')
plt.ylabel('mean square error')

plt.title('mean square error on each fold: Lars (trian time: %0.2fs)' %t_lasso_lars_cv)
plt.axis('tight')
plt.ylim(ymin, ymax)

plt.show()







