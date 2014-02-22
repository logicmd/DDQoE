import numpy as np
from sklearn import datasets, preprocessing
from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import load_svmlight_file
import sys

def do(file_src):
    X_train, y_train = load_svmlight_file(file_src)

    X_train = X_train.toarray()
    #y_train = y_train.toarray()
    #print X_train
    X_test, y_test = X_train, y_train

    X_scaler = preprocessing.MinMaxScaler()
    X = X_scaler.fit_transform(X_train)
    #print X
    #Y_scaler = preprocessing.MinMaxScaler()
    #y = Y_scaler.fit_transform(y_train)

    if 'ad' not in file_src:
        y = ( y_train - np.min(y_train) ) / (np.max(y_train) - np.min(y_train))
        y_test = y
    else:
        y = y_train

    for depth in xrange(2,5):
        clf = DecisionTreeRegressor(max_depth=depth)

        clf.fit(X, y)

        y_predict = clf.predict(X)

        print("DT=%d Residual sum of squares: %.4f"
            % (depth, np.mean((y_predict - y_test) ** 2)))


if __name__ == "__main__":
    do(sys.argv[1])
