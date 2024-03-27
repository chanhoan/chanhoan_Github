import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import collections
import itertools
import os

data_28 = pd.read_csv('./analyze.csv')
data_29 = pd.read_csv('./analyze.csv')
data_30 = pd.read_csv('./analyze.csv')
time_28 = pd.read_csv('./analyze2.csv')['28Time'].dropna()
time_29 = pd.read_csv('./analyze2.csv')['29Time'].dropna()
time_30 = pd.read_csv('./analyze2.csv')['30Time'].dropna()
v_28 = pd.read_csv('./analyze2.csv')['velocity_28'].dropna()
v_29 = pd.read_csv('./analyze2.csv')['velocity_29'].dropna()
v_30 = pd.read_csv('./analyze2.csv')['velocity_30'].dropna()

time28_dt = []
time29_dt = []
time30_dt = []

for i in range(len(time_28)):
    time28_dt.append(dt.datetime.strptime(time_28[i],'%Y-%m-%d %H:%M:%S'))
for i in range(len(time_29)):
    time29_dt.append(dt.datetime.strptime(time_29[i],'%Y-%m-%d %H:%M:%S'))
for i in range(len(time_30)):
    time30_dt.append(dt.datetime.strptime(time_30[i],'%Y-%m-%d %H:%M:%S'))

df28 = pd.concat([pd.DataFrame(time28_dt,columns=['28Time']),v_28],axis=1).set_index('28Time').dropna()
df29 = pd.concat([pd.DataFrame(time29_dt,columns=['29Time']),v_29],axis=1).set_index('29Time').dropna()
df30 = pd.concat([pd.DataFrame(time30_dt,columns=['30Time']),v_30],axis=1).set_index('30Time').dropna()


time28_compo = []
time29_compo = []
time30_compo = []
for i in range(len(time_28)):
    if time_28[i][11:16] not in time28_compo:
        time28_compo.append(time_28[i][11:16])
for i in range(len(time_29)):
    if time_29[i][11:16] not in time29_compo:
        time29_compo.append(time_29[i][11:16])
for i in range(len(time_30)):
    if time_30[i][11:16] not in time30_compo:
        time30_compo.append(time_30[i][11:16])

print(time28_compo)
print(time29_compo)
print(time30_compo)

drop_idx_28 = []
drop_idx_29 = []
drop_idx_30 = []

for i in range(len(data_28)):
    if data_28['Time'][i][0:5] not in time28_compo:
        drop_idx_28.append(i)
for i in range(len(data_29)):
    if data_29['Time'][i][0:5] not in time29_compo:
        drop_idx_29.append(i)
for i in range(len(data_30)):
    if data_30['Time'][i][0:5] not in time30_compo:
        drop_idx_30.append(i)

data_28 = data_28.drop(drop_idx_28,axis=0).reset_index()
data_29 = data_29.drop(drop_idx_29,axis=0).reset_index()
data_30 = data_30.drop(drop_idx_30,axis=0).reset_index()
print(data_28)
fs_28 = data_28['fan_step_28'].dropna()
fs_29 = data_29['fan_step_29'].dropna()
fs_30 = data_30['fan_step_30'].dropna()

fs_28_compo = []
fs_29_compo = []
fs_30_compo = []

for i in range(len(fs_28)):
    if fs_28[i] not in fs_28_compo and fs_28[i] != 0:
        fs_28_compo.append(fs_28[i])
for i in range(len(fs_29)):
    if fs_29[i] not in fs_29_compo and fs_29[i] != 0:
        fs_29_compo.append(fs_29[i])
for i in range(len(fs_30)):
    if fs_30[i] not in fs_30_compo and fs_30[i] != 0:
        fs_30_compo.append(fs_30[i])

print(fs_28_compo)
print(fs_29_compo)
print(fs_30_compo)

fs_2829 = []
fs_2830 = []

for i in range(len(fs_28_compo)):
    if fs_28_compo[i] in fs_29_compo:
        fs_2829.append(fs_28_compo[i])
    if fs_28_compo[i] in fs_30_compo:
        fs_2830.append(fs_28_compo[i])

print(fs_2829)
print(fs_2830)

fs_2829_idx = {key:[] for key in fs_2829}
fs_2830_idx = {key:[] for key in fs_2830}
fs_29_idx = {key:[] for key in fs_2829}
fs_30_idx = {key:[] for key in fs_2830}

df28_mean = pd.DataFrame()
df29_mean = pd.DataFrame()
df30_mean = pd.DataFrame()

df28_mean['velocity_28'] = df28['velocity_28'].resample('1T').mean().dropna()
df29_mean['velocity_29'] = df29['velocity_29'].resample('1T').mean().dropna()
df30_mean['velocity_30'] = df30['velocity_30'].resample('1T').mean().dropna()

for key in fs_2829:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2829_idx[key].append(df28_mean['velocity_28'][i])
for key in fs_2830:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2830_idx[key].append(df28_mean['velocity_28'][i])
for key in fs_2829:
    for i in range(len(fs_29)):
        if fs_29[i] == key:
            fs_29_idx[key].append(df29_mean['velocity_29'][i])
for key in fs_2830:
    for i in range(len(fs_30)):
        if fs_30[i] == key:
            fs_30_idx[key].append(df30_mean['velocity_30'][i])

fs_2829_idx = sorted(fs_2829_idx.items())
fs_2830_idx = sorted(fs_2830_idx.items())
fs_29_idx = sorted(fs_29_idx.items())
fs_30_idx = sorted(fs_30_idx.items())


def xyl(dict):
    k = 0
    x = []
    y = []
    l = []
    for key, value in dict:
        for i in range(len(value)):
            x.append(k)
            y.append(value[i])
            l.append(key)
        k+=1
    return x,y,l


fs_2829_x, fs_2829_y, fs_2829_l = xyl(fs_2829_idx)
fs_2830_x, fs_2830_y, fs_2830_l = xyl(fs_2830_idx)
fs_29_x, fs_29_y, fs_29_l = xyl(fs_29_idx)
fs_30_x, fs_30_y, fs_30_l = xyl(fs_30_idx)


def plotting(x1,y1,x2,y2,l,comp_num,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Air velocity and Fan step ({} / {})'.format(cond1,cond2),fontsize=16)
    ax1.scatter(x1,y1,c='b')
    ax1.scatter(x2,y2,c='r')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l)
    ax1.set_xlabel('Fan step'.format(comp_num),fontsize=14)
    ax1.set_ylabel('Air velocity [m/s]',fontsize=14)
    ax1.legend(['{}'.format(cond1),'{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    plt.savefig('./그림/Air velocity and Fan step_({}vs{})_scatter.png'.format(date1,date2))


plotting(fs_2829_x,fs_2829_y,fs_29_x,fs_29_y,fs_2829_l,1,'No fault','Mesh layer','0728','0729')
plotting(fs_2830_x,fs_2830_y,fs_30_x,fs_30_y,fs_2830_l,1,'No fault','kitchen towel','0728','0730')