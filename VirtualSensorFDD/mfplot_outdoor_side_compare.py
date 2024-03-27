import matplotlib.pyplot as plt
import CoolProp as CP
import datetime as dt
import numpy as np
import pandas as pd
import collections
import itertools
import os
import statistics

for loop in range(4):
    if loop == 0:
        legend = True
        ssd = False
        rolling = True
        POWER = False
        print('Legend - Fan step')
    elif loop == 1:
        legend = True
        ssd = False
        rolling = True
        POWER = True
        print('Legend - Power')
    elif loop == 2:
        legend = False
        ssd = False
        rolling = True
        POWER = True
        print('Rolling - power')
    elif loop == 3:
        legend = False
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
        rolling_std = testing_std_as_df.replace(np.nan,testing_std_as_df.loc[window_size - 1]).round(3).iloc[:,0].tolist()
        std = np.std(residual)
        return {'stationary standard_deviation': round(std, 3), 'anomalies_dict': collections.OrderedDict([(index, y_i) for index, y_i, avg_i, rs_i in zip(itertools.count(), y, avg_list, rolling_std) if (y_i > avg_i + (sigma * rs_i)) | (y_i < avg_i - (sigma * rs_i))])}

    data_normal = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-07-28\0728 flow.csv', engine='python')
    data_point_normal = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-07-28\point_time_side.csv')
    power_normal = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-07-28\outdoor_28_3066.csv')

    data_fault = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-05\0805 flow.csv',engine='python')
    data_point_fault = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-05\point_time_side.csv')
    power_fault = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-05\outdoor_05_3066.csv')

    normal_normal = data_point_normal['nolayer']
    low_normal = data_point_normal['lowlevel']
    high_normal = data_point_normal['highlevel']
    normal_finish_normal = data_point_normal['nolayer_finish']
    low_finish_normal = data_point_normal['lowlevel_finish']
    high_finish_normal = data_point_normal['highlevel_finish']

    normal_fault = data_point_fault['nolayer']
    low_fault = data_point_fault['lowlevel']
    high_fault = data_point_fault['highlevel']
    normal_finish_fault = data_point_fault['nolayer_finish']
    low_finish_fault = data_point_fault['lowlevel_finish']
    high_finish_fault = data_point_fault['highlevel_finish']

    for i in range(3600):
        if i % 2 == 1:
            data_normal.loc[i,:] = np.nan
    data_normal = data_normal.dropna().reset_index()
    print(data_point_normal)
    print(data_point_fault)

    if rolling:
        y_n = data_normal['Standard Velocity (Matrix)'].rolling(30).mean().fillna(method='bfill')
        y_f = data_fault['Standard Velocity (Matrix)'].rolling(30).mean().fillna(method='bfill')
        if POWER:
            y2_n = power_normal['value']
            y2_f = power_fault['value']
        elif not POWER:
            y2_n = power_normal['fan_step']
            y2_f = power_fault['fan_step']

    normal_index_normal = []
    low_index_normal = []
    high_index_normal = []
    normal_finish_index_normal = []
    low_finish_index_normal = []
    high_finish_index_normal = []

    power_index_normal = []
    power_finish_normal = []
    power_index_low_normal = []
    power_finish_low_normal = []
    power_index_high_normal = []
    power_finish_high_normal = []

    normal_index_fault = []
    low_index_fault = []
    high_index_fault = []
    normal_finish_index_fault = []
    low_finish_index_fault = []
    high_finish_index_fault = []

    power_index_fault = []
    power_finish_fault = []
    power_index_low_fault = []
    power_finish_low_fault = []
    power_index_high_fault = []
    power_finish_high_fault = []

    for i in range(len(data_normal)):
        for j in range(len(data_point_normal)):
            if data_normal['Time'][i] == normal_normal[j]:
                normal_index_normal.append(i)
            elif data_normal['Time'][i] == low_normal[j]:
                low_index_normal.append(i)
            elif data_normal['Time'][i] == high_normal[j]:
                high_index_normal.append(i)
            elif data_normal['Time'][i] == normal_finish_normal[j]:
                normal_finish_index_normal.append(i)
            elif data_normal['Time'][i] == low_finish_normal[j]:
                low_finish_index_normal.append(i)
            elif data_normal['Time'][i] == high_finish_normal[j]:
                high_finish_index_normal.append(i)

    for i in range(len(power_normal)):
        for j in range(len(data_point_normal)):
            if power_normal['Time'][i] == normal_finish_normal[j][0:5]+':00':
                power_finish_normal.append(i)
            elif power_normal['Time'][i] == normal_normal[j][0:5]+':00':
                power_index_normal.append(i)
            elif power_normal['Time'][i] == low_finish_normal[j][0:5]+':00':
                power_finish_low_normal.append(i)
            elif power_normal['Time'][i] == low_normal[j][0:5]+':00':
                power_index_low_normal.append(i)
            elif power_normal['Time'][i] == high_normal[j][0:5]+':00':
                power_index_high_normal.append(i)
            elif power_normal['Time'][i] == high_finish_normal[j][0:5]+':00':
                power_finish_high_normal.append(i)

    for i in range(len(data_fault)):
        for j in range(len(data_point_fault)):
            if data_fault['Time'][i] == normal_fault[j]:
                normal_index_fault.append(i)
            elif data_fault['Time'][i] == low_fault[j]:
                low_index_fault.append(i)
            elif data_fault['Time'][i] == high_fault[j]:
                high_index_fault.append(i)
            elif data_fault['Time'][i] == normal_finish_fault[j]:
                normal_finish_index_fault.append(i)
            elif data_fault['Time'][i] == low_finish_fault[j]:
                low_finish_index_fault.append(i)
            elif data_fault['Time'][i] == high_finish_fault[j]:
                high_finish_index_fault.append(i)

    for i in range(len(power_fault)):
        for j in range(len(data_point_fault)):
            if power_fault['Time'][i] == normal_finish_fault[j][0:5]+':00':
                power_finish_fault.append(i)
            elif power_fault['Time'][i] == normal_fault[j][0:5]+':00':
                power_index_fault.append(i)
            elif power_fault['Time'][i] == low_finish_fault[j][0:5]+':00':
                power_finish_low_fault.append(i)
            elif power_fault['Time'][i] == low_fault[j][0:5]+':00':
                power_index_low_fault.append(i)
            elif power_fault['Time'][i] == high_fault[j][0:5]+':00':
                power_index_high_fault.append(i)
            elif power_fault['Time'][i] == high_finish_fault[j][0:5]+':00':
                power_finish_high_fault.append(i)

    print(normal_index_normal)
    print(normal_finish_index_normal)
    print(low_index_normal)
    print(low_finish_index_normal)
    print(high_index_normal)
    print(high_finish_index_normal)
    print(power_index_normal)
    print(power_finish_normal)
    print(power_index_low_normal)
    print(power_finish_low_normal)
    print(power_index_high_normal)
    print(power_finish_high_normal)

    print(normal_index_fault)
    print(normal_finish_index_fault)
    print(low_index_fault)
    print(low_finish_index_fault)
    print(high_index_fault)
    print(high_finish_index_fault)
    print(power_index_fault)
    print(power_finish_fault)
    print(power_index_low_fault)
    print(power_finish_low_fault)
    print(power_index_high_fault)
    print(power_finish_high_fault)

    fig, ax1 = plt.subplots(3,2,figsize=(12, 10))

    x = []
    zero = dt.datetime.strptime('00:00:00','%H:%M:%S')
    for i in range(6*7):
        x.append(zero)
        zero = zero + dt.timedelta(seconds=100)

    ex1_mean = []
    ex2_mean = []
    ex3_mean = []

    ex1_p_mean = []
    ex2_p_mean = []
    ex3_p_mean = []

    ex1_mean_f = []
    ex2_mean_f = []
    ex3_mean_f = []

    ex1_p_mean_f = []
    ex2_p_mean_f = []
    ex3_p_mean_f = []

    k = 0
    for i in range(3):
        for j in range(2):
            x_normal_normal = range(len(y_n[normal_index_normal[k]:normal_finish_index_normal[k]])*3)
            y_normal_normal = [y_n[normal_index_normal[k]:normal_finish_index_normal[k]].values.tolist()[l] for l in range(len(y_n[normal_index_normal[k]:normal_finish_index_normal[k]].values.tolist())) for n in range(3)]
            x_normal_low = range(len(y_n[low_index_normal[k]+30:low_finish_index_normal[k]])*3)
            y_normal_low = [y_n[low_index_normal[k]+30:low_finish_index_normal[k]].values.tolist()[l] for l in range(len(y_n[low_index_normal[k]+30:low_finish_index_normal[k]].values.tolist())) for n in range(3)]
            x_normal_high = range(len(y_n[high_index_normal[k]+30:high_finish_index_normal[k]])*3)
            y_normal_high = [y_n[high_index_normal[k]+30:high_finish_index_normal[k]].values.tolist()[l] for l in range(len(y_n[high_index_normal[k]+30:high_finish_index_normal[k]].values.tolist())) for n in range(3)]

            x_fault_normal = range(len(y_f[normal_index_fault[k]:normal_finish_index_fault[k]]))
            y_fault_normal = y_f[normal_index_fault[k]:normal_finish_index_fault[k]]
            # x_fault_low = range(len(y_f[low_index_fault[k]+30:low_finish_index_fault[k]]))
            # y_fault_low = y_f[low_index_fault[k]+30:low_finish_index_fault[k]]
            # x_fault_high = range(len(y_f[high_index_fault[k]+30:high_finish_index_fault[k]]))
            # y_fault_high = y_f[high_index_fault[k]+30:high_finish_index_fault[k]]

            ax1[i,j].plot(x_normal_normal, y_normal_normal, color='b', linewidth=1.5,linestyle='-')
            ax1[i, j].plot(x_normal_low, y_normal_low, color='g', linewidth=1.5, linestyle='-')
            ax1[i, j].plot(x_normal_high, y_normal_high, color='r', linewidth=1.5, linestyle='-')
            ax1[i,j].plot(x_fault_normal, y_fault_normal, color='b', linewidth=1.5,linestyle='--')
            # ax1[i, j].plot(x_fault_low, y_fault_low, color='g', linewidth=1.5, linestyle='--')
            # ax1[i, j].plot(x_fault_high, y_fault_high, color='r', linewidth=1.5, linestyle='--')

            ex1_mean.append(statistics.mean(y_normal_normal))
            ex2_mean.append(statistics.mean(y_normal_low))
            ex3_mean.append(statistics.mean(y_normal_high))

            ex1_mean_f.append(y_fault_normal.mean())
            # ex2_mean_f.append(statistics.mean(y_fault_low))
            # ex3_mean_f.append(statistics.mean(y_fault_high))

            px_normal_normal = range(len(y2_n[power_index_normal[k]:power_finish_normal[k]])*90)
            py_normal_normal = [y2_n[power_index_normal[k]:power_finish_normal[k]].values.tolist()[l] for l in range(len(y2_n[power_index_normal[k]:power_finish_normal[k]].values.tolist())) for m in range(90)]
            px_normal_low = range(len(y2_n[power_index_low_normal[k]:power_finish_low_normal[k]]) * 90)
            py_normal_low = [y2_n[power_index_low_normal[k]:power_finish_low_normal[k]].values.tolist()[l] for l in range(len(y2_n[power_index_low_normal[k]:power_finish_low_normal[k]].values.tolist())) for m in range(90)]
            px_normal_high = range(len(y2_n[power_index_high_normal[k]:power_finish_high_normal[k]]) * 90)
            py_normal_high = [y2_n[power_index_high_normal[k]:power_finish_high_normal[k]].values.tolist()[l] for l in range(len(y2_n[power_index_high_normal[k]:power_finish_high_normal[k]].values.tolist())) for m in range(90)]

            px_fault_normal = range(len(y2_f[power_index_fault[k]:power_finish_fault[k]]) * 30)
            py_fault_normal = [y2_f[power_index_fault[k]:power_finish_fault[k]].values.tolist()[l] for l in range(len(y2_f[power_index_fault[k]:power_finish_fault[k]].values.tolist())) for m in range(30)]
            px_fault_low = range(len(y2_f[power_index_low_fault[k]:power_finish_low_fault[k]]) * 30)
            py_fault_low = [y2_f[power_index_low_fault[k]:power_finish_low_fault[k]].values.tolist()[l] for l in range(len(y2_f[power_index_low_fault[k]:power_finish_low_fault[k]].values.tolist())) for m in range(30)]
            px_fault_high = range(len(y2_f[power_index_high_fault[k]:power_finish_high_fault[k]]) * 30)
            py_fault_high = [y2_f[power_index_high_fault[k]:power_finish_high_fault[k]].values.tolist()[l] for l in range(len(y2_f[power_index_high_fault[k]:power_finish_high_fault[k]].values.tolist())) for m in range(30)]

            ax2 = ax1[i,j].twinx()
            ax2.plot(px_normal_normal, py_normal_normal,color='gray', linewidth=1.5, linestyle='-')
            ax2.plot(px_normal_low, py_normal_low, color='c', linewidth=1.5, linestyle='-')
            ax2.plot(px_normal_high, py_normal_high, color='m', linewidth=1.5, linestyle='-')
            ax2.plot(px_fault_normal, py_fault_normal, color='gray', linewidth=1.5, linestyle='--')
            # ax2.plot(px_fault_low, py_fault_low, color='c', linewidth=1.5, linestyle='--')
            # ax2.plot(px_fault_high, py_fault_high, color='m', linewidth=1.5, linestyle='--')

            ex1_p_mean.append(statistics.mean(py_normal_normal))
            ex2_p_mean.append(statistics.mean(py_normal_low))
            ex3_p_mean.append(statistics.mean(py_normal_high))

            ex1_p_mean_f.append(statistics.mean(py_fault_normal))
            # ex2_p_mean_f.append(statistics.mean(py_fault_low))
            # ex3_p_mean_f.append(statistics.mean(py_fault_high))

            ax1[i,j].set_yticks([-2, -1.5, -1, -0.5, 0, 0.5, 1.0, 1.5, 2.0])
            ax1[i, j].set_xticks([0, 150, 300, 450, 600, 750, 899])
            ax1[i,j].set_xticklabels([x[6*k:6*(k+1)+1][n].strftime('%H:%M:%S') for n in range(len(x[6*k:6*(k+1)+1]))])

            if POWER:
                ax2.set_yticks([0,1000,2000,3000,4000,5000,6000,7000])
            elif not POWER:
                ax2.set_yticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
            if i == 1 and j== 1:
                if POWER:
                    ax2.set_ylabel('Power [kW]', fontsize=14)
                    if legend:
                        ax2.legend(['No fault conditions 1 (Power) - {}~{}'.format(normal_normal.values[0],normal_finish_normal.values[-1]),
                                    'No fault conditions 2 (Power) - {}~{}'.format(low_normal.values[0],low_finish_normal.values[-1]),
                                    'No fault conditions 3 (Power) - {}~{}'.format(high_normal.values[0],high_finish_normal.values[-1]),
                                    'Fault conditions  1 (Power) - {}~{}'.format(normal_fault.values[0],normal_finish_fault.values[-1]),
                                    'Fault conditions 2 (Power) - {}~{}'.format(low_fault.values[0],low_finish_fault.values[-1]),
                                    'Fault conditions 3 (Power) - {}~{}'.format(high_fault.values[0],high_finish_fault.values[-1])],
                                   bbox_to_anchor=(1, -1))
                elif not POWER:
                    ax2.set_ylabel('Fan step', fontsize=14)
                    if legend:
                        ax2.legend(['No fault conditions 1 (Fan step) - {}~{}'.format(normal_normal.values[0],normal_finish_normal.values[-1]),
                                    'No fault conditions 2 (Fan step) - {}~{}'.format(low_normal.values[0],low_finish_normal.values[-1]),
                                    'No fault conditions 3 (Fan step) - {}~{}'.format(high_normal.values[0],high_finish_normal.values[-1]),
                                    'Fault conditions 1 (Fan step) - {}~{}'.format(normal_fault.values[0],normal_finish_fault.values[-1]),
                                    'Fault conditions 2 (Fan step) - {}~{}'.format(low_fault.values[0],low_finish_fault.values[-1]),
                                    'Fault conditions 3 (Fan step) - {}~{}'.format(high_fault.values[0],high_finish_fault.values[-1])],
                                   bbox_to_anchor=(1, -1))
            k += 1

    #Air velocity
    if legend:
        ax1[0,0].legend(['No fault conditions 1 (Air velocity) - {}~{}'.format(normal_normal.values[0],normal_finish_normal.values[-1]),
                         'No fault conditions 2 (Air velocity) - {}~{}'.format(low_normal.values[0],low_finish_normal.values[-1]),
                         'No fault conditions 3 (Air velocity) - {}~{}'.format(high_normal.values[0],high_finish_normal.values[-1]),
                         'Fault conditions 1 (Air velocity) - {}~{}'.format(normal_fault.values[0],normal_finish_fault.values[-1]),
                         'Fault conditions 2 (Air velocity) - {}~{}'.format(low_fault.values[0],low_finish_fault.values[-1]),
                         'Fault conditions 3 (Air velocity) - {}~{}'.format(high_fault.values[0],high_finish_fault.values[-1])],
                        bbox_to_anchor=(1, -1))

    ax1[1,0].set_ylabel('Air Velocity [m/s]',fontsize=14)
    ax1[0, 0].set_title('Air velocity (side)', fontsize=16)

    # ax2.set_ylabel('Power [kW]',fontsize=14)

    ax1[2,0].set_xlabel('Time',fontsize=14)
    ax1[2,1].set_xlabel('Time',fontsize=14)

    plt.tight_layout()


    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Result\{}'.format(folder_name)

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)

    if POWER:
        if legend:
            plt.savefig(directory+'\MassFlow_side_legend.png',dpi=300)
        else:
            plt.savefig(directory + '\MassFlow_side_ma.png', dpi=300)

    elif not POWER:
        if legend:
            plt.savefig(directory + '\MassFlow_side_legend_fanstep.png', dpi=300)
        else:
            plt.savefig(directory+'\MassFlow_side_ma_fanstep.png',dpi=300)


    print('No fault conditions 1 : {}'.format(statistics.mean(ex1_mean)))
    print('No fault conditions 2 : {}'.format(statistics.mean(ex2_mean)))
    print('No fault conditions 3 : {}'.format(statistics.mean(ex3_mean)))
    print('No fault conditions 1 Power or Fan_step : {}'.format(statistics.mean(ex1_p_mean)))
    print('No fault conditions 2 Power or Fan_step : {}'.format(statistics.mean(ex2_p_mean)))
    print('No fault conditions 3 Power or Fan_step : {}'.format(statistics.mean(ex3_p_mean)))

    print('Fault conditions 1 : {}'.format(statistics.mean(ex1_mean_f)))
    # print('Fault conditions 2 : {}'.format(statistics.mean(ex2_mean_f)))
    # print('Fault conditions 3 : {}'.format(statistics.mean(ex3_mean_f)))
    print('Fault conditions 1 Power or Fan_step : {}'.format(statistics.mean(ex1_p_mean_f)))
    # print('Fault conditions 2 Power or Fan_step : {}'.format(statistics.mean(ex2_p_mean_f)))
    # print('Fault conditions 3 Power or Fan_step : {}'.format(statistics.mean(ex3_p_mean_f)))

    print('\n')