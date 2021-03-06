import numpy as np
from sklearn import datasets, linear_model, preprocessing
from sklearn.datasets import load_svmlight_file
import sys

'''class Linear:
    def __init__(self, file_src):
        self.file_src = file_src
        self.X_train = None
        self.Y_train = None
        self.X_train
'''
def do(file_src):
    X_train, y_train = load_svmlight_file(file_src)

    X_train = X_train.toarray()
    #y_train = y_train.toarray()
    #print X_train
    X_train = X_train[:,[0,2]]
    X_test, y_test = X_train, y_train

    X_scaler = preprocessing.MinMaxScaler()
    X = X_scaler.fit_transform(X_train)
    #print X
    #Y_scaler = preprocessing.MinMaxScaler()
    #y = Y_scaler.fit_transform(y_train)

    regr = linear_model.LinearRegression()
    regr.fit(X, y_train)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean square error
    print("Residual sum of squares: %.2f"
            % np.mean((regr.predict(X) - y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    #print('Variance score: %.2f' % regr.score(X_test, y_test))
    #print regr.get_params()

if __name__ == "__main__":
    #print sys.argv[1]
    do(sys.argv[1])
