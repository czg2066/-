import os
import pandas as pd
import numpy as np


def get_mse(records_real):
    """
    均方误差
    """
    records_real = np.transpose(np.array(records_real))
    records_predict = np.copy(records_real)
    records_predict[:] = fee_mean
    if len(records_real) == len(records_predict):
        return float((sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real))**0.5)
    else:
        return None

pth_xls = os.listdir(os.getcwd()+"\\data_code")[0]
pth_xls = os.path.join(os.getcwd()+"\\data_code", pth_xls)
data = np.array(pd.read_excel(pth_xls))
fee_mean = sum(data[:, 2])/len(data)
client = list(set(data[:, 0]))
time_variance = []
cost_variance = []
time_mean = []
cost_mean = []
res_data = []
mse = []
res_data.append(client)
proba = []
client_rank = 1
flag = 0
sma_num = 1
for i in range(1, len(data)):
    if data[i, 0] == client[client_rank-1]:
        time_mean.append((data[i, 1]-data[i-1, 1]).days)
        time_variance.append((data[i, 1]-data[i-1, 1]).days)
        if data[i, 2] < fee_mean:
            sma_num += 1
    else:
        cost_mean.append(data[flag:i, 2])
        cost_variance.append(data[flag:i, 2])
        mse.append(get_mse(cost_mean[client_rank - 1:]))
        cost_mean[client_rank - 1] = np.mean(cost_mean[client_rank - 1:])
        time_mean[client_rank-1] = np.mean(time_mean[client_rank-1:])
        # sum(time_mean[client_rank-1:])/(len(time_mean[client_rank-1:]))
        cost_variance[client_rank - 1] = np.var(cost_variance[client_rank - 1:])
        time_variance[client_rank-1] = np.var(time_mean[client_rank-1:])
        proba.append(sma_num/len(time_mean[client_rank-1:]))
        time_mean[client_rank:] = []
        cost_mean[client_rank:] = []
        time_variance[client_rank:] = []
        cost_variance[client_rank:] = []
        client_rank += 1
        flag = i
        sma_num = 0
proba.append(sma_num/len(time_mean[client_rank-1:]))
cost_mean.append(data[flag:i, 2])
cost_variance.append(data[flag:i, 2])
mse.append(get_mse(cost_mean[client_rank - 1:]))
print(mse)
cost_mean[client_rank - 1] = np.mean(cost_mean[client_rank - 1:])
time_mean[client_rank-1] = np.mean(time_mean[client_rank-1:])
# sum(time_mean[client_rank-1:])/(len(time_mean[client_rank-1:]))
cost_variance[client_rank - 1] = np.var(cost_variance[client_rank - 1:])
time_variance[client_rank-1] = np.var(time_mean[client_rank-1:])
time_mean[client_rank:] = []
cost_mean[client_rank:] = []
time_variance[client_rank:] = []
cost_variance[client_rank:] = []
res_data.append(time_mean)
res_data.append(cost_mean)
res_data.append(time_variance)
res_data.append(cost_variance)
tag = np.array(pd.read_excel(os.getcwd()+"\\data_code\\q1_q2.xlsx"))
tag_races = tag[:, 2]
tag_num = list(tag_races)
ori_tag = ["高价值型客户", "潜力型客户", "大众型客户", "低价值型客户"]
ee = 0
for i in range(len(tag_races)):
    for j in range(4):
        if str(tag_races[i]) == ori_tag[j]:
            tag_num[i] = j
            break
res_pth = os.getcwd()+"\\data_code\\wait_to_train.xlsx"
if (os.path.exists(res_pth)):
    os.remove(res_pth)
c = pd.ExcelWriter(res_pth)
c.save()
mse[83] = 25                    # 异常值
mse[:] = (i/(max(mse)-min(mse)) for i in mse)
file_xlsx = pd.read_excel(res_pth)
file_xlsx['客户编号'] = pd.Series(res_data[0])
file_xlsx['平均缴费时间'] = pd.Series(res_data[1])
file_xlsx['平均缴费金额'] = pd.Series(res_data[2])
file_xlsx['缴费时间方差'] = pd.Series(res_data[3])
file_xlsx['缴费金额方差'] = pd.Series(res_data[4])
file_xlsx['客户类型'] = pd.Series(tag_races)
file_xlsx['客户类型编号'] = pd.Series(tag_num)
file_xlsx['风险概率'] = pd.Series(proba)
file_xlsx['均方误差'] = pd.Series(mse)
file_xlsx.to_excel(res_pth, sheet_name='Sheet1', index=False, header=True)