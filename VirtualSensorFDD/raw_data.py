import matplotlib.pyplot as plt
import CoolProp as CP
import datetime as dt
import numpy as np
import pandas as pd
import collections
import itertools
import os
import statistics

interval = 60

x = []
zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
for i in range(1500):
    x.append(zero)
    zero = zero + dt.timedelta(seconds=2)

def data(unit,month,date):
    data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\{}{} flow.csv'.format(month,date,month,date), engine='python')
    data_point = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\point_time_upper.csv'.format(month,date))
    power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\outdoor_{}_{}.csv'.format(month,date,date,unit))
    normal = data_point['nolayer']
    low = data_point['lowlevel']
    high = data_point['highlevel']
    normal_finish = data_point['nolayer_finish']
    low_finish = data_point['lowlevel_finish']
    high_finish = data_point['highlevel_finish']

    y = data['Standard Velocity (Matrix)'].rolling(60).mean().fillna(method='bfill')
    y2 = power['fan_step']

    normal_index = []
    low_index = []
    high_index = []
    normal_finish_index = []
    low_finish_index = []
    high_finish_index = []

    power_index = []
    power_finish = []
    power_index_low = []
    power_finish_low = []
    power_index_high = []
    power_finish_high = []

    for i in range(len(data)):
        for j in range(len(data_point)):
            if data['Time'][i] == normal[j]:
                normal_index.append(i)
            elif data['Time'][i] == low[j]:
                low_index.append(i)
            elif data['Time'][i] == high[j]:
                high_index.append(i)
            elif data['Time'][i] == normal_finish[j]:
                normal_finish_index.append(i)
            elif data['Time'][i] == low_finish[j]:
                low_finish_index.append(i)
            elif data['Time'][i] == high_finish[j]:
                high_finish_index.append(i)

    for i in range(len(power)):
        for j in range(len(data_point)):
            if power['Time'][i] == normal_finish[j][0:5] + ':00':
                power_finish.append(i)
            elif power['Time'][i] == normal[j][0:5] + ':00':
                power_index.append(i)
            elif power['Time'][i] == low_finish[j][0:5] + ':00':
                power_finish_low.append(i)
            elif power['Time'][i] == low[j][0:5] + ':00':
                power_index_low.append(i)
            elif power['Time'][i] == high[j][0:5] + ':00':
                power_index_high.append(i)
            elif power['Time'][i] == high_finish[j][0:5] + ':00':
                power_finish_high.append(i)

    print(normal_index)
    print(normal_finish_index)
    print(low_index)
    print(low_finish_index)
    print(high_index)
    print(high_finish_index)
    print(power_index)
    print(power_finish)
    print(power_index_low)
    print(power_finish_low)
    print(power_index_high)
    print(power_finish_high)

    return y,y2,normal_index, normal_finish_index, power_index, power_finish


def temp_data(unit,month,date):
    data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\{}{} temp.csv'.format(month,date,month,date), engine='python').fillna(method='bfill')
    data_point = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\point_time_temp.csv'.format(month,date))
    power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\outdoor_{}_{}.csv'.format(month,date,date,unit))
    normal = data_point['nolayer']
    low = data_point['lowlevel']
    high = data_point['highlevel']
    normal_finish = data_point['nolayer_finish']
    low_finish = data_point['lowlevel_finish']
    high_finish = data_point['highlevel_finish']
    print(data_point)

    window_size = 300

    y1 = data['point 1'].rolling(window_size).mean().fillna(method='bfill')
    y2 = data['point 2'].rolling(window_size).mean().fillna(method='bfill')
    y3 = data['point 3'].rolling(window_size).mean().fillna(method='bfill')
    y4 = data['point 4'].rolling(window_size).mean().fillna(method='bfill')
    y5 = data['point 5'].rolling(window_size).mean().fillna(method='bfill')
    y6 = data['point 6'].rolling(window_size).mean().fillna(method='bfill')
    y7 = data['point 7'].rolling(window_size).mean().fillna(method='bfill')
    y8 = data['point 8'].rolling(window_size).mean().fillna(method='bfill')
    y9 = data['point 9'].rolling(window_size).mean().fillna(method='bfill')
    y10 = data['point 10'].rolling(window_size).mean().fillna(method='bfill')
    y11 = data['point 11'].rolling(window_size).mean().fillna(method='bfill')
    y12 = data['point 12'].rolling(window_size).mean().fillna(method='bfill')
    y13 = data['point 13'].rolling(window_size).mean().fillna(method='bfill')
    y14 = data['point 14'].rolling(window_size).mean().fillna(method='bfill')
    y15 = data['point 15'].rolling(window_size).mean().fillna(method='bfill')
    y16 = data['point 16'].rolling(window_size).mean().fillna(method='bfill')
    y17 = data['point 17'].rolling(window_size).mean().fillna(method='bfill')
    y18 = data['point 18'].rolling(window_size).mean().fillna(method='bfill')
    y19 = data['point 19'].rolling(window_size).mean().fillna(method='bfill')
    y20 = data['point 20'].rolling(window_size).mean().fillna(method='bfill')
    y21 = data['point 21'].rolling(window_size).mean().fillna(method='bfill')
    y22 = data['point 22'].rolling(window_size).mean().fillna(method='bfill')
    y23 = data['point 23'].rolling(window_size).mean().fillna(method='bfill')
    y24 = data['point 24'].rolling(window_size).mean().fillna(method='bfill')
    y25 = data['point 25'].rolling(window_size).mean().fillna(method='bfill')

    y1 = (y1 + y2 + y3 + y4 + y5) / 5
    y2 = (y6 + y7 + y8 + y9 + y10) / 5
    y3 = (y11 + y12 + y13 + y14 + y15) / 5
    y4 = (y16 + y17 + y18 + y19 + y20) / 5
    y5 = (y21 + y22 + y23 + y24 + y25) / 5

    normal_index = []
    low_index = []
    high_index = []
    normal_finish_index = []
    low_finish_index = []
    high_finish_index = []

    power_index = []
    power_finish = []
    power_index_low = []
    power_finish_low = []
    power_index_high = []
    power_finish_high = []

    for i in range(len(data)):
        for j in range(len(data_point)):
            if data['Time'][i] == normal[j]:
                normal_index.append(i)
            elif data['Time'][i] == low[j]:
                low_index.append(i)
            elif data['Time'][i] == high[j]:
                high_index.append(i)
            elif data['Time'][i] == normal_finish[j]:
                normal_finish_index.append(i)
            elif data['Time'][i] == low_finish[j]:
                low_finish_index.append(i)
            elif data['Time'][i] == high_finish[j]:
                high_finish_index.append(i)

    for i in range(len(power)):
        for j in range(len(data_point)):
            if power['Time'][i] == normal_finish[j][0:5] + ':00':
                power_finish.append(i)
            elif power['Time'][i] == normal[j][0:5] + ':00':
                power_index.append(i)
            elif power['Time'][i] == low_finish[j][0:5] + ':00':
                power_finish_low.append(i)
            elif power['Time'][i] == low[j][0:5] + ':00':
                power_index_low.append(i)
            elif power['Time'][i] == high[j][0:5] + ':00':
                power_index_high.append(i)
            elif power['Time'][i] == high_finish[j][0:5] + ':00':
                power_finish_high.append(i)

    print(normal_index)
    print(normal_finish_index)
    print(low_index)
    print(low_finish_index)
    print(high_index)
    print(high_finish_index)
    print(power_index)
    print(power_finish)
    print(power_index_low)
    print(power_finish_low)
    print(power_index_high)
    print(power_finish_high)

    return y1,y2,y3,y4,y5,normal_index,normal_finish_index


def upper_temp_data(unit,month,date):
    data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\{}{} temp.csv'.format(month,date,month,date), engine='python').fillna(method='bfill')
    data_point = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\point_time_temp.csv'.format(month,date))
    power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\outdoor_{}_{}.csv'.format(month,date,date,unit))
    normal = data_point['nolayer']
    low = data_point['lowlevel']
    high = data_point['highlevel']
    normal_finish = data_point['nolayer_finish']
    low_finish = data_point['lowlevel_finish']
    high_finish = data_point['highlevel_finish']
    print(data_point)

    window_size = 300

    y1 = data['point 52'].rolling(window_size).mean().fillna(method='bfill')-2
    y2 = data['point 54'].rolling(window_size).mean().fillna(method='bfill')-2
    y3 = data['point 56'].rolling(window_size).mean().fillna(method='bfill')-2
    y4 = data['point 58'].rolling(window_size).mean().fillna(method='bfill')-4
    y5 = data['point 60'].rolling(window_size).mean().fillna(method='bfill')-4

    normal_index = []
    low_index = []
    high_index = []
    normal_finish_index = []
    low_finish_index = []
    high_finish_index = []

    power_index = []
    power_finish = []
    power_index_low = []
    power_finish_low = []
    power_index_high = []
    power_finish_high = []

    for i in range(len(data)):
        for j in range(len(data_point)):
            if data['Time'][i] == normal[j]:
                normal_index.append(i)
            elif data['Time'][i] == low[j]:
                low_index.append(i)
            elif data['Time'][i] == high[j]:
                high_index.append(i)
            elif data['Time'][i] == normal_finish[j]:
                normal_finish_index.append(i)
            elif data['Time'][i] == low_finish[j]:
                low_finish_index.append(i)
            elif data['Time'][i] == high_finish[j]:
                high_finish_index.append(i)

    for i in range(len(power)):
        for j in range(len(data_point)):
            if power['Time'][i] == normal_finish[j][0:5] + ':00':
                power_finish.append(i)
            elif power['Time'][i] == normal[j][0:5] + ':00':
                power_index.append(i)
            elif power['Time'][i] == low_finish[j][0:5] + ':00':
                power_finish_low.append(i)
            elif power['Time'][i] == low[j][0:5] + ':00':
                power_index_low.append(i)
            elif power['Time'][i] == high[j][0:5] + ':00':
                power_index_high.append(i)
            elif power['Time'][i] == high_finish[j][0:5] + ':00':
                power_finish_high.append(i)

    print(normal_index)
    print(normal_finish_index)
    print(low_index)
    print(low_finish_index)
    print(high_index)
    print(high_finish_index)
    print(power_index)
    print(power_finish)
    print(power_index_low)
    print(power_finish_low)
    print(power_index_high)
    print(power_finish_high)

    return y1,y2,y3,y4,y5,normal_index,normal_finish_index


def upper_temp_data2(unit,month,date):
    data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\{}{} temp.csv'.format(month,date,month,date), engine='python').fillna(method='bfill')
    data_point = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\point_time_temp.csv'.format(month,date))
    power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-{}-{}\outdoor_{}_{}.csv'.format(month,date,date,unit))
    normal = data_point['nolayer']
    low = data_point['lowlevel']
    high = data_point['highlevel']
    normal_finish = data_point['nolayer_finish']
    low_finish = data_point['lowlevel_finish']
    high_finish = data_point['highlevel_finish']
    print(data_point)

    window_size = 300

    y1 = data['point 26'].rolling(window_size).mean().fillna(method='bfill')
    y2 = data['point 27'].rolling(window_size).mean().fillna(method='bfill')
    y3 = data['point 28'].rolling(window_size).mean().fillna(method='bfill')
    y4 = data['point 29'].rolling(window_size).mean().fillna(method='bfill')
    y5 = data['point 30'].rolling(window_size).mean().fillna(method='bfill')

    normal_index = []
    low_index = []
    high_index = []
    normal_finish_index = []
    low_finish_index = []
    high_finish_index = []

    power_index = []
    power_finish = []
    power_index_low = []
    power_finish_low = []
    power_index_high = []
    power_finish_high = []

    for i in range(len(data)):
        for j in range(len(data_point)):
            if data['Time'][i] == normal[j]:
                normal_index.append(i)
            elif data['Time'][i] == low[j]:
                low_index.append(i)
            elif data['Time'][i] == high[j]:
                high_index.append(i)
            elif data['Time'][i] == normal_finish[j]:
                normal_finish_index.append(i)
            elif data['Time'][i] == low_finish[j]:
                low_finish_index.append(i)
            elif data['Time'][i] == high_finish[j]:
                high_finish_index.append(i)

    for i in range(len(power)):
        for j in range(len(data_point)):
            if power['Time'][i] == normal_finish[j][0:5] + ':00':
                power_finish.append(i)
            elif power['Time'][i] == normal[j][0:5] + ':00':
                power_index.append(i)
            elif power['Time'][i] == low_finish[j][0:5] + ':00':
                power_finish_low.append(i)
            elif power['Time'][i] == low[j][0:5] + ':00':
                power_index_low.append(i)
            elif power['Time'][i] == high[j][0:5] + ':00':
                power_index_high.append(i)
            elif power['Time'][i] == high_finish[j][0:5] + ':00':
                power_finish_high.append(i)

    print(normal_index)
    print(normal_finish_index)
    print(low_index)
    print(low_finish_index)
    print(high_index)
    print(high_finish_index)
    print(power_index)
    print(power_finish)
    print(power_index_low)
    print(power_finish_low)
    print(power_index_high)
    print(power_finish_high)

    return y1,y2,y3,y4,y5,normal_index,normal_finish_index


def plot(normaly,normaly2,normal_index,normal_finish_index,power_index,power_finish,faulty,faulty2,normal_index_f,normal_finish_index_f,power_index_f,power_finish_f):
    k = 0
    fig, ax1 = plt.subplots(3, 1, figsize=(9, 10))
    for i in range(3):
        ax1[i].plot(range(len(normaly[normal_index[k]:normal_finish_index[k]])), normaly[normal_index[k]:normal_finish_index[k]], color='b', linewidth=1.5,linestyle='-')
        ax2 = ax1[i].twinx()
        ax2.plot(range(len(normaly2[power_index[k]:power_finish[k]])*60), [normaly2[power_index[k]:power_finish[k]].values.tolist()[l] for l in range(len(normaly2[power_index[k]:power_finish[k]].values.tolist())) for m in range(60)],color='c', linewidth=1.5, linestyle='--')

        ax1[i].plot(range(len(faulty[normal_index_f[k]:normal_finish_index_f[k]])*2), [faulty[normal_index_f[k]:normal_finish_index_f[k]].values.tolist()[l] for l in range(len(faulty[normal_index_f[k]:normal_finish_index_f[k]].values.tolist())) for m in range(2)], color='g', linewidth=1.5, linestyle='-')
        ax2.plot(range(len(faulty2[power_index_f[k]:power_finish_f[k]]) * 60),[faulty2[power_index_f[k]:power_finish_f[k]].values.tolist()[l] for l in range(len(faulty2[power_index_f[k]:power_finish_f[k]].values.tolist())) for m in range(60)], color='m', linewidth=1.5, linestyle='--')

        ax1[i].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax1[i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=16)

        ax1[i].set_xticks([0, 100, 200, 300, 400, 500, 599])
        ax1[i].set_xticklabels([x[6 * k:6 * (k + 1) + 1][n].strftime('%H:%M:%S') for n in range(len(x[6 * k:6 * (k + 1) + 1]))],fontsize=16)

        ax2.set_yticks([0, 20, 40, 60, 80, 100, 120])
        ax2.set_yticklabels([0, 20, 40, 60, 80, 100, 120], fontsize=16)

        ax2.set_ylabel('Fan step [step]', fontsize=18)
        ax1[i].set_ylabel('Air velocity [kg/s]', fontsize=18)

        ax1[i].grid(linestyle=':', color='dimgray')
        ax1[i].autoscale(enable=True, axis='x', tight=True)

        k += 1
    plt.tight_layout()
    plt.show()


def uppper_plot(normaly,normaly2,normal_index,normal_finish_index,power_index,power_finish,faulty,faulty2,normal_index_f,normal_finish_index_f,power_index_f,power_finish_f):
    k = 0
    fig, ax1 = plt.subplots(1, 1, figsize=(9, 10))
    for i in range(1):
        ax1.plot(range(len(normaly[normal_index[k]:normal_finish_index[k]])), normaly[normal_index[k]:normal_finish_index[k]], color='b', linewidth=1.5,linestyle='-')
        ax2 = ax1.twinx()
        ax2.plot(range(len(normaly2[power_index[k]:power_finish[k]])*60), [normaly2[power_index[k]:power_finish[k]].values.tolist()[l] for l in range(len(normaly2[power_index[k]:power_finish[k]].values.tolist())) for m in range(60)],color='c', linewidth=1.5, linestyle='--')

        ax1.plot(range(len(faulty[normal_index_f[k]:normal_finish_index_f[k]])*2), [faulty[normal_index_f[k]:normal_finish_index_f[k]].values.tolist()[l] for l in range(len(faulty[normal_index_f[k]:normal_finish_index_f[k]].values.tolist())) for m in range(2)], color='g', linewidth=1.5, linestyle='-')
        ax2.plot(range(len(faulty2[power_index_f[k]:power_finish_f[k]]) * 60),[faulty2[power_index_f[k]:power_finish_f[k]].values.tolist()[l] for l in range(len(faulty2[power_index_f[k]:power_finish_f[k]].values.tolist())) for m in range(60)], color='m', linewidth=1.5, linestyle='--')

        ax1.set_yticks([0,1000,2000,3000,4000])
        ax1.set_yticklabels([0,1000,2000,3000,4000], fontsize=16)

        ax1.set_xticks([0, 100, 200, 300, 400, 500, 599])
        ax1.set_xticklabels([x[6 * k:6 * (k + 1) + 1][n].strftime('%H:%M:%S') for n in range(len(x[6 * k:6 * (k + 1) + 1]))],fontsize=16)

        ax2.set_yticks([0, 20, 40, 60, 80, 100, 120])
        ax2.set_yticklabels([0, 20, 40, 60, 80, 100, 120], fontsize=16)

        ax2.set_ylabel('Fan step [step]', fontsize=18)
        ax1.set_ylabel('Air volume [$m^3/h$]', fontsize=18)

        ax1.grid(linestyle=':', color='dimgray')
        ax1.autoscale(enable=True, axis='x', tight=True)

        k += 1
    plt.tight_layout()
    plt.show()


def side_temp_plot(y1,y2,y3,y4,y5,normal_index,normal_finish_index,fy1,fy2,fy3,fy4,fy5,fnormal_index,fnormal_finish_index):
    x_length = [normal_finish_index[-1] - normal_index[0]]
    x = []
    zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
    for i in range(max(x_length)):
        x.append(zero)
        zero = zero + dt.timedelta(seconds=2)

    fx_length = [fnormal_finish_index[-1] - fnormal_index[0]]
    fx = []
    fzero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
    for i in range(max(fx_length)):
        fx.append(fzero)
        fzero = fzero + dt.timedelta(seconds=2)

    interval = 2 * 30 * 5
    fig, ax1 = plt.subplots(5, 1, figsize=(9, 10))

    ax1[0].plot(range(len(y1[normal_index[0]:normal_finish_index[-1]])), y1[normal_index[0]:normal_finish_index[-1]],color='b', linewidth=1.5, linestyle='-')
    ax1[0].plot(range(len(fy1[fnormal_index[0]:fnormal_finish_index[-1]])), fy1[fnormal_index[0]:fnormal_finish_index[-1]],color='g', linewidth=1.5, linestyle='-')
    ax1[0].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[0].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[1].plot(range(len(y2[normal_index[0]:normal_finish_index[-1]])), y2[normal_index[0]:normal_finish_index[-1]],color='b', linewidth=1.5, linestyle='-')
    ax1[1].plot(range(len(fy2[fnormal_index[0]:fnormal_finish_index[-1]])),fy2[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[1].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[1].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[2].plot(range(len(y3[normal_index[0]:normal_finish_index[-1]])), y3[normal_index[0]:normal_finish_index[-1]],color='b', linewidth=1.5, linestyle='-')
    ax1[2].plot(range(len(fy3[fnormal_index[0]:fnormal_finish_index[-1]])),fy3[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[2].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[2].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[3].plot(range(len(y4[normal_index[0]:normal_finish_index[-1]])), y4[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    ax1[3].plot(range(len(fy4[fnormal_index[0]:fnormal_finish_index[-1]])),fy4[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[3].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[3].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[4].plot(range(len(y5[normal_index[0]:normal_finish_index[-1]])), y5[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    ax1[4].plot(range(len(fy5[fnormal_index[0]:fnormal_finish_index[-1]])),fy5[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[4].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[4].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[4].set_xlabel('Time',fontsize=16)

    for o in range(5):
        ax1[o].set_ylabel('Temperature [C]', fontsize=14)
        ax1[o].set_yticks([30,35,40,45,50])
        ax1[o].set_yticklabels([30, 35, 40, 45, 50],fontsize=14)
        ax1[o].grid(linestyle=':', color='dimgray')
        ax1[o].autoscale(enable=True, axis='x', tight=True)

    plt.tight_layout()
    plt.show()


def upper_temp_plot(y1,y2,y3,y4,y5,normal_index,normal_finish_index,fy1,fy2,fy3,fy4,fy5,fnormal_index,fnormal_finish_index):
    x_length = [normal_finish_index[-1] - normal_index[0]]
    x = []
    zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
    for i in range(max(x_length)):
        x.append(zero)
        zero = zero + dt.timedelta(seconds=2)

    fx_length = [fnormal_finish_index[-1] - fnormal_index[0]]
    fx = []
    fzero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
    for i in range(max(fx_length)):
        fx.append(fzero)
        fzero = fzero + dt.timedelta(seconds=2)

    interval = 2 * 30 * 5
    fig, ax1 = plt.subplots(5, 1, figsize=(9, 12))

    ax1[0].plot(range(len(y1[normal_index[0]:normal_finish_index[-1]])), y1[normal_index[0]:normal_finish_index[-1]],color='b', linewidth=1.5, linestyle='-')
    ax1[0].plot(range(len(fy1[fnormal_index[0]:fnormal_finish_index[-1]])), fy1[fnormal_index[0]:fnormal_finish_index[-1]],color='g', linewidth=1.5, linestyle='-')
    ax1[0].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[0].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[1].plot(range(len(y2[normal_index[0]:normal_finish_index[-1]])), y2[normal_index[0]:normal_finish_index[-1]],color='b', linewidth=1.5, linestyle='-')
    ax1[1].plot(range(len(fy2[fnormal_index[0]:fnormal_finish_index[-1]])),fy2[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[1].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[1].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[2].plot(range(len(y3[normal_index[0]:normal_finish_index[-1]])), y3[normal_index[0]:normal_finish_index[-1]],color='b', linewidth=1.5, linestyle='-')
    ax1[2].plot(range(len(fy3[fnormal_index[0]:fnormal_finish_index[-1]])),fy3[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[2].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[2].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[3].plot(range(len(y4[normal_index[0]:normal_finish_index[-1]])), y4[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    ax1[3].plot(range(len(fy4[fnormal_index[0]:fnormal_finish_index[-1]])),fy4[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[3].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[3].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[4].plot(range(len(y5[normal_index[0]:normal_finish_index[-1]])), y5[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    ax1[4].plot(range(len(fy5[fnormal_index[0]:fnormal_finish_index[-1]])),fy5[fnormal_index[0]:fnormal_finish_index[-1]], color='g', linewidth=1.5, linestyle='-')
    ax1[4].set_xticks([n for n in range(len(fx)) if n % interval == 0])
    ax1[4].set_xticklabels([fx[n].strftime('%H:%M:%S') for n in range(len(fx)) if n % interval == 0],fontsize=14)

    ax1[4].set_xlabel('Time',fontsize=16)

    for o in range(5):
        ax1[o].set_ylabel('Temperature [C]', fontsize=14)
        ax1[o].set_yticks([30,35,40,45,50])
        ax1[o].set_yticklabels([30, 35, 40, 45, 50],fontsize=14)
        ax1[o].grid(linestyle=':', color='dimgray')
        ax1[o].autoscale(enable=True, axis='x', tight=True)

    plt.tight_layout()
    plt.show()


# normaly,normaly2,normal_index,normal_finish_index,power_index,power_finish = data('3066','07','28')
# faulty,faulty2,normal_index_f,normal_finish_index_f,power_index_f,power_finish_f = data('3066','07','30')

# plot(normaly,normaly2,normal_index,normal_finish_index,power_index,power_finish,faulty,faulty2,normal_index_f,normal_finish_index_f,power_index_f,power_finish_f)

# uppper_plot(normaly,normaly2,normal_index,normal_finish_index,power_index,power_finish,faulty,faulty2,normal_index_f,normal_finish_index_f,power_index_f,power_finish_f)

y1,y2,y3,y4,y5,normal_index,normal_finish_index = temp_data('3066','07','28')
fy1,fy2,fy3,fy4,fy5,fnormal_index,fnormal_finish_index = temp_dat
a('3066','07','30')

side_temp_plot(y1,y2,y3,y4,y5,normal_index,normal_finish_index,fy1,fy2,fy3,fy4,fy5,fnormal_index,fnormal_finish_index)
