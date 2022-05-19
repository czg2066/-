from keras import models
from keras import layers
import os
import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from matplotlib import cm
from sklearn.neighbors import KNeighborsClassifier


def draw_different_score(X_train, X_test, y_train, y_test):
    k_range = range(1, 20)
    scores = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        scores.append(knn.score(X_test, y_test))
    plt.figure()
    plt.xlabel('k')
    plt.ylabel(' accuracy ')
    plt.scatter(k_range, scores)
    plt.xticks([0, 5, 10, 15, 20])
    plt.show()


res_pth = os.getcwd()+"\\data_code\\wait_to_train.xlsx"
data = np.array(pd.read_excel(res_pth))

X = data[:, 1:5].astype('int')
y = data[:, 6].astype('int')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=3)
# cmap = cm.get_cmap('gnuplot')
# scatter = pd.scatter_matrix(X_train, c=y_train, marker='o', s=40, hist_kwds={'bins': 15}, figsize=(9, 9), cmap=cmap)
knn = KNeighborsClassifier(n_neighbors=8)
knn.fit(X_train, y_train)
# test the score
score = knn.score(X_test, y_test)
# try to predict
prediction = knn.predict_proba([[52.71428571, 123.375, 150.6455643, 3039.484375]])
print(prediction)
# test


