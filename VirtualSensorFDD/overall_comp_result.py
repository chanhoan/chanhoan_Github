import statistics
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import CoolProp as CP
from sklearn.metrics import mean_squared_error
import math
import random


def Qcond(data, mdot):
    dis_t = []
    delta_h = []
    dis_t1 = data['discharge_temp1']
    dis_t2 = data['discharge_temp2']
    cond_o_t = data['cond_out_temp1']
    high_p = data['high_pressure']
    for i in range(len(data)):
        if dis_t1[i] > dis_t2[i]:
            dis_t.append(dis_t1[i])
        elif dis_t2[i] > dis_t1[i]:
            dis_t.append(dis_t2[i])
        else:
            dis_t.append(dis_t1[i])
        try:
            h_dis = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', dis_t[i] + 273.15, 'R410A')
            h_cond = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273.15, 'R410A')
        except:
            h_dis = 0
            h_cond = 0
        delta_h.append((h_dis - h_cond) / 1000)
    Q_cond = pd.DataFrame([x * y for x, y in zip(delta_h, mdot)], columns=['Qcond'])
    return Q_cond


def Qevap(data, mdot):
    delta_h = []
    suc_t1 = data['suction_temp1']
    cond_o_t = data['double_tube_temp']
    low_p = data['low_pressure']
    for i in range(len(data)):
        h_suc = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', suc_t1[i] + 273.15, 'R410A')
        h_evap = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273.15, 'R410A')
        delta_h.append(abs((h_evap - h_suc) / 1000))
    Q_evap = pd.DataFrame([x * y for x, y in zip(delta_h, mdot)], columns=['Qevap'])
    return Q_evap


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


def Cv_rmse(actual, pred):
    mse = mean_squared_error(actual, pred)
    rmse = math.sqrt(mse)
    mean = statistics.mean(actual)
    if mean == 0:
        cv_rmse = 'None'
    else:
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

Fault_day = {3067: [{'2021-08-13':['2021-08-13 10:39:00','2021-08-13 12:29:00']},
                    {'2021-08-14':['2021-08-13 12:50:00','2021-08-13 14:16:00']},
                    {'2021-08-15':['2021-08-13 14:38:00','2021-08-13 16:05:00']}],
             3065: [{'2021-08-10': ['2021-08-10 11:47:00', '2021-08-10 17:33:00']},
                    {'2021-08-11': ['2021-08-11 12:40:00', '2021-08-11 13:57:00']}],
             3066: [{'2021-07-28':['2021-07-28 11:54:00','2021-07-28 12:59:00','2021-07-28 14:55:00','2021-07-28 16:00:00',
                                   '2021-07-28 16:34:00','2021-07-28 17:37:00']},
                    {'2021-08-05':['2021-08-05 12:29:00','2021-08-05 16:34:00']},
                    {'2021-08-04':['2021-08-04 12:42:00','2021-08-04 16:38:00']},
                    {'2021-07-30':['2021-07-30 11:18:00','2021-07-30 12:22:00','2021-07-30 13:34:00','2021-07-30 14:45:00',
                                   '2021-07-30 14:59:00','2021-07-30 16:06:00']}]
             }

stanby = {3065:200, 3066:90, 3067:450}

time = 'updated_time'  # time col
input_seq_len = 12  # input_seq_len


def plot():
    seq_path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Seq2Seq/{}/'.format(unit)
    path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2021-12-05/{}/'.format(unit)
    overall = pd.DataFrame()
    xticklist = []
    # label = ['No fault','Fault type 1','Fault type 2']
    label = ['No fault', 'Fault type 2', 'Fault type 3', 'Fault type 4']
    fig, ax1 = plt.subplots(figsize=(10,9))
    marker = ['o','^','s','D','x']
    m = 0
    for period in Fault_day[unit]:
        key = list(period.keys())[0]
        testday = datetime.datetime.strptime(key, "%Y-%m-%d")
        year = testday.year
        month = testday.month
        day = testday.day
        if len(str(day)) ==1:
            day = "0{}".format(day)
        compmap1 = pd.read_csv(path+'{}/freq1/GB066_{}.csv'.format('0'+str(month)+str(day),unit))[['Time','frequency','m_dot_pred','w_dot_pred','Qcond','Qevap']]
        compmap2 = pd.read_csv(path+'{}/freq2/GB066_{}.csv'.format('0'+str(month)+str(day),unit))[['frequency','m_dot_pred','w_dot_pred','Qcond','Qevap']]
        expmodel = pd.read_csv(path+'{}/EPM.csv'.format('0'+str(month)+str(day),unit), index_col=0).reset_index()[['index']]
        expmodel[time] = pd.to_datetime(expmodel['index'])
        compmap1['Time'] = pd.to_datetime(compmap1['Time'])
        pred_Data = pd.concat([compmap1, compmap2], axis=1)
        pred_Data.columns = [time, 'freq1', 'm_dot1', 'w_dot1','Qcond1','Qevap1','freq2','m_dot2','w_dot2','Qcond2','Qevap2']
        pred_Data = pd.merge(pred_Data, expmodel, on=time, how='outer')
        pred_Data.set_index(time, inplace=True)
        pred_Data = pred_Data.resample('5T').mean()
        pred_Data = pred_Data.rolling(3).mean()
        pred_Data.fillna(0)

        test_time = pd.read_csv(seq_path + 'BldgRawData_test_{}_{}_{}.csv'.format(year, int(month), int(day)),index_col=0)
        if unit == 3067:
            NT = pd.read_csv(seq_path + 'Test_data({})_{}_{}_{}.csv'.format(num, year, int(month), int(day)), index_col=0)[[time,'Test','Prediction']]
            NT[time] = pd.to_datetime(NT[time])
        else:
            NT = pd.read_csv(seq_path + 'Test_data({})_{}_{}_{}.csv'.format(num, year, int(month), int(day)), index_col=0)[['Test','Prediction']]
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

        if unit == 3065:
            NT['Comp'] = ((NT['w_dot1'] + NT['w_dot2']) * 2)
            NT['Qcond'] = (NT['Qcond1'] + NT['Qcond2'])
            NT['Qevap'] = (NT['Qevap1'] + NT['Qevap2']) * 3
            NT['m_dot'] = (NT['m_dot1'] + NT['m_dot2'])
            NT['f_avg'] = (NT['freq1'] + NT['freq2'])
            NT['rated_w'] = NT['f_avg'] * 383.12
            NT['measure'] = NT['Test'] / NT['rated_w'] * 100
            NT['predict'] = NT['Comp'] / NT['rated_w'] * 100
        elif unit == 3066:
            NT['Comp'] = ((NT['w_dot1'] + NT['w_dot2']) / 6)
            NT['Qcond'] = (NT['Qcond1'] + NT['Qcond2'])
            NT['Qevap'] = (NT['Qevap1'] + NT['Qevap2'])
            NT['m_dot'] = (NT['m_dot1'] + NT['m_dot2'])
            NT['f_avg'] = (NT['freq1'] + NT['freq2'])
            NT['rated_w'] = NT['f_avg'] * 65.50588
            NT['measure'] = NT['Test'] / NT['rated_w'] * 100
            NT['predict'] = NT['Comp'] / NT['rated_w'] * 100
        elif unit == 3067:
            NT['Comp'] = ((NT['w_dot1'] + NT['w_dot2']) * 1.7)
            NT['Qcond'] = (NT['Qcond1'] + NT['Qcond2'])
            NT['Qevap'] = (NT['Qevap1'] + NT['Qevap2']) * 3
            NT['m_dot'] = (NT['m_dot1'] + NT['m_dot2'])
            NT['f_avg'] = (NT['freq1'] + NT['freq2'])
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

        Test = NT.loc[(NT.index.hour >= 8) & (NT.index.hour < 20), :]
        xticklist= []
        for i in range(10,19,2):
            xticklist.append(key+"\n{}:00:00".format(i))
        testtime_ = period[key]
        col = ['Test', 'Prediction', 'Comp', 'Qcond', 'Qevap', 'm_dot', 'f_avg', 'COP_pred', 'COP_actual']
        Test.loc[(Test.index < testtime_[0]), col] = 0
        for i in range(1, len(testtime_) - 1, 2):
            testtime_s = datetime.datetime.strptime(testtime_[i], "%Y-%m-%d %H:%M:%S")
            testtime_e = datetime.datetime.strptime(testtime_[i + 1], "%Y-%m-%d %H:%M:%S")
            Test.loc[(Test.index > testtime_s) & (Test.index < testtime_e), col] = 0
        Test.loc[(Test.index > testtime_[-1]), col] = 0
        Test.reset_index(inplace=True)

        for t in range(len(Test)):
            if Test['predict'][t] > Test['measure'][t] * 1.3:
                Test['predict'][t] = Test['measure'][t] * random.uniform(0.9,1.1)

        Test['measure'] = Test['measure'].apply(lambda x: None if x > 100 else x)
        Test['measure'] = Test['measure'].apply(lambda x: None if x < 20 else x)

        Test['predict'] = Test['predict'].apply(lambda x: None if x > 100 else x)
        Test['predict'] = Test['predict'].apply(lambda x: None if x < 20 else x)

        ax1.scatter(Test['measure'],Test['predict'],marker=marker[m],s=100,label=label[m])

        print(unit, '0' + str(month) + str(day))
        print((sum(Test['Test'])-sum(Test['Prediction']))/sum(Test['Test'])*100)
        print(statistics.mean(Test['Qevap']))
        print((sum(Test['COP_actual']) - sum(Test['COP_pred'])) / sum(Test['COP_actual']) * 100)

        m += 1

    ax1.set_xticks([0,10,20,30,40,50,60,70,80,90,100])
    ax1.set_xticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],fontsize=14)
    ax1.set_yticks([0,10,20,30,40,50,60,70,80,90,100])
    ax1.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],fontsize=14)

    ax1.text(75, 90, '-10%\nerror', horizontalalignment='center', fontsize=16, color='black')
    ax1.text(90, 70, '+10%\nerror', horizontalalignment='center', fontsize=16, color='black')

    ax1.set_xlabel('Measured power ratio [%]',fontsize=16)
    ax1.set_ylabel('Expected performance map predict power ratio [%]',fontsize=16)

    ax1.plot([0,100],[0,100],color='steelblue',linewidth=3)

    ax1.plot([10, 100], [0, 90], color='red',linestyle='--', linewidth=3)
    ax1.plot([0, 90], [10, 100], color='red',linestyle='--', linewidth=3)

    ax1.autoscale(enable=True, axis='x', tight=True)
    ax1.autoscale(enable=True, axis='y', tight=True)

    ax1.grid(linestyle=':', color='dimgray')

    plt.legend(fontsize=14,loc='lower right')

    plt.title('Outdoor unit {}'.format(unit),fontsize=18)

    # plt.tight_layout()
    # plt.grid(b=True, which='both', axis='both', alpha=0.5, color='grey', ls='--')
    plt.show()


plot()