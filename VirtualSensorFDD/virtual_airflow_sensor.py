from scipy.stats import norm
import CoolProp as CP
import pandas as pd
import os
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import statistics


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


def solve(m1, m2, std1, std2):
    aa = 1 / (2 * std1 ** 2) - 1 / (2 * std2 ** 2)
    b = m2 / (std2 ** 2) - m1 / (std1 ** 2)
    cc = m1 ** 2 / (2 * std1 ** 2) - m2 ** 2 / (2 * std2 ** 2) - np.log(std2 / std1)
    return np.roots([aa, b, cc])


path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2022-01-19/'
save_path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_airflow_sensor/'
datalist = {'3069': ['0117','0118','0119_1','0119_2'],}

c_p = 1.005
air_specific_volume = 1/1.225

def airflow_sensor(path,unit,datelist):
    for date in datelist:
        data_ = pd.DataFrame()
        cond_in_h = []
        cond_out_h = []
        data = pd.DataFrame()
        dic = path + unit + '/' + date
        for i in os.listdir(dic):
            if 'outdoor' in i:
                df_outdoor = pd.read_csv(dic + '/' + i)
                data['Time'] = df_outdoor['updated_time']
                data['comp1'] = df_outdoor['comp1']
                data['comp2'] = df_outdoor['comp2']
                data['discharge_temp1'] = df_outdoor['discharge_temp1']
                data['discharge_temp2'] = df_outdoor['discharge_temp2']
                data['freq1'] = df_outdoor['comp_current_frequency1']
                data['freq2'] = df_outdoor['comp_current_frequency2']
                data['freq_avg'] = (data['freq1'] + data['freq2']) / 2
                data['fan_step'] = df_outdoor['fan_step']
                if unit != '3065':
                    for j in range(len(data)):
                        if data['comp1'][j] == 0:
                            data.loc[j,'discharge_temp1'] = data.loc[j,'discharge_temp2']
                    for j in range(len(data)):
                        if data['comp2'][j] == 0:
                            data.loc[j,'discharge_temp2'] = data.loc[j,'discharge_temp1']

                    data['cond_in_ref'] = (data['discharge_temp1'] + data['discharge_temp2']) / 2
                else:
                    data['cond_in_ref'] = data['discharge_temp1']

                data['cond_out_ref'] = df_outdoor['cond_out_temp1']

                data['high_pressure'] = df_outdoor['high_pressure']

                data['cond_in_air'] = df_outdoor.filter(regex='point').min(axis=1)

                data['cond_out_air'] = df_outdoor.filter(regex='condout').max(axis=1)

        m_dot_freq1 = pd.read_csv(dic+'/freq1/GB066_{}.csv'.format(unit))['m_dot_pred']
        m_dot_freq2 = pd.read_csv(dic + '/freq2/GB066_{}.csv'.format(unit))['m_dot_pred']
        data['m_dot_ref'] = m_dot_freq1 + m_dot_freq2

        data = data.dropna(axis=0)
        for j in range(len(data)):
            try:
                cond_in_h.append(CP.CoolProp.PropsSI('H','P',data['high_pressure'][j]*98.0665*1000,'T',data['cond_in_ref'][j]+273,'R410A')/1000)
            except:
                cond_in_h.append(None)
        for j in range(len(data)):
            try:
                cond_out_h.append(CP.CoolProp.PropsSI('H','P',data['high_pressure'][j]*98.0665*1000,'T',data['cond_out_ref'][j]+273,'R410A')/1000)
            except:
                cond_out_h.append(None)

        data['cond_in_h'] = cond_in_h
        data['cond_out_h'] = cond_out_h
        data['m_dot_air'] = air_specific_volume*(data['m_dot_ref']*(data['cond_in_h']-data['cond_out_h'])) / (c_p * (data['cond_out_air']-data['cond_in_air']))

        data_ = pd.concat([data_,data],axis=0)
    print(data_)
    # data_['m_dot_air'] = data_['m_dot_air'].apply(lambda x: None if x < 0 else x)
    # data_['m_dot_air'] = data_['m_dot_air'].apply(lambda x: None if x > 100 else x)
    data_ = data_.dropna(axis=0).reset_index()
    create_folder(save_path+unit+'/'+date)
    data_.to_csv(save_path+unit+'/'+date+'/'+'/virtual_airflow_sensor.csv')

def plot(path,datelist):
    result_list = {}
    time = []
    max_list = []
    for date in datelist:
        result_list[date] = pd.read_csv(path+'/'+date+'/virtual_airflow_sensor.csv').reset_index().drop('index',axis=1)
        print(result_list)
        if date == '0810' and unit == '3066':
            result_list[date]['m_dot_air'] = result_list[date]['m_dot_air'].rolling(15).mean() +1
        elif date == '0813' and unit == '3067':
            result_list[date]['m_dot_air'] = result_list[date]['m_dot_air'].rolling(15).mean() -0.3
        else:
            result_list[date]['m_dot_air'] = result_list[date]['m_dot_air'].rolling(15).mean()
        result_list[date] = result_list[date].dropna(axis=0).reset_index()
        result_list[date]['Time'] = [dt.datetime.strptime(result_list[date]['Time'][i],'%Y-%m-%d %H:%M') for i in range(len(result_list[date]))]
        max_list.append(len(result_list[date]))

    max_len = max(max_list)

    first_time = dt.datetime.strptime("00:00","%H:%M")
    for j in range(max_len):
        time.append(first_time)
        time[j] = time[j].strftime("%H:%M")
        first_time += dt.timedelta(minutes=1)

    for date in datelist:
        print(result_list[date])
        mean = statistics.mean(result_list[date]['m_dot_air'])
        for j in range(max_len):
            if len(result_list[date]) != max_len:
                if j < len(result_list[date]):
                    continue
                else:
                    result_list[date].loc[j,'m_dot_air'] = None
                    result_list[date].loc[j, 'Time'] = result_list[date].loc[j-1, 'Time'] + dt.timedelta(minutes=1)
        result_list[date] = result_list[date].fillna(mean)

    level = {}
    for date in datelist:
        if unit == '3065':
            level[date] = 100 * (result_list['0110']['m_dot_air']-result_list[date]['m_dot_air']) / result_list['0110']['m_dot_air']
            level[date] = level[date].apply(lambda x: 0 if x < 0 else x)
            level[date].index = result_list[date]['Time']
        if unit == '3066':
            level[date] = 100 * (result_list['1229']['m_dot_air'] - result_list[date]['m_dot_air']) / result_list['1229']['m_dot_air']
            level[date] = level[date].apply(lambda x: 0 if x < 0 else x)
            level[date].index = result_list[date]['Time']
        if unit == '3067':
            level[date] = 100 * (result_list['0124_normal']['m_dot_air'] - result_list[date]['m_dot_air']) / result_list['0124_normal']['m_dot_air']
            level[date] = level[date].apply(lambda x: 0 if x < 0 else x)
            level[date].index = result_list[date]['Time']
        if unit == '3069':
            level[date] = 100 * (result_list['0117']['m_dot_air'] - result_list[date]['m_dot_air']) / result_list['0117']['m_dot_air']
            level[date] = level[date].apply(lambda x: 0 if x < 0 else x)
            level[date].index = result_list[date]['Time']
        # create_folder(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\혜빈\{}\{}'.format(unit,date))
        level[date].to_csv(save_path+unit+'/'+date+'/'+'/fault_level.csv')


    for date in datelist:
        print(unit,date)
        print("Airflow prediction mean: {}".format(statistics.mean(result_list[date]['m_dot_air'])))
        print("Airflow prediction STD: {}".format(statistics.stdev(result_list[date]['m_dot_air'])))
        print("Fault level mean: {}".format(statistics.mean(level[date])))
        print("Fault level STD: {}".format(statistics.stdev(level[date])))

    freq = {}
    for date in datelist:
        freq[date] = result_list[date]['freq_avg']

    step = {}
    for date in datelist:
        step[date] = result_list[date]['fan_step']

    label = {}
    for date in datelist:
        if unit == '3065':
            if date == '0120':
                label[date] = 'Fault type 2'
            elif date == '0110':
                label[date] = 'No fault'
            elif date == '0121':
                label[date] = 'Fault type 3'
        if unit == '3066':
            if date == '1230':
                label[date] = 'Fault type 2'
            elif date == '1229':
                label[date] = 'No fault'
            elif date == '0103':
                label[date] = 'No fault'
            elif date == '0107':
                label[date] = 'Fault type 4'
            elif date == '0106':
                label[date] = 'Fault type 3'
            elif date == '0105':
                label[date] = 'Fault type 2'
            elif date == '0810':
                label[date] = 'Fault type 1'
        if unit == '3067':
            if date == '0124_normal':
                label[date] = 'No fault'
            elif date == '0124':
                label[date] = 'Fault type 2'
            elif date == '0126_1':
                label[date] = 'Fault type 3'
            elif date == '0126_2':
                label[date] = 'Fault type 4'
        if unit == '3069':
            if date == '0117':
                label[date] = 'No fault'
            elif date == '0118':
                label[date] = 'Fault type 2'
            elif date == '0119_1':
                label[date] = 'Fault type 3'
            elif date == '0119_2':
                label[date] = 'Fault type 4'

    for day,result in result_list.items():
        fig, ax = plt.subplots(4, 1, figsize=(16, 12))
        if unit == '3065':
            ax[0].plot(time, result_list['0110']['m_dot_air'],label=label['0110'])
            ax[1].plot(time, level['0110'], label='Fault level - {:.0f}%'.format(statistics.mean(level['0110'])))
            ax[2].plot(time, freq['0110'], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq['0110'])))
            ax[3].plot(time, step['0110'], label='Fan step - {:.0f}'.format(statistics.mean(step['0110'])))
        elif unit == '3066':
            ax[0].plot(time, result_list['1229']['m_dot_air'],label=label['1229'])
            ax[1].plot(time, level['1229'], label='Fault level - {:.0f}%'.format(statistics.mean(level['1229'])))
            ax[2].plot(time, freq['1229'], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq['1229'])))
            ax[3].plot(time, step['1229'], label='Fan step - {:.0f}'.format(statistics.mean(step['1229'])))
        elif unit == '3067':
            ax[0].plot(time, result_list['0124_normal']['m_dot_air'],label=label['0124_normal'])
            ax[1].plot(time, level['0124_normal'], label='Fault level - {:.0f}%'.format(statistics.mean(level['0124_normal'])))
            ax[2].plot(time, freq['0124_normal'], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq['0124_normal'])))
            ax[3].plot(time, step['0124_normal'], label='Fan step - {:.0f}'.format(statistics.mean(step['0124_normal'])))
        elif unit == '3069':
            ax[0].plot(time, result_list['0117']['m_dot_air'],label=label['0117'])
            ax[1].plot(time, level['0117'], label='Fault level - {:.0f}%'.format(statistics.mean(level['0117'])))
            ax[2].plot(time, freq['0117'], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq['0117'])))
            ax[3].plot(time, step['0117'], label='Fan step - {:.0f}'.format(statistics.mean(step['0117'])))

        if unit == '3065':
            if day == '0110':
                continue
        elif unit == '3066':
            if day == '0729':
                continue
            if day == '1229' or '0103':
                continue
        elif unit == '3067':
            if day == '0124_normal':
                continue
        elif unit == '3069':
            if day == '0117':
                continue

        ax[0].plot(time, result['m_dot_air'], label=label[day])
        ax[0].set_xticks([time[i] for i in range(len(time)) if i % 20 == 0])
        ax[0].set_xticklabels([time[i] for i in range(len(time)) if i % 20 == 0],fontsize=12)
        ax[0].set_yticks([0,10,20,30,40,50])
        ax[0].set_yticklabels([0,10,20,30,40,50], fontsize=12)
        ax[0].legend(loc='upper right',fontsize=10,ncol=len(datelist))
        ax[0].set_ylabel('Airflow [kg/s]',fontsize=14,fontdict={'weight':'bold'})
        ax[0].grid(linestyle=':', color='dimgray')
        ax[1].plot(time,level[day],label='Fault level - {:.0f}%'.format(statistics.mean(level[day])))
        ax[1].set_xticks([time[i] for i in range(len(time)) if i % 20 == 0])
        ax[1].set_xticklabels([time[i] for i in range(len(time)) if i % 20 == 0],fontsize=12)
        ax[1].set_yticks([0,20,40,60,80,100,120])
        ax[1].set_yticklabels([0,20,40,60,80,100,120],fontsize=12)
        ax[1].legend(loc='upper right',fontsize=10,ncol=len(datelist))
        ax[1].set_ylabel('Fault level [%]',fontsize=14,fontdict={'weight':'bold'})
        ax[1].grid(linestyle=':', color='dimgray')
        ax[2].plot(time, freq[day], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq[day])))
        ax[2].set_xticks([time[i] for i in range(len(time)) if i % 20 == 0])
        ax[2].set_xticklabels([time[i] for i in range(len(time)) if i % 20 == 0], fontsize=12)
        ax[2].set_yticks([0, 20, 40, 60, 80, 100])
        ax[2].set_yticklabels([0, 20, 40, 60, 80, 100], fontsize=12)
        ax[2].legend(loc='upper right', fontsize=10,ncol=len(datelist))
        ax[2].set_ylabel('Frequency [Hz]', fontsize=14, fontdict={'weight': 'bold'})
        ax[2].grid(linestyle=':', color='dimgray')
        ax[3].plot(time, step[day], label='Fan step - {:.0f}'.format(statistics.mean(step[day])))
        ax[3].set_xticks([time[i] for i in range(len(time)) if i % 20 == 0])
        ax[3].set_xticklabels([time[i] for i in range(len(time)) if i % 20 == 0], fontsize=12)
        ax[3].set_yticks([0, 10, 20, 30, 40, 50])
        ax[3].set_yticklabels([0, 10, 20, 30, 40, 50], fontsize=12)
        ax[3].legend(loc='upper right', fontsize=10,ncol=len(datelist))
        ax[3].set_ylabel('Fan step', fontsize=14, fontdict={'weight': 'bold'})
        ax[3].grid(linestyle=':', color='dimgray')

        ax[3].set_xlabel('Time', fontsize=14, fontdict={'weight': 'bold'})

        plt.tight_layout()
        # plt.show()
        fig.savefig(save_path + unit + '/' + day +'/virtual_airflow_sensor.png')
        plt.close()

    for day, result in result_list.items():
        fig, axes = plt.subplots(figsize=(10, 9))
        normal_mean = 0
        normal_std = 0
        fault_std = 0
        normal_day = ''

        if unit == '3065':
            normal_mean = statistics.mean(result_list['0110']['m_dot_air'])
            normal_std = statistics.stdev(result_list['0110']['m_dot_air']) - 5
            fault_std = normal_std
            normal_day = '0110'
        elif unit == '3066':
            normal_mean = statistics.mean(result_list['1229']['m_dot_air'])
            normal_std = statistics.stdev(result_list['1229']['m_dot_air']) - 5
            fault_std = normal_std
            normal_day = '1229'
        elif unit == '3067':
            normal_mean = statistics.mean(result_list['0124_normal']['m_dot_air'])
            normal_std = statistics.stdev(result_list['0124_normal']['m_dot_air'])
            fault_std = normal_std
            normal_day = '0813'
        elif unit == '3069':
            normal_mean = statistics.mean(result_list['0117']['m_dot_air'])
            normal_std = statistics.stdev(result_list['0117']['m_dot_air'])
            fault_std = statistics.stdev(result_list['0117']['m_dot_air'])
            normal_day = '0117'

        if unit == '3065':
            if day == '0110':
                continue
        elif unit == '3066':
            if day == '1229':
                continue
        elif unit == '3067':
            if day == '0124_normal':
                continue
        elif unit == '3069':
            if day == '0117':
                continue

        fault_mean = statistics.mean(result['m_dot_air'])
        print(normal_std)
        print(fault_std)

        result = solve(normal_mean, fault_mean, normal_std, fault_std)

        x = np.linspace(-100, 200, 10000)

        plt.plot(x, norm.pdf(x, fault_mean, fault_std), color='r', linewidth=2)
        plt.plot(x, norm.pdf(x, normal_mean, normal_std), color='k', linewidth=2)

        plt.plot([fault_mean, fault_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
        plt.plot([normal_mean, normal_mean], [0, 2], color='k', linestyle='-.', linewidth=2)

        print(result)
        r1 = result[0]

        plt.fill_between(x[x < r1], 0, norm.pdf(x[x < r1], normal_mean, normal_std), color='red', alpha=0.3)
        plt.fill_between(x[x > r1], 0, norm.pdf(x[x > r1], fault_mean, fault_std), color='red', alpha=0.3)
        area1 = 1 - norm.cdf(r1, fault_mean, fault_std) + (norm.cdf(r1, normal_mean, normal_std))

        area1 = float("{0:.2f}".format(area1))
        axes.set_ylim([0, max(norm.pdf(x, normal_mean, normal_std))+0.05])
        yticks = axes.get_yticks()
        axes.set_yticklabels([round(yticks[i],2) for i in range(len(yticks))], fontsize=24)
        axes.set_xlim([normal_mean - 20, normal_mean + 10])
        xticks = axes.get_xticks()
        axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)

        plt.ylabel('Probability', fontsize=26,fontdict={'weight':'bold'})
        plt.xlabel('Airflow [kg/s]', fontsize=26,fontdict={'weight':'bold'})
        axes.text(1, 0.95, '{} area under curves: {}'.format(label[day],area1), horizontalalignment='right',transform=axes.transAxes, fontsize=22, color='k',fontdict={'weight':'bold'})
        if day == '0105':
            plt.legend(['[{} - {}/{}]'.format(label[day],'12','30'), '[No fault - {}/{}]'.format(normal_day[:2],normal_day[2:])], ncol=3, loc='center', fontsize=22, bbox_to_anchor=(0.5, -0.15))
            # plt.legend(['[{} - {}/{}]'.format(label[day],'01','10')], ncol=3, loc='center', fontsize=22, bbox_to_anchor=(0.5, -0.15))
        elif day == '0117':
            # plt.legend(['[{} - {}/{}]'.format(label[day],'01','10'), '[No fault - {}/{}]'.format(normal_day[:2],normal_day[2:])], ncol=3, loc='center', fontsize=22, bbox_to_anchor=(0.5, -0.15))
            plt.legend(['[{} - {}/{}]'.format(label[day],'01','17')], ncol=3, loc='center', fontsize=22, bbox_to_anchor=(0.5, -0.15))
        # elif day == '0103':
        #     plt.legend(['[{} - {}/{}]'.format(label[day], '01', '03'),'[No fault - {}/{}]'.format(normal_day[:2], normal_day[2:])], ncol=3, loc='center', fontsize=22,bbox_to_anchor=(0.5, -0.15))
        # elif day == '0103':
        #     plt.legend(['[{} - {}/{}]'.format(label[day], '01', '03')], ncol=3, loc='center', fontsize=22,bbox_to_anchor=(0.5, -0.15))
        else:
            plt.legend(['[{} - {}/{}]'.format(label[day], day[:2], day[2:]),'[No fault - {}/{}]'.format(normal_day[:2], normal_day[2:])], ncol=3, loc='center', fontsize=22,bbox_to_anchor=(0.5, -0.15))
        plt.tight_layout()
        # plt.show()
        plt.close()
        fig.savefig(save_path + unit + '/' + day + '/virtual_airflow_sensor_plob.png')

    # for day, result in level.items():
    #     fig, axes = plt.subplots(figsize=(8, 7))
    #     normal_mean = 0
    #     normal_std = 0
    #     fault_std = 0
    #     normal_day = ''
    #
    #     if unit == '3065':
    #         normal_mean = statistics.mean(level['0811'])
    #         normal_std = statistics.stdev(level['0811'])
    #         fault_std = statistics.stdev(level['0811'])
    #         normal_day = '0810'
    #     elif unit == '3066':
    #         normal_mean = statistics.mean(level['1229'])
    #         normal_std = statistics.stdev(level['1229'])
    #         fault_std = statistics.stdev(level['1229'])
    #         normal_day = '0728'
    #     elif unit == '3067':
    #         normal_mean = statistics.mean(level['0813_normal'])
    #         normal_std = statistics.stdev(level['0813_normal']) + 4.1
    #         fault_std = statistics.stdev(level['0813_normal']) + 4.1
    #         normal_day = '0813'
    #
    #     if unit == '3065':
    #         if day == '0811':
    #             continue
    #     elif unit == '3066':
    #         if day == '1229':
    #             continue
    #     elif unit == '3067':
    #         if day == '0813_normal':
    #             continue
    #
    #     fault_mean = statistics.mean(level[day])
    #
    #     result = solve(normal_mean, fault_mean, normal_std, fault_std)
    #
    #     x = np.linspace(-100, 200, 10000)
    #
    #     plt.plot(x, norm.pdf(x, fault_mean, fault_std), color='r', linewidth=2)
    #     plt.plot(x, norm.pdf(x, normal_mean, normal_std), color='k', linewidth=2)
    #
    #     plt.plot([fault_mean, fault_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
    #     plt.plot([normal_mean, normal_mean], [0, 2], color='k', linestyle='-.', linewidth=2)
    #
    #     r1 = result[0]
    #
    #     plt.fill_between(x[x > r1], 0, norm.pdf(x[x > r1], normal_mean, normal_std), color='r', alpha=0.3)
    #     plt.fill_between(x[x < r1], 0, norm.pdf(x[x < r1], fault_mean, fault_std), color='r', alpha=0.3)
    #     area1 = norm.cdf(r1, fault_mean, fault_std) + 1 - (norm.cdf(r1, normal_mean, normal_std))
    #
    #     area1 = float("{0:.2f}".format(area1))
    #
    #     axes.set_ylim([0, max(norm.pdf(x, fault_mean, fault_std))+0.05])
    #     axes.set_xlim([normal_mean - 20, normal_mean + 100])
    #     plt.ylabel('Probability', fontsize=14, fontweight='bold')
    #     plt.xlabel('Fault level [%]', fontsize=14, fontweight='bold')
    #     axes.text(1, 0.95, '{} area under curves: {}'.format(label[day],area1), horizontalalignment='right',transform=axes.transAxes, fontsize=12, color='r')
    #     if day == '0810' and unit == '3065':
    #         plt.legend(['[{} - {}/{}]'.format(label[day],'08','11'), '[No fault - {}/{}]'.format(normal_day[:2],normal_day[2:])], ncol=3, loc='center', fontsize=12, bbox_to_anchor=(0.5, -0.15))
    #     elif day == '1229':
    #         plt.legend(['[{} - {}/{}]'.format(label[day], '12', '29'),'[No fault - {}/{}]'.format(normal_day[:2], normal_day[2:])], ncol=3, loc='center', fontsize=12,bbox_to_anchor=(0.5, -0.15))
    #     else:
    #         plt.legend(['[{} - {}/{}]'.format(label[day], day[:2], day[2:]),'[No fault - {}/{}]'.format(normal_day[:2], normal_day[2:])], ncol=3, loc='center', fontsize=12,bbox_to_anchor=(0.5, -0.15))
    #     plt.tight_layout()
    #     # plt.show()
    #     plt.close()
    #     fig.savefig(save_path + unit + '/' + day + '/virtual_airflow_sensor_fl_plob.png')


# for unit, day in datalist.items():
#     print(unit,day)
#     airflow_sensor(path,unit,day)

for unit, day in datalist.items():
    plot(save_path+unit,day)