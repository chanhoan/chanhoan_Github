import pandas as pd
import matplotlib.pyplot as plt
import CoolProp as CP
import datetime as dt
import numpy as np
import collections
import itertools
import os

data = pd.read_csv('./analyze.csv')
new_data = pd.DataFrame()

print(data)

f1_28 = data['comp_current_frequency1_28']
f1_29 = data['comp_current_frequency1_29']
f1_30 = data['comp_current_frequency1_30']

f2_28 = data['comp_current_frequency2_28']
f2_29 = data['comp_current_frequency2_29']
f2_30 = data['comp_current_frequency2_30']

fs_28 = data['fan_step_28']
fs_29 = data['fan_step_29']
fs_30 = data['fan_step_30']

power_28 = data['power_28']
power_29 = data['power_29']
power_30 = data['power_30']

f1_28_compo = []
f1_29_compo = []
f1_30_compo = []

f2_28_compo = []
f2_29_compo = []
f2_30_compo = []

fs_28_compo = []
fs_29_compo = []
fs_30_compo = []

for i in range(len(data)):
    if f1_28[i] not in f1_28_compo and f1_28[i] != 0:
        f1_28_compo.append(f1_28[i])
    if f1_29[i] not in f1_29_compo and f1_29[i] != 0:
        f1_29_compo.append(f1_29[i])
    if f1_30[i] not in f1_30_compo and f1_30[i] != 0:
        f1_30_compo.append(f1_30[i])

    if f2_28[i] not in f2_28_compo and f2_28[i] != 0:
        f2_28_compo.append(f2_28[i])
    if f2_29[i] not in f2_29_compo and f2_29[i] != 0:
        f2_29_compo.append(f2_29[i])
    if f2_30[i] not in f2_30_compo and f2_30[i] != 0:
        f2_30_compo.append(f2_30[i])

    if fs_28[i] not in fs_28_compo and fs_28[i] != 0:
        fs_28_compo.append(fs_28[i])
    if fs_29[i] not in fs_29_compo and fs_29[i] != 0:
        fs_29_compo.append(fs_29[i])
    if fs_30[i] not in fs_30_compo and fs_30[i] != 0:
        fs_30_compo.append(fs_30[i])

print(f1_28_compo)
print(f1_29_compo)
print(f1_30_compo)
print(f2_28_compo)
print(f2_29_compo)
print(f2_30_compo)
print(fs_28_compo)
print(fs_29_compo)
print(fs_30_compo)

f1_2829 = []
f1_2830 = []

f2_2829 = []
f2_2830 = []

fs_2829 = []
fs_2830 = []

for i in range(len(f1_28_compo)):
    if f1_28_compo[i] in f1_29_compo:
        f1_2829.append(f1_28_compo[i])
    if f1_28_compo[i] in f1_30_compo:
        f1_2830.append(f1_28_compo[i])

for i in range(len(f2_28_compo)):
    if f2_28_compo[i] in f2_29_compo:
        f2_2829.append(f2_28_compo[i])
    if f2_28_compo[i] in f2_30_compo:
        f2_2830.append(f2_28_compo[i])

for i in range(len(fs_28_compo)):
    if fs_28_compo[i] in fs_29_compo:
        fs_2829.append(fs_28_compo[i])
    if fs_28_compo[i] in fs_30_compo:
        fs_2830.append(fs_28_compo[i])

print('\n')
print(f1_2829)
print(f1_2830)
print(f2_2829)
print(f2_2830)
print(fs_2829)
print(fs_2830)

f1_2829_idx = {key:[] for key in f1_2829}
f1_2830_idx = {key:[] for key in f1_2830}
f1_29_idx = {key:[] for key in f1_2829}
f1_30_idx = {key:[] for key in f1_2830}

f2_2829_idx = {key:[] for key in f2_2829}
f2_2830_idx = {key:[] for key in f2_2830}
f2_29_idx = {key:[] for key in f2_2829}
f2_30_idx = {key:[] for key in f2_2830}

fs_2829_idx = {key:[] for key in fs_2829}
fs_2830_idx = {key:[] for key in fs_2830}
fs_29_idx = {key:[] for key in fs_2829}
fs_30_idx = {key:[] for key in fs_2830}

for key in f1_2829:
    for i in range(len(f1_28)):
        if f1_28[i] == key:
            f1_2829_idx[key].append(i)
for key in f1_2830:
    for i in range(len(f1_28)):
        if f1_28[i] == key:
            f1_2830_idx[key].append(i)
for key in f1_2829:
    for i in range(len(f1_29)):
        if f1_29[i] == key:
            f1_29_idx[key].append(i)
for key in f1_2830:
    for i in range(len(f1_30)):
        if f1_30[i] == key:
            f1_30_idx[key].append(i)
for key in f2_2829:
    for i in range(len(f2_28)):
        if f2_28[i] == key:
            f2_2829_idx[key].append(i)
for key in f2_2830:
    for i in range(len(f2_28)):
        if f2_28[i] == key:
            f2_2830_idx[key].append(i)
for key in f2_2829:
    for i in range(len(f2_29)):
        if f2_29[i] == key:
            f2_29_idx[key].append(i)
for key in f2_2830:
    for i in range(len(f2_30)):
        if f2_30[i] == key:
            f2_30_idx[key].append(i)
for key in fs_2829:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2829_idx[key].append(i)
for key in fs_2830:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2830_idx[key].append(i)
for key in fs_2829:
    for i in range(len(fs_29)):
        if fs_29[i] == key:
            fs_29_idx[key].append(i)
for key in fs_2830:
    for i in range(len(fs_30)):
        if fs_30[i] == key:
            fs_30_idx[key].append(i)

print('\n')
print(f1_2829_idx)
print(f1_2830_idx)
print(f1_29_idx)
print(f1_30_idx)
print(f2_2829_idx)
print(f2_2830_idx)
print(f2_29_idx)
print(f2_30_idx)
print(fs_2829_idx)
print(fs_2830_idx)
print(fs_29_idx)
print(fs_30_idx)

x = []
zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
for i in range(1000):
    x.append(zero)
    zero = zero + dt.timedelta(minutes=1)


def comp_power(dict1,dict2,date1,date2,data1_,data2_,fre):
    print(data1_)
    for key, value in dict1.items():
        print(data1_)
        data1 = data1_
        data2 = data2_
        # print(data1)
        # print(data2)
        data1_value = []
        data2_value = []
        freq_value = []
        for j in range(len(value)):
            data1_value.append(data1[value[j]])
            data2_value.append(data2[value[j]])
            freq_value.append(fre[value[j]])
        # print(data1_value)
        # print(data2_value)
        for i in range(len(data1)):
            if data1[i] not in data1_value:
                data1.loc[i] = np.nan
            if data2[i] not in data2_value:
                data2.loc[i] = np.nan
            if fre[i] not in freq_value:
                fre.loc[i] = np.nan
        fig, ax1 = plt.subplots(figsize=(12, 10))
        ax1.set_title('Power Comparison at Compressor frequency: {} ({} and {})'.format(key, date1, date2))
        ax1.plot(data['Time'],data1,color='b', linewidth=1.5,linestyle='-')
        ax1.plot(range(len(data2)), data2, color='g', linewidth=1.5, linestyle='-')
        ax2 = ax1.twinx()
        ax2.plot(range(len(fre)),fre, color='C', linewidth=1.5, linestyle='--')
        ax1.legend(['Power {}'.format(date1),'Power {}'.format(date2)],loc='upper left')
        ax2.legend(['Compressor frequency: {}'.format(key)],loc='upper right')
        ax1.set_ylabel('Power [kW]', fontsize=14)
        ax2.set_ylabel('Compressor frequency', fontsize=14)
        ax1.set_xlabel('Time', fontsize=14)
        ax1.set_xticks([data['Time'][k] for k in range(len(data)) if k % 100 == 0])
        ax2.set_yticks([0,10,20,30,40,50,60])
        plt.savefig('./Power_Comp_{}_({}vs{}).png'.format(key,date1,date2))

# comp_power(f1_2829_idx,f1_29_idx,'0728','0729',power_28,power_29)
comp_power(f1_2830_idx,f1_30_idx,'0728','0730',power_28,power_30,f1_28)