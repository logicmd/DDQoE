import numpy as np
from sklearn import datasets, linear_model
from sklearn.datasets import load_svmlight_file

X_train, y_train = load_svmlight_file("../dump/time_train4")

X_test, y_test = X_train, y_train

regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
              % np.mean((regr.predict(X_test) - y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_test, y_test))


X_train, y_train = load_svmlight_file("../dump/ad_train4")

X_test, y_test = X_train, y_train

regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
              % np.mean((regr.predict(X_test) - y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_test, y_test))


'''
# Plot outputs

pl.scatter(diabetes_X_test, diabetes_y_test,  color='black')
pl.plot(diabetes_X_test, regr.predict(diabetes_X_test), color='blue',
                linewidth=3)

pl.xticks(())
pl.yticks(())

pl.show()
'''
