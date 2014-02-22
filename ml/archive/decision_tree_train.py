from sklearn.datasets import load_svmlight_file
from sklearn.tree import DecisionTreeRegressor

X_train, y_train = load_svmlight_file("../dump/time_train")

X_test, y_test = X_train, y_train

clf_1 = DecisionTreeRegressor(max_depth=2)
clf_2 = DecisionTreeRegressor(max_depth=5)

clf_1.fit(X_train, y_train)
clf_2.fit(X_train, y_train)

y_1 = clf_1.predict(X_test)
y_2 = clf_2.predict(X_test)

# The mean square error
print("Residual sum of squares(depth=2): %.2f"
              % np.mean((clf_1.predict(X_test) - y_test) ** 2))

print("Residual sum of squares(depth=2): %.2f"
              % np.mean((clf_2.predict(X_test) - y_test) ** 2))


X_train, y_train = load_svmlight_file("../dump/ad_train")

X_test, y_test = X_train, y_train

clf_1 = DecisionTreeRegressor(max_depth=2)
clf_2 = DecisionTreeRegressor(max_depth=5)

clf_1.fit(X_train, y_train)
clf_2.fit(X_train, y_train)

y_1 = clf_1.predict(X_test)
y_2 = clf_2.predict(X_test)

# The mean square error
print("Residual sum of squares(depth=2): %.2f"
              % np.mean((clf_1.predict(X_test) - y_test) ** 2))

print("Residual sum of squares(depth=2): %.2f"
              % np.mean((clf_2.predict(X_test) - y_test) ** 2))
