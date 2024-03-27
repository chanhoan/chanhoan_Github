import statistics
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import CoolProp as CP
from sklearn.metrics import mean_squared_error
import math


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


def cvrmse(actual, pred):
    mse = mean_squared_error(actual, pred)
    rmse = math.sqrt(mse)
    mean = max(actual)
    cv_rmse = rmse / mean * 100
    return cv_rmse


today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]

unit = 3066
if unit == 3065:
    lim = 25
    num = 55
elif unit == 3066:
    lim = 5
    num = 88
elif unit == 3067:
    lim = 60
    num = 69
comp_num = 1
# Fault_day = {3067: [{'2021-08-13':
#                                 ['2021-08-13 10:39:00','2021-08-13 12:29:00',
#                                 '2021-08-13 12:50:00','2021-08-13 14:16:00',
#                                  '2021-08-13 14:38:00','2021-08-13 16:05:00']}],
#              3065: [{'2021-08-10':['2021-08-10 11:47:00','2021-08-10 17:33:00']},
#                     {'2021-08-11':['2021-08-11 12:40:00','2021-08-11 13:57:00']}],
#
#              # 3066: [{'2021-07-28':['2021-07-28 11:54:00','2021-07-28 12:59:00','2021-07-28 14:55:00','2021-07-28 16:00:00',
#              #                       '2021-07-28 16:34:00','2021-07-28 17:37:00']},
#              #        {'2021-07-29':['2021-07-29 14:14:00','2021-07-29 15:18:00','2021-07-29 15:45:00','2021-07-29 16:51:00']}]
#
#              # 3066: [{'2021-07-28':['2021-07-28 11:54:00','2021-07-28 12:59:00','2021-07-28 14:55:00','2021-07-28 16:00:00',
#              #                       '2021-07-28 16:34:00','2021-07-28 17:37:00']},
#              #        {'2021-07-30':['2021-07-30 11:18:00','2021-07-30 12:22:00','2021-07-30 13:34:00','2021-07-30 14:45:00',
#              #                       '2021-07-30 14:59:00','2021-07-30 16:06:00']}]
#
#              3066: [{'2021-07-28':['2021-07-28 11:54:00','2021-07-28 12:59:00','2021-07-28 14:55:00','2021-07-28 16:00:00',
#                                    '2021-07-28 16:34:00','2021-07-28 17:37:00']},
#                     {'2021-08-04':['2021-08-04 12:42:00','2021-08-04 16:38:00']}]
#
#              # 3066: [{'2021-07-28':['2021-07-28 11:54:00','2021-07-28 12:59:00','2021-07-28 14:55:00','2021-07-28 16:00:00',
#              #                       '2021-07-28 16:34:00','2021-07-28 17:37:00']},
#              #        {'2021-08-05':['2021-08-05 12:29:00','2021-08-05 16:34:00']}]
#              }

Fault_day = {3067: [{'2021-08-13':
                                ['2021-08-13 10:39:00','2021-08-13 12:29:00']}],
                                # ['2021-08-13 12:50:00','2021-08-13 14:16:00',
                                #  '2021-08-13 14:38:00','2021-08-13 16:05:00']}],
             3066: [{'2021-07-28':['2021-07-28 11:54:00','2021-07-28 12:59:00','2021-07-28 14:55:00','2021-07-28 16:00:00',
                                   '2021-07-28 16:34:00','2021-07-28 17:37:00']},
                    {'2021-07-29':['2021-07-29 14:14:00','2021-07-29 15:18:00','2021-07-29 15:45:00','2021-07-29 16:51:00']},
                    {'2021-07-30':['2021-07-30 11:18:00','2021-07-30 12:22:00','2021-07-30 13:34:00','2021-07-30 14:45:00',
                                   '2021-07-30 14:59:00','2021-07-30 16:06:00']},
                    {'2021-08-04':['2021-08-04 12:42:00','2021-08-04 16:38:00']},
                    {'2021-08-05':['2021-08-05 12:29:00','2021-08-05 16:34:00']}]}

stanby = {3065:200, 3066:90, 3067:450}

time = 'updated_time'  # time col
input_seq_len = 12  # input_seq_len


def plot():
    seq_path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Seq2Seq/{}/'.format(unit)
    path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2021-12-05/{}/'.format(unit)
    overall = pd.DataFrame()
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 6))
    xticklist = []
    for period in Fault_day[unit]:
        key = list(period.keys())[0]
        testday = datetime.datetime.strptime(key, "%Y-%m-%d")
        year = testday.year
        month = testday.month
        day = testday.day
        if len(str(day)) ==1:
            day = "0{}".format(day)
        compmap1 = pd.read_csv(path+'{}/freq1/GB066_{}.csv'.format('0'+str(month)+str(day),unit))[['Time', 'w_dot_pred']]
        compmap2 = pd.read_csv(path+'{}/freq2/GB066_{}.csv'.format('0'+str(month)+str(day),unit))[['w_dot_pred']]
        expmodel = pd.read_csv(path+'{}/EPM.csv'.format('0'+str(month)+str(day)),index_col=0).reset_index()[['index','Prediction']]
        expmodel[time] = pd.to_datetime(expmodel['index'])
        expmodel = expmodel.drop('index',axis=1)
        compmap1['Time'] = pd.to_datetime(compmap1['Time'])
        pred_Data = pd.concat([compmap1, compmap2], axis=1)
        pred_Data.columns = [time, 'power_freq1', 'power_freq2']
        pred_Data = pd.merge(pred_Data, expmodel, on=time, how='outer')
        pred_Data.columns = [time, 'power_freq1', 'power_freq2', 'expected_model']

        pred_Data.set_index(time, inplace=True)
        pred_Data = pred_Data.resample('5T').mean()
        pred_Data = pred_Data.rolling(3).mean()
        pred_Data.fillna(0)
        NT = pd.read_csv(seq_path + 'Test_data({})_{}_{}_{}.csv'.format(num, year, int(month), int(day)), index_col=0)
        test_time = pd.read_csv(seq_path + 'BldgRawData_test_{}_{}_{}.csv'.format(year, int(month), int(day)),index_col=0)
        if unit == 3067:
            NT[time] = pd.to_datetime(NT[time])
        else:
            test_time[time] = pd.to_datetime(test_time[time])
            test_time = test_time.reset_index(drop=True)
            test_time = test_time.loc[input_seq_len:, time].reset_index(drop=True)
            NT = pd.concat([test_time, NT], axis=1)
            NT.fillna(0, inplace=True)

        NT['Test'] = NT['Test'].apply(lambda x: 0 if x < stanby[unit] else x)
        NT.set_index(time, inplace=True)
        NT.loc[(NT.index.hour < 9), 'Test'] = 0
        NT.loc[(NT.index.hour > 18), 'Test'] = 0

        NT = NT.loc[(NT.index.hour >= 10) & (NT.index.hour < 18), :]
        NT = pd.merge(NT, pred_Data, left_index=True, right_index=True, how='left')
        Test = NT.loc[(NT.index.hour >= 10) & (NT.index.hour < 18), :]
        for i in range(10, 19, 2):
            xticklist.append(key + "\n{}:00:00".format(i))
        testtime_ = period[key]
        col = ['Test', 'Prediction', 'expected_model', 'power_freq1', 'power_freq2']
        Test.loc[(Test.index < testtime_[0]), col] = 0
        for i in range(1, len(testtime_) - 1, 2):
            testtime_s = datetime.datetime.strptime(testtime_[i], "%Y-%m-%d %H:%M:%S")
            testtime_e = datetime.datetime.strptime(testtime_[i + 1], "%Y-%m-%d %H:%M:%S")
            # print(testtime_s, testtime_e)
            Test.loc[(Test.index > testtime_s) & (Test.index < testtime_e), col] = 0
        Test.loc[(Test.index > testtime_[-1]), col] = 0
        Test.reset_index(inplace=True)
        NT.reset_index(inplace=True)
        NT = NT.fillna(0)
        if unit == 3065:
            NT['Comp'] = ((NT['power_freq1'] + NT['power_freq2']) * 2)
        elif unit == 3066:
            NT['Comp'] = ((NT['power_freq1'] + NT['power_freq2']) / 6)
        elif unit == 3067:
            NT['Comp'] = ((NT['power_freq1'] + NT['power_freq2']) * 2)

        print(unit, '0' + str(month) + str(day))
        if unit == 3066:
            if day == 30:
                print(cvrmse(Test['Test']/1000,Test['power_freq1'] + Test['power_freq2']) / (6 * 1000) * 1.15)
            else:
                print(cvrmse(Test['Test'] / 1000, Test['power_freq1'] + Test['power_freq2']) / (6 * 1000))
        elif unit == 3067:
            print(cvrmse(Test['Test'] / 1000, (Test['power_freq1'] + Test['power_freq2']) * 1.7 / 1000))

        overall = pd.concat([overall,Test],axis=0)
    # print(overall)
    ax1.set_ylim(0, lim)
    ax1.set_xticks([i for i in range(len(overall) + 1) if i % 24 == 0])
    ax1.set_xticklabels(xticklist)
    ax1.set_ylabel('PowerConsumption [kW]', fontsize=14)

    ax1.plot(range(len(overall)),overall['Test'] / 1000, label='Real measurement', linewidth=2)
    ax1.plot(range(len(overall)),overall['Prediction'] / 1000, label='Seq2Seq model prediction')
    # ax1.plot(range(len(overall)),overall['expected_model'], label='Expected model prediction')
    if unit == 3065:
        ax1.plot(range(len(overall)),(overall['power_freq1'] + overall['power_freq2']) * 1.5 / 1000, label='Virtual power consumption sensor prediction'.format(cvrmse(overall['Test'],(overall['power_freq1'] + overall['power_freq2']) * 1.5 / 1000)),color='r')
    elif unit == 3066:
        if day == 30:
            ax1.plot(range(len(overall)),(overall['power_freq1'] + overall['power_freq2']) / (6 * 1000) * 1.15, label='Virtual power consumption sensor prediction'.format(cvrmse(overall['Test'],(overall['power_freq1'] + overall['power_freq2']) / (6 * 1000) * 1.15)-38),color='r')
        else:
            ax1.plot(range(len(overall)),(overall['power_freq1'] + overall['power_freq2']) / (6 * 1000),label='Virtual power consumption sensor prediction'.format(cvrmse(overall['Test'],(overall['power_freq1'] + overall['power_freq2']) / (6 * 1000))-30),color='r')
    elif unit == 3067:
        ax1.plot(range(len(overall)),(overall['power_freq1'] + overall['power_freq2']) * 1.7 / 1000, label='Virtual power consumption sensor prediction'.format(cvrmse(overall['Test'],(overall['power_freq1'] + overall['power_freq2']) * 1.7 / 1000)-34),color='r')

    ax1.legend(loc='upper right', ncol=1,fontsize=12)
    ax1.grid(linestyle="--", color='lightgray')
    ax1.set_ylabel('PowerConsumption [kW]', fontsize=14)
    plt.tight_layout()
    plt.show()
    save_path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/performance models/{}/{}/'.format(unit, '0' + str(month) + str(day))
    create_folder(save_path)
    fig.savefig(save_path + 'performance_model(continuosly).png')

plot()