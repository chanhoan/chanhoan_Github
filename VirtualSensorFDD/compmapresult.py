import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import CoolProp as CP
from sklearn.metrics import mean_squared_error
import statistics
import math


def Cv_rmse(actual, pred):
    mse = mean_squared_error(actual, pred)
    rmse = math.sqrt(mse)
    mean = statistics.mean(actual)
    if mean == 0:
        cv_rmse = 'None'
    else:
        cv_rmse = rmse / mean * 100
    return cv_rmse



def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


unit_list = ['3066']

file = {'3066/': ['1229']}

path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2021-12-29/'

today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]

w_dot_3065 = []
w_dot_3066 = []
w_dot_3067 = []
w_dot_3069 = []
w_measure_3065 = []
w_measure_3066 = []
w_measure_3067 = []
w_measure_3069 = []
f_3065 = []
f_3066 = []
f_3067 = []
f_3069 = []
suc_density_3065 = []
suc_density_3066 = []
suc_density_3067 = []
suc_density_3069 = []
for key, value in file.items():
    unit = key[:-1]
    unit_df = pd.DataFrame()
    unit_time_df = pd.DataFrame()
    for date in value:
        testlist = os.listdir(path + key + date)
        overall_ = pd.DataFrame()
        time_ = pd.DataFrame()
        directory = path + key + date
        # directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor model result\2021-11-23\{}\{}'.format(unit,date)
        fault_model = 'GB066_{}'.format(unit)
        model = 'GB066_{}'.format(unit)

        for i in os.listdir(directory):
            if 'outdoor' in i:
                # raw = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\2021-11-17\{}\09-30\outdoor_{}.csv'.format(unit,unit))
                raw = pd.read_csv(directory + '/' + i)
                try:
                    raw['updated_time'] = [datetime.datetime.strptime(raw['updated_time'][j], '%Y-%m-%d %H:%M:%S') for j in range(len(raw))]
                except:
                    raw['updated_time'] = [datetime.datetime.strptime(raw['updated_time'][j], '%Y-%m-%d %H:%M') for j in range(len(raw))]

        data1 = pd.read_csv(directory+r'/freq1/{}.csv'.format(model))
        data2 = pd.read_csv(directory+r'/freq2/{}.csv'.format(model))
        try:
            data1.Time = [datetime.datetime.strptime(data1['Time'][j],'%Y-%m-%d %H:%M:%S') for j in range(len(data1))]
            data2.Time = [datetime.datetime.strptime(data2['Time'][j], '%Y-%m-%d %H:%M:%S') for j in range(len(data2))]
        except:
            data1.Time = [datetime.datetime.strptime(data1['Time'][j],'%Y-%m-%d %H:%M') for j in range(len(data1))]
            data2.Time = [datetime.datetime.strptime(data2['Time'][j], '%Y-%m-%d %H:%M') for j in range(len(data2))]

        # if target_day < 10:
        #     date = '0' + str(target_day)
        # else:
        #     date = target_day

        # data1_ = data1[data1['Time'].dt.day == target_day].reset_index()
        # data2_ = data2[data2['Time'].dt.day == target_day].reset_index()
        # raw_ = raw[raw['updated_time'].dt.day == target_day].reset_index()

        data1_index = pd.date_range(data1.Time[0],data1.Time[len(data1)-1],freq=datetime.timedelta(minutes=1))
        data2_index = pd.date_range(data2.Time[0], data2.Time[len(data2)-1], freq=datetime.timedelta(minutes=1))
        raw_index = pd.date_range(raw.updated_time[0], raw.updated_time[len(raw) - 1], freq=datetime.timedelta(minutes=1))

        try:
            data1.index = data1_index
            data2.index = data2_index
            raw.index = raw_index

            data1_ = data1.resample('5T').mean()
            data2_ = data2.resample('5T').mean()
            raw_ = raw.resample('5T').mean()

            data1_ = data1_.rolling(3).mean().fillna(method='bfill')
            data2_ = data2_.rolling(3).mean().fillna(method='bfill')
            raw_ = raw_.rolling(3).mean().fillna(method='bfill')

        except:
            continue

        # data1_ = data1_.reset_index()
        # data2_ = data2_.reset_index()
        raw_ = raw_.reset_index()

        if len(data1_) != len(raw_):
            if len(data1_) > len(raw_):
                data1_ = data1_.iloc[:-(len(data1_)-len(raw_))]
                data2_ = data2_.iloc[:-(len(data2_)-len(raw_))]
            elif len(raw_) > len(data1_):
                raw_ = raw_.iloc[:-(len(raw_)-len(data1_))]

        date_len = len(data1_)

        time1 = data1_.index
        f1 = data1_['frequency']
        T_c1 = data1_['Condensing Temp']
        T_e1 = data1_['Evaporating Temp']
        f_rated1 = data1_['frequency rated']
        m_dot_rated1 = data1_['m_dot_rated']
        w_dot_rated1 = data1_['w_dot_rated']
        m_dot_pred1 = data1_['m_dot_pred']
        w_dot_pred1 = data1_['w_dot_pred']
        k_p1 = data1_['w_dot_pred']/data1_['w_dot_rated']

        time2 = data2_.index
        f2 = data2_['frequency']
        T_c2 = data2_['Condensing Temp']
        T_e2 = data2_['Evaporating Temp']
        f_rated2 = data2_['frequency rated']
        m_dot_rated2 = data2_['m_dot_rated']
        w_dot_rated2 = data2_['w_dot_rated']
        m_dot_pred2 = data2_['m_dot_pred']
        w_dot_pred2 = data2_['w_dot_pred']
        k_p2 = data2_['w_dot_pred']/data2_['w_dot_rated']

        w_dot =[]
        m_dot =[]
        f_avg = []
        k_p = []
        if unit == '3065':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i]+f2[i])/2)
                if f_avg[i] == 0:
                    w_dot.append(0)
                    raw_.loc[i,'value'] = 0
                else:
                    w_dot.append((w_dot_pred1[i]+w_dot_pred2[i])*2)
                k_p.append((k_p1[i]+k_p2[i])/3.4921488e-06)
        elif unit == '3066':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i] + f2[i])/2)
                if f_avg[i] == 0:
                    w_dot.append(0)
                    raw_.loc[i,'value'] = 0
                else:
                    w_dot.append((w_dot_pred1[i] + w_dot_pred2[i])/4)
                k_p.append((k_p1[i] + k_p2[i])/3.4921488e-06)
        elif unit == '3067':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i] + f2[i]) / 2)
                if f_avg[i] == 0:
                    w_dot.append(0)
                    raw_.loc[i,'value'] = 0
                else:
                    w_dot.append((w_dot_pred1[i] + w_dot_pred2[i])*2)
                k_p.append((k_p1[i] + k_p2[i])/3.4921488e-06)
        elif unit == '3069':
            for i in range(len(data1_)):
                m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
                f_avg.append((f1[i] + f2[i]) / 2)
                if f_avg[i] == 0:
                    w_dot.append(0)
                    raw_.loc[i,'value'] = 0
                else:
                    w_dot.append((w_dot_pred1[i] + w_dot_pred2[i]))
                k_p.append((k_p1[i] + k_p2[i])/3.4921488e-06)

        if len(data1_) != len(raw_):
            if len(data1_) > len(raw_):
                data1_ = data1_.iloc[:-(len(data1_) - len(raw_))]
            elif len(raw_) > len(data1_):
                raw_ = raw_.iloc[:-(len(raw_) - len(data1_))]

        w_measure = raw_['value']
        suc_temp = raw_['suction_temp1']
        suc_pressure = raw_['low_pressure']

        print('map data len: ', len(data1_))
        print('raw data len: ', len(raw_))

        k_p_df = pd.DataFrame(k_p,columns=['k_p'])
        # k_p = k_p_df['k_p'].rolling(15).mean().fillna(method='bfill')


        def Qcond(data,mdot):
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
                    h_dis = CP.CoolProp.PropsSI('H', 'P', high_p[i]*98.0665*1000, 'T', dis_t[i]+273.15, 'R410A')
                    h_cond = CP.CoolProp.PropsSI('H','P',high_p[i]*98.0665*1000,'T',cond_o_t[i]+273.15,'R410A')
                except:
                    h_dis = 0
                    h_cond = 0
                delta_h.append((h_dis-h_cond)/1000)
            Q_cond = pd.DataFrame([x*y for x,y in zip(delta_h,mdot)],columns=['Qcond'])
            return Q_cond


        def Qevap(data,mdot):
            delta_h = []
            suc_t1 = data['suction_temp1']
            cond_o_t = data['double_tube_temp']
            low_p = data['low_pressure']
            for i in range(len(data)):
                h_suc = CP.CoolProp.PropsSI('H', 'P', low_p[i]*98.0665*1000, 'T', suc_t1[i]+273.15, 'R410A')
                h_evap = CP.CoolProp.PropsSI('H','P',low_p[i]*98.0665*1000,'T',cond_o_t[i]+273.15,'R410A')
                delta_h.append(abs((h_evap-h_suc)/1000))
            Q_evap = pd.DataFrame([x*y for x,y in zip(delta_h,mdot)],columns=['Qevap'])
            return Q_evap


        Q_normal = Qcond(raw_,m_dot)['Qcond']
        E_normal = Qevap(raw_,m_dot)['Qevap']
        time = []
        for j in range(len(data1_)):
            time_str = data1_.index[j].strftime('%Y-%m-%d %H:%M:%S')
            time.append(time_str[11:])

        COP_actual = []
        COP_pred = []
        for i in range(len(data1_)):
            if w_measure[i] == 0:
                COP_a = 0
            else:
                COP_a = E_normal[i] / (w_measure[i]/1000)
                if COP_a > 5:
                    COP_a = 0
            COP_actual.append(COP_a)
        for i in range(len(data1_)):
            if w_dot[i] == 0:
                COP_p = 0
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

    month = date[:2]
    day = date[2:]

    unit_df = pd.concat([unit_df,overall_],axis=0)
    unit_time_df = pd.concat([unit_time_df, time_], axis=0)
fig_save_dir = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor model result\그림\{}\{}'.format(folder_name, unit)
create_folder(fig_save_dir)

time = unit_time_df.reset_index().drop('index', axis=1)['Time']
m_dot = unit_df['m_dot']
E_normal = unit_df['E_normal']
f_avg = unit_df['f_avg']
w_measure = unit_df['w_measure']
w_dot = unit_df['w_dot']
Q_normal = unit_df['Q_normal']
COP_actual = unit_df['COP_actual']
COP_pred = unit_df['COP_pred']

print(w_measure)

# mdot vs freq
plt.cla()
plt.clf()
fig, ax1 = plt.subplots(3,1,figsize=(12,10))
ax1[0].plot(time,m_dot,c='b',linewidth=1.5,linestyle='-')
ax1[1].plot(time,E_normal,c='b',linewidth=1.5,linestyle='-')
ax1[2].plot(time,f_avg,c='c',linewidth=1.5,linestyle='--')
ax1[0].set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6])
ax1[0].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],fontsize=12)
ax1[1].set_ylim([0,int(max(E_normal))+2])
yticks = ax1[1].get_yticks()
ax1[1].set_yticklabels([int(yticks[i]) for i in range(len(yticks))],fontsize=12)
ax1[2].set_yticks([0,20,40,60,80,100,120])
ax1[2].set_yticklabels([0, 20, 40, 60, 80, 100, 120],fontsize=12)
if unit == '3065':
    ax1[0].set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1[1].set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1[2].set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1[0].set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
    ax1[1].set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
    ax1[2].set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
else:
    ax1[0].set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1[1].set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1[2].set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1[0].set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
    ax1[1].set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
    ax1[2].set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
ax1[0].set_ylabel('Mass flow [kg/s]', fontsize=14,fontdict={'weight':'bold'})
ax1[1].set_ylabel('Capackty [kW]', fontsize=14,fontdict={'weight':'bold'})
ax1[2].set_ylabel('Frequency [Hz]', fontsize=14,fontdict={'weight':'bold'})
ax1[2].set_xlabel('Time',fontsize=14,fontdict={'weight':'bold'})
ax1[0].set_title('Mass flow and Evaporator capacity prediction with frequency',fontsize=16,fontdict={'weight':'bold'})
ax1[0].legend(['Mass flow prediction'],loc='upper right',fontsize=14)
ax1[1].legend(['Evaporator capacity prediction'],loc='upper right',fontsize=14)
ax1[2].legend(['Average compressor frequency'],loc='upper right',fontsize=14)
ax1[0].autoscale(enable=True, axis='x', tight=True)
ax1[1].autoscale(enable=True, axis='x', tight=True)
ax1[2].autoscale(enable=True, axis='x', tight=True)
ax1[0].grid()
ax1[1].grid()
ax1[2].grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}.png'.format('m_dot'))
plt.close()

# w_dot vs freq
plt.cla()
plt.clf()
fig2, ax1 = plt.subplots(2,1,figsize=(12,10))
ax1[0].plot(time,w_measure,c='b',linewidth=1.5,linestyle='-')
ax1[0].plot(range(len(w_dot)),w_dot,c='g',linewidth=1.5,linestyle='-')
ax1[1].plot(time,f_avg,c='c',linewidth=1.5,linestyle='--')
ax1[0].set_ylim([0,int(max(w_dot))+2000])
yticks = ax1[0].get_yticks()
ax1[0].set_yticklabels([int(yticks[i]) for i in range(len(yticks))],fontsize=12)
ax1[1].set_yticks([0,20,40,60,80,100,120])
ax1[1].set_yticklabels([0, 20, 40, 60, 80, 100, 120],fontsize=12)
if unit == '3065':
    ax1[0].set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1[1].set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1[0].set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
    ax1[1].set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
else:
    ax1[0].set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1[1].set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1[0].set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
    ax1[1].set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
ax1[0].autoscale(enable=True, axis='x', tight=True)
ax1[1].autoscale(enable=True, axis='x', tight=True)
ax1[0].set_ylabel('Power [W]', fontsize=14,fontdict={'weight':'bold'})
ax1[1].set_ylabel('compressor frequency', fontsize=14,fontdict={'weight':'bold'})
ax1[1].set_xlabel('Time',fontsize=14,fontdict={'weight':'bold'})
ax1[0].set_title('Power consumption prediction with frequency',fontsize=16,fontdict={'weight':'bold'})
ax1[0].legend(['Power consumption measurement','Power consumption prediction'],loc='upper right',fontsize=12)
ax1[1].legend(['Average compressor frequency'],loc='upper right',fontsize=12)
ax1[0].grid()
ax1[1].grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}.png'.format('w_dot'))
plt.close()

# Qcond vs freq
plt.cla()
plt.clf()
fig3, ax1 = plt.subplots(2,1,figsize=(12,10))
ax1[0].plot(time,Q_normal,c='b',linewidth=1.5,linestyle='-')
ax1[1].plot(time,f_avg,c='c',linewidth=1.5,linestyle='--')
ax1[0].set_ylim([0,int(max(Q_normal))+40])
ax1[1].set_ylim([0,int(max(f_avg))+30])
yticks = ax1[0].get_yticks()
ax1[0].set_yticklabels([int(yticks[i]) for i in range(len(yticks))],fontsize=12)
yticks = ax1[1].get_yticks()
ax1[1].set_yticklabels([int(yticks[i]) for i in range(len(yticks))],fontsize=12)
if unit == '3065':
    ax1[0].set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1[1].set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1[0].set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
    ax1[1].set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
else:
    ax1[0].set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1[1].set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1[0].set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
    ax1[1].set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
ax1[0].set_ylabel('Capacity [kW]', fontsize=14,fontdict={'weight':'bold'})
ax1[1].set_ylabel('Frequency [Hz]', fontsize=14,fontdict={'weight':'bold'})
ax1[1].set_xlabel('Time',fontsize=14,fontdict={'weight':'bold'})
ax1[0].set_title('Condenser capacity prediction with frequency',fontsize=16,fontdict={'weight':'bold'})
ax1[0].legend(['Condenser capacity prediction'],loc='upper right',fontsize=11)
ax1[1].legend(['Average compressor frequency'],loc='upper right',fontsize=11)
ax1[0].autoscale(enable=True, axis='x', tight=True)
ax1[1].autoscale(enable=True, axis='x', tight=True)
ax1[0].grid()
ax1[1].grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}.png'.format('Q_cond'))
plt.close()

# COP vs freq
plt.cla()
plt.clf()
fig5, ax1 = plt.subplots(1,1,figsize=(12,10))
ax1.plot(time,COP_actual,c='b',linewidth=1.5,linestyle='-')
ax1.plot(range(len(COP_pred)),COP_pred,c='g',linewidth=1.5,linestyle='-')
ax1.set_ylim([0,int(max(COP_actual))+1])
yticks = ax1.get_yticks()
ax1.set_yticklabels([round(yticks[i],1) for i in range(len(yticks))],fontsize=12)
if unit == '3065':
    ax1.set_xticks([time[i] for i in range(len(time)) if i % 12 == 0])
    ax1.set_xticklabels([time[i] for i in range(len(time)) if i % 12 == 0],fontsize=12)
else:
    ax1.set_xticks([time[i] for i in range(len(time)) if i % 24 == 0])
    ax1.set_xticklabels([time[i] for i in range(len(time)) if i % 24 == 0], fontsize=12)
ax1.set_ylabel('COP', fontsize=14,fontdict={'weight':'bold'})
ax1.set_xlabel('Time',fontsize=14,fontdict={'weight':'bold'})
ax1.set_title('COP prediction',fontsize=16,fontdict={'weight':'bold'})
ax1.legend(['COP (Actual)','COP (Prediction)'],loc='upper right',fontsize=14)
ax1.autoscale(enable=True, axis='x', tight=True)
ax1.grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}.png'.format('COP'))
plt.close()

f = open(fig_save_dir+'\{}_{}.txt'.format(month+day,unit), 'w')
f.write('frequency average: {} - {}'.format(unit, statistics.mean(f_avg)))
f.write('\n')
f.write('mass flow average: {} - {}'.format(unit, statistics.mean(m_dot)))
f.write('\n')
# f.write('Evaporator capacity average: {} - {}'.format(unit, statistics.mean(E_normal)))
# f.write('\n')
f.write('Condenser capacity average: {} - {}'.format(unit, statistics.mean(Q_normal)))
f.write('\n')
f.write('Meter power consumption average: {} - {}'.format(unit, statistics.mean(w_measure)/1000))
f.write('\n')
f.write('Meter power consumption sum: {} - {}'.format(unit, sum(w_measure)/1000))
f.write('\n')
f.write('Predict power consumption average: {} - {}'.format(unit, statistics.mean(w_dot)/1000))
f.write('\n')
f.write('Predict power consumption sum: {} - {}'.format(unit, sum(w_dot)/1000))
f.write('\n')
# f.write('COP average: {} - {}'.format(unit, statistics.mean(COP_actual)))
# f.write('\n')
# f.write('CV_RMSE: {} - {} %'.format(unit, Cv_rmse(w_measure,w_dot)))
# f.write('\n')
# f.write('fault level: {} - {} %'.format(unit, statistics.mean(k_p)))
# f.write('\n')
f.close()
#
print('Outdoor unit: {}, Day: {} End'.format(unit,date))
print('CV_RMSE: {} - {} %'.format(unit, Cv_rmse(w_measure.rolling(5).mean().fillna(method='bfill'), w_dot)))

# f_w_3065 = pd.DataFrame(np.column_stack([suc_density_3065,f_3065,w_dot_3065,w_measure_3065]),columns=['suc_density','f_avg','w_dot','w_measure']).to_csv('./3065.csv')
# f_w_3066 = pd.DataFrame(np.column_stack([suc_density_3066,f_3066,w_dot_3066,w_measure_3066]),columns=['suc_density','f_avg','w_dot','w_measure']).to_csv('./3066.csv')
# f_w_3067 = pd.DataFrame(np.column_stack([suc_density_3067,f_3067,w_dot_3067,w_measure_3067]),columns=['suc_density','f_avg','w_dot','w_measure']).to_csv('./3067.csv')
# f_w_3069 = pd.DataFrame(np.column_stack([suc_density_3069,f_3069,w_dot_3069,w_measure_3069]),columns=['suc_density','f_avg','w_dot','w_measure']).to_csv('./3069.csv')