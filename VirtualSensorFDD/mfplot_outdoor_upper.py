import matplotlib.pyplot as plt
import os
import CoolProp as CP
import datetime as dt
import numpy as np
import pandas as pd
import collections
import itertools
import statistics

for loop in range(6):
    if loop == 0:
        ssd = False
        rolling = False
        POWER = True
        print('None Doing - power')
    elif loop == 1:
        ssd = True
        rolling = False
        POWER = True
        print('Steady state detection - power')
    elif loop == 2:
        ssd = False
        rolling = True
        POWER = True
        print('Rolling - power')
    elif loop == 3:
        ssd = False
        rolling = False
        POWER = False
        print('None Doing - fan step')
    elif loop == 4:
        ssd = True
        rolling = False
        POWER = False
        print('Steady state detection - fan step')
    elif loop == 5:
        ssd = False
        rolling = True
        POWER = False
        print('Rolling - fan step')


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
        rolling_std = testing_std_as_df.replace(np.nan, testing_std_as_df.loc[window_size - 1]).round(3).iloc[:,
                      0].tolist()
        std = np.std(residual)
        return {'stationary standard_deviation': round(std, 3), 'anomalies_dict': collections.OrderedDict(
            [(index, y_i) for index, y_i, avg_i, rs_i in zip(itertools.count(), y, avg_list, rolling_std) if
             (y_i > avg_i + (sigma * rs_i)) | (y_i < avg_i - (sigma * rs_i))])}


    data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-06\0806 flow.csv', engine='python')
    data_point = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-06\point_time_upper.csv')
    power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-06\outdoor_06_3069.csv')
    normal = data_point['nolayer']
    low = data_point['lowlevel']
    high = data_point['highlevel']
    normal_finish = data_point['nolayer_finish']
    low_finish = data_point['lowlevel_finish']
    high_finish = data_point['highlevel_finish']

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
            data['Standard Velocity (Matrix)'][drop[i]] = np.nan  # Stead state detection
    interval = 60

    y = data['Standard Velocity (Matrix)']
    if POWER:
        y2 = power['value']
    elif not POWER:
        y2 = power['fan_step']

    if rolling:
        y = data['Standard Velocity (Matrix)'].rolling(30).mean().fillna(method='bfill')


    print(data_point)
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
            if power['Time'][i] == normal_finish[j][0:5]+':00':
                power_finish.append(i)
            elif power['Time'][i] == normal[j][0:5]+':00':
                power_index.append(i)
            elif power['Time'][i] == low_finish[j][0:5]+':00':
                power_finish_low.append(i)
            elif power['Time'][i] == low[j][0:5]+':00':
                power_index_low.append(i)
            elif power['Time'][i] == high[j][0:5]+':00':
                power_index_high.append(i)
            elif power['Time'][i] == high_finish[j][0:5]+':00':
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

    gap = int(interval / 3)
    fig, ax1 = plt.subplots(1,1,figsize=(12, 10))

    x = []
    zero = dt.datetime.strptime('00:00:00','%H:%M:%S')
    for i in range(7000):
        x.append(zero)
        zero = zero + dt.timedelta(seconds=2)

    ex1_mean = []
    ex2_mean = []
    ex3_mean = []

    ex1_p_mean = []
    ex2_p_mean = []
    ex3_p_mean = []

    k = 0
    for j in range(1):
        if rolling:
            ax1.plot(range(len(y[normal_index[k]:normal_finish_index[k]])), y[normal_index[k]:normal_finish_index[k]], color='b', linewidth=1.5,linestyle='-')
            ax1.plot(range(len(y[low_index[k] + 30:low_finish_index[k]])),y[low_index[k] + 30:low_finish_index[k]], color='g',linewidth=1.5, linestyle='-')
            # ax1.plot(range(len(y[high_index[k] + 30:high_finish_index[k]])),y[high_index[k] + 30:high_finish_index[k]], color='r',linewidth=1.5, linestyle='-')
        else:
            ax1.plot(range(len(y[normal_index[k]:normal_finish_index[k]])),y[normal_index[k]:normal_finish_index[k]], color='b', linewidth=1.5, linestyle='-')
            ax1.plot(range(len(y[low_index[k]:low_finish_index[k]])),y[low_index[k]:low_finish_index[k]], color='g',linewidth=1.5, linestyle='-')
            # ax1.plot(range(len(y[high_index[k]:high_finish_index[k]])),y[high_index[k]:high_finish_index[k]], color='r',linewidth=1.5, linestyle='-')
        ex1_mean.append(y[normal_index[k]:normal_finish_index[k]].mean())
        ex2_mean.append(statistics.mean(y[low_index[k]:low_finish_index[k]]))
        # ex3_mean.append(statistics.mean(y[high_index[k]:high_finish_index[k]]))
        ax2 = ax1.twinx()
        ax2.plot(range(len(y2[power_index[k]:power_finish[k]])*30), [y2[power_index[k]:power_finish[k]].values.tolist()[l] for l in range(len(y2[power_index[k]:power_finish[k]].values.tolist())) for m in range(30)], color='gray', linewidth=1.5, linestyle='--')
        ax2.plot(range(len(y2[power_index_low[k]:power_finish_low[k]])*30), [y2[power_index_low[k]:power_finish_low[k]].values.tolist()[l] for l in range(len(y2[power_index_low[k]:power_finish_low[k]].values.tolist())) for m in range(30)], color='c', linewidth=1.5, linestyle='--')
        # ax2.plot(range(len(y2[power_index_high[k]:power_finish_high[k]])*30), [y2[power_index_high[k]:power_finish_high[k]].values.tolist()[l] for l in range(len(y2[power_index_high[k]:power_finish_high[k]].values.tolist())) for m in range(30)], color='m', linewidth=1.5, linestyle='--')
        ex1_p_mean.append(statistics.mean([y2[power_index[k]:power_finish[k]].values.tolist()[l] for l in range(len(y2[power_index[k]:power_finish[k]].values.tolist())) for m in range(30)]))
        ex2_p_mean.append(statistics.mean([y2[power_index_low[k]:power_finish_low[k]].values.tolist()[l] for l in range(len(y2[power_index_low[k]:power_finish_low[k]].values.tolist())) for m in range(30)]))
        # ex3_p_mean.append(statistics.mean([y2[power_index_high[k]:power_finish_high[k]].values.tolist()[l] for l in range(len(y2[power_index_high[k]:power_finish_high[k]].values.tolist())) for m in range(30)]))
        if POWER:
            ax2.set_yticks([0,10000,20000,30000,40000,50000,60000])
        elif not POWER:
            ax2.set_yticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
        ax1.set_yticks([-2000,-1000,0,1000,2000,3000,4000])
        ax1.set_xticks([0, 100, 200, 300, 400, 500, 599])
        ax1.set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % 1000 == 0])
        # if k == 0:
        #     ax1[4, 4].set_xticklabels([x[n].strftime('%H:%M:%S') for n in range(len(x)) if n % 2000 == 0])
        # else:
        #     ax1.set_xticklabels([x[6 * k-1:6 * (k + 1)+1][n].strftime('%H:%M:%S') for n in range(len(x[6 * k:6 * (k + 1)+1]))])
        if j == 0:
            if POWER:
                ax2.set_ylabel('Power [kW]', fontsize=14)
                # lg1 = ax2.legend(['Experiment 1 (Power) - {}~{}'.format(normal.values[0],normal_finish.values[-1]),
                #             'Experiment 2 (Power) - {}~{}'.format(low.values[0],low_finish.values[-1]),
                #             'Experiment 3 (Power) - {}~{}'.format(high.values[0],high_finish.values[-1])],
                #            bbox_to_anchor=(1,-1))
            elif not POWER:
                ax2.set_ylabel('Fan step', fontsize=14)
                # lg1 = ax2.legend(['Experiment 1 (Fan step) - {}~{}'.format(normal.values[0],normal_finish.values[-1]),
                #             'Experiment 2 (Fan step) - {}~{}'.format(low.values[0],low_finish.values[-1]),
                #             'Experiment 3 (Fan step) - {}~{}'.format(high.values[0],high_finish.values[-1])],
                #            bbox_to_anchor=(1,-1))
        k += 1

    #Air velocity
    # lg2 = ax1.legend(['Experiment 1 (Air volume) - {}~{}'.format(normal.values[0],normal_finish.values[-1]),
    #                  'Experiment 2 (Air volume) - {}~{}'.format(low.values[0],low_finish.values[-1]),
    #                  'Experiment 3 (Air volume) - {}~{}'.format(high.values[0],high_finish.values[-1])],bbox_to_anchor=(0, -1))
    #

    ax1.set_ylabel('Air Volume [$m^3$/h]',fontsize=14)
    ax1.set_ylabel('Air Volume [$m^3$/h]',fontsize=14)
    # ax1[0].set_xlabel('Time',fontsize=14)
    ax1.set_xlabel('Time',fontsize=14)
    ax1.set_title('Air Volume (upper)',fontsize=16)

    plt.tight_layout()

    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Result\{}'.format(
        folder_name)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)

    if POWER:
        if ssd:
            plt.savefig(directory + '\MassFlow_upper_ssd.png')
        elif rolling:
            plt.savefig(directory + '\MassFlow_upper_ma.png')
        elif not ssd and not rolling:
            plt.savefig(directory + '\MassFlow_upper.png')
    elif not POWER:
        if ssd:
            plt.savefig(directory + '\MassFlow_upper_ssd_fanstep.png')
        elif rolling:
            plt.savefig(directory + '\MassFlow_upper_ma_fanstep.png')
        elif not ssd and not rolling:
            plt.savefig(directory + '\MassFlow_upper_fanstep.png')

    if rolling:
        print('Experiment 1 : {}'.format(statistics.mean(ex1_mean)))
        print('Experiment 2 : {}'.format(statistics.mean(ex2_mean)))
        # print('Experiment 3 : {}'.format(statistics.mean(ex3_mean)))
        print('Experiment 1 Power or Fan_step : {}'.format(statistics.mean(ex1_p_mean)))
        print('Experiment 2 Power or Fan_step : {}'.format(statistics.mean(ex2_p_mean)))
        # print('Experiment 3 Power or Fan_step : {}'.format(statistics.mean(ex3_p_mean)))

    print('\n')