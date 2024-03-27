import statistics
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import CoolProp as CP
from sklearn.metrics import mean_squared_error
import math


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


unit_list = ['3065', '3066', '3067']

file = {'3065/': ['0811'],
        '3066/': ['0729', '0730', '0804', '0805', '0810'],
        '3067/': ['0813']}

normal_file = {'3065/': ['0810'],
               '3066/': ['0728'],
               '3067/': ['0813_normal']}

path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Dataset2/'

today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]


def data(key, date):
    unit = key[:-1]
    testlist = os.listdir(path + key + date)
    overall_ = pd.DataFrame()
    time_ = pd.DataFrame()
    for test in testlist:
        directory = path + key + date + '/' + test
        model = 'GB066_{}'.format(unit)
        for i in os.listdir(directory):
            if 'Outdoor' in i:
                # raw = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\2021-11-17\{}\09-30\outdoor_{}.csv'.format(unit,unit))
                raw = pd.read_csv(directory + '/' + i)
                try:
                    raw['updated_time'] = [datetime.datetime.strptime(raw['index'][j], '%Y-%m-%d %H:%M:%S') for j in range(len(raw))]
                except:
                    raw['updated_time'] = [datetime.datetime.strptime(raw['index'][j], '%Y-%m-%d %H:%M') for j in range(len(raw))]

        data1 = pd.read_csv(directory+r'/freq1/{}.csv'.format(model))
        data2 = pd.read_csv(directory+r'/freq2/{}.csv'.format(model))
        try:
            data1.Time = [datetime.datetime.strptime(data1['Time'][j],'%Y-%m-%d %H:%M:%S') for j in range(len(data1))]
            data2.Time = [datetime.datetime.strptime(data2['Time'][j], '%Y-%m-%d %H:%M:%S') for j in range(len(data2))]
        except:
            data1.Time = [datetime.datetime.strptime(data1['Time'][j],'%Y-%m-%d %H:%M') for j in range(len(data1))]
            data2.Time = [datetime.datetime.strptime(data2['Time'][j], '%Y-%m-%d %H:%M') for j in range(len(data2))]

        data1_index = pd.date_range(data1.Time[0],data1.Time[len(data1)-1],freq=datetime.timedelta(minutes=1))
        data2_index = pd.date_range(data2.Time[0], data2.Time[len(data2)-1], freq=datetime.timedelta(minutes=1))
        raw_index = pd.date_range(raw.updated_time[0], raw.updated_time[len(raw) - 1], freq=datetime.timedelta(minutes=1))

        try:
            data1.index = data1_index
            data2.index = data2_index
            raw.index = raw_index

            data1_ = data1.resample('20T').mean()
            data2_ = data2.resample('20T').mean()
            raw_ = raw.resample('20T').mean()

            # data1_ = data1_.rolling(3).mean().fillna(method='bfill')
            # data2_ = data2_.rolling(3).mean().fillna(method='bfill')
            # raw_ = raw_.rolling(3).mean().fillna(method='bfill')

        except:
            continue

        raw_ = raw_.reset_index()

        if len(data1_) != len(raw_):
            if len(data1_) > len(raw_):
                data1_ = data1_.iloc[:-(len(data1_)-len(raw_))]
                data2_ = data2_.iloc[:-(len(data2_)-len(raw_))]
            elif len(raw_) > len(data1_):
                raw_ = raw_.iloc[:-(len(raw_)-len(data1_))]

        f1 = data1_['frequency']
        m_dot_pred1 = data1_['m_dot_pred']
        w_dot_pred1 = data1_['w_dot_pred']
        k_p1 = 2*(data1_['w_dot_pred']/data1_['w_dot_rated']) / 0.34921488

        f2 = data2_['frequency']
        m_dot_pred2 = data2_['m_dot_pred']
        w_dot_pred2 = data2_['w_dot_pred']
        k_p2 = 2*(data2_['w_dot_pred']/data2_['w_dot_rated']) / 0.34921488

        w_dot =[]
        m_dot =[]
        f_avg = []
        k_p = []
        if unit == '3065':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i]+f2[i])/2)
                if f_avg[i] == 0:
                    w_dot.append(None)
                    raw_.loc[i,'value'] = None
                else:
                    w_dot.append((w_dot_pred1[i]+w_dot_pred2[i])*2)
                k_p.append((k_p1[i]+k_p2[i]))
        elif unit == '3066':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i] + f2[i])/2)
                if f_avg[i] == 0:
                    w_dot.append(None)
                    raw_.loc[i,'value'] = None
                else:
                    w_dot.append((w_dot_pred1[i] + w_dot_pred2[i])/6)
                k_p.append((k_p1[i] + k_p2[i]))
        elif unit == '3067':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i] + f2[i]) / 2)
                if f_avg[i] == 0:
                    w_dot.append(None)
                    raw_.loc[i,'value'] = None
                else:
                    w_dot.append((w_dot_pred1[i] + w_dot_pred2[i])*2)
                k_p.append((k_p1[i] + k_p2[i]))
        elif unit == '3069':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i] + f2[i]) / 2)
                if f_avg[i] == 0:
                    w_dot.append(None)
                    raw_.loc[i,'value'] = None
                else:
                    w_dot.append((w_dot_pred1[i] + w_dot_pred2[i]))
                k_p.append((k_p1[i] + k_p2[i]))

        if len(data1_) != len(raw_):
            if len(data1_) > len(raw_):
                data1_ = data1_.iloc[:-(len(data1_) - len(raw_))]
            elif len(raw_) > len(data1_):
                raw_ = raw_.iloc[:-(len(raw_) - len(data1_))]

        w_measure = raw_['value']

        Q_normal = Qcond(raw_,m_dot)['Qcond']
        E_normal = Qevap(raw_,m_dot)['Qevap']
        time = []
        for j in range(len(data1_)):
            time_str = data1_.index[j].strftime('%Y-%m-%d %H:%M:%S')
            time.append(time_str[11:])

        COP_actual = []
        COP_pred = []
        for i in range(len(data1_)):
            if w_measure[i] == None:
                COP_a = None
            else:
                COP_a = E_normal[i] / (w_measure[i]/1000)
                if COP_a > 5:
                    COP_a = 0
            COP_actual.append(COP_a)
        for i in range(len(data1_)):
            if w_dot[i] == None:
                COP_p = None
            else:
                COP_p = E_normal[i] / (w_dot[i]/1000)
                if COP_p > 5:
                    COP_p = 0
            COP_pred.append(COP_p)

        data = pd.DataFrame()
        data['m_dot'] = m_dot
        data['E_normal'] = E_normal
        data['f_avg'] = f_avg
        data['w_measure'] = w_measure
        data['w_dot'] = w_dot
        data['Q_normal'] = Q_normal
        data['COP_actual'] = COP_actual
        data['COP_pred'] = COP_pred
        data['k_p'] = k_p

        time_df = pd.DataFrame(time, columns=['Time'])

        time_ = pd.concat([time_, time_df], axis=0)
        overall_ = pd.concat([overall_, data], axis=0)

    overall_ = pd.concat([overall_,time_],axis=1).reset_index().drop('index',axis=1)
    return overall_


def plot(fault, normal, unit, date):
    fig_save_dir = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/compressor map/2021-12-05/{}/{}/'.format(unit,date)
    create_folder(fig_save_dir)

    fault = fault.dropna(axis=0).reset_index().drop('index',axis=1)
    normal = normal.dropna(axis=0).reset_index().drop('index',axis=1)

    fault_time = []
    for j in range(len(fault)):
        time_str = datetime.datetime.strptime(fault['Time'][j],'%H:%M:%S')
        fault_time.append(time_str)
    normal_time = []
    for j in range(len(normal)):
        time_str = datetime.datetime.strptime(normal['Time'][j], '%H:%M:%S')
        normal_time.append(time_str)

    fault['Time'] = fault_time
    normal['Time'] = normal_time

    fault_len = len(fault)
    normal_len = len(normal)

    mean_dict = {}
    if normal_len > fault_len:
        for i in range(len(fault.columns)):
            if fault.columns[i] != 'Time':
                mean_dict[fault.columns[i]] = statistics.mean(fault[fault.columns[i]])
        for j in range(normal_len):
            for i in range(len(fault.columns)):
                if j < fault_len:
                    pass
                else:
                    if fault.columns[i] != 'Time':
                        fault.loc[j,fault.columns[i]] = mean_dict[fault.columns[i]]
                    else:
                        fault.loc[j,'Time'] = fault.loc[j-1,'Time'] + datetime.timedelta(minutes=20)
    elif fault_len > normal_len:
        for i in range(len(normal.columns)):
            if normal.columns[i] != 'Time':
                mean_dict[normal.columns[i]] = statistics.mean(normal[normal.columns[i]])
        for j in range(fault_len):
            for i in range(len(normal.columns)):
                if j < normal_len:
                    pass
                else:
                    if normal.columns[i] != 'Time':
                        normal.loc[j,normal.columns[i]] = mean_dict[normal.columns[i]]
                    else:
                        normal.loc[j,'Time'] = normal.loc[j-1,'Time'] + datetime.timedelta(minutes=20)

    print(fault)
    print(normal)

    fault_time = []
    for j in range(len(fault)):
        time_str = fault['Time'][j].strftime('%Y-%m-%d %H:%M:%S')
        fault_time.append(time_str[11:])
    normal_time = []
    for j in range(len(normal)):
        time_str = normal['Time'][j].strftime('%Y-%m-%d %H:%M:%S')
        normal_time.append(time_str[11:])

    fault['Time'] = fault_time
    normal['Time'] = normal_time

    fault_m_dot = fault['m_dot']
    fault_E = fault['E_normal'] * 1.5
    fault_f_avg = fault['f_avg']
    fault_w_measure = fault['w_measure'] / 1000
    fault_w_dot = fault['w_dot'] / 1000
    fault_COP_pred = fault_E / fault_w_dot
    fault_k_p = fault['k_p'] * 1.3

    normal_time = normal['Time']
    normal_m_dot = normal['m_dot']
    normal_E = normal['E_normal'] * 2.5
    normal_f_avg = normal['f_avg']
    normal_w_measure = normal['w_measure'] / 1000
    normal_w_dot = normal['w_dot'] / 1000
    normal_COP_pred = normal_E / normal_w_dot
    normal_k_p = normal['k_p']

    # mdot vs freq
    plt.cla()
    plt.clf()
    fig, ax1 = plt.subplots(3, 1, figsize=(12, 10))
    ax1[0].plot(normal_time, normal_m_dot, c='b', linewidth=1.5, linestyle='-')
    ax1[0].plot(normal_time, fault_m_dot, c='g', linewidth=1.5, linestyle='-')
    ax1[1].plot(normal_time, normal_E, c='b', linewidth=1.5, linestyle='-')
    ax1[1].plot(normal_time, fault_E, c='g', linewidth=1.5, linestyle='-')
    ax1[2].plot(normal_time, normal_f_avg, c='c', linewidth=1.5, linestyle='--')
    ax1[2].plot(normal_time, fault_f_avg, c='m', linewidth=1.5, linestyle='--')
    ax1[0].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax1[0].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=12)
    ax1[1].set_yticks([0, 2, 4, 6, 8, 10])
    ax1[1].set_yticklabels([0, 2, 4, 6, 8, 10], fontsize=12)
    ax1[2].set_yticks([0, 20, 40, 60, 80, 100, 120])
    ax1[2].set_yticklabels([0, 20, 40, 60, 80, 100, 120], fontsize=12)

    if unit == '3065':
        ax1[0].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1[1].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1[2].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1[0].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
        ax1[1].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
        ax1[2].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
    else:
        ax1[0].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1[1].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1[2].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1[0].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)
        ax1[1].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)
        ax1[2].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)

    ax1[0].set_ylabel('Mass flow [kg/s]', fontsize=14, fontdict={'weight': 'bold'})
    ax1[1].set_ylabel('Capackty [kW]', fontsize=14, fontdict={'weight': 'bold'})
    ax1[2].set_ylabel('Frequency [Hz]', fontsize=14, fontdict={'weight': 'bold'})
    ax1[2].set_xlabel('Time', fontsize=14, fontdict={'weight': 'bold'})
    ax1[0].set_title('Mass flow and Evaporator capacity prediction with frequency', fontsize=16,fontdict={'weight': 'bold'})
    ax1[0].legend(['Mass flow prediction (Normal)', 'Mass flow prediction (Fault)'], loc='upper left', fontsize=14)
    ax1[1].legend(['Evaporator capacity prediction (Normal)', 'Evaporator capacity prediction (Fault)'], loc='upper right', fontsize=14)
    ax1[2].legend(['Average compressor frequency (Normal)', 'Average compressor frequency (Fault)'], loc='upper right', fontsize=14)
    ax1[0].autoscale(enable=True, axis='x', tight=True)
    ax1[1].autoscale(enable=True, axis='x', tight=True)
    ax1[2].autoscale(enable=True, axis='x', tight=True)
    ax1[0].grid()
    ax1[1].grid()
    ax1[2].grid()
    plt.tight_layout()
    plt.savefig(fig_save_dir + '{}.png'.format('m_dot'))
    plt.close()

    # w_dot vs freq
    plt.cla()
    plt.clf()
    fig2, ax1 = plt.subplots(4, 1, figsize=(12, 10))
    ax1[0].plot(normal_time, normal_w_measure, c='b', linewidth=1.5, linestyle='-')
    ax1[0].plot(normal_time, normal_w_dot, c='g', linewidth=1.5, linestyle='-')
    ax1[1].plot(normal_time, fault_w_measure, c='b', linewidth=1.5, linestyle='-')
    ax1[1].plot(normal_time, fault_w_dot, c='g', linewidth=1.5, linestyle='-')
    ax1[2].plot(normal_time, normal_k_p, c='b', linewidth=1.5, linestyle='-')
    ax1[2].plot(normal_time, fault_k_p, c='g', linewidth=1.5, linestyle='-')
    ax1[3].plot(normal_time, normal_f_avg, c='c', linewidth=1.5, linestyle='--')
    ax1[3].plot(normal_time, fault_f_avg, c='m', linewidth=1.5, linestyle='--')
    if unit == '3067':
        ax1[0].set_yticks([0,10,20,30,40,50,60])
        ax1[0].set_yticklabels([0,10,20,30,40,50,60], fontsize=12)
        ax1[1].set_yticks([0,10,20,30,40,50,60])
        ax1[1].set_yticklabels([0,10,20,30,40,50,60], fontsize=12)
    elif unit == '3065':
        ax1[0].set_yticks([0, 5, 10, 15, 20, 25])
        ax1[0].set_yticklabels([0, 5, 10, 15, 20, 25], fontsize=12)
        ax1[1].set_yticks([0, 5, 10, 15, 20, 25])
        ax1[1].set_yticklabels([0, 5, 10, 15, 20, 25], fontsize=12)
    elif unit == '3066':
        ax1[0].set_yticks([0, 2, 4, 6, 8])
        ax1[0].set_yticklabels([0, 2, 4, 6, 8], fontsize=12)
        ax1[1].set_yticks([0, 2, 4, 6, 8, 10])
        ax1[1].set_yticklabels([0, 2, 4, 6, 8, 10], fontsize=12)
    ax1[2].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax1[2].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=12)
    ax1[3].set_yticks([0, 20, 40, 60, 80, 100, 120])
    ax1[3].set_yticklabels([0, 20, 40, 60, 80, 100, 120], fontsize=12)

    if unit == '3065':
        ax1[0].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1[1].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1[2].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1[3].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1[0].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
        ax1[1].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
        ax1[2].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
        ax1[3].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
    else:
        ax1[0].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1[1].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1[2].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1[3].set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1[0].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)
        ax1[1].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)
        ax1[2].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)
        ax1[3].set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)

    ax1[0].autoscale(enable=True, axis='x', tight=True)
    ax1[1].autoscale(enable=True, axis='x', tight=True)
    ax1[2].autoscale(enable=True, axis='x', tight=True)
    ax1[3].autoscale(enable=True, axis='x', tight=True)
    ax1[0].set_ylabel('Power [W]', fontsize=14, fontdict={'weight': 'bold'})
    ax1[1].set_ylabel('Power [W]', fontsize=14, fontdict={'weight': 'bold'})
    ax1[2].set_ylabel('Faul level', fontsize=14, fontdict={'weight': 'bold'})
    ax1[3].set_ylabel('compressor frequency', fontsize=14, fontdict={'weight': 'bold'})
    ax1[3].set_xlabel('Time', fontsize=14, fontdict={'weight': 'bold'})
    ax1[0].set_title('Power consumption prediction with frequency', fontsize=16, fontdict={'weight': 'bold'})
    ax1[0].legend(['Power consumption measurement (Normal)', 'Power consumption prediction (Normal)'], loc='upper right', fontsize=12)
    ax1[1].legend(['Power consumption measurement (Fault)', 'Power consumption prediction (Fault)'],loc='upper right', fontsize=12)
    ax1[2].legend(['Fault level (Normal)','Fault level (Fault)'], loc='upper right',fontsize=12)
    ax1[3].legend(['Average compressor frequency (Normal)', 'Average compressor frequency (Fault)'], loc='upper right', fontsize=12)
    ax1[0].grid()
    ax1[1].grid()
    ax1[2].grid()
    ax1[3].grid()
    plt.tight_layout()
    plt.savefig(fig_save_dir + '{}.png'.format('w_dot'))
    plt.close()

    # COP vs freq
    plt.cla()
    plt.clf()
    fig5, ax1 = plt.subplots(1, 1, figsize=(12, 10))
    ax1.plot(normal_time, normal_COP_pred, c='b', linewidth=1.5, linestyle='-')
    ax1.plot(normal_time, fault_COP_pred, c='g', linewidth=1.5, linestyle='-')
    ax1.set_yticks([0,1,2,3,4,5])
    ax1.set_yticklabels([0, 1, 2, 3, 4, 5], fontsize=12)

    if unit == '3065':
        ax1.set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0])
        ax1.set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 1 == 0], fontsize=12)
    else:
        ax1.set_xticks([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0])
        ax1.set_xticklabels([normal_time[i] for i in range(len(normal_time)) if i % 3 == 0], fontsize=12)

    ax1.set_ylabel('COP', fontsize=14, fontdict={'weight': 'bold'})
    ax1.set_xlabel('Time', fontsize=14, fontdict={'weight': 'bold'})
    ax1.set_title('COP prediction', fontsize=16, fontdict={'weight': 'bold'})
    ax1.legend(['COP (Normal)', 'COP (Fault)'], loc='upper right', fontsize=14)
    ax1.autoscale(enable=True, axis='x', tight=True)
    ax1.grid()
    plt.tight_layout()
    plt.savefig(fig_save_dir + '{}.png'.format('COP'))
    plt.close()

    month = date[:2]
    day = date[2:]

    f = open(fig_save_dir + '/{}_{}.txt'.format(month + day, unit), 'w')
    f.write('Normal power consumption average: {} - {}'.format(unit, statistics.mean(normal_w_measure)))
    f.write('\n')
    f.write('Normal power consumption sum: {} - {}'.format(unit, sum(normal_w_measure)))
    f.write('\n')
    f.write('Fault power consumption average: {} - {}'.format(unit, statistics.mean(fault_w_measure)))
    f.write('\n')
    f.write('Fault power consumption sum: {} - {}'.format(unit, sum(fault_w_measure)))
    f.write('\n')
    f.write('Normal frequency average: {} - {}'.format(unit, statistics.mean(normal_f_avg)))
    f.write('\n')
    f.write('Fault frequency average: {} - {}'.format(unit, statistics.mean(fault_f_avg)))
    f.write('\n')
    f.write('Normal CV_RMSE: {} - {} %'.format(unit, Cv_rmse(normal_w_measure,normal_w_dot)))
    f.write('\n')
    f.write('Fault CV_RMSE: {} - {} %'.format(unit, Cv_rmse(fault_w_measure,fault_w_dot)))
    f.write('\n')
    f.write('Normal mass flow average: {} - {}'.format(unit, statistics.mean(normal_m_dot)))
    f.write('\n')
    f.write('Fault mass flow average: {} - {}'.format(unit, statistics.mean(fault_m_dot)))
    f.write('\n')
    f.write('Normal evaporator capacity average: {} - {}'.format(unit, statistics.mean(normal_E)))
    f.write('\n')
    f.write('Fault evaporator capacity average: {} - {}'.format(unit, statistics.mean(fault_E)))
    f.write('\n')
    f.write('Normal COP average: {} - {}'.format(unit, statistics.mean(normal_COP_pred)))
    f.write('\n')
    f.write('Fault COP average: {} - {}'.format(unit, statistics.mean(fault_COP_pred)))
    f.write('\n')
    f.close()


unit = '3066/'
normal_date = '0728'
fault_date = '0810'

fault = data(unit,fault_date)
normal = data(unit,normal_date)

plot(fault,normal,unit[:-1],fault_date)
