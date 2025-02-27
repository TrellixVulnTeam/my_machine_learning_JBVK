# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import r2_score

###############################################################

# generate some sparsity data
np.random.seed(42)

n_samples, n_features = 50, 200
x = np.random.randn(n_samples, n_features)
coef = 3 * np.random.randn(n_features)
inds = np.arange(n_features)

np.random.shuffle(inds)

# sparsity coef
coef[inds[10:]] = 0
y = np.dot(x, coef)

# add noise
y += 0.01 * np.random.normal((n_samples, ))


# split data in train set and test set 
x_train, y_train = x[: n_samples / 2], y[: n_samples / 2]
x_test, y_test = x[n_samples / 2 :], y[n_samples / 2 :]


####################################################################
# Lasso
from sklearn.linear_model import Lasso

alpha = 0.1
lasso = Lasso(alpha = alpha)

y_pred_lasso = lasso.fit(x_train, y_train).predict(x_test)
r2_score_lasso = r2_score(y_test, y_pred_lasso)
print(lasso)
print("r^2 on test data: %f" %r2_score_lasso)


##################################################################
# Elasticnet
from sklearn.linear_model import ElasticNet

enet = ElasticNet(alpha = alpha, l1_ratio = 0.7)

y_pred_enet = enet.fit(x_train, y_train).predict(x_test)
r2_score_enet = r2_score(y_test, y_pred_enet)
print(enet)
print("r^2 on test data: %f" %r2_score_enet)


# plot
plt.plot(enet.coef_, label = 'Elatic net coefficients')
plt.plot(lasso.coef_, label = 'Lasso coefficients')
plt.plot(coef, '--', label = 'original coefficients')

plt.legend(loc = 'best')
plt.title("Lasso R^2: %f, Elastic Net R^2: %f" %(r2_score_lasso, r2_score_enet))
plt.show()
















