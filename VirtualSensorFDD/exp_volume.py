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
day = '24'

if len(month) == 1:
    month = '0' + month
if len(day) == 1:
    day = '0' + day

data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\{}{} volume1.csv'.format(month,day,month,day),engine='python')
power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\outdoor_3069.csv'.format(month,day))

time1 = data['Time']

velocity1 = data[['Time','volume']]
velocity1['volume'] = velocity1['volume'].apply(lambda x: 0 if x < 0 else x)

velocity1.index = pd.to_datetime(velocity1['Time'])
velocity1.drop('Time',inplace=True,axis=1)
velocity1 = velocity1.volume.resample('1T').mean()
velocity1 = velocity1.dropna()
velocity1 = velocity1

power.index = pd.to_datetime(power['updated_time'])
power1 = power.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'value'].apply(lambda x: -x if x<0 else x)
# power1 = power.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'fan_step']

print(power1)
print(statistics.mean([statistics.mean(velocity1)]))
print(statistics.mean([statistics.mean(power1)]))

x1 = []
zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(velocity1)):
    x1.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

fig, ax1 = plt.subplots(figsize=(15, 4))
print(len(x1))
ax1.plot(range(len(x1)), velocity1, color='b', linewidth=1.5,linestyle='-')
ax1.set_xticks([0,10,20,30])
ax1.set_xticklabels([x1[0],x1[10],x1[20],x1[29]])
ax1.set_yticks([0,1000,2000,3000,4000,5000])
ax2 = ax1.twinx()
ax2.plot(range(len(x1)), power1,color='gray', linewidth=1.5, linestyle='--')
ax2.set_yticks([0,5000,10000,15000,20000,25000,30000,35000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
ax2.set_ylabel('Power [kW]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)
#
ax1.set_ylabel('Air Volume [$m^3/h$]', fontsize=14)
ax1.grid(linestyle="--", color='lightgray')
# ax1[i,j].set_xticks([0, 100, 200, 300, 400, 500, 599])
# ax1[i].set_xticklabels([x[6 * k:6 * (k + 1) + 1][n].strftime('%H:%M:%S') for n in range(len(x[6 * k:6 * (k + 1) + 1]))])

plt.tight_layout()
plt.show()
