import matplotlib.pyplot as plt
import CoolProp as CP
import datetime as dt
import numpy as np
import pandas as pd
import collections
import itertools
import os
import statistics
import datetime

# month = str(datetime.datetime.today().month)
# day = str(datetime.datetime.today().day)
month = '02'
day = '22'

if len(month) == 1:
    month = '0' + month
if len(day) == 1:
    day = '0' + day

data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\{}{} temp.csv'.format(month,day,month,day),engine='python').fillna(method='bfill').fillna(method='ffill')
power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\outdoor_3069.csv'.format(month,day))

# data['Date'] + ' ' +
data['updated_time'] = data['Time']

y1 = data[['updated_time','point41']]
y2 = data[['updated_time','point42']]
y3 = data[['updated_time','point43']]
y4 = data[['updated_time','point44']]
y5 = data[['updated_time','point45']]
y6 = data[['updated_time','point46']]
y7 = data[['updated_time','point47']]
y8 = data[['updated_time','point48']]
y9 = data[['updated_time','point49']]
y10 = data[['updated_time','point50']]
# y11 = data[['updated_time','point63']]
# y12 = data[['updated_time','point64']]
# y13 = data[['updated_time','point65']]

y1.index = pd.to_datetime(y1['updated_time'])
y1.drop('updated_time',inplace=True,axis=1)
y1 = y1.point41.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y2.index = pd.to_datetime(y2['updated_time'])
y2.drop('updated_time',inplace=True,axis=1)
y2 = y2.point42.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y3.index = pd.to_datetime(y3['updated_time'])
y3.drop('updated_time',inplace=True,axis=1)
y3 = y3.point43.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y4.index = pd.to_datetime(y4['updated_time'])
y4.drop('updated_time',inplace=True,axis=1)
y4 = y4.point44.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y5.index = pd.to_datetime(y5['updated_time'])
y5.drop('updated_time',inplace=True,axis=1)
y5 = y5.point45.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
y6.index = pd.to_datetime(y6['updated_time'])
y6.drop('updated_time',inplace=True,axis=1)
y6 = y6.point46.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
y7.index = pd.to_datetime(y7['updated_time'])
y7.drop('updated_time',inplace=True,axis=1)
y7 = y7.point47.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
y8.index = pd.to_datetime(y8['updated_time'])
y8.drop('updated_time',inplace=True,axis=1)
y8 = y8.point48.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
y9.index = pd.to_datetime(y9['updated_time'])
y9.drop('updated_time',inplace=True,axis=1)
y9 = y9.point49.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
y10.index = pd.to_datetime(y10['updated_time'])
y10.drop('updated_time',inplace=True,axis=1)
y10 = y10.point50.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
# y11.index = pd.to_datetime(y11['updated_time'])
# y11.drop('updated_time',inplace=True,axis=1)
# y11 = y11.point63.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
# y12.index = pd.to_datetime(y12['updated_time'])
# y12.drop('updated_time',inplace=True,axis=1)
# y12 = y12.point64.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')
# y13.index = pd.to_datetime(y13['updated_time'])
# y13.drop('updated_time',inplace=True,axis=1)
# y13 = y13.point65.resample('1T').mean().apply(lambda x: None if x<-10 or x>15 else x).fillna(method='bfill').fillna(method='ffill')

#y11,y12,y13
overall = pd.concat([y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,],axis=1).to_csv('./temp_resample_upper.csv')

#
#                        statistics.mean(y11),statistics.mean(y12),statistics.mean(y13)
# print(statistics.mean([statistics.mean(y1),statistics.mean(y2),statistics.mean(y3),statistics.mean(y4),
#                        statistics.mean(y5),statistics.mean(y6),statistics.mean(y7),statistics.mean(y8),
#                        statistics.mean(y9),statistics.mean(y10)]))

power.index = pd.to_datetime(power['updated_time'])
power = power.loc[y1.index[0]:y1.index[len(y1)-1],'value'].apply(lambda x: -x if x<0 else x)
# power = power.loc[y1.index[0]:y1.index[len(y1)-1],'fan_step']
print(statistics.mean(power))

x = []
zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(y1)):
    x.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

fig, ax1 = plt.subplots(2,5, figsize=(10,12))
ax1[0,0].plot(range(len(x)), y1, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[0,0].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

ax1[0,1].plot(range(len(x)), y2, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[0,1].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

ax1[0,2].plot(range(len(x)), y3, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[0,2].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

ax1[0,3].plot(range(len(x)), y4, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[0,3].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

ax1[0, 4].plot(range(len(x)), y5, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[0, 4].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

ax1[1, 0].plot(range(len(x)), y6, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[1, 0].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])

ax1[1, 1].plot(range(len(x)), y7, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[1, 1].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])

ax1[1, 2].plot(range(len(x)), y8, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[1, 2].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])

ax1[1, 3].plot(range(len(x)), y9, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[1, 3].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])

ax1[1, 4].plot(range(len(x)), y10, color='b', linewidth=1.5,linestyle='-')
ax2 = ax1[1, 4].twinx()
ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
ax2.set_yticks([0,10000,20000,30000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

# ax1[2, 1].plot(range(len(x)), y11, color='b', linewidth=1.5,linestyle='-')
# ax2 = ax1[2, 1].twinx()
# ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
# ax2.set_yticks([0,10000,20000,30000,40000])
# # ax2.set_yticks([0,10,20,30,40,50])
#
# ax1[2, 2].plot(range(len(x)), y12, color='b', linewidth=1.5,linestyle='-')
# ax2 = ax1[2, 2].twinx()
# ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
# ax2.set_yticks([0,10000,20000,30000,40000])
# # ax2.set_yticks([0,10,20,30,40,50])
#
# ax1[2, 3].plot(range(len(x)), y13, color='b', linewidth=1.5,linestyle='-')
# ax2 = ax1[2, 3].twinx()
# ax2.plot(range(len(x)), power, color='gray', linewidth=1.5,linestyle='--')
# ax2.set_yticks([0,10000,20000,30000,40000])
# # ax2.set_yticks([0,10,20,30,40,50])
#
# ax2 = ax1[2, 0].twinx()
# ax2.set_yticks([0,10000,20000,30000,40000])
# # ax2.set_yticks([0,10,20,30,40,50])
#
# ax2 = ax1[2, 4].twinx()
# ax2.set_yticks([0,10000,20000,30000,40000])
# # ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [W]', fontsize=14)
# # ax2.set_ylabel('Fan step [step]', fontsize=14)

for i in range(2):
    for j in range(5):
        ax1[i,j].set_yticks([-20,-10,0,10,20])
        ax1[i,0].set_ylabel('Temperature [C]', fontsize=14)
        ax1[i,j].set_xticks([0, (len(x) // 2), len(x)])
        ax1[i,j].set_xticklabels([x[n] for n in range(len(x)) if n % (len(x) // 2) == 0 or x[n] == x[-1]])
        ax1[i,j].grid(linestyle="--", color='lightgray')

plt.tight_layout()
plt.show()
