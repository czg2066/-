import os
import pandas as pd
import numpy as np

pth_xls = os.listdir(os.getcwd()+"\\data_code")[0]
pth_xls = os.path.join(os.getcwd()+"\\data_code", pth_xls)
data = np.array(pd.read_excel(pth_xls))
flag = '1'
amount = []
amounttimes = []
add_data = []
all_data = []
date = []
date_med = []
for i in range(len(data)):
    if flag != data[i, 0]:
        flag = data[i, 0]
        if add_data:
            amount.append(sum(add_data)/len(add_data))
            amounttimes.append(t)
            all_data.append(add_data)
            date.append(date_med)
        add_data = []
        date_med = []
        add_data.append(data[i, 2])
        date_med.append(data[i, 1])
        t = 1
    else:
        date_med.append(data[i, 1])
        add_data.append(data[i, 2])
        t += 1

amount.append(sum(add_data)/len(add_data))
amounttimes.append(t)
all_data.append(add_data)
date.append(date_med)
amount.append(sum(amount)/len(amount))
amounttimes.append(sum(amounttimes)/len(amounttimes))
rates = []
for i in range(len(amount)):
    if amount[i] >= amount[-1]:
        if amounttimes[i] >= amounttimes[-1]:
            rates.append("高价值型客户")
        else:
            rates.append("潜力型客户")
    else:
        if amounttimes[i] >= amounttimes[-1]:
            rates.append("大众型客户")
        else:
            rates.append("低价值型客户")

rates = pd.Series(rates)
amount = pd.Series(amount)
amounttimes = pd.Series(amounttimes)
res_pth = os.getcwd()+"\\data_code\\居民客户的用电缴费习惯分析1.xlsx"
if (os.path.exists(res_pth)):
    os.remove(res_pth)
c = pd.ExcelWriter(res_pth)
c.save()
file_xlsx = pd.read_excel(res_pth)
file_xlsx['客户编号'] = pd.Series(list(set(data[:, 0])))
file_xlsx['平均缴费金额'] = amount
file_xlsx['缴费次数'] = amounttimes
file_xlsx.to_excel(res_pth, sheet_name='Sheet1', index=False, header=True)
file_xlsx.to_csv(os.getcwd()+"\\data_code\\居民客户的用电缴费习惯分析1.csv", encoding='utf-8')
res_pth = os.getcwd()+"\\data_code\\居民客户的用电缴费习惯分析2.xlsx"
if (os.path.exists(res_pth)):
    os.remove(res_pth)
c = pd.ExcelWriter(res_pth)
c.save()
file_xlsx = pd.read_excel(res_pth)
file_xlsx['客户编号'] = pd.Series(list(set(data[:, 0])))
file_xlsx['客户类型'] = rates
file_xlsx.to_excel(res_pth, sheet_name='Sheet1', index=False, header=True)
file_xlsx.to_csv(os.getcwd()+"\\data_code\\居民客户的用电缴费习惯分析2.csv", encoding='utf-8')

res_pth = os.getcwd()+"\\data_code\\deal_q3.xlsx"
if (os.path.exists(res_pth)):
    os.remove(res_pth)
c = pd.ExcelWriter(res_pth)
c.save()
file_xls = pd.read_excel(res_pth)
for i in range(1, len(all_data)):
    med2 = pd.Series(date[i])
    file_xls['time'+str(i)] = med2
    file_xls['x' + str(i)] = pd.Series(range(1, len(med2)+1))
    med1 = pd.Series(all_data[i])
    file_xls['y1'+str(i)] = med1
    file_xls['y2' + str(i)] = amounttimes
file_xls.to_excel(res_pth, sheet_name='Sheet1', index=False, header=True)
file_xls.to_csv(os.getcwd()+"\\data_code\\deal_q3.csv", encoding='utf-8')
