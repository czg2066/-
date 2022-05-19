from sklearn import tree    # 导入需要的模块
import os
import pandas as pd
import numpy as np
import sklearn
import graphviz
from sklearn.model_selection import train_test_split


def bubble_sort(li):
    """冒泡排序"""
    for i in range(len(li) - 1):
        # 创建一个标志位，用来记录本轮冒泡，是否有数据交换位置
        status = False
        for j in range(len(li) - i - 1):
            if li[j] < li[j + 1]:
                li[j], li[j + 1] = li[j + 1], li[j]
                # 只要由数据交换位置，则修改statusd的值
                status = True
        # 每一轮冒泡结束之后，判断当前status是否为Flase,
        # 如果为Flase，则说明上一轮冒泡没有修改任何数据的顺序（即数据是有序的）
        if not status:
            return li
    return li


res_pth = os.getcwd()+"\\data_code\\wait_to_train.xlsx"
data_ori = np.array(pd.read_excel(res_pth))
data = np.delete(data_ori, np.where(data_ori[:, 6] == 1)[:][0], axis=0)
data = np.delete(data, np.where(data[:, 6] == 2)[:][0], axis=0)
X = data[:, 1:5].astype('int')
y = data[:, 6].astype('int')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=10)
clf = tree.DecisionTreeClassifier(criterion="entropy",
                                  random_state=30,
                                  splitter="random",
                                  max_depth=20,
                                  min_samples_leaf=3,     # 一个节点分支后，每一个子节点至少包含10个样本
                                  min_samples_split=3)    # 一个点至少包含10个样本才会分支
# clf = tree.DecisionTreeRegressor(max_depth=5)
clf = clf.fit(X_train, y_train)          # 用训练集数据训练模型
result = clf.score(X_test, y_test)       # 对我们训练的模型精度进行打分
print(result)
possi = []
predict_data = np.delete(data_ori, np.where(data_ori[:, 6] == 0)[:][0], axis=0)
predict_data = np.delete(predict_data, np.where(predict_data[:, 6] == 3)[:][0], axis=0)
for i in range(len(predict_data)):
    prediction = clf.predict_proba([predict_data[i, 1:5]])
    possi.append(prediction[0])
feature_name = ['high value', 'potential', 'public', 'low value']
dot_data = tree.export_graphviz(clf,      # 训练好的模型
                                out_file=os.getcwd()+"\\data_code\\tree3.dot",
                                feature_names=feature_name,
                                class_names=["high value", "low value"],
                                filled=True,    # 进行颜色填充
                                rounded=True)   # 树节点的形状控制
res = []
for i in range(len(data)):
    res.append(possi[i][0]*(1-data[i][7])*data[i][8])
ori_res = np.copy(res)
res = bubble_sort(res)
five_comsumers = []
for i in range(5):
    five_comsumers.append(int(data[np.where(ori_res[:] == res[i])[0], 0]))
print(five_comsumers)
