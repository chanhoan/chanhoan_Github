import matplotlib.pyplot as plt
import CoolProp as CP
import datetime as dt
import numpy as np
import pandas as pd
import collections
import itertools
import os
import statistics


for loop in range(3):
    if loop == 0:
        ssd = False
        rolling = True
        legend = True
        print('None Doing ')
    elif loop == 1:
        continue
        ssd = True
        rolling = False
        print('Steady state detection')
    elif loop == 2:
        legend = False
        ssd = False
        rolling = True
        print('Rolling')

    def moving_average(data, window_size):
        window = np.ones(int(window_size))/float(window_size)
        return np.convolve(data, window, 'same')


    def explain_anomalies(y, window_size, sigma=1.0):
        avg = moving_average(y, window_size).tolist()
        residual = y - avg
        # Calculate the variation in the distribution of the residual
        std = np.std(residual)
        return {'standard_deviation': round(std, 3),'anomalies_dict': collections.OrderedDict([(index, y_i) for index, y_i, avg_i in zip(itertools.count(), y, avg) if (y_i > avg_i + (sigma*std)) | (y_i < avg_i - (sigma*std))])}


    def explain_anomalies_rolling_std(y, window_size, sigma=1.0):
        avg = moving_average(y, window_size)
        avg_list = avg.tolist()
        residual = y - avg
        # Calculate the variation in the distribution of the residual
        testing_std = residual.rolling(window_size).std()
        testing_std_as_df = pd.DataFrame(testing_std)
        rolling_std = testing_std_as_df.replace(np.nan,testing_std_as_df.loc[window_size - 1]).round(3).iloc[:,0].tolist()
        std = np.std(residual)
        return {'stationary standard_deviation': round(std, 3), 'anomalies_dict': collections.OrderedDict([(index, y_i) for index, y_i, avg_i, rs_i in zip(itertools.count(), y, avg_list, rolling_std) if (y_i > avg_i + (sigma * rs_i)) | (y_i < avg_i - (sigma * rs_i))])}


    data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-13\0813 temp.csv',engine='python').fillna(method='bfill')
    data_point = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-13\point_time_temp_3067.csv')
    power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-13\outdoor_13_3067.csv')
    normal = data_point['nolayer']
    low = data_point['lowlevel']
    high = data_point['highlevel']
    normal_finish = data_point['nolayer_finish']
    low_finish = data_point['lowlevel_finish']
    high_finish = data_point['highlevel_finish']
    print(data_point)

    window_size = 300

    if ssd:
        if ssd:
            p_suc = power['low_pressure']
            t_suc = power['suction_temp1']
            t_sat = []
            t_sh = []
            for i in range(len(p_suc)):
                t_sat.append(CP.CoolProp.PropsSI('T', 'P', p_suc[i] * 98.0665 * 1000, 'Q', 0.5, 'R410A') - 273.15)
                t_sh_ = t_suc[i] - t_sat[i]
                if t_sh_ < 0:
                    t_sh_ = 0
                t_sh.append(t_sh_)

            events = explain_anomalies_rolling_std(pd.Series(t_sh), window_size=6, sigma=1)
            drop = []

            for key, value in events['anomalies_dict'].items():
                for i in range(len(data)):
                    if data['Time'][i][0:5] == power['Time'][key][0:5]:
                        drop.append(i)

            for i in range(len(drop)):
                data['point 1'][drop[i]] = np.nan  # Stead state detection
                data['point 2'][drop[i]] = np.nan  # Stead state detection
                data['point 3'][drop[i]] = np.nan  # Stead state detection
                data['point 4'][drop[i]] = np.nan  # Stead state detection
                data['point 5'][drop[i]] = np.nan  # Stead state detection
                data['point 6'][drop[i]] = np.nan  # Stead state detection
                data['point 7'][drop[i]] = np.nan  # Stead state detection
                data['point 8'][drop[i]] = np.nan  # Stead state detection
                data['point 9'][drop[i]] = np.nan  # Stead state detection
                data['point 10'][drop[i]] = np.nan  # Stead state detection
                data['point 11'][drop[i]] = np.nan  # Stead state detection
                data['point 12'][drop[i]] = np.nan  # Stead state detection
                data['point 13'][drop[i]] = np.nan  # Stead state detection
                data['point 14'][drop[i]] = np.nan  # Stead state detection
                data['point 15'][drop[i]] = np.nan  # Stead state detection
                data['point 16'][drop[i]] = np.nan  # Stead state detection
                data['point 17'][drop[i]] = np.nan  # Stead state detection
                data['point 18'][drop[i]] = np.nan  # Stead state detection
                data['point 19'][drop[i]] = np.nan  # Stead state detection
                data['point 20'][drop[i]] = np.nan  # Stead state detection
                data['point 21'][drop[i]] = np.nan  # Stead state detection
                data['point 22'][drop[i]] = np.nan  # Stead state detection
                data['point 23'][drop[i]] = np.nan  # Stead state detection
                data['point 24'][drop[i]] = np.nan  # Stead state detection
                data['point 25'][drop[i]] = np.nan  # Stead state detection

            y1 = data['point 1']
            y2 = data['point 2']
            y3 = data['point 3']
            y4 = data['point 4']
            y5 = data['point 5']
            y6 = data['point 6']
            y7 = data['point 7']
            y8 = data['point 8']
            y9 = data['point 9']
            y10 = data['point 10']
            y11 = data['point 11']
            y12 = data['point 12']
            y13 = data['point 13']
            y14 = data['point 14']
            y15 = data['point 15']
            y16 = data['point 42']
            y17 = data['point 44']
            y18 = data['point 46']
            y19 = data['point 48']
            y20 = data['point 50']
            y21 = data['point 51']
            y22 = data['point 53']
            y23 = data['point 55']
            y24 = data['point 57']
            y25 = data['point 59']

    elif rolling:
        y1 = data['point 51'].rolling(window_size).mean().fillna(method='bfill')
        y2 = data['point 52'].rolling(window_size).mean().fillna(method='bfill')
        y3 = data['point 53'].rolling(window_size).mean().fillna(method='bfill')
        y4 = data['point 54'].rolling(window_size).mean().fillna(method='bfill')
        y5 = data['point 55'].rolling(window_size).mean().fillna(method='bfill')
        y6 = data['point 54'].rolling(window_size).mean().fillna(method='bfill')
        y7 = data['point 55'].rolling(window_size).mean().fillna(method='bfill')
        y8 = data['point 56'].rolling(window_size).mean().fillna(method='bfill')
        y9 = data['point 59'].rolling(window_size).mean().fillna(method='bfill')
        y10 = data['point 10'].rolling(window_size).mean().fillna(method='bfill')
        y11 = data['point 57'].rolling(window_size).mean().fillna(method='bfill')
        y12 = data['point 58'].rolling(window_size).mean().fillna(method='bfill')
        y13 = data['point 59'].rolling(window_size).mean().fillna(method='bfill')
        y14 = data['point 14'].rolling(window_size).mean().fillna(method='bfill')
        y15 = data['point 15'].rolling(window_size).mean().fillna(method='bfill')
        y16 = data['point 46'].rolling(window_size).mean().fillna(method='bfill')
        y17 = data['point 47'].rolling(window_size).mean().fillna(method='bfill')
        y18 = data['point 48'].rolling(window_size).mean().fillna(method='bfill')
        y19 = data['point 49'].rolling(window_size).mean().fillna(method='bfill')
        y20 = data['point 50'].rolling(window_size).mean().fillna(method='bfill')
        y21 = data['point 32'].rolling(window_size).mean().fillna(method='bfill')
        y22 = data['point 34'].rolling(window_size).mean().fillna(method='bfill')
        y23 = data['point 36'].rolling(window_size).mean().fillna(method='bfill')
        y24 = data['point 38'].rolling(window_size).mean().fillna(method='bfill')
        y25 = data['point 40'].rolling(window_size).mean().fillna(method='bfill')

    elif not ssd and not rolling:
        y1 = data['point 51']
        y2 = data['point 53']
        y3 = data['point 55']
        y4 = data['point 57']
        y5 = data['point 59']
        y6 = data['point 52']
        y7 = data['point 54']
        y8 = data['point 56']
        y9 = data['point 58']
        y10 = data['point 60']
        y11 = data['point 42']
        y12 = data['point 44']
        y13 = data['point 46']
        y14 = data['point 48']
        y15 = data['point 50']
        y16 = data['point 42']
        y17 = data['point 44']
        y18 = data['point 46']
        y19 = data['point 48']
        y20 = data['point 50']
        y21 = data['point 51']
        y22 = data['point 53']
        y23 = data['point 55']
        y24 = data['point 57']
        y25 = data['point 59']

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

    # ,low_finish_index[-1]-low_index[0],high_finish_index[-1]-high_index[0]
    x_length = [normal_finish_index[-1]-normal_index[0]]
    x = []
    zero = dt.datetime.strptime('00:00:00','%H:%M:%S')
    for i in range(max(x_length)):
        x.append(zero)
        zero = zero + dt.timedelta(seconds=2)
    fig, ax1 = plt.subplots(3,3,figsize=(9, 10))
    ax1[0,0].plot(range(len(y1[normal_index[0]:normal_finish_index[-1]])), y1[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[0,0].plot(range(len(y1[low_index[0]:low_finish_index[-1]])), y1[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[0,0].plot(range(len(y1[high_index[0]:high_finish_index[-1]])), y1[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[0,0].set_xticks([0, (len(x)//2), len(x)])
    ax1[0,0].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[0,1].plot(range(len(y2[normal_index[0]:normal_finish_index[-1]])), y2[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[0,1].plot(range(len(y2[low_index[0]:low_finish_index[-1]])), y2[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[0,1].plot(range(len(y2[high_index[0]:high_finish_index[-1]])), y2[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[0,1].set_xticks([0, (len(x)//2), len(x)])
    ax1[0,1].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[0,2].plot(range(len(y3[normal_index[0]:normal_finish_index[-1]])), y3[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[0,2].plot(range(len(y3[low_index[0]:low_finish_index[-1]])), y3[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[0,2].plot(range(len(y3[high_index[0]:high_finish_index[-1]])), y3[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[0,2].set_xticks([0, (len(x)//2), len(x)])
    ax1[0,2].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    # ax1[0,3].plot(range(len(y4[normal_index[0]:normal_finish_index[-1]])), y4[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[0,3].plot(range(len(y4[low_index[0]:low_finish_index[-1]])), y4[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # # ax1[0,3].plot(range(len(y4[high_index[0]:high_finish_index[-1]])), y4[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[0,3].set_xticks([0, (len(x)//2), len(x)])
    # ax1[0,3].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[0,4].plot(range(len(y5[normal_index[0]:normal_finish_index[-1]])), y5[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[0,4].plot(range(len(y5[low_index[0]:low_finish_index[-1]])), y5[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # # ax1[0,4].plot(range(len(y5[high_index[0]:high_finish_index[-1]])), y5[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[0,4].set_xticks([0, (len(x)//2), len(x)])
    # ax1[0,4].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[1,0].plot(range(len(y6[normal_index[0]:normal_finish_index[-1]])), y6[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[1,0].plot(range(len(y6[low_index[0]:low_finish_index[-1]])), y6[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[1,0].plot(range(len(y6[high_index[0]:high_finish_index[-1]])), y6[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[1,0].set_xticks([0, (len(x)//2), len(x)])
    ax1[1,0].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[1,1].plot(range(len(y7[normal_index[0]:normal_finish_index[-1]])), y7[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[1,1].plot(range(len(y7[low_index[0]:low_finish_index[-1]])), y7[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[1,1].plot(range(len(y7[high_index[0]:high_finish_index[-1]])), y7[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[1,1].set_xticks([0, (len(x)//2), len(x)])
    ax1[1,1].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[1,2].plot(range(len(y8[normal_index[0]:normal_finish_index[-1]])), y8[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[1,2].plot(range(len(y8[low_index[0]:low_finish_index[-1]])), y8[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[1,2].plot(range(len(y8[high_index[0]:high_finish_index[-1]])), y8[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[1,2].set_xticks([0, (len(x)//2), len(x)])
    ax1[1,2].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    # ax1[1,3].plot(range(len(y9[normal_index[0]:normal_finish_index[-1]])), y9[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[1,3].plot(range(len(y9[low_index[0]:low_finish_index[-1]])), y9[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[1,3].plot(range(len(y9[high_index[0]:high_finish_index[-1]])), y9[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[1,3].set_xticks([0, (len(x)//2), len(x)])
    # ax1[1,3].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[1,4].plot(range(len(y10[normal_index[0]:normal_finish_index[-1]])), y10[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[1,4].plot(range(len(y10[low_index[0]:low_finish_index[-1]])), y10[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # # ax1[1,4].plot(range(len(y10[high_index[0]:high_finish_index[-1]])), y10[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[1,4].set_xticks([0, (len(x)//2), len(x)])
    # ax1[1,4].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[2,0].plot(range(len(y11[normal_index[0]:normal_finish_index[-1]])), y11[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[2,0].plot(range(len(y11[low_index[0]:low_finish_index[-1]])), y11[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[2,0].plot(range(len(y11[high_index[0]:high_finish_index[-1]])), y11[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[2,0].set_xticks([0, (len(x)//2), len(x)])
    ax1[2,0].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[2,1].plot(range(len(y12[normal_index[0]:normal_finish_index[-1]])), y12[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[2,1].plot(range(len(y12[low_index[0]:low_finish_index[-1]])), y12[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[2,1].plot(range(len(y12[high_index[0]:high_finish_index[-1]])), y12[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[2,1].set_xticks([0, (len(x)//2), len(x)])
    ax1[2,1].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    ax1[2,2].plot(range(len(y13[normal_index[0]:normal_finish_index[-1]])), y13[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[2,2].plot(range(len(y13[low_index[0]:low_finish_index[-1]])), y13[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # ax1[2,2].plot(range(len(y13[high_index[0]:high_finish_index[-1]])), y13[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    ax1[2,2].set_xticks([0, (len(x)//2), len(x)])
    ax1[2,2].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[2,3].plot(range(len(y14[normal_index[0]:normal_finish_index[-1]])), y14[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[2,3].plot(range(len(y14[low_index[0]:low_finish_index[-1]])), y14[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # # ax1[2,3].plot(range(len(y14[high_index[0]:high_finish_index[-1]])), y14[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[2,3].set_xticks([0, (len(x)//2), len(x)])
    # ax1[2,3].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[2,4].plot(range(len(y15[normal_index[0]:normal_finish_index[-1]])), y15[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[2,4].plot(range(len(y15[low_index[0]:low_finish_index[-1]])), y15[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # # ax1[2,4].plot(range(len(y15[high_index[0]:high_finish_index[-1]])), y15[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[2,4].set_xticks([0, (len(x)//2), len(x)])
    # ax1[2,4].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    # ax1[3,0].plot(range(len(y16[normal_index[0]:normal_finish_index[-1]])), y16[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[3,0].plot(range(len(y16[low_index[0]:low_finish_index[-1]])), y16[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[3,0].plot(range(len(y16[high_index[0]:high_finish_index[-1]])), y16[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[3,0].set_xticks([0, (len(x)//2), len(x)])
    # ax1[3,0].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[3,1].plot(range(len(y17[normal_index[0]:normal_finish_index[-1]])), y17[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[3,1].plot(range(len(y17[low_index[0]:low_finish_index[-1]])), y17[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[3,1].plot(range(len(y17[high_index[0]:high_finish_index[-1]])), y17[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[3,1].set_xticks([0, (len(x)//2), len(x)])
    # ax1[3,1].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[3,2].plot(range(len(y18[normal_index[0]:normal_finish_index[-1]])), y18[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[3,2].plot(range(len(y18[low_index[0]:low_finish_index[-1]])), y18[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[3,2].plot(range(len(y18[high_index[0]:high_finish_index[-1]])), y18[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[3,2].set_xticks([0, (len(x)//2), len(x)])
    # ax1[3,2].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[3,3].plot(range(len(y19[normal_index[0]:normal_finish_index[-1]])), y19[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[3,3].plot(range(len(y19[low_index[0]:low_finish_index[-1]])), y19[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[3,3].plot(range(len(y19[high_index[0]:high_finish_index[-1]])), y19[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[3,3].set_xticks([0, (len(x)//2), len(x)])
    # ax1[3,3].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[3,4].plot(range(len(y20[normal_index[0]:normal_finish_index[-1]])), y20[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[3,4].plot(range(len(y20[low_index[0]:low_finish_index[-1]])), y20[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[3,4].plot(range(len(y20[high_index[0]:high_finish_index[-1]])), y20[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[3,4].set_xticks([0, (len(x)//2), len(x)])
    # ax1[3,4].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[4,0].plot(range(len(y21[normal_index[0]:normal_finish_index[-1]])), y21[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[4,0].plot(range(len(y21[low_index[0]:low_finish_index[-1]])), y21[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[4,0].plot(range(len(y21[high_index[0]:high_finish_index[-1]])), y21[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[4,0].set_xticks([0, (len(x)//2), len(x)])
    # ax1[4,0].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[4,1].plot(range(len(y22[normal_index[0]:normal_finish_index[-1]])), y22[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[4,1].plot(range(len(y22[low_index[0]:low_finish_index[-1]])), y22[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[4,1].plot(range(len(y22[high_index[0]:high_finish_index[-1]])), y22[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[4,1].set_xticks([0, (len(x)//2), len(x)])
    # ax1[4,1].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[4,2].plot(range(len(y23[normal_index[0]:normal_finish_index[-1]])), y23[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[4,2].plot(range(len(y23[low_index[0]:low_finish_index[-1]])), y23[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[4,2].plot(range(len(y23[high_index[0]:high_finish_index[-1]])), y23[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[4,2].set_xticks([0, (len(x)//2), len(x)])
    # ax1[4,2].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[4,3].plot(range(len(y24[normal_index[0]:normal_finish_index[-1]])), y24[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[4,3].plot(range(len(y24[low_index[0]:low_finish_index[-1]])), y24[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[4,3].plot(range(len(y24[high_index[0]:high_finish_index[-1]])), y24[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[4,3].set_xticks([0, (len(x)//2), len(x)])
    # ax1[4,3].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])
    #
    # ax1[4,4].plot(range(len(y25[normal_index[0]:normal_finish_index[-1]])), y25[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # # ax1[4,4].plot(range(len(y25[low_index[0]:low_finish_index[-1]])), y25[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    # # ax1[4,4].plot(range(len(y25[high_index[0]:high_finish_index[-1]])), y25[high_index[0]:high_finish_index[-1]], color='r', linewidth=1.5,linestyle='-')
    # ax1[4,4].set_xticks([0, (len(x)//2), len(x)])
    # ax1[4,4].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % (len(x)//2) == 0 or x[n]==x[-1]])

    if legend:
        ax1[2,0].legend(['Experiment 2 (Temperature) - {}~{}'.format(normal.values[0],normal_finish.values[-1]),
                         'Experiment 2 (Temperature) - {}~{}'.format(low.values[0],low_finish.values[-1]),
                         'Experiment 3 (Temperature) - {}~{}'.format(high.values[0],high_finish.values[-1])],bbox_to_anchor=(0,-0.3))

    for i in range(3):
        for j in range(3):
            ax1[i, j].set_yticks([25,30,35,40,45,50,55,60])

    ax1[1,0].set_ylabel('Temperature [C]',fontsize=14)
    ax1[2,1].set_xlabel('Time',fontsize=14)
    ax1[0,1].set_title('Temperature (side)',fontsize=16)
    # ax1[0,0].legend(['Temperature (normal)'],bbox_to_anchor=(1,-1))

    plt.tight_layout()

    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Result\{}'.format(folder_name)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)

    if legend:
        plt.savefig(directory+'\Temp_side_ssd.png',dpi=300)
    elif rolling:
        plt.savefig(directory+'\Temp_side_ma.png',dpi=300)
    elif not ssd and not rolling:
        plt.savefig(directory+'\Temp_side.png',dpi=300)

    normal_mean = [y1[normal_index[0]:normal_finish_index[-1]].mean(),
                   y2[normal_index[0]:normal_finish_index[-1]].mean(),
                   y3[normal_index[0]:normal_finish_index[-1]].mean(),
                   y4[normal_index[0]:normal_finish_index[-1]].mean(),
                   y5[normal_index[0]:normal_finish_index[-1]].mean(),
                   y6[normal_index[0]:normal_finish_index[-1]].mean(),
                   y7[normal_index[0]:normal_finish_index[-1]].mean(),
                   y8[normal_index[0]:normal_finish_index[-1]].mean(),
                   y9[normal_index[0]:normal_finish_index[-1]].mean(),
                   y10[normal_index[0]:normal_finish_index[-1]].mean(),
                   y11[normal_index[0]:normal_finish_index[-1]].mean(),
                   y12[normal_index[0]:normal_finish_index[-1]].mean(),
                   y13[normal_index[0]:normal_finish_index[-1]].mean(),
                   y14[normal_index[0]:normal_finish_index[-1]].mean(),
                   y15[normal_index[0]:normal_finish_index[-1]].mean(),
                   y16[normal_index[0]:normal_finish_index[-1]].mean(),
                   y17[normal_index[0]:normal_finish_index[-1]].mean(),
                   y18[normal_index[0]:normal_finish_index[-1]].mean(),
                   y19[normal_index[0]:normal_finish_index[-1]].mean(),
                   y20[normal_index[0]:normal_finish_index[-1]].mean(),
                   y21[normal_index[0]:normal_finish_index[-1]].mean(),
                   y22[normal_index[0]:normal_finish_index[-1]].mean(),
                   y23[normal_index[0]:normal_finish_index[-1]].mean(),
                   y24[normal_index[0]:normal_finish_index[-1]].mean(),
                   y25[normal_index[0]:normal_finish_index[-1]].mean()]

    # low_mean = [y1[low_index[0]:low_finish_index[-1]].mean(),
    #             y2[low_index[0]:low_finish_index[-1]].mean(),
    #             y3[low_index[0]:low_finish_index[-1]].mean(),
    #             y4[low_index[0]:low_finish_index[-1]].mean(),
    #             y5[low_index[0]:low_finish_index[-1]].mean(),
    #             y6[low_index[0]:low_finish_index[-1]].mean(),
    #             y7[low_index[0]:low_finish_index[-1]].mean(),
    #             y8[low_index[0]:low_finish_index[-1]].mean(),
    #             y9[low_index[0]:low_finish_index[-1]].mean(),
    #             y10[low_index[0]:low_finish_index[-1]].mean(),
    #             y11[low_index[0]:low_finish_index[-1]].mean(),
    #             y12[low_index[0]:low_finish_index[-1]].mean(),
    #             y13[low_index[0]:low_finish_index[-1]].mean(),
    #             y14[low_index[0]:low_finish_index[-1]].mean(),
    #             y15[low_index[0]:low_finish_index[-1]].mean(),
    #             y16[low_index[0]:low_finish_index[-1]].mean(),
    #             y17[low_index[0]:low_finish_index[-1]].mean(),
    #             y18[low_index[0]:low_finish_index[-1]].mean(),
    #             y19[low_index[0]:low_finish_index[-1]].mean(),
    #             y20[low_index[0]:low_finish_index[-1]].mean(),
    #             y21[low_index[0]:low_finish_index[-1]].mean(),
    #             y22[low_index[0]:low_finish_index[-1]].mean(),
    #             y23[low_index[0]:low_finish_index[-1]].mean(),
    #             y24[low_index[0]:low_finish_index[-1]].mean(),
    #             y25[low_index[0]:low_finish_index[-1]].mean()]

    # high_mean = [y1[high_index[0]:high_finish_index[-1]].mean(),
    #              y2[high_index[0]:high_finish_index[-1]].mean(),
    #              y3[high_index[0]:high_finish_index[-1]].mean(),
    #              y4[high_index[0]:high_finish_index[-1]].mean(),
    #              y5[high_index[0]:high_finish_index[-1]].mean(),
    #              y6[high_index[0]:high_finish_index[-1]].mean(),
    #              y7[high_index[0]:high_finish_index[-1]].mean(),
    #              y8[high_index[0]:high_finish_index[-1]].mean(),
    #              y9[high_index[0]:high_finish_index[-1]].mean(),
    #              y10[high_index[0]:high_finish_index[-1]].mean(),
    #              y11[high_index[0]:high_finish_index[-1]].mean(),
    #              y12[high_index[0]:high_finish_index[-1]].mean(),
    #              y13[high_index[0]:high_finish_index[-1]].mean(),
    #              y14[high_index[0]:high_finish_index[-1]].mean(),
    #              y15[high_index[0]:high_finish_index[-1]].mean(),
    #              y16[high_index[0]:high_finish_index[-1]].mean(),
    #              y17[high_index[0]:high_finish_index[-1]].mean(),
    #              y18[high_index[0]:high_finish_index[-1]].mean(),
    #              y19[high_index[0]:high_finish_index[-1]].mean(),
    #              y20[high_index[0]:high_finish_index[-1]].mean(),
    #              y21[high_index[0]:high_finish_index[-1]].mean(),
    #              y22[high_index[0]:high_finish_index[-1]].mean(),
    #              y23[high_index[0]:high_finish_index[-1]].mean(),
    #              y24[high_index[0]:high_finish_index[-1]].mean(),
    #              y25[high_index[0]:high_finish_index[-1]].mean()]

    print('Experiment 1: ',statistics.mean(normal_mean))
    # print('Experiment 2: ',statistics.mean(low_mean))
    # print('Experiment 3: ',statistics.mean(high_mean))