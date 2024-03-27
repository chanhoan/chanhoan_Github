import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import statistics
from datetime import datetime, timedelta
import math
import os
from glob import glob


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


time = 'updated_time'  # time col
input_seq_len = 12  # input_seq_len

unit = 3067
if unit == 3065:
    lim = 25
    num = 55
elif unit == 3066:
    lim = 5
    num = 88
elif unit == 3067:
    lim = 60
    num = 69
elif unit == 3069:
    lim = 60
    num = 69
comp_num = 1
Fault_day = {3067: [{'2022-01-26':['2022-01-26 14:28:00','2022-01-26 17:13:00']}]
             }

stanby = {3065:0, 3066:90, 3067:0, 3069:0}


def virtual_plot():
    seq_path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Seq2Seq/{}/'.format(
        unit)
    path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2022-02-03/{}/'.format(
        unit)
    overall = pd.DataFrame()
    for period in Fault_day[unit]:
        fig, ax1 = plt.subplots(1, 1, figsize=(12, 4))
        key = list(period.keys())[0]
        testday = datetime.strptime(key, "%Y-%m-%d")
        year = testday.year
        month = testday.month
        day = testday.day
        if len(str(month)) == 1:
            month = "0{}".format(month)
        if len(str(day)) == 1:
            day = "0{}".format(day)
        compmap1 = pd.read_csv(path + '{}/freq1/GB066_{}.csv'.format(str(month) + str(day), unit))[
            ['Time', 'frequency', 'm_dot_pred', 'w_dot_pred', 'Qcond', 'Qevap']]
        compmap2 = pd.read_csv(path + '{}/freq2/GB066_{}.csv'.format(str(month) + str(day), unit))[
            ['frequency', 'm_dot_pred', 'w_dot_pred', 'Qcond', 'Qevap']]
        expmodel = pd.read_csv(path + '{}/EPM.csv'.format(str(month) + str(day)), index_col=0).reset_index()[['index','Prediction']]
        expmodel.columns = ['index','expected_model']
        expmodel[time] = pd.to_datetime(expmodel['index'])
        expmodel = expmodel.drop('index', axis=1)
        compmap1['Time'] = pd.to_datetime(compmap1['Time'])
        pred_Data = pd.concat([compmap1, compmap2], axis=1)
        pred_Data.columns = [time, 'freq1', 'm_dot1', 'w_dot1','Qcond1','Qevap1','freq2','m_dot2','w_dot2','Qcond2','Qevap2']
        pred_Data = pd.merge(pred_Data, expmodel, on=time, how='outer')
        # pred_Data.columns = [time, 'power_freq1', 'power_freq2', 'expected_model']

        pred_Data.set_index(time, inplace=True)
        pred_Data = pred_Data.resample('5T').mean()
        pred_Data = pred_Data.rolling(3).mean().fillna(method='bfill')
        pred_Data.fillna(0)
        NT = pd.read_csv(seq_path + 'Test_ODU{}_{}{}.csv'.format(unit, month, day), index_col=0)
        NT[time] = pd.to_datetime(NT[time])
        # test_time = pd.read_csv(seq_path + 'Test_ODU{}_{}{}.csv'.format(unit, int(month), int(day)), index_col=0)
        # if unit == 3067:
        #     NT[time] = pd.to_datetime(NT[time])
        # else:
        #     test_time[time] = pd.to_datetime(test_time[time])
        #     test_time = test_time.reset_index(drop=True)
        #     test_time = test_time.loc[input_seq_len:, time].reset_index(drop=True)
        #     NT = pd.concat([test_time, NT], axis=1)
        #     NT.fillna(0, inplace=True)


        NT['Test'] = NT['Test'].apply(lambda x: 0 if x < stanby[unit] else x)
        NT.set_index(time, inplace=True)
        NT.loc[(NT.index.hour < 9), 'Test'] = 0
        NT.loc[(NT.index.hour > 18), 'Test'] = 0

        NT = NT.loc[(NT.index.hour >= 10) & (NT.index.hour < 18), :]
        NT = pd.merge(NT, pred_Data, left_index=True, right_index=True, how='left')
        Test = NT.loc[(NT.index.hour >= 10) & (NT.index.hour < 18), :]
        xticklist = []
        for i in range(10, 19, 2):
            xticklist.append(key + "\n{}:00:00".format(i))
        testtime_ = period[key]
        col = ['Test', 'Prediction', 'expected_model', 'w_dot1', 'w_dot2']
        Test.loc[(Test.index < testtime_[0]), col] = 0
        for i in range(1, len(testtime_) - 1, 2):
            testtime_s = datetime.strptime(testtime_[i], "%Y-%m-%d %H:%M:%S")
            testtime_e = datetime.strptime(testtime_[i + 1], "%Y-%m-%d %H:%M:%S")
            # print(testtime_s, testtime_e)
            Test.loc[(Test.index < testtime_s) & (Test.index > testtime_e), col] = 0
        Test.loc[(Test.index > testtime_[-1]), col] = 0
        Test.reset_index(inplace=True)
        NT.reset_index(inplace=True)
        NT = NT.fillna(0)
        if unit == 3065:
            NT['Comp'] = ((NT['w_dot1'] + NT['w_dot2']) * 2)
            NT['Qcond'] = (NT['Qcond1'] + NT['Qcond2'])
            NT['Qevap'] = (NT['Qevap1'] + NT['Qevap2'])
            NT['m_dot'] = (NT['m_dot1'] + NT['m_dot2'])
            NT['f_avg'] = (NT['freq1'] + NT['freq2']) / 2
        elif unit == 3066:
            NT['Comp'] = ((NT['w_dot1'] + NT['w_dot2']) / 4)
            NT['Qcond'] = (NT['Qcond1'] + NT['Qcond2'])
            NT['Qevap'] = (NT['Qevap1'] + NT['Qevap2'])
            NT['m_dot'] = (NT['m_dot1'] + NT['m_dot2'])
            NT['f_avg'] = (NT['freq1'] + NT['freq2'])
        elif unit == 3067:
            NT['Comp'] = ((NT['w_dot1'] + NT['w_dot2']) * 1.7)
            NT['Qcond'] = (NT['Qcond1'] + NT['Qcond2'])
            NT['Qevap'] = (NT['Qevap1'] + NT['Qevap2']) * 3
            NT['m_dot'] = (NT['m_dot1'] + NT['m_dot2'])
            NT['f_avg'] = (NT['freq1'] + NT['freq2']) /2
            NT['rated_w'] = NT['f_avg'] * 497.83
            NT['measure'] = NT['Test'] / NT['rated_w'] * 100
            NT['predict'] = NT['Comp'] / NT['rated_w'] * 100
        elif unit == 3069:
            NT['Comp'] = ((NT['w_dot1'] + NT['w_dot2']) * 5)
            NT['Qcond'] = (NT['Qcond1'] + NT['Qcond2'])
            NT['Qevap'] = (NT['Qevap1'] + NT['Qevap2']) * 3
            NT['m_dot'] = (NT['m_dot1'] + NT['m_dot2'])
            NT['f_avg'] = (NT['freq1'] + NT['freq2']) /2
            NT['rated_w'] = NT['f_avg'] * 497.83
            NT['measure'] = NT['Test'] / NT['rated_w'] * 100
            NT['predict'] = NT['Comp'] / NT['rated_w'] * 100

        COP_actual = []
        COP_pred = []

        for i in range(len(NT)):
            if NT['Test'][i] == 0:
                COP_a = 0
            else:
                COP_a = NT['Qevap'][i] / (NT['Test'][i] / 1000)
                if COP_a > 5:
                    COP_a = 0
            COP_actual.append(COP_a)
        for i in range(len(NT)):
            if NT['Comp'][i] == 0:
                COP_p = 0
            else:
                COP_p = NT['Qevap'][i] / (NT['Prediction'][i] / 1000)
                if COP_p > 5:
                    COP_p = 0
            COP_pred.append(COP_p)

        NT['COP_actual'] = COP_actual
        NT['COP_pred'] = COP_pred

        NT['COP_rate'] = (NT['COP_actual']-NT['COP_pred'])/NT['COP_actual']

        print(statistics.mean(NT['f_avg']))
        print(statistics.mean(NT['m_dot']))
        print(statistics.mean(Test['Test']))
        print(statistics.mean(Test['expected_model']))
        print(statistics.mean(NT['Qcond']))
        print(statistics.mean(NT['COP_rate']))

        ax1.set_ylim(0,lim)
        ax1.set_xticks([i for i in range(len(NT)+1) if i % 24 == 0])
        ax1.set_xticklabels(xticklist,fontsize=12)
        ax1.set_ylabel('PowerConsumption [kW]', fontsize=14)

        ax1.plot(range(len(Test)), Test['Test'], label='Real measurement', linewidth=2)
        ax1.plot(range(len(Test)), Test['Prediction'],label='Seq2Seq model prediction - {:.0f}%'.format(cvrmse(Test['Test']/1000, Test['Prediction']/1000)))
        ax1.plot(range(len(Test)),Test['expected_model'], label='Expected model prediction - {:.0f}%'.format(cvrmse(Test['Test'], Test['expected_model'])))
        ax1.plot((Test['w_dot1'] + Test['w_dot2'])*2.5 / (1000),label='Compressor map model prediction - {:.0f}%'.format(cvrmse(Test['Test'], (Test['w_dot1'] + Test['w_dot2'])*2.5 / (1000))),color='r')

        ax1.legend(loc='upper right', ncol = 2,fontsize=12)
        ax1.grid(linestyle="--", color='lightgray')
        ax1.set_ylabel('PowerConsumption [kW]', fontsize=14)
        # ax1.sharey(ax1[0])
        # ax1.sharex(ax1[0])

        # print(statistics.mean(Test['Test']))
        # print(statistics.mean(Test['Prediction']))
        # print(statistics.mean(Test['expected_model']))
        # print(statistics.mean(NT['f_avg']))
        # print(statistics.mean(Test['Test']))

        print(Test['Test'].values.tolist())
        print(Test['Prediction'].values.tolist())
        print(Test['expected_model'].values.tolist())

        print(unit, str(month) + str(day))
        plt.tight_layout()
        # plt.show()
        # save_path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/performance models/{}/{}/'.format(unit,str(month) + str(day))
        # create_folder(save_path)
        # fig.savefig(save_path + 'overall_performance_model_result.png')

        # comp = (Test['power_freq1']+Test['power_freq2'])*comp_num
        # cvrmse(Test['Test'], Test['Prediction'], "{}{}_seq2seq".format(month,day))
        # cvrmse(Test['Test'], Test['expected_model']*1000, "{}{}_expmodel".format(month,day))
        # cvrmse(Test['Test'], (Test['power_freq1']+Test['power_freq2'])*comp_num, "{}{}_comp".format(month, day))

        print("Power consumption increase(+) or decrease(-) - {}{} : {:.1f}%".format(month,day, 100 * (sum(Test['Test']) - sum(Test['Prediction'])) / sum(Test['Test'])))
        #
        print("Power consumption increase(+) or decrease(-) - {}{} : {:.1f}%".format(month,day, 100 * (sum(Test['Test']) - sum(Test['expected_model'])) / sum(Test['Test'])))

def cvrmse(actual, pred):
    mse = mean_squared_error(actual, pred)
    rmse = math.sqrt(mse)
    mean = statistics.mean(actual)
    cv_rmse = rmse / mean * 100
    return cv_rmse

# dic = 'D:/실증결과/transfer_model/jinri/mon/'
# for x in glob(dic+'/*'):
#     if os.path.isdir(x):
#         Dic2 = x
#         for x in os.listdir(Dic2):
#             if 'Test_data' in x:
#                 Dic = os.path.join(Dic2,x)
#                 print('\n')
#                 print(Dic)
#                 test_df = pd.read_csv(Dic, index_col=0)
#                 test_df = test_df.fillna(0)
#                 test_df['updated_time'] = pd.to_datetime(test_df['updated_time'])
#                 test_df.loc[(test_df.updated_time.dt.hour <9) | (test_df.updated_time.dt.hour>18), 'Prediction'] = 0
#                 cv_list = []
#                 for date in [2,9,23,30,6,13,27,4,11]:
#                     df = test_df[test_df.updated_time.dt.day == date]
#                     cv = cvrmse(df['Test'], df['Prediction'], date)
#                     cv_list.append(cv)
#                 print('max:{} / mean:{}'.format(max(cv_list), min(cv_list)))
# test_df['updated_time'] = pd.to_datetime(test_df['updated_time'])
# test_df.loc[(test_df.updated_time.dt.hour < 8) | (test_df.updated_time.dt.hour > 18), 'Test'] = 0
# for date in range(19,26):
#     print(date)
#     df = test_df[test_df.updated_time.dt.day == date]
#     print(df)
#     cvrmse(df['Test'], df['Prediction'], date)

virtual_plot()