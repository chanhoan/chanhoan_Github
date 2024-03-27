import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import collections
import itertools
import os
import statistics


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]
directory = r'C:\Users\com\Desktop\samsung\Analyze\Data\{}\analyze.csv'.format(folder_name)

data = pd.read_csv(directory)
print(data)

f1_28 = data['comp_current_frequency1_10']
f1_29 = data['comp_current_frequency1_11']
f1_30 = data['comp_current_frequency1_30']
f1_04 = data['comp_current_frequency1_04']
f1_05 = data['comp_current_frequency1_05']

f2_28 = data['comp_current_frequency2_10']
f2_29 = data['comp_current_frequency2_11']
f2_30 = data['comp_current_frequency2_30']
f2_04 = data['comp_current_frequency2_04']
f2_05 = data['comp_current_frequency2_05']

f_28 = []
f_29 = []
f_30 = []
f_04 = []
f_05 = []

for i in range(len(f1_28)):
    f_28.append((f1_28[i]+f2_28[i])/2)
for i in range(len(f1_29)):
    f_29.append((f1_29[i]+f2_29[i])/2)
for i in range(len(f1_30)):
    f_30.append((f1_30[i]+f2_30[i])/2)
for i in range(len(f1_04)):
    f_04.append((f1_04[i]+f2_04[i])/2)
for i in range(len(f1_05)):
    f_05.append((f1_05[i]+f2_05[i])/2)

fs_28 = data['fan_step_10']
fs_29 = data['fan_step_11']
fs_30 = data['fan_step_30']
fs_04 = data['fan_step_04']
fs_05 = data['fan_step_05']

power_28 = data['power_10']
power_29 = data['power_11']
power_30 = data['power_30']
power_04 = data['power_04']
power_05 = data['power_05']

power_28_pred = data['power_10_pred']
power_29_pred = data['power_11_pred']
power_30_pred = data['power_30_pred']
power_04_pred = data['power_04_pred']
power_05_pred = data['power_05_pred']

Qcond_28 = data['Qcond_10']
Qcond_29 = data['Qcond_11']
Qcond_30 = data['Qcond_30']
Qcond_04 = data['Qcond_04']
Qcond_05 = data['Qcond_05']

Qevap_28 = data['Qevap_10']
Qevap_29 = data['Qevap_11']
Qevap_30 = data['Qevap_30']
Qevap_04 = data['Qevap_04']
Qevap_05 = data['Qevap_05']

f_28_compo = []
f_29_compo = []
f_30_compo = []
f_04_compo = []
f_05_compo = []

fs_28_compo = []
fs_29_compo = []
fs_30_compo = []
fs_04_compo = []
fs_05_compo = []

for i in range(len(data)):
    if f_28[i] not in f_28_compo:
        f_28_compo.append(f_28[i])
    if f_29[i] not in f_29_compo:
        f_29_compo.append(f_29[i])
    if f_30[i] not in f_30_compo:
        f_30_compo.append(f_30[i])
    if f_04[i] not in f_04_compo:
        f_04_compo.append(f_04[i])
    if f_05[i] not in f_05_compo:
        f_05_compo.append(f_05[i])

    if fs_28[i] not in fs_28_compo:
        fs_28_compo.append(fs_28[i])
    if fs_29[i] not in fs_29_compo:
        fs_29_compo.append(fs_29[i])
    if fs_30[i] not in fs_30_compo:
        fs_30_compo.append(fs_30[i])
    if fs_04[i] not in fs_04_compo:
        fs_04_compo.append(fs_04[i])
    if fs_05[i] not in fs_05_compo:
        fs_05_compo.append(fs_05[i])

f_2829 = []
f_2830 = []
f_2804 = []
f_2805 = []

fs_2829 = []
fs_2830 = []
fs_2804 = []
fs_2805 = []

for i in range(len(f_28_compo)):
    if f_28_compo[i] in f_29_compo:
        f_2829.append(f_28_compo[i])
    if f_28_compo[i] in f_30_compo:
        f_2830.append(f_28_compo[i])
    if f_28_compo[i] in f_04_compo:
        f_2804.append(f_28_compo[i])
    if f_28_compo[i] in f_05_compo:
        f_2805.append(f_28_compo[i])

for i in range(len(fs_28_compo)):
    if fs_28_compo[i] in fs_29_compo:
        fs_2829.append(fs_28_compo[i])
    if fs_28_compo[i] in fs_30_compo:
        fs_2830.append(fs_28_compo[i])
    if fs_28_compo[i] in fs_04_compo:
        fs_2804.append(fs_28_compo[i])
    if fs_28_compo[i] in fs_05_compo:
        fs_2805.append(fs_28_compo[i])

f_2829_idx = {key:[] for key in f_2829}
f_2830_idx = {key:[] for key in f_2830}
f_2804_idx = {key:[] for key in f_2804}
f_2805_idx = {key:[] for key in f_2805}
f_2829_idx_pred = {key:[] for key in f_2829}
f_2830_idx_pred = {key:[] for key in f_2830}
f_2804_idx_pred = {key:[] for key in f_2804}
f_2805_idx_pred = {key:[] for key in f_2805}
f_2829_idx_cond = {key:[] for key in f_2829}
f_2830_idx_cond = {key:[] for key in f_2830}
f_2804_idx_cond = {key:[] for key in f_2804}
f_2805_idx_cond = {key:[] for key in f_2805}
f_2829_idx_evap = {key:[] for key in f_2829}
f_2830_idx_evap = {key:[] for key in f_2830}
f_2804_idx_evap = {key:[] for key in f_2804}
f_2805_idx_evap = {key:[] for key in f_2805}
f_29_idx = {key:[] for key in f_2829}
f_30_idx = {key:[] for key in f_2830}
f_04_idx = {key:[] for key in f_2804}
f_05_idx = {key:[] for key in f_2805}
f_29_idx_pred = {key:[] for key in f_2829}
f_30_idx_pred = {key:[] for key in f_2830}
f_04_idx_pred = {key:[] for key in f_2804}
f_05_idx_pred = {key:[] for key in f_2805}
f_29_idx_cond = {key:[] for key in f_2829}
f_30_idx_cond = {key:[] for key in f_2830}
f_04_idx_cond = {key:[] for key in f_2804}
f_05_idx_cond = {key:[] for key in f_2805}
f_29_idx_evap = {key:[] for key in f_2829}
f_30_idx_evap = {key:[] for key in f_2830}
f_04_idx_evap = {key:[] for key in f_2804}
f_05_idx_evap = {key:[] for key in f_2805}

fs_2829_idx_cond = {key:[] for key in fs_2829}
fs_2830_idx_cond = {key:[] for key in fs_2830}
fs_2804_idx_cond = {key:[] for key in fs_2804}
fs_2805_idx_cond = {key:[] for key in fs_2805}
fs_2829_idx_evap = {key:[] for key in fs_2829}
fs_2830_idx_evap = {key:[] for key in fs_2830}
fs_2804_idx_evap = {key:[] for key in fs_2804}
fs_2805_idx_evap = {key:[] for key in fs_2805}
fs_29_idx_cond = {key:[] for key in fs_2829}
fs_30_idx_cond = {key:[] for key in fs_2830}
fs_04_idx_cond = {key:[] for key in fs_2804}
fs_05_idx_cond = {key:[] for key in fs_2805}
fs_29_idx_evap = {key:[] for key in fs_2829}
fs_30_idx_evap = {key:[] for key in fs_2830}
fs_04_idx_evap = {key:[] for key in fs_2804}
fs_05_idx_evap = {key:[] for key in fs_2805}

for key in fs_2829:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2829_idx_cond[key].append(Qcond_28[i])
            fs_2829_idx_evap[key].append(Qevap_28[i])
for key in fs_2830:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2830_idx_cond[key].append(Qcond_28[i])
            fs_2830_idx_evap[key].append(Qevap_28[i])
for key in fs_2804:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2804_idx_cond[key].append(Qcond_28[i])
            fs_2804_idx_evap[key].append(Qevap_28[i])
for key in fs_2805:
    for i in range(len(fs_28)):
        if fs_28[i] == key:
            fs_2805_idx_cond[key].append(Qcond_28[i])
            fs_2805_idx_evap[key].append(Qevap_28[i])
for key in fs_2829:
    for i in range(len(fs_29)):
        if fs_29[i] == key:
            fs_29_idx_cond[key].append(Qcond_29[i])
            fs_29_idx_evap[key].append(Qevap_29[i])
for key in fs_2830:
    for i in range(len(fs_30)):
        if fs_30[i] == key:
            fs_30_idx_cond[key].append(Qcond_30[i])
            fs_30_idx_evap[key].append(Qevap_30[i])
for key in fs_2804:
    for i in range(len(fs_04)):
        if fs_04[i] == key:
            fs_04_idx_cond[key].append(Qcond_04[i])
            fs_04_idx_evap[key].append(Qevap_04[i])
for key in fs_2805:
    for i in range(len(fs_05)):
        if fs_05[i] == key:
            fs_05_idx_cond[key].append(Qcond_05[i])
            fs_05_idx_evap[key].append(Qevap_05[i])


for key in f_2829:
    for i in range(len(f1_28)):
        if f_28[i] == key:
            f_2829_idx[key].append(power_28[i])
            f_2829_idx_pred[key].append(power_28_pred[i])
            f_2829_idx_cond[key].append(Qcond_28[i])
            f_2829_idx_evap[key].append(Qevap_28[i])
for key in f_2830:
    for i in range(len(f1_28)):
        if f_28[i] == key:
            f_2830_idx[key].append(power_28[i])
            f_2830_idx_pred[key].append(power_28_pred[i])
            f_2830_idx_cond[key].append(Qcond_28[i])
            f_2830_idx_evap[key].append(Qevap_28[i])
for key in f_2804:
    for i in range(len(f1_28)):
        if f_28[i] == key:
            f_2804_idx[key].append(power_28[i])
            f_2804_idx_pred[key].append(power_28_pred[i])
            f_2804_idx_cond[key].append(Qcond_28[i])
            f_2804_idx_evap[key].append(Qevap_28[i])
for key in f_2805:
    for i in range(len(f1_28)):
        if f_28[i] == key:
            f_2805_idx[key].append(power_28[i])
            f_2805_idx_pred[key].append(power_28_pred[i])
            f_2805_idx_cond[key].append(Qcond_28[i])
            f_2805_idx_evap[key].append(Qevap_28[i])
for key in f_2829:
    for i in range(len(f1_29)):
        if f_29[i] == key:
            f_29_idx[key].append(power_29[i])
            f_29_idx_pred[key].append(power_29_pred[i])
            f_29_idx_cond[key].append(Qcond_29[i])
            f_29_idx_evap[key].append(Qevap_29[i])
for key in f_2830:
    for i in range(len(f1_30)):
        if f_30[i] == key:
            f_30_idx[key].append(power_30[i])
            f_30_idx_pred[key].append(power_30_pred[i])
            f_30_idx_cond[key].append(Qcond_30[i])
            f_30_idx_evap[key].append(Qevap_30[i])
for key in f_2804:
    for i in range(len(f1_04)):
        if f_04[i] == key:
            f_04_idx[key].append(power_04[i])
            f_04_idx_pred[key].append(power_04_pred[i])
            f_04_idx_cond[key].append(Qcond_04[i])
            f_04_idx_evap[key].append(Qevap_04[i])
for key in f_2805:
    for i in range(len(f1_05)):
        if f_05[i] == key:
            f_05_idx[key].append(power_05[i])
            f_05_idx_pred[key].append(power_05_pred[i])
            f_05_idx_cond[key].append(Qcond_05[i])
            f_05_idx_evap[key].append(Qevap_05[i])

f_2829_idx = sorted(f_2829_idx.items())
f_2830_idx = sorted(f_2830_idx.items())
f_2804_idx = sorted(f_2804_idx.items())
f_2805_idx = sorted(f_2805_idx.items())
f_2829_idx_pred = sorted(f_2829_idx_pred.items())
f_2830_idx_pred = sorted(f_2830_idx_pred.items())
f_2804_idx_pred = sorted(f_2804_idx_pred.items())
f_2805_idx_pred = sorted(f_2805_idx_pred.items())
f_2829_idx_cond = sorted(f_2829_idx_cond.items())
f_2830_idx_cond = sorted(f_2830_idx_cond.items())
f_2804_idx_cond = sorted(f_2804_idx_cond.items())
f_2805_idx_cond = sorted(f_2805_idx_cond.items())
f_2829_idx_evap = sorted(f_2829_idx_evap.items())
f_2830_idx_evap = sorted(f_2830_idx_evap.items())
f_2804_idx_evap = sorted(f_2804_idx_evap.items())
f_2805_idx_evap = sorted(f_2805_idx_evap.items())
f_29_idx = sorted(f_29_idx.items())
f_30_idx = sorted(f_30_idx.items())
f_04_idx = sorted(f_04_idx.items())
f_05_idx = sorted(f_05_idx.items())
f_29_idx_pred = sorted(f_29_idx_pred.items())
f_30_idx_pred = sorted(f_30_idx_pred.items())
f_04_idx_pred = sorted(f_04_idx_pred.items())
f_05_idx_pred = sorted(f_05_idx_pred.items())
f_29_idx_cond = sorted(f_29_idx_cond.items())
f_30_idx_cond = sorted(f_30_idx_cond.items())
f_04_idx_cond = sorted(f_04_idx_cond.items())
f_05_idx_cond = sorted(f_05_idx_cond.items())
f_29_idx_evap = sorted(f_29_idx_evap.items())
f_30_idx_evap = sorted(f_30_idx_evap.items())
f_04_idx_evap = sorted(f_04_idx_evap.items())
f_05_idx_evap = sorted(f_05_idx_evap.items())

fs_2829_idx_cond = sorted(fs_2829_idx_cond.items())
fs_2830_idx_cond = sorted(fs_2830_idx_cond.items())
fs_2804_idx_cond = sorted(fs_2804_idx_cond.items())
fs_2805_idx_cond = sorted(fs_2805_idx_cond.items())
fs_2829_idx_evap = sorted(fs_2829_idx_evap.items())
fs_2830_idx_evap = sorted(fs_2830_idx_evap.items())
fs_2804_idx_evap = sorted(fs_2804_idx_evap.items())
fs_2805_idx_evap = sorted(fs_2805_idx_evap.items())
fs_29_idx_cond = sorted(fs_29_idx_cond.items())
fs_30_idx_cond = sorted(fs_30_idx_cond.items())
fs_04_idx_cond = sorted(fs_04_idx_cond.items())
fs_05_idx_cond = sorted(fs_05_idx_cond.items())
fs_29_idx_evap = sorted(fs_29_idx_evap.items())
fs_30_idx_evap = sorted(fs_30_idx_evap.items())
fs_04_idx_evap = sorted(fs_04_idx_evap.items())
fs_05_idx_evap = sorted(fs_05_idx_evap.items())


def xyl(dict):
    k = 0
    x = []
    y = []
    l = []
    for key, value in dict:
        x.append(k)
        y.append(statistics.mean(value))
        l.append(key)
        k+=1
    return x,y,l


f_2829_x, f_2829_y, f_2829_l = xyl(f_2829_idx)
f_2830_x, f_2830_y, f_2830_l = xyl(f_2830_idx)
f_2804_x, f_2804_y, f_2804_l = xyl(f_2804_idx)
f_2805_x, f_2805_y, f_2805_l = xyl(f_2805_idx)
f_2829_x_pred, f_2829_y_pred, f_2829_l_pred = xyl(f_2829_idx_pred)
f_2830_x_pred, f_2830_y_pred, f_2830_l_pred = xyl(f_2830_idx_pred)
f_2804_x_pred, f_2804_y_pred, f_2804_l_pred = xyl(f_2804_idx_pred)
f_2805_x_pred, f_2805_y_pred, f_2805_l_pred = xyl(f_2805_idx_pred)
f_2829_x_cond, f_2829_y_cond, f_2829_l_cond = xyl(f_2829_idx_cond)
f_2830_x_cond, f_2830_y_cond, f_2830_l_cond = xyl(f_2830_idx_cond)
f_2804_x_cond, f_2804_y_cond, f_2804_l_cond = xyl(f_2804_idx_cond)
f_2805_x_cond, f_2805_y_cond, f_2805_l_cond = xyl(f_2805_idx_cond)
f_2829_x_evap, f_2829_y_evap, f_2829_l_evap = xyl(f_2829_idx_evap)
f_2830_x_evap, f_2830_y_evap, f_2830_l_evap = xyl(f_2830_idx_evap)
f_2804_x_evap, f_2804_y_evap, f_2804_l_evap = xyl(f_2804_idx_evap)
f_2805_x_evap, f_2805_y_evap, f_2805_l_evap = xyl(f_2805_idx_evap)
f_29_x, f_29_y, f_29_l = xyl(f_29_idx)
f_30_x, f_30_y, f_30_l = xyl(f_30_idx)
f_04_x, f_04_y, f_04_l = xyl(f_04_idx)
f_05_x, f_05_y, f_05_l = xyl(f_05_idx)
f_29_x_pred, f_29_y_pred, f_29_l_pred = xyl(f_29_idx_pred)
f_30_x_pred, f_30_y_pred, f_30_l_pred = xyl(f_30_idx_pred)
f_04_x_pred, f_04_y_pred, f_04_l_pred = xyl(f_04_idx_pred)
f_05_x_pred, f_05_y_pred, f_05_l_pred = xyl(f_05_idx_pred)
f_29_x_cond, f_29_y_cond, f_29_l_cond = xyl(f_29_idx_cond)
f_30_x_cond, f_30_y_cond, f_30_l_cond = xyl(f_30_idx_cond)
f_04_x_cond, f_04_y_cond, f_04_l_cond = xyl(f_04_idx_cond)
f_05_x_cond, f_05_y_cond, f_05_l_cond = xyl(f_05_idx_cond)
f_29_x_evap, f_29_y_evap, f_29_l_evap = xyl(f_29_idx_evap)
f_30_x_evap, f_30_y_evap, f_30_l_evap = xyl(f_30_idx_evap)
f_04_x_evap, f_04_y_evap, f_04_l_evap = xyl(f_04_idx_evap)
f_05_x_evap, f_05_y_evap, f_05_l_evap = xyl(f_05_idx_evap)

fs_2829_x_cond, fs_2829_y_cond, fs_2829_l_cond = xyl(fs_2829_idx_cond)
fs_2830_x_cond, fs_2830_y_cond, fs_2830_l_cond = xyl(fs_2830_idx_cond)
fs_2804_x_cond, fs_2804_y_cond, fs_2804_l_cond = xyl(fs_2804_idx_cond)
fs_2805_x_cond, fs_2805_y_cond, fs_2805_l_cond = xyl(fs_2805_idx_cond)
fs_2829_x_evap, fs_2829_y_evap, fs_2829_l_evap = xyl(fs_2829_idx_evap)
fs_2830_x_evap, fs_2830_y_evap, fs_2830_l_evap = xyl(fs_2830_idx_evap)
fs_2804_x_evap, fs_2804_y_evap, fs_2804_l_evap = xyl(fs_2804_idx_evap)
fs_2805_x_evap, fs_2805_y_evap, fs_2805_l_evap = xyl(fs_2805_idx_evap)
fs_29_x_cond, fs_29_y_cond, fs_29_l_cond = xyl(fs_29_idx_cond)
fs_30_x_cond, fs_30_y_cond, fs_30_l_cond = xyl(fs_30_idx_cond)
fs_04_x_cond, fs_04_y_cond, fs_04_l_cond = xyl(fs_04_idx_cond)
fs_05_x_cond, fs_05_y_cond, fs_05_l_cond = xyl(fs_05_idx_cond)
fs_29_x_evap, fs_29_y_evap, fs_29_l_evap = xyl(fs_29_idx_evap)
fs_30_x_evap, fs_30_y_evap, fs_30_l_evap = xyl(fs_30_idx_evap)
fs_04_x_evap, fs_04_y_evap, fs_04_l_evap = xyl(fs_04_idx_evap)
fs_05_x_evap, fs_05_y_evap, fs_05_l_evap = xyl(fs_05_idx_evap)


def plotting(x1,y1,x2,y2,l,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Power comparison at same compressor frequency',fontsize=16)
    ax1.step(x1,y1,c='b')
    ax1.step(x2,y2,c='r')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l)
    ax1.set_yticks([0,500,1000,1500,2000,2500,3000,3500,4000])
    ax1.set_xlabel('Compressor frequency [Hz]',fontsize=14)
    ax1.set_ylabel('Power [kW]',fontsize=14)
    ax1.legend(['{}'.format(cond1),'{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    fig_save_dir = r'C:\Users\com\Desktop\samsung\Analyze\Result\{}'.format(folder_name)
    create_folder(fig_save_dir)
    plt.savefig(fig_save_dir+'\Compressor frequency and Power_({}vs{})_mean.png'.format(date1,date2))


plotting(f_2829_x,f_2829_y,f_29_x,f_29_y,f_2829_l,'No fault','Fault','0728','0729')
# plotting(f_2830_x,f_2830_y,f_30_x,f_30_y,f_2830_l,'No fault','Fault','0728','0730')
# plotting(f_2804_x,f_2804_y,f_04_x,f_04_y,f_2804_l,'No fault','Fault','0728','0804')
# plotting(f_2805_x,f_2805_y,f_05_x,f_05_y,f_2805_l,'No fault','Fault','0728','0805')


def plotting2(x1,y1,x2,y2,l,x1_pred,y1_pred,x2_pred,y2_pred,l_pred,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(2,1,figsize=(12,10))
    ax1[0].set_title('Power comparison at same compressor frequency',fontsize=16)
    ax1[0].step(x1_pred,y1_pred,c='b')
    ax1[0].step(x2_pred,y2_pred,c='r')
    ax1[1].step(x1, y1, c='b')
    ax1[1].step(x2, y2, c='r')
    ax1[0].set_xticks(x1_pred)
    ax1[0].set_xticklabels(l_pred)
    ax1[1].set_xticks(x1)
    ax1[1].set_xticklabels(l)
    ax1[0].set_yticks([0,3000,6000,9000,12000,15000,18000,21000])
    ax1[1].set_yticks([0,3000,6000,9000,12000,15000,18000,21000])
    ax1[1].set_xlabel('Compressor frequency [Hz]', fontsize=14)
    ax1[0].set_ylabel('Power [kW]',fontsize=14)
    ax1[1].set_ylabel('Power [kW]', fontsize=14)
    ax1[0].legend(['{}'.format(cond1),'{}'.format(cond2)],loc='upper left',fontsize='large')
    ax1[1].legend(['{}'.format(cond1), '{}'.format(cond2)],loc='upper left', fontsize='large')
    plt.tight_layout()
    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    fig_save_dir = r'C:\Users\com\Desktop\samsung\Analyze\Result\{}'.format(folder_name)
    create_folder(fig_save_dir)
    plt.savefig(fig_save_dir+'\Compressor frequency and Power_({}vs{})_mean.png'.format(date1,date2))


plotting2(f_2829_x,f_2829_y,f_29_x,f_29_y,f_2829_l,f_2829_x_pred,f_2829_y_pred,f_29_x_pred,f_29_y_pred,f_2829_l_pred,'No fault','Fault','0728','0729')
# plotting2(f_2830_x,f_2830_y,f_30_x,f_30_y,f_2830_l,f_2830_x_pred,f_2830_y_pred,f_30_x_pred,f_30_y_pred,f_2830_l_pred,'No fault','Fault','0728','0730')
# plotting2(f_2804_x,f_2804_y,f_04_x,f_04_y,f_2804_l,f_2804_x_pred,f_2804_y_pred,f_04_x_pred,f_04_y_pred,f_2804_l_pred,'No fault','Fault','0728','0804')
# plotting2(f_2805_x,f_2805_y,f_05_x,f_05_y,f_2805_l,f_2805_x_pred,f_2805_y_pred,f_05_x_pred,f_05_y_pred,f_2805_l_pred,'No fault','Fault','0728','0805')


def plotting3(x1,y1,x2,y2,l,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Condenser capacity comparison at same compressor frequency',fontsize=16)
    ax1.step(x1,y1,c='b')
    ax1.step(x2,y2,c='r')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l)
    ax1.set_yticks([0,10,20,30,40,50])
    ax1.set_xlabel('Compressor frequency [Hz]',fontsize=14)
    ax1.set_ylabel('Condenser capacity [kW]',fontsize=14)
    ax1.legend(['{}'.format(cond1),'{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    fig_save_dir = r'C:\Users\com\Desktop\samsung\Analyze\Result\{}'.format(folder_name)
    create_folder(fig_save_dir)
    plt.savefig(fig_save_dir+'\Compressor frequency and Condenser capacity_({}vs{})_mean.png'.format(date1,date2))


plotting3(f_2829_x_cond,f_2829_y_cond,f_29_x_cond,f_29_y_cond,f_2829_l_cond,'No fault','Fault','0728','0729')
# plotting3(f_2830_x_cond,f_2830_y_cond,f_30_x_cond,f_30_y_cond,f_2830_l_cond,'No fault','Fault','0728','0730')
# plotting3(f_2804_x_cond,f_2804_y_cond,f_04_x_cond,f_04_y_cond,f_2804_l_cond,'No fault','Fault','0728','0804')
# plotting3(f_2805_x_cond,f_2805_y_cond,f_05_x_cond,f_05_y_cond,f_2805_l_cond,'No fault','Fault','0728','0805')


def plotting4(x1,y1,x2,y2,l,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Evaporator capacity comparison at same compressor frequency',fontsize=16)
    ax1.step(x1,y1,c='b')
    ax1.step(x2,y2,c='r')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l)
    ax1.set_yticks([0,1,2,3,4,5,6])
    ax1.set_xlabel('Compressor frequency [Hz]',fontsize=14)
    ax1.set_ylabel('Evaporator capacity [kW]',fontsize=14)
    ax1.legend(['{}'.format(cond1),'{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    fig_save_dir = r'C:\Users\com\Desktop\samsung\Analyze\Result\{}'.format(folder_name)
    create_folder(fig_save_dir)
    plt.savefig(fig_save_dir+'\Compressor frequency and Evaporator capacity_({}vs{})_mean.png'.format(date1,date2))


plotting4(f_2829_x_evap,f_2829_y_evap,f_29_x_evap,f_29_y_evap,f_2829_l_evap,'No fault','Fault','0728','0729')
# plotting4(f_2830_x_evap,f_2830_y_evap,f_30_x_evap,f_30_y_evap,f_2830_l_evap,'No fault','Fault','0728','0730')
# plotting4(f_2804_x_evap,f_2804_y_evap,f_04_x_evap,f_04_y_evap,f_2804_l_evap,'No fault','Fault','0728','0804')
# plotting4(f_2805_x_evap,f_2805_y_evap,f_05_x_evap,f_05_y_evap,f_2805_l_evap,'No fault','Fault','0728','0805')


def plotting5(x1,y1,x2,y2,l,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Condenser capacity comparison at same fan step',fontsize=16)
    ax1.step(x1,y1,c='b')
    ax1.step(x2,y2,c='r')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l)
    ax1.set_yticks([0,10,20,30,40,50])
    ax1.set_xlabel('Fan step',fontsize=14)
    ax1.set_ylabel('Condenser capacity [kW]',fontsize=14)
    ax1.legend(['{}'.format(cond1),'{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    fig_save_dir = r'C:\Users\com\Desktop\samsung\Analyze\Result\{}'.format(folder_name)
    create_folder(fig_save_dir)
    plt.savefig(fig_save_dir+'\Fan step and Condenser capacity_({}vs{})_mean.png'.format(date1,date2))


plotting5(fs_2829_x_cond,fs_2829_y_cond,fs_29_x_cond,fs_29_y_cond,fs_2829_l_cond,'No fault','Fault','0728','0729')
# plotting5(fs_2830_x_cond,fs_2830_y_cond,fs_30_x_cond,fs_30_y_cond,fs_2830_l_cond,'No fault','Fault','0728','0730')
# plotting5(fs_2804_x_cond,fs_2804_y_cond,fs_04_x_cond,fs_04_y_cond,fs_2804_l_cond,'No fault','Fault','0728','0804')
# plotting5(fs_2805_x_cond,fs_2805_y_cond,fs_05_x_cond,fs_05_y_cond,fs_2805_l_cond,'No fault','Fault','0728','0805')
#

def plotting6(x1,y1,x2,y2,l,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Evaporator capacity comparison at same fan step',fontsize=16)
    ax1.step(x1,y1,c='b')
    ax1.step(x2,y2,c='r')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l)
    ax1.set_yticks([0,1,2,3,4,5,6])
    ax1.set_xlabel('Fan step',fontsize=14)
    ax1.set_ylabel('Evaporator capacity [kW]',fontsize=14)
    ax1.legend(['{}'.format(cond1),'{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    fig_save_dir = r'C:\Users\com\Desktop\samsung\Analyze\Result\{}'.format(folder_name)
    create_folder(fig_save_dir)
    plt.savefig(fig_save_dir+'\Fan step and Evaporator capacity_({}vs{})_mean.png'.format(date1,date2))


plotting6(fs_2829_x_evap,fs_2829_y_evap,fs_29_x_evap,fs_29_y_evap,fs_2829_l_evap,'No fault','Fault','0728','0729')
# plotting6(fs_2830_x_evap,fs_2830_y_evap,fs_30_x_evap,fs_30_y_evap,fs_2830_l_evap,'No fault','Fault','0728','0730')
# plotting6(fs_2804_x_evap,fs_2804_y_evap,fs_04_x_evap,fs_04_y_evap,fs_2804_l_evap,'No fault','Fault','0728','0804')
# plotting6(fs_2805_x_evap,fs_2805_y_evap,fs_05_x_evap,fs_05_y_evap,fs_2805_l_evap,'No fault','Fault','0728','0805')