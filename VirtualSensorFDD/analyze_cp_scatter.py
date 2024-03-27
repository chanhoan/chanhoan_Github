import pandas as pd
import matplotlib.pyplot as plt
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
            f1_2829_idx[key].append(power_28[i])
for key in f1_2830:
    for i in range(len(f1_28)):
        if f1_28[i] == key:
            f1_2830_idx[key].append(power_28[i])
for key in f1_2829:
    for i in range(len(f1_29)):
        if f1_29[i] == key:
            f1_29_idx[key].append(power_29[i])
for key in f1_2830:
    for i in range(len(f1_30)):
        if f1_30[i] == key:
            f1_30_idx[key].append(power_30[i])
for key in f2_2829:
    for i in range(len(f2_28)):
        if f2_28[i] == key:
            f2_2829_idx[key].append(power_28[i])
for key in f2_2830:
    for i in range(len(f2_28)):
        if f2_28[i] == key:
            f2_2830_idx[key].append(power_28[i])
for key in f2_2829:
    for i in range(len(f2_29)):
        if f2_29[i] == key:
            f2_29_idx[key].append(power_29[i])
for key in f2_2830:
    for i in range(len(f2_30)):
        if f2_30[i] == key:
            f2_30_idx[key].append(power_30[i])
# for key in fs_2829:
#     for i in range(len(fs_28)):
#         if fs_28[i] == key:
#             fs_2829_idx[key].append(power_28(i))
# for key in fs_2830:
#     for i in range(len(fs_28)):
#         if fs_28[i] == key:
#             fs_2830_idx[key].append(i)
# for key in fs_2829:
#     for i in range(len(fs_29)):
#         if fs_29[i] == key:
#             fs_29_idx[key].append(i)
# for key in fs_2830:
#     for i in range(len(fs_30)):
#         if fs_30[i] == key:
#             fs_30_idx[key].append(i)

f1_2829_idx = sorted(f1_2829_idx.items())
f1_2830_idx = sorted(f1_2830_idx.items())
f1_29_idx = sorted(f1_29_idx.items())
f1_30_idx = sorted(f1_30_idx.items())

f2_2829_idx = sorted(f2_2829_idx.items())
f2_2830_idx = sorted(f2_2830_idx.items())
f2_29_idx = sorted(f2_29_idx.items())
f2_30_idx = sorted(f2_30_idx.items())


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


f1_2829_x, f1_2829_y, f1_2829_l = xyl(f1_2829_idx)
f1_2830_x, f1_2830_y, f1_2830_l = xyl(f1_2830_idx)
f1_29_x, f1_29_y, f1_29_l = xyl(f1_29_idx)
f1_30_x, f1_30_y, f1_30_l = xyl(f1_30_idx)

f2_2829_x, f2_2829_y, f2_2829_l = xyl(f2_2829_idx)
f2_2830_x, f2_2830_y, f2_2830_l = xyl(f2_2830_idx)
f2_29_x, f2_29_y, f2_29_l = xyl(f2_29_idx)
f2_30_x, f2_30_y, f2_30_l = xyl(f2_30_idx)


def plotting(x1,y1,x2,y2,l,comp_num,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Power comparison at same compressor {} frequency ({} / {})'.format(comp_num,cond1,cond2),fontsize=16)
    ax1.scatter(x1,y1,c='b')
    ax1.scatter(x2,y2,c='r')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l)
    ax1.set_xlabel('Compressor {} frequency [Hz]'.format(comp_num),fontsize=14)
    ax1.set_ylabel('Power [kW]',fontsize=14)
    ax1.legend(['{}'.format(cond1),'{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    plt.savefig('./그림/Compressor {} and Power_({}vs{})_scatter.png'.format(comp_num,date1,date2))


plotting(f1_2829_x,f1_2829_y,f1_29_x,f1_29_y,f1_2829_l,1,'No fault','Mesh layer','0728','0729')
plotting(f1_2830_x,f1_2830_y,f1_30_x,f1_30_y,f1_2830_l,1,'No fault','kitchen towel','0728','0730')
plotting(f2_2829_x,f2_2829_y,f2_29_x,f2_29_y,f2_2829_l,2,'No fault','Mesh layer','0728','0729')
plotting(f2_2830_x,f2_2830_y,f2_30_x,f2_30_y,f2_2830_l,2,'No fault','kitchen towel','0728','0730')