import matplotlib.pyplot as plt
import CoolProp as CP
import datetime as dt
import numpy as np
import pandas as pd
import collections
import itertools
import os


for loop in range(3):
    if loop == 0:
        continue
        ssd = False
        rolling = False
        print('None Doing ')
    elif loop == 1:
        continue
        ssd = True
        rolling = False
        print('Steady state detection')
    elif loop == 2:
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


    data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-02\0802 temp.csv',engine='python').fillna(method='bfill')
    data_point = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-02\point_time_temp.csv')
    power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-02\outdoor_02_3069.csv')
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
                data['point 51'][drop[i]] = np.nan  # Stead state detection
                data['point 52'][drop[i]] = np.nan  # Stead state detection
                data['point 53'][drop[i]] = np.nan  # Stead state detection
                data['point 54'][drop[i]] = np.nan  # Stead state detection
                data['point 55'][drop[i]] = np.nan  # Stead state detection
                data['point 56'][drop[i]] = np.nan  # Stead state detection
                data['point 57'][drop[i]] = np.nan  # Stead state detection
                data['point 58'][drop[i]] = np.nan  # Stead state detection
                data['point 59'][drop[i]] = np.nan  # Stead state detection

            y1 = data['point 51']
            y2 = data['point 52']
            y3 = data['point 53']
            y4 = data['point 54']
            y5 = data['point 55']
            y6 = data['point 56']
            y7 = data['point 57']
            y8 = data['point 58']
            y9 = data['point 59']

    elif rolling:
        y1 = data['point 51'].rolling(window_size).mean().fillna(method='bfill')
        y2 = data['point 52'].rolling(window_size).mean().fillna(method='bfill')
        y3 = data['point 53'].rolling(window_size).mean().fillna(method='bfill')
        y4 = data['point 54'].rolling(window_size).mean().fillna(method='bfill')
        y5 = data['point 55'].rolling(window_size).mean().fillna(method='bfill')
        y6 = data['point 56'].rolling(window_size).mean().fillna(method='bfill')
        y7 = data['point 57'].rolling(window_size).mean().fillna(method='bfill')
        y8 = data['point 58'].rolling(window_size).mean().fillna(method='bfill')
        y9 = data['point 59'].rolling(window_size).mean().fillna(method='bfill')

    elif not ssd and not rolling:
        y1 = data['point 51']
        y2 = data['point 52']
        y3 = data['point 53']
        y4 = data['point 54']
        y5 = data['point 55']
        y6 = data['point 56']
        y7 = data['point 57']
        y8 = data['point 58']
        y9 = data['point 59']

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
    # print(power_index)
    # print(power_finish)
    # print(power_index_low)
    # print(power_finish_low)
    # print(power_index_high)
    # print(power_finish_high)

    x_length = [normal_finish_index[-1]-normal_index[0],low_finish_index[-1]-low_index[0],high_finish_index[-1]-high_index[0]]
    x = []
    zero = dt.datetime.strptime('00:00:00','%H:%M:%S')
    for i in range(max(x_length)):
        x.append(zero)
        zero = zero + dt.timedelta(seconds=2)

    y1 = (y1 + y2 + y3) / 3
    y2 = (y4 + y5 + y6) / 3
    y3 = (y7 + y8 + y9) / 3

    fig, ax1 = plt.subplots(3,1,figsize=(9, 10))
    ax1[0].plot(range(len(y1[normal_index[0]:normal_finish_index[-1]])), y1[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[0,0].plot(range(len(y1[low_index[0]:low_finish_index[-1]])), y1[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    ax1[0].plot(range(len(y1[high_index[0]:high_finish_index[-1]])), y1[high_index[0]:high_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    ax1[0].set_xticks([0, 500,1000, 1500])
    ax1[0].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % 500 == 0],fontsize=16)

    ax1[1].plot(range(len(y2[normal_index[0]:normal_finish_index[-1]])), y2[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[1,0].plot(range(len(y4[low_index[0]:low_finish_index[-1]])), y4[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    ax1[1].plot(range(len(y2[high_index[0]:high_finish_index[-1]])), y2[high_index[0]:high_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    ax1[1].set_xticks([0, 500,1000, 1500])
    ax1[1].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % 500 == 0],fontsize=16)

    ax1[2].plot(range(len(y3[normal_index[0]:normal_finish_index[-1]])), y3[normal_index[0]:normal_finish_index[-1]], color='b', linewidth=1.5,linestyle='-')
    # ax1[2,0].plot(range(len(y7[low_index[0]:low_finish_index[-1]])), y7[low_index[0]:low_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    ax1[2].plot(range(len(y3[high_index[0]:high_finish_index[-1]])), y3[high_index[0]:high_finish_index[-1]], color='g', linewidth=1.5,linestyle='-')
    ax1[2].set_xticks([0, 500,1000, 1500])
    ax1[2].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % 500 == 0],fontsize=16)


    ax1[2].set_xlabel('Time',fontsize=18)
    # ax1[0,0].legend(['Temperature (normal)'],bbox_to_anchor=(1,-1))

    for i in range(3):
        ax1[i].set_ylabel('Temperature [C]', fontsize=18)
        ax1[i].set_yticks([20,22,24,26,28,30])
        ax1[i].set_yticklabels([20, 22, 24, 26, 28, 30],fontsize=16)
        ax1[i].grid(linestyle=':', color='dimgray')
        ax1[i].autoscale(enable=True, axis='x', tight=True)

    plt.tight_layout()

    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Result\{}'.format(folder_name)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)

    if ssd:
        plt.savefig(directory+'\Temp_side_ssd.png',dpi=300)
    elif rolling:
        plt.savefig(directory+'\Temp_side_ma.png',dpi=300)
    elif not ssd and not rolling:
        plt.savefig(directory+'\Temp_side.png',dpi=300)