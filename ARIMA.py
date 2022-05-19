import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
i = 0
res = []
res_pth = os.getcwd() + "\\data_code\\predict_q3.xlsx"
if (os.path.exists(res_pth)):
    os.remove(res_pth)
c = pd.ExcelWriter(res_pth)
c.save()
rmse_s = 100
if (os.path.exists(res_pth)):
    os.remove(res_pth)
c = pd.ExcelWriter(res_pth)
c.save()
while True:
    i += 1
    j = 0
    rmse_s = 100
    while True:
        j += 1
        a1 = int(j % 10)
        a2 = int(j % 100/10)
        a3 = int(j/100)
        df = pd.read_csv(os.getcwd()+"\\data_code\\deal_q3.csv", header=0, usecols=["time1", "x"+str(i), "y1"+str(i)])
        df1 = pd.read_csv(os.getcwd() + "\\data_code\\deal_q3.csv", header=0,usecols=["time1", "x" + str(i), "y2" + str(i)])
        # Creating train and test set
        # Index 10392 marks the end of October 2013
        train = df[:]
        test = df[:]
        train1 = df1[:]
        test1 = df1[:]

        ts_ARIMA = train['y1'+str(i)].astype(float)
        ts_ARIMA1 = train1['y2' + str(i)].astype(float)
        try:
            fit1 = ARIMA(ts_ARIMA, order=(a3, a2, a1)).fit()
            y_hat_ARIMA = fit1.predict(start=0, end=6, dynamic=False)
            plt.figure(figsize=(16, 8))
            plt.plot(train['y1'+str(i)], label='Train')
            plt.plot(test['y1'+str(i)], label='Test')


            from sklearn.metrics import mean_squared_error
            from math import sqrt

            rmse = sqrt(mean_squared_error(test['y1'+str(i)], y_hat_ARIMA.to_frame()))
            print("##################################################", rmse, a3, a2, a1, i)
            plt.plot(y_hat_ARIMA, label=rmse)
            plt.legend(loc='best')
            plt.show()
            fit2 = ARIMA(ts_ARIMA1, order=(a3, a2, a1)).fit()
            y_hat_ARIMA = fit1.predict(start=0, end=12, dynamic=False)
            y_hat_ARIMA1 = fit2.predict(start=0, end=12, dynamic=False)
            res_pth = os.getcwd() + "\\data_code\\predict_q3.xlsx"
            if rmse < rmse_s:
                rmse_s = rmse

                file_xls = pd.read_excel(res_pth)
                med = pd.Series(y_hat_ARIMA)
                med1 = pd.Series(y_hat_ARIMA1)
                file_xls['客户' + str(i) + "缴费金额"] = med
                file_xls['客户' + str(i) + "缴费次数"] = med1
                file_xls.to_excel(res_pth, sheet_name='Sheet1', index=False, header=True)

        except:
            pass
        if j > 777:
            break
    print("##################################################################################################################################################", i)
    if i > 1:
        break
print("\n\n\n\n\n\n\n", res)


