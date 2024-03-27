import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
import CoolProp as CP


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


unit = '3067'
today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]
normal = '0930'
date = '0930'
directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\2021-11-17'.format(folder_name)
model = 'GB066_{}'.format(unit)

data = {'3065': ['0810','0811'],
        '3066': ['0728','0729','0730','0804','0805','0810','0811'],
        '3067': ['0813']}

dir = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Performance degradation'

for unit, date_list in data.items():
    for date in date_list:
        save_dir = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Performance degradation\capacity\{}'.format(date)
        create_folder(save_dir)

        data1 = pd.read_csv(dir+'\comp_map\{}\{}\GB066_{}_{}.csv'.format(date,'freq1',date,unit))
        data2 = pd.read_csv(dir+'\comp_map\{}\{}\GB066_{}_{}.csv'.format(date,'freq2',date,unit))

        normal_raw = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Performance degradation\raw\{}\outdoor_{}.csv'.format(date,unit))

        time1 = data1['Time']
        f1 = data1['frequency']
        T_c1 = data1['Condensing Temp']
        T_e1 = data1['Evaporating Temp']
        f_rated1 = data1['frequency rated']
        m_dot_rated1 = data1['m_dot_rated']
        w_dot_rated1 = data1['w_dot_rated']
        m_dot_pred1 = data1['m_dot_pred']
        w_dot_pred1 = data1['w_dot_pred']

        time2 = data2['Time']
        f2 = data2['frequency']
        T_c2 = data2['Condensing Temp']
        T_e2 = data2['Evaporating Temp']
        f_rated2 = data2['frequency rated']
        m_dot_rated2 = data2['m_dot_rated']
        w_dot_rated2 = data2['w_dot_rated']
        m_dot_pred2 = data2['m_dot_pred']
        w_dot_pred2 = data2['w_dot_pred']

        w_dot =[]
        m_dot =[]
        f_avg = []
        for i in range(len(data1)):
            w_dot.append((w_dot_pred1[i]+w_dot_pred2[i])*2)
            m_dot.append(m_dot_pred1[i] + m_dot_pred2[i])
            f_avg.append((f1[i]+f2[i])/2)

        columns = ['power_{}_pred'.format(date[2:])]
        pd.DataFrame(w_dot,columns=columns).to_csv(save_dir+'\power_{}_pred.csv'.format(normal[2:]))


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
                delta_h.append(abs((h_dis-h_cond)/1000))
            data['Qcond'] = pd.DataFrame(delta_h)*pd.DataFrame(mdot)
            return data['Qcond']


        def Qevap(data,mdot):
            delta_h = []
            suc_t1 = data['suction_temp1']
            cond_o_t = data['double_tube_temp']
            low_p = data['low_pressure']
            for i in range(len(data)):
                h_suc = CP.CoolProp.PropsSI('H', 'P', low_p[i]*98.0665*1000, 'T', suc_t1[i]+273.15, 'R410A')
                h_evap = CP.CoolProp.PropsSI('H','P',low_p[i]*98.0665*1000,'T',cond_o_t[i]+273.15,'R410A')
                delta_h.append(abs((h_evap-h_suc)/1000))
            data['Qevap'] = pd.DataFrame(delta_h)*pd.DataFrame(mdot)
            return data['Qevap']


        Q_normal = Qcond(normal_raw,m_dot)
        E_normal = Qevap(normal_raw,m_dot)
        time = pd.DataFrame(time1)

        pd.DataFrame(pd.concat([time,Q_normal,E_normal],axis=1)).to_csv(save_dir+'\Q_{}.csv'.format(unit))