import pandas as pd
import os
import CoolProp as CP

path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2021-12-08/'
datalist = {'3065': ['0830'],
            '3066': ['0830'],
            '3067': ['0830'],
            '3069': ['0830']}


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


def T_vapor(P_dis, P_suc, ref):
    T_c = []
    T_e = []
    for i in range(len(P_dis)):
        T_c.append(CP.CoolProp.PropsSI('T', 'P', P_dis[i] * 98.0665 * 1000, 'Q', 1, ref) - 273)
        T_e.append(CP.CoolProp.PropsSI('T', 'P', P_suc[i] * 98.0665 * 1000, 'Q', 1, ref) - 273)
    T_c = pd.DataFrame(T_c,columns=['Condenser saturation'])
    T_e = pd.DataFrame(T_e, columns=['Evaporator saturation'])
    return T_c, T_e


def T_liquid(P_dis, P_suc, ref):
    T_c = []
    T_e = []
    for i in range(len(P_dis)):
        T_c.append(CP.CoolProp.PropsSI('T', 'P', P_dis[i] * 98.0665 * 1000, 'Q', 0, ref) - 273)
        T_e.append(CP.CoolProp.PropsSI('T', 'P', P_suc[i] * 98.0665 * 1000, 'Q', 0, ref) - 273)
    T_c = pd.DataFrame(T_c, columns=['Condenser saturation'])
    T_e = pd.DataFrame(T_e, columns=['Evaporator saturation'])
    return T_c, T_e


def plot(path, datelist):
    # col = []
    for date in datelist:
        testlist = os.listdir(path + date)
        evap_out_list = []
        evap_in_list = []
        evap_out_avg = 0
        evap_in_avg = 0
        df_plot = pd.DataFrame()
        df_temp = pd.DataFrame()
        df_outdoor = pd.DataFrame()
        # for test in testlist:
        #     dic = path + date + '/' + test
        dic = path + date + '/'
        for i in os.listdir(dic):
            if 'indoor' in i:
                indoor_evap_out = pd.read_csv(dic + '/' + i)['evaout_temp']
                indoor_evap_in = pd.read_csv(dic + '/' + i)['evain_temp']
                evap_out_list.append(indoor_evap_out)
                evap_in_list.append(indoor_evap_in)
            elif 'outdoor' in i:
                try:
                    df_outdoor = pd.read_csv(dic + '/' + i, index_col=0).reset_index()
                except:
                    df_outdoor = pd.read_csv(dic + '/' + i, index_col=0)
                # df_outdoor = df_outdoor.drop(len(df_outdoor)-1,axis=0)
        for j in range(len(evap_out_list)):
            evap_out_avg += evap_out_list[j]
            evap_in_avg += evap_in_list[j]
        df_plot['cond_out_temp1'] = df_outdoor['cond_out_temp1']
        df_plot['suction_temp1'] = df_outdoor['suction_temp1']
        df_plot['discharge_temp1'] = df_outdoor['discharge_temp1']
        df_plot['discharge_temp2'] = df_outdoor['discharge_temp2']
        df_plot['high_pressure'] = df_outdoor['high_pressure']
        df_plot['low_pressure'] = df_outdoor['low_pressure']
        df_plot['double_tube_temp'] = df_outdoor['double_tube_temp']
        if unit == '3065':
            df_plot['discharge_temp'] = df_plot['discharge_temp1']
        else:
            df_plot['discharge_temp'] = (df_plot['discharge_temp1'] + df_plot['discharge_temp2']) / 2
        df_plot['T_c_vapor'], df_plot['T_e_vapor'] = T_vapor(df_plot['high_pressure'],df_plot['low_pressure'],'R410A')
        df_plot['T_c_liquid'], df_plot['T_e_liquid'] = T_liquid(df_plot['high_pressure'], df_plot['low_pressure'], 'R410A')
        df_plot['evap_out_avg'] = evap_out_avg / len(evap_out_list)
        df_plot['evap_in_avg'] = evap_in_avg / len(evap_in_list)
        df_temp['SC_cond_out'] = df_plot['cond_out_temp1'] - df_plot['T_c_liquid']
        df_temp['SC_double'] = df_plot['double_tube_temp'] - df_plot['T_c_liquid']
        df_temp['SH_evapout'] = df_plot['evap_out_avg'] - df_plot['T_e_vapor']
        df_temp['SH_suction'] = df_plot['suction_temp1'] - df_plot['T_e_vapor']
        df_temp['SH_evap'] = df_plot['evap_out_avg'] - df_plot['evap_in_avg']
        df_temp['DSH'] = df_plot['discharge_temp'] - df_plot['T_c_vapor']

        df_outdoor = pd.concat([df_outdoor,df_temp],axis=1).to_csv(dic + '/temperature.csv')


for unit, day in datalist.items():
    print(unit,day)
    plot(path+unit+'/',day)
