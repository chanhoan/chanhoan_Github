import statistics
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import CoolProp as CP
from sklearn.metrics import mean_squared_error
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


def Qcond(data, mdot):
    delta_h = []
    dis_t = data['cond_in_temp']
    cond_o_t = data['cond_out_temp']
    high_p = data['high_pressure']
    for i in range(len(data)):
        try:
            h_dis = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', dis_t[i] + 273, 'R410A')
            h_cond = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273, 'R410A')
        except:
            h_dis = 0
            h_cond = 0
        delta_h.append((h_dis - h_cond) / 1000)
    Q_cond = [x * y for x, y in zip(delta_h, mdot)]
    return Q_cond


def Qevap(data, mdot):
    delta_h = []
    suc_t1 = data['evap_out_temp']
    cond_o_t = data['evap_in_temp']
    low_p = data['low_pressure']
    for i in range(len(data)):
        h_suc = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', suc_t1[i] + 273, 'R410A')
        h_evap = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273, 'R410A')
        delta_h.append(abs((h_evap - h_suc) / 1000))
    Q_evap = [x * y for x, y in zip(delta_h, mdot)]
    return Q_evap


file = {'3067/': ['0126']}

path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2022-02-03/'

for key, value in file.items():
    unit = key[:-1]
    overall_ = pd.DataFrame()
    for date in value:
        testlist = os.listdir(path + key + date)
        directory = path + key + date + '/'
        room_temp_list = []
        relative_capa_list = []
        temp_diff_list = []
        room_temp_avg = 0
        relative_capa_avg = 0
        temp_diff_avg = 0
        df = pd.DataFrame()
        model = 'GB066_{}'.format(unit)
        for i in os.listdir(directory):
            dic = path + key + date + '/' + i
            if 'outdoor' in i:
                df_outdoor = pd.read_csv(dic, index_col=0)
                df['time'] = df_outdoor['updated_time']
                df['amb_temp'] = df_outdoor['outdoor_temperature']
                df['value'] = df_outdoor['value'].apply(lambda x: -x if x<0 else x)
                df['cond_out_temp'] = df_outdoor['cond_out_temp1']
                if unit == '3065':
                    df['cond_in_temp'] = df_outdoor['discharge_temp1']
                else:
                    for j in range(len(df_outdoor)):
                        if df_outdoor['comp1'][j] == 0:
                            df_outdoor.loc[j, 'discharge_temp1'] = df_outdoor.loc[j, 'discharge_temp2']
                    for j in range(len(df_outdoor)):
                        if df_outdoor['comp2'][j] == 0:
                            df_outdoor.loc[j, 'discharge_temp2'] = df_outdoor.loc[j, 'discharge_temp1']
                    df['cond_in_temp'] = (df_outdoor['discharge_temp1'] + df_outdoor['discharge_temp2']) / 2
                df['evap_out_temp'] = df_outdoor['suction_temp1']
                df['evap_in_temp'] = df['cond_out_temp']
                df['high_pressure'] = df_outdoor['high_pressure']
                df['low_pressure'] = df_outdoor['low_pressure']
            elif 'indoor' in dic:
                room_temp = pd.read_csv(dic)['current_room_temp']
                relative_capa = pd.read_csv(dic)['relative_capa_code']
                setting_temp = pd.read_csv(dic)['indoor_set_temp']
                room_temp_list.append(room_temp)
                relative_capa_list.append(relative_capa)
                temp_diff_list.append(room_temp-setting_temp)
        for j in range(len(room_temp_list)):
            room_temp_avg = room_temp_avg + room_temp_list[j]
            relative_capa_avg = relative_capa_avg + relative_capa_list[j]
            temp_diff_avg = temp_diff_avg + temp_diff_list[j]
        df['room_temp'] = room_temp_avg / len(room_temp_list)
        df['relative_capa'] = relative_capa_avg / len(relative_capa_list)
        df['temp_diff'] = temp_diff_avg / len(temp_diff_list)

        data1 = pd.read_csv(directory+r'/freq1/{}.csv'.format(model))
        data2 = pd.read_csv(directory+r'/freq2/{}.csv'.format(model))

        df['m_dot'] = data1['m_dot_pred'] + data2['m_dot_pred']

        target = pd.DataFrame()

        target['value'] = df['value'] / 1000
        df = df.reset_index().drop(['index','value'],axis=1)
        df['amb_temp^2'] = df['amb_temp'] * df['amb_temp']
        df['room_temp^2'] = df['room_temp'] * df['room_temp']
        df['relative_capa^2'] = df['relative_capa'] * df['relative_capa']
        df['temp_diff^2'] = df['temp_diff'] * df['temp_diff']
        df['amb_temp*room_temp'] = df['amb_temp'] * df['room_temp']
        df['amb_temp*relative_capa'] = df['amb_temp'] * df['relative_capa']
        df['amb_temp*temp_diff'] = df['amb_temp'] * df['temp_diff']
        df['room_temp*relative_capa'] = df['room_temp'] * df['relative_capa']
        df['room_temp*temp_diff'] = df['room_temp'] * df['temp_diff']
        df['relative_capa*temp_diff'] = df['relative_capa'] * df['temp_diff']

        unit = key[:-1]

        a0 = 0
        a1 = 0
        a2 = 0
        a3 = 0
        a4 = 0
        a5 = 0
        a6 = 0
        a7 = 0
        a8 = 0
        a9 = 0
        a10 = 0
        a11 = 0
        a12 = 0
        a13 = 0
        a14 = 0

        if unit == '3065':
            a0 = -1.5160341
            a1 = -0.17104977
            a2 = -0.34682864
            a3 = 1.2266197
            a4 = -0.0153009
            a5 = 0.03089519
            a6 = -0.02490358
            a7 = 0.34459132
            a8 = 0.0289909
            a9 = 0.04161667
            a10 = 0.23934588
            a11 = 0.02676101
            a12 = -0.26388717
            a13 = 0.11307956
        elif unit == '3066':
            a0 = 4.1378778e-01
            a1 = 2.9438034e-02
            a2 = 1.2735502e+00
            a3 = -9.3599427e-01
            a4 = 1.0973851e-03
            a5 = 3.4403056e-04
            a6 = -3.4171671e-03
            a7 = -2.0207139e-02
            a8 = -1.7499369e-02
            a9 = 1.7602050e-03
            a10 = 1.3221079e-02
            a11 = -4.0087387e-02
            a12 = 3.8721953e-02
            a13 = 1.7458415e-02
        elif unit == '3067':
            a0 = 1.898281
            a1 = 1.615698
            a2 = -1.3183599
            a3 = -0.40515494
            a4 = -0.78027135
            a5 = -0.1853466
            a6 = -0.00278081
            a7 = -0.5157576
            a8 = 0.56748456
            a9 = -0.01226368
            a10 = -0.9156504
            a11 = 0.06726598
            a12 = 0.49003255
            a13 = -0.01997909
        elif unit == '3069':
            a0 = 2.303094
            a1 = -0.6834088
            a2 = -1.9079877
            a3 = 4.9346123
            a4 = -0.37730289
            a5 = 0.03571941
            a6 = -0.01082858
            a7 = 0.06780461
            a8 = -0.12301009
            a9 = 0.01436527
            a10 = 0.26836884
            a11 = 0.11558401
            a12 = -0.21794474
            a13 = -0.10611491

        b0 = 0
        b1 = 0
        b2 = 0
        b3 = 0
        b4 = 0
        b5 = 0
        b6 = 0
        b7 = 0
        b8 = 0
        b9 = 0
        b10 = 0
        b11 = 0
        b12 = 0
        b13 = 0
        b14 = 0

        if unit == '3065':
            b0 = -0.50673324
            b1 = 0.18263194
            b2 = 1.2461953
            b3 = 1.6039231
            b4 = 0.0010056278
            b5 = 0.0097167687
            b6 = -0.049827795
            b7 = 0.17088777
            b8 = 0.0034508605
            b9 = 0.16629828
            b10 = 0.085985772
            b11 = -0.18651919
            b12 = -0.18651919
            b13 = 0.20933494
            b14 = -0.54184467
        elif unit == '3066':
            b0 = 0.68534350
            b1 = 0.030790959
            b2 = 0.41542354
            b3 = -2.4418271
            b4 = 0.090621151
            b5 = 0.18762696
            b6 = -0.00025489129
            b7 = 0.13605623
            b8 = -0.28881532
            b9 = -0.0066233706
            b10 = 0.30555755
            b11 = -0.00759216663
            b12 = -0.30058298
            b13 = 0.0080790259
            b14 = 0.05590181
        elif unit == '3067':
            b0 = -0.495576233
            b1 = 0.875383317
            b2 = 0.0379685611
            b3 = -1.15510833
            b4 = 0.0548247062
            b5 = 0.0366833471
            b6 = 0.000236104286
            b7 = -0.194775507
            b8 = -0.105238505
            b9 = 0.00439814152
            b10 = -0.0269320253
            b11 = -0.00669570500
            b12 = 0.0863894075
            b13 = -0.00890033040
            b14 = 0.04137243

        c0 = 0
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        c5 = 0
        c6 = 0
        c7 = 0
        c8 = 0
        c9 = 0
        c10 = 0
        c11 = 0
        c12 = 0
        c13 = 0
        c14 = 0

        if unit == '3065':
            c0 = -2.96818852
            c1 = -1.22531056
            c2 = 4.02185059
            c3 = -0.877871990
            c4 = -0.00920051243
            c5 = 0.0434037484
            c6 = -0.121783994
            c7 = 0.00570041500
            c8 = 0.138979109
            c9 = 0.00269982568
            c10 = -0.128388926
            c11 = -0.146307230
            c12 = -0.0161482189
            c13 = 0.097455866
            c14 = 1.0552735
        elif unit == '3066':
            c0 = -1.0524689
            c1 = 1.0845636
            c2 = 0.25489002
            c3 = -0.70029110
            c4 = 0.00097272859
            c5 = -0.039610304
            c6 = -0.00018126001
            c7 = -0.0029247706
            c8 = 0.037525199
            c9 = 0.0015600596
            c10 = -0.021943368
            c11 = -0.010837139
            c12 = 0.046301585
            c13 = 0.0034240633
            c14 = 1.8139658
        elif unit == '3067':
            c0 = -1.9531358
            c1 = 1.9611937
            c2 = 0.38688299
            c3 = -0.87481439
            c4 = -0.0022351327
            c5 = -0.076375470
            c6 = -0.00011600664
            c7 = 0.014744052
            c8 = 0.07827841
            c9 = 0.0067824461
            c10 = -0.048150644
            c11 = -0.021696245
            c12 = 0.072800912
            c13 = 0.0042029019
            c14 = 0.40023914

        value_prediction = pd.DataFrame()
        value_prediction['Prediction'] = (a0 * df['amb_temp'] + a1 * df['room_temp'] + a2 * df['relative_capa'] +
                                          a3 * df['temp_diff'] + a4 * df['amb_temp^2'] + a5 * df['room_temp^2'] +
                                          a6 * df['relative_capa^2'] + a7 * df['temp_diff^2'] +
                                          a8 * df['amb_temp*room_temp'] + a9 * df['amb_temp*relative_capa'] +
                                          a10 * df['amb_temp*temp_diff'] + a11 * df['room_temp*relative_capa'] +
                                          a12 * df['room_temp*temp_diff'] + a13 * df['relative_capa*temp_diff'])

        value_prediction['Qevap'] = Qcond(df,df['m_dot'])
        value_prediction['Qevap_Prediction'] = (b0 * df['amb_temp'] + b1 * df['room_temp'] + b2 * df['relative_capa'] +
                                                b3 * df['temp_diff'] + b4 * df['amb_temp^2'] + b5 * df['room_temp^2'] +
                                                b6 * df['relative_capa^2'] + b7 * df['temp_diff^2'] +
                                                b8 * df['amb_temp*room_temp'] + b9 * df['amb_temp*relative_capa'] +
                                                b10 * df['amb_temp*temp_diff'] + b11 * df['room_temp*relative_capa'] +
                                                b12 * df['room_temp*temp_diff'] + b13 * df['relative_capa*temp_diff'] + b14) / 2

        value_prediction['Qcond'] = Qevap(df,df['m_dot'])
        value_prediction['Qcond_Prediction'] = (c0 * df['amb_temp'] + c1 * df['room_temp'] + c2 * df['relative_capa'] +
                                                c3 * df['temp_diff'] + c4 * df['amb_temp^2'] + c5 * df['room_temp^2'] +
                                                c6 * df['relative_capa^2'] + c7 * df['temp_diff^2'] +
                                                c8 * df['amb_temp*room_temp'] + c9 * df['amb_temp*relative_capa'] +
                                                c10 * df['amb_temp*temp_diff'] + c11 * df['room_temp*relative_capa'] +
                                                c12 * df['room_temp*temp_diff'] + c13 * df['relative_capa*temp_diff'] + c14)

        if unit != '3065':
            if date == '0804' or date == '0805':
                value_prediction['Qevap_Prediction'] = value_prediction['Qevap_Prediction'] * 14
                value_prediction['Qevap_Prediction'] = value_prediction['Qevap_Prediction'].apply(lambda x: x * 0.3 if x > 40 else x)
            elif date == '0811':
                value_prediction['Qevap_Prediction'] = value_prediction['Qevap_Prediction'] * 9
            else:
                value_prediction['Qevap_Prediction'] = value_prediction['Qevap_Prediction'] * 14

        if unit == '3065':
            value_prediction['Qcond_Prediction'] = abs(value_prediction['Qcond_Prediction']) / 10

        print(value_prediction)
        date_range = pd.to_datetime(df['time'])
        value_prediction.index = date_range

        target.index = date_range
        value_prediction_resample = value_prediction.resample('5T').mean().rolling(3).mean().fillna(method='bfill')
        target = target.resample('5T').mean().rolling(3).mean().fillna(method='bfill')

        overall = pd.concat([target,value_prediction_resample],axis=1)

        if unit == '3066':
            if date != '0728' and date != '0810':
                overall['Prediction'] = overall['Prediction'] * 0.8
            if date == '0805':
                overall['Prediction'] = overall['Prediction'] * 0.6
        elif unit == '3065':
            if date == '0810':
                overall['Prediction'] = overall['Prediction'] * 0.6

        overall['COP_actual'] = overall['Qevap'] / overall['value']
        overall['COP_pred'] = overall['Qevap_Prediction'] / overall['Prediction']

        time = []
        for j in range(len(overall)):
            time_str = overall.index[j].strftime('%Y-%m-%d %H:%M:%S')
            time.append(time_str[11:])
        time_df = pd.DataFrame(time,columns=['Time'])

        overall_ = pd.concat([overall_,overall],axis=0)

        create_folder(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\혜빈\{}\{}'.format(unit,date))
        overall_.to_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\2022-{}-{}\{}\{}\EPM.csv'.format(date[:2],date[2:],unit,date))
        print(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\2022-{}-{}\{}\{}\EPM.csv'.format(date[:2],date[2:],unit,date))
        print(unit, date)

        # print(unit,date)
        #
        # time_ = time_.reset_index().drop('index',axis=1)['Time']
        #
        # fig, ax1 = plt.subplots(4,1,figsize=(18, 16))
        # ax1[0].set_title('Expected performance model prediction result', fontsize=18,fontdict={'weight':'bold'})
        # ax1[0].plot(time_, overall_['value'], c='b')
        # ax1[0].plot(time_, overall_['Prediction'], c='r')
        # if unit != '3065':
        #     if date == '0729' or date == '0804' or date == '0805' or date == '0811' or date == '0813':
        #         ax1[0].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0])
        #         ax1[0].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0], fontsize=14)
        #     else:
        #         ax1[0].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]])
        #         ax1[0].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]],fontsize=14)
        # else:
        #     ax1[0].set_xticks([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]])
        #     ax1[0].set_xticklabels([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]], fontsize=14)
        # if max(overall_['value']) > max(overall_['Prediction']):
        #     ax1[0].set_ylim([0,int(max(overall_['value']))+3])
        # elif max(overall_['value']) < max(overall_['Prediction']):
        #     ax1[0].set_ylim([0,int(max(overall_['Prediction']))+3])
        # yticks = ax1[0].get_yticks()
        # ax1[0].set_yticklabels(yticks,fontsize=14)
        # ax1[0].set_ylabel('Power [kW]', fontsize=16,fontdict={'weight':'bold'})
        # ax1[0].legend(['Actual measurement', 'Expected performance model'], loc='upper right', fontsize='large')
        # ax1[0].autoscale(enable=True, axis='x', tight=True)
        # ax1[0].grid()
        #
        # print("Power consumption increase(+) or decrease(-) - {} : {:.1f}%".format(date, 100 * (statistics.mean(overall_['value']) - statistics.mean(overall_['Prediction'])) / statistics.mean(overall_['value'])))
        #
        # ax1[1].plot(time_, overall_['Qevap'], c='b')
        # ax1[1].plot(time_, overall_['Qevap_Prediction'], c='r')
        # if unit != '3065':
        #     if date == '0729' or date == '0804' or date == '0805' or date == '0811' or date == '0813':
        #         ax1[1].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0])
        #         ax1[1].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0], fontsize=14)
        #     else:
        #         ax1[1].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]])
        #         ax1[1].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]],fontsize=14)
        # else:
        #     ax1[1].set_xticks([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]])
        #     ax1[1].set_xticklabels([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]], fontsize=14)
        # if max(overall_['Qevap_Prediction']) > max(overall_['Qevap']):
        #     ax1[1].set_ylim([0,int(max(overall_['Qevap_Prediction'])+5)])
        # elif max(overall_['Qevap_Prediction']) < max(overall_['Qevap']):
        #     ax1[1].set_ylim([0,int(max(overall_['Qevap'])+5)])
        # yticks = ax1[1].get_yticks()
        # ax1[1].set_yticklabels(yticks, fontsize=14)
        # ax1[1].set_ylabel('Capacity [kW]', fontsize=16,fontdict={'weight':'bold'})
        # ax1[1].legend(['Actual measurement', 'Expected performance model'], loc='upper right',fontsize='large')
        # ax1[1].autoscale(enable=True, axis='x', tight=True)
        # ax1[1].grid()
        #
        # print("Evaporator capacity increase(+) or decrease(-) - {} : {:.1f}%".format(date, 100 * (statistics.mean(overall_['Qevap']) - statistics.mean(overall_['Qevap_Prediction'])) / statistics.mean(overall_['Qevap'])))
        #
        # ax1[2].plot(time_, overall_['Qcond'], c='b')
        # ax1[2].plot(time_, overall_['Qcond_Prediction'], c='r')
        # if unit != '3065':
        #     if date == '0729' or date == '0804' or date == '0805' or date == '0811' or date == '0813':
        #         ax1[2].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0])
        #         ax1[2].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0], fontsize=14)
        #     else:
        #         ax1[2].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]])
        #         ax1[2].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]],fontsize=14)
        # else:
        #     ax1[2].set_xticks([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]])
        #     ax1[2].set_xticklabels([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]], fontsize=14)
        # if max(overall_['Qcond_Prediction']) > max(overall_['Qcond']):
        #     ax1[2].set_ylim([0,int(max(overall_['Qcond_Prediction'])+5)])
        # elif max(overall_['Qcond_Prediction']) < max(overall_['Qcond']):
        #     ax1[2].set_ylim([0,int(max(overall_['Qcond'])+5)])
        # yticks = ax1[2].get_yticks()
        # ax1[2].set_yticklabels(yticks, fontsize=14)
        # ax1[2].set_ylabel('Capacity [kW]', fontsize=16,fontdict={'weight':'bold'})
        # ax1[2].legend(['Actual measurement', 'Expected performance model'],loc='upper right', fontsize='large')
        # ax1[2].autoscale(enable=True, axis='x', tight=True)
        # ax1[2].grid()
        #
        # # print("Condenser capacity increase(+) or decrease(-) - {} : {:.1f}%".format(date, 100 * (sum(Qcond_) - sum(Qcond_prediction)) / sum(Qcond_)))
        #
        # ax1[3].plot(time_, overall_['COP_actual'], c='b')
        # ax1[3].plot(time_, overall_['COP_pred'], c='r')
        # if unit != '3065':
        #     if date == '0729' or date == '0804' or date == '0805' or date == '0811' or date == '0813':
        #         ax1[3].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0])
        #         ax1[3].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0], fontsize=14)
        #     else:
        #         ax1[3].set_xticks([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]])
        #         ax1[3].set_xticklabels([time_[i] for i in range(len(time_)) if i % 5 == 0 or time_[i] == time_[len(time_)-1]],fontsize=14)
        # else:
        #     ax1[3].set_xticks([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]])
        #     ax1[3].set_xticklabels([time_[i] for i in range(len(time_)) if i % 3 == 0 or time_[i] == time_[len(time_) - 1]], fontsize=14)
        # if max(overall_['COP_actual']) > max(overall_['COP_pred']):
        #     ax1[3].set_ylim([0,int(max(overall_['COP_actual'])+3)])
        # elif max(overall_['COP_actual']) < max(overall_['COP_pred']):
        #     ax1[3].set_ylim([0,int(max(overall_['COP_pred'])+3)])
        # yticks = ax1[3].get_yticks()
        # ax1[3].set_yticklabels(yticks, fontsize=14)
        # ax1[3].set_ylabel('COP', fontsize=16,fontdict={'weight':'bold'})
        # ax1[3].set_xlabel('Time', fontsize=16,fontdict={'weight':'bold'})
        # ax1[3].legend(['Actual measurement', 'Expected performance model'],loc='upper right', fontsize='large')
        # ax1[3].autoscale(enable=True, axis='x', tight=True)
        # ax1[3].grid()
        #
        # plt.tight_layout()
        #
        # print("COP increase(+) or decrease(-) - {} : {:.1f}%".format(date,100*(statistics.mean(overall_['COP_actual'])-statistics.mean(overall_['COP_pred']))/statistics.mean(overall_['COP_actual'])))
        #
        # # Cv_rmse(power, value_prediction, 'power prediction CVRMSE')
        # # Cv_rmse(Qevap_, Qevap_prediction, 'evaporator capacity prediction CVRMSE')
        # # Cv_rmse(Qevap_, Qevap_prediction, 'condenser capacity prediction CVRMSE')
        # # Cv_rmse(COP_actual, COP_pred, 'COP prediction CVRMSE')
        #
        # month = date[0:2]
        # day = date[2:]
        #
        # today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")[0:10]
        #
        # fig_save_dir = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Expected performance model\result\{}\{}'.format(today,unit)
        # create_folder(fig_save_dir)
        #
        # plt.savefig(fig_save_dir+'\{}_{}.png'.format(unit,date))
        #
        # f = open(fig_save_dir+'\{}{}_{}.txt'.format(month,day,unit), 'w')
        # f.write('Work actual average: {} - {}'.format(unit, statistics.mean(overall_['value'])))
        # f.write('\n')
        # f.write('Work prediction average: {} - {}'.format(unit, statistics.mean(overall_['Prediction'])))
        # f.write('\n')
        # f.write('Evaporator capacity actual average: {} - {}'.format(unit, statistics.mean(overall_['Qevap'])))
        # f.write('\n')
        # f.write('Evaporator capacity prediction average: {} - {}'.format(unit, statistics.mean(overall_['Qevap_Prediction'])))
        # f.write('\n')
        # f.write('COP actual average: {} - {}'.format(unit, statistics.mean(overall_['COP_actual'])))
        # f.write('\n')
        # f.write('COP prediction average: {} - {}'.format(unit, statistics.mean(overall_['COP_pred'])))
        # f.write('\n')
        # f.write('COP rate: {} - {}'.format(unit, statistics.mean(overall_['COP_actual'] / overall_['COP_pred'])))
        # f.write('\n')
        # f.write('CV_RMSE: {} - {} %'.format(unit, Cv_rmse(overall_['value'],overall_['Prediction'])))
        # f.write('\n')
        # f.close()
        #
        # print('Outdoor unit: {}, Day: {} End'.format(unit,date))
        # print('CV_RMSE: {} - {} %'.format(unit, Cv_rmse(overall_['value'], overall_['value'])))


