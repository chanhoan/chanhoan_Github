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
day = '25'

if len(month) == 1:
    month = '0' + month
if len(day) == 1:
    day = '0' + day

data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\{}{} flow2.csv'.format(month,day,month,day),engine='python')
power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\outdoor_3069.csv'.format(month,day))

velocity1 = data[['Time1','velocity1']]
velocity2 = data[['Time2','velocity2']]
velocity3 = data[['Time3','velocity3']]
velocity4 = data[['Time4','velocity4']]
velocity5 = data[['Time5','velocity5']]
velocity6 = data[['Time6','velocity6']]
velocity7 = data[['Time7','velocity7']]
velocity8 = data[['Time8','velocity8']]

velocity1.index = pd.to_datetime(velocity1['Time1'])
velocity1.drop('Time1',inplace=True,axis=1)
velocity1 = velocity1.velocity1.resample('1T').mean()
velocity1 = velocity1.apply(lambda x: 0 if x<0 else x)
velocity2.index = pd.to_datetime(velocity2['Time2'])
velocity2.drop('Time2',inplace=True,axis=1)
velocity2 = velocity2.velocity2.resample('1T').mean()
velocity2 = velocity2.apply(lambda x: 0 if x<0 else x)
velocity3.index = pd.to_datetime(velocity3['Time3'])
velocity3.drop('Time3',inplace=True,axis=1)
velocity3 = velocity3.velocity3.resample('1T').mean()
velocity3 = velocity3.apply(lambda x: 0 if x<0 else x)
velocity4.index = pd.to_datetime(velocity4['Time4'])
velocity4.drop('Time4',inplace=True,axis=1)
velocity4 = velocity4.velocity4.resample('1T').mean()
velocity4 = velocity4.apply(lambda x: 0 if x<0 else x)
velocity5.index = pd.to_datetime(velocity5['Time5'])
velocity5.drop('Time5',inplace=True,axis=1)
velocity5 = velocity5.velocity5.resample('1T').mean()
velocity5 = velocity5.apply(lambda x: 0 if x<0 else x)
velocity6.index = pd.to_datetime(velocity6['Time6'])
velocity6.drop('Time6',inplace=True,axis=1)
velocity6 = velocity6.velocity6.resample('1T').mean()
velocity6 = velocity6.apply(lambda x: 0 if x<0 else x)
velocity7.index = pd.to_datetime(velocity7['Time7'])
velocity7.drop('Time7',inplace=True,axis=1)
velocity7 = velocity7.velocity7.resample('1T').mean()
velocity7 = velocity7.apply(lambda x: 0 if x<0 else x)
velocity8.index = pd.to_datetime(velocity8['Time8'])
velocity8.drop('Time8',inplace=True,axis=1)
velocity8 = velocity8.velocity8.resample('1T').mean()
velocity8 = velocity8.apply(lambda x: 0 if x<0 else x)

power.index = pd.to_datetime(power['updated_time'])
# power1 = power.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'value'].apply(lambda x: -x if x<0 else x)
# power2 = power.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'value'].apply(lambda x: -x if x<0 else x)
# power3 = power.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'value'].apply(lambda x: -x if x<0 else x)
# power4 = power.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'value'].apply(lambda x: -x if x<0 else x)
# power5 = power.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'value'].apply(lambda x: -x if x<0 else x)
# power6 = power.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'value'].apply(lambda x: -x if x<0 else x)
# power7 = power.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'value'].apply(lambda x: -x if x<0 else x)
# power8 = power.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'value'].apply(lambda x: -x if x<0 else x)
power1 = power.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'fan_step']
power2 = power.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'fan_step']
power3 = power.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'fan_step']
power4 = power.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'fan_step']
power5 = power.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'fan_step']
power6 = power.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'fan_step']
# power7 = power.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'fan_step']
# power8 = power.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'fan_step']

# statistics.mean(velocity7), statistics.mean(velocity8),
print(statistics.mean([statistics.mean(velocity1), statistics.mean(velocity2), statistics.mean(velocity3),]))

                       # statistics.mean(power7), statistics.mean(power8),
print(statistics.mean([statistics.mean(power1),statistics.mean(power2),statistics.mean(power3)]))

x1 = []
x2 = []
x3 = []
x4 = []
x5 = []
x6 = []
x7 = []
x8 = []
zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(velocity1)):
    x1.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(velocity2)):
    x2.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(velocity3)):
    x3.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(velocity4)):
    x4.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(velocity5)):
    x5.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(velocity6)):
    x6.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

# zero = dt.datetime.strptime('00:00', '%H:%M')
# for i in range(len(velocity7)):
#     x7.append(zero.strftime("%H:%M"))
#     zero = zero + dt.timedelta(minutes=1)
#
# zero = dt.datetime.strptime('00:00', '%H:%M')
# for i in range(len(velocity8)):
#     x8.append(zero.strftime("%H:%M"))
#     zero = zero + dt.timedelta(minutes=1)

fig, ax1 = plt.subplots(2, 3, figsize=(10, 4))
print(len(x1))
ax1[0].plot(range(len(x1)), velocity1, color='b', linewidth=1.5,linestyle='-')
ax1[0].set_xticks([0,10,20,30,40])
ax1[0].set_xticklabels([x1[0],x1[10],x1[20],x1[30]])
ax2 = ax1[0].twinx()
ax2.plot(range(len(x1)), power1,color='gray', linewidth=1.5, linestyle='--')
# ax2.set_yticks([0,10000,20000,30000,40000])
ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [kW]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

ax1[1].plot(range(len(x2)), velocity2, color='b', linewidth=1.5,linestyle='-')
ax1[1].set_xticks([0,10,20,30,40])
ax1[1].set_xticklabels([x2[0],x2[10],x2[20],x2[30]])
ax2 = ax1[1].twinx()
ax2.plot(range(len(x2)), power2,color='gray', linewidth=1.5, linestyle='--')
# ax2.set_yticks([0,10000,20000,30000,40000])
ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [kW]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

ax1[2].plot(range(len(x3)), velocity3, color='b', linewidth=1.5,linestyle='-')
ax1[2].set_xticks([0,10,20,30])
ax1[2].set_xticklabels([x3[0],x3[10],x3[20],x3[30]])
ax2 = ax1[2].twinx()
ax2.plot(range(len(x3)), power3,color='gray', linewidth=1.5, linestyle='--')
# ax2.set_yticks([0,10000,20000,30000,40000])
ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [kW]', fontsize=14)
ax2.set_ylabel('Fan step [step]', fontsize=14)

# ax1[1,0].plot(range(len(x4)), velocity4, color='b', linewidth=1.5,linestyle='-')
# ax1[1,0].set_xticks([0,10,20,30,40])
# ax1[1,0].set_xticklabels([x4[0],x4[10],x4[20],x4[30]])
# ax2 = ax1[1,0].twinx()
# ax2.plot(range(len(x4)), power4,color='gray', linewidth=1.5, linestyle='--')
# # ax2.set_yticks([0,5000,10000,15000,20000,25000,30000,35000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# # ax2.set_ylabel('Power [kW]', fontsize=14)
# # ax2.set_ylabel('Fan step [step]', fontsize=14)
#
# ax1[1,1].plot(range(len(x5)), velocity5, color='b', linewidth=1.5,linestyle='-')
# ax1[1,1].set_xticks([0,10,20,30,40,])
# ax1[1,1].set_xticklabels([x5[0],x5[10],x5[20],x5[30]])
# ax2 = ax1[1,1].twinx()
# ax2.plot(range(len(x5)), power5,color='gray', linewidth=1.5, linestyle='--')
# # ax2.set_yticks([0,5000,10000,15000,20000,25000,30000,35000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
#
# ax1[1,2].plot(range(len(x6)), velocity6, color='b', linewidth=1.5,linestyle='-')
# ax1[1,2].set_xticks([0,10,20,30,40,])
# ax1[1,2].set_xticklabels([x6[0],x6[10],x6[18],x6[30]])
# ax2 = ax1[1,2].twinx()
# ax2.plot(range(len(x6)), power6,color='gray', linewidth=1.5, linestyle='--')
# # ax2.set_yticks([0,5000,10000,15000,20000,25000,30000,35000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# # ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

# ax1[1, 2].plot(range(len(x7)), velocity7, color='b', linewidth=1.5,linestyle='-')
# ax1[1, 2].set_xticks([0,10,20,30,40,])
# ax1[1, 2].set_xticklabels([x7[0],x7[10],x7[18],x7[30]])
# ax2 = ax1[1, 2].twinx()
# ax2.plot(range(len(x7)), power7,color='gray', linewidth=1.5, linestyle='--')
# # ax2.set_yticks([0,5000,10000,15000,20000,25000,30000,35000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# #
# ax1[1, 3].plot(range(len(x8)), velocity8, color='b', linewidth=1.5,linestyle='-')
# ax1[1, 3].set_xticks([0,10,20,30,40,])
# ax1[1, 3].set_xticklabels([x8[0],x8[10],x8[18],x8[30]])
# ax2 = ax1[1, 3].twinx()
# ax2.plot(range(len(x8)), power8,color='gray', linewidth=1.5, linestyle='--')
# # ax2.set_yticks([0,5000,10000,15000,20000,25000,30000,35000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# # ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)
#
# ax2 = ax1[2, 2].twinx()
# ax2.set_yticks([0,5000,10000,15000,20000,25000,30000,35000,40000])
# ax2.set_yticks([0,10,20,30,40,50])
# ax2.set_ylabel('Power [W]', fontsize=14)
# ax2.set_ylabel('Fan step [step]', fontsize=14)

for i in range(2):
    # for j in range(3):
    ax1[i].set_yticks([0,0.5,1.0,1.5,2.0,2.5,3.0])
    ax1[0].set_ylabel('Air Velocity [m/s]', fontsize=14)
    ax1[i].grid(linestyle="--", color='lightgray')
    # ax1[i,j].set_xticks([0, 100, 200, 300, 400, 500, 599])
    # ax1[i].set_xticklabels([x[6 * k:6 * (k + 1) + 1][n].strftime('%H:%M:%S') for n in range(len(x[6 * k:6 * (k + 1) + 1]))])

plt.tight_layout()
plt.show()
