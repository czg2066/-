import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller

df = pd.read_csv(os.getcwd()+"\\data_code\\deal_q3.csv", header=0)# , usecols=["time1", "x1", "y12"])
df['y1'] = df['y12'].diff().shift()
print(df['y1'])
i = 0
while True:
    i += 1
    plt.plot(df["y1"+str(i)])
    plt.show()
    if i>100:
        break


# Creating train and test set
# Index 10392 marks the end of October 2013
train = df[:]
test = df[:]

ts_ARIMA = train['y12'].astype(float)

fit1 = ARIMA(ts_ARIMA, order=(1, 0, 1)).fit()
y_hat_ARIMA = fit1.predict(start=0, end=6, dynamic=False)
print(y_hat_ARIMA)
plt.figure(figsize=(16, 8))
plt.plot(train['y12'], label='Train')
plt.plot(test['y12'], label='Test')


from sklearn.metrics import mean_squared_error
from math import sqrt

rmse = sqrt(mean_squared_error(test['y12'], y_hat_ARIMA.to_frame()))
print("##################################################", rmse)
y_hat_ARIMA = fit1.predict(start=0, end=7, dynamic=False)
# file_handle.writelines(str([a3, a2, a1, i, rmse, y_hat_ARIMA[6]])+"\n")
plt.plot(y_hat_ARIMA, label=rmse)
plt.legend(loc='best')

diff1 = df.y12.diff().dropna()
plot_acf(diff1) #生成自相关图
diff2 = df.y12.diff(2).dropna()
yarn_result = adfuller(df.y12, 1, autolag='AIC')
yarn_result2 = adfuller(diff1, 1, autolag='AIC')
yarn_result3 = adfuller(diff2, 1, autolag='AIC')
print('1阶差分后 ADF: %f' % yarn_result2[0])
print('1阶差分后 p value: %f' % yarn_result2[1])
print('2阶差分后 ADF: %f' % yarn_result3[0])
print('2阶差分后 p value: %f' % yarn_result3[1])
print('差分前 ADF: %f' % yarn_result[0])
print('差分前 p value: %f' % yarn_result[1])
print(yarn_result, "\n", yarn_result2, "\n", yarn_result3, "\n")
plt.show()
