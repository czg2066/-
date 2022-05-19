import pandas as pd
import matplotlib.pyplot as plt

# Subsetting the dataset
# Index 11856 marks the end of year 2013
df = pd.read_csv('train.csv', nrows=11856)
# Creating train and test set
# Index 10392 marks the end of October 2013
train = df[0:10392]
test = df[10392:]

# Aggregating the dataset at daily level
df['Timestamp'] = pd.to_datetime(df['Datetime'], format='%d-%m-%Y %H:%M')  # 4位年用Y，2位年用y
df.index = df['Timestamp']
df = df.resample('D').mean()  # 按天采样    ，计算均值

train['Timestamp'] = pd.to_datetime(train['Datetime'], format='%d-%m-%Y %H:%M')
train.index = train['Timestamp']
train = train.resample('D').mean()  #
print(train, train.Count)
test['Timestamp'] = pd.to_datetime(test['Datetime'], format='%d-%m-%Y %H:%M')
test.index = test['Timestamp']
test = test.resample('D').mean()

# Plotting data
# print("train", type(train.Count), train.Count, "\ntest", test)
train.Count.plot(figsize=(15, 8), title='Daily Ridership', fontsize=14)
test.Count.plot(figsize=(15, 8), title='Daily Ridership', fontsize=14)
plt.show()
