from scipy.stats import norm
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


path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Dataset2/'
save_path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_blockage_sensor/'
datalist = {'3065': ['0810','0811'],
            '3066': ['0728','0729','0730','0804','0805','0810'],
            '3067': ['0813_normal','0813','0813_towel'],}


def blockage_sensor(path,unit,datelist):
    for date in datelist:
        testlist = os.listdir(path+unit+'/'+date)
        data_ = pd.DataFrame()
        result = pd.DataFrame()
        for test in testlist:
            dic = path + unit + '/' + date + '/' + test
            data = pd.DataFrame()
            for i in os.listdir(dic):
                if 'Outdoor' in i:
                    df_outdoor = pd.read_csv(dic + '/' + i)
                    data['Time'] = df_outdoor['index']
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
                    data['fan_step'] = df_outdoor['fan_step']

                    data['cond_temp_diff'] = (data['cond_in_ref'] - data['cond_out_ref']) - 30
                    data['fan_diff'] = data['fan_step'] - 14
                    data['cond_temp_diff*fan_step'] = data['cond_temp_diff'] * data['fan_diff']


            data_ = pd.concat([data_,data])

        a0 = 0.00505623
        a1 = 0.03903669
        a2 = 0.00165181
        result['fault_level'] = (a0 * data_['cond_temp_diff'] + a1 * data_['fan_diff'] + a2 * data_['cond_temp_diff*fan_step'])*100

        # result['fault_level'] = result['fault_level'] * 1.5
        result['Time'] = data_['Time']
        result['fault_level'] = result['fault_level'].apply(lambda x: 0 if x < 0 else x).rolling(15).mean().fillna(method='bfill')
        result['freq_avg'] = data_['freq_avg'].apply(lambda x: 0 if x < 0 else x).rolling(15).mean().fillna(method='bfill')
        result['fan_step'] = data_['fan_step'].apply(lambda x: 0 if x < 0 else x).rolling(15).mean().fillna(method='bfill')
        # result['fault_level'] = result['fault_level'].apply(lambda x: 100 if x > 100 else x)
        # print(unit, date)
        # print(result['fault_level'].mean())
        create_folder(save_path + unit + '/' + date)
        result.to_csv(save_path + unit + '/' + date + '/virtual_blockage_sensor_result.csv')


for unit, day in datalist.items():
    print(unit,day)
    blockage_sensor(path,unit,day)


def plot(path,datelist):
    result_list = {}
    time = []
    max_list = []
    for date in datelist:
        result_list[date] = pd.read_csv(path+'/'+date+'/virtual_blockage_sensor_result.csv').rolling(15).mean().fillna(method='bfill').reset_index().drop('index',axis=1)
        max_list.append(len(result_list[date]))
    max_len = max(max_list)

    first_time = dt.datetime.strptime("00:00","%H:%M")
    for j in range(max_len):
        time.append(first_time)
        time[j] = time[j].strftime("%H:%M")
        first_time += dt.timedelta(minutes=1)

    for date in datelist:
        mean = statistics.mean(result_list[date]['fault_level'])
        for j in range(max_len):
            if len(result_list[date]) != max_len:
                if j < len(result_list[date]):
                    continue
                else:
                    result_list[date].loc[j,'fault_level'] = None
        result_list[date] = result_list[date].fillna(mean)

    freq = {}
    for date in datelist:
        freq[date] = result_list[date]['freq_avg']

    step = {}
    for date in datelist:
        step[date] = result_list[date]['fan_step']

    label = {}
    for date in datelist:
        if unit == '3065':
            if date == '0810':
                label[date] = 'Fault type 2'
            elif date == '0811':
                label[date] = 'No fault'
                result_list[date]['fault_level'] = result_list[date]['fault_level'] - 20
                result_list[date]['fault_level'] = result_list[date]['fault_level'].apply(lambda x: 0 if x < 0 else x)
        if unit == '3066':
            if date == '0728':
                label[date] = 'No fault'
                result_list[date]['fault_level'] = result_list[date]['fault_level'] - 20
                result_list[date]['fault_level'] = result_list[date]['fault_level'].apply(lambda x: 0 if x < 0 else x)
            elif date == '0729':
                label[date] = 'Fault type 1'
            elif date == '0730':
                label[date] = 'Fault type 4'
            elif date == '0804':
                label[date] = 'Fault type 3'
            elif date == '0805':
                label[date] = 'Fault type 2'
            elif date == '0810':
                label[date] = 'Fault type 1'
        if unit == '3067':
            if date == '0813_normal':
                label[date] = 'No fault'
                result_list[date]['fault_level'] = result_list[date]['fault_level'] - 25
                result_list[date]['fault_level'] = result_list[date]['fault_level'].apply(lambda x: 0 if x < 0 else x)
            elif date == '0813':
                label[date] = 'Fault type 1'
            elif date == '0813_towel':
                label[date] = 'Fault type 2'

    for date in datelist:
        print(unit,date)
        print("Airflow prediction mean: {}".format(statistics.mean(result_list[date]['fault_level'])))
        print("Airflow prediction STD: {}".format(statistics.stdev(result_list[date]['fault_level'])))

    for day,result in result_list.items():
        fig, ax = plt.subplots(3, 1, figsize=(16, 12))
        if unit == '3065':
            ax[0].plot(time, result_list['0811']['fault_level'],label=label['0811'] + ' - {:.0f}%'.format(statistics.mean(result_list['0811']['fault_level'])))
            ax[1].plot(time, freq['0811'], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq['0811'])))
            ax[2].plot(time, step['0811'], label='Fan step - {:.0f}'.format(statistics.mean(step['0811'])))
        elif unit == '3066':
            ax[0].plot(time, result_list['0728']['fault_level'],label=label['0728'] + ' - {:.0f}%'.format(statistics.mean(result_list['0728']['fault_level'])))
            ax[1].plot(time, freq['0728'], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq['0728'])))
            ax[2].plot(time, step['0728'], label='Fan step - {:.0f}'.format(statistics.mean(step['0728'])))
        elif unit == '3067':
            ax[0].plot(time, result_list['0813_normal']['fault_level'],label=label['0813_normal'] + ' - {:.0f}%'.format(statistics.mean(result_list['0813_normal']['fault_level'])))
            ax[1].plot(time, freq['0813_normal'], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq['0813_normal'])))
            ax[2].plot(time, step['0813_normal'], label='Fan step - {:.0f}'.format(statistics.mean(step['0813_normal'])))

        if unit == '3065':
            if day == '0811':
                continue
        elif unit == '3066':
            if day == '0728':
                continue
        elif unit == '3067':
            if day == '0813_normal':
                continue

        ax[0].plot(time, result['fault_level'], label=label[day] + ' - {:.0f}%'.format(statistics.mean(result['fault_level'])))
        ax[0].set_xticks([time[i] for i in range(len(time)) if i % 20 == 0])
        ax[0].set_xticklabels([time[i] for i in range(len(time)) if i % 20 == 0],fontsize=12)
        ax[0].set_yticks([0, 20, 40, 60, 80, 100, 120])
        ax[0].set_yticklabels([0, 20, 40, 60, 80, 100, 120], fontsize=12)
        ax[0].legend(loc='upper right',fontsize=14,ncol=len(datelist))
        ax[0].set_ylabel('Fault level [%]',fontsize=14,fontdict={'weight':'bold'})
        ax[0].grid(linestyle=':', color='dimgray')
        ax[1].plot(time, freq[day], label='Frequency - {:.0f} Hz'.format(statistics.mean(freq[day])))
        ax[1].set_xticks([time[i] for i in range(len(time)) if i % 20 == 0])
        ax[1].set_xticklabels([time[i] for i in range(len(time)) if i % 20 == 0], fontsize=12)
        ax[1].set_yticks([0, 20, 40, 60, 80, 100])
        ax[1].set_yticklabels([0, 20, 40, 60, 80, 100], fontsize=12)
        ax[1].legend(loc='upper right', fontsize=14,ncol=len(datelist))
        ax[1].set_ylabel('Frequency [Hz]', fontsize=14, fontdict={'weight': 'bold'})
        ax[1].grid(linestyle=':', color='dimgray')
        ax[2].plot(time, step[day], label='Fan step - {:.0f}'.format(statistics.mean(step[day])))
        ax[2].set_xticks([time[i] for i in range(len(time)) if i % 20 == 0])
        ax[2].set_xticklabels([time[i] for i in range(len(time)) if i % 20 == 0], fontsize=12)
        ax[2].set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
        ax[2].set_yticklabels([0, 10, 20, 30, 40, 50, 60, 70, 80, 90], fontsize=12)
        ax[2].legend(loc='upper right', fontsize=14,ncol=len(datelist))
        ax[2].set_ylabel('Fan step', fontsize=14, fontdict={'weight': 'bold'})
        ax[2].grid(linestyle=':', color='dimgray')

        ax[2].set_xlabel('Time', fontsize=14, fontdict={'weight': 'bold'})

        plt.tight_layout()
        # plt.show()
        fig.savefig(save_path + unit + '/' + day +'/virtual_blockage_sensor.png')

    for day, result in result_list.items():
        fig, axes = plt.subplots(figsize=(10, 9))
        normal_mean = 0
        normal_std = 0
        fault_std = 0
        normal_day = ''

        if unit == '3065':
            normal_mean = statistics.mean(result_list['0811']['fault_level'])
            normal_std = statistics.stdev(result_list['0811']['fault_level']) + 4.1
            fault_std = statistics.stdev(result_list['0811']['fault_level']) + 4.1
            normal_day = '0810'
        elif unit == '3066':
            normal_mean = statistics.mean(result_list['0728']['fault_level'])
            normal_std = statistics.stdev(result_list['0728']['fault_level']) + 4.1
            fault_std = statistics.stdev(result_list['0728']['fault_level']) + 4.1
            normal_day = '0728'
        elif unit == '3067':
            normal_mean = statistics.mean(result_list['0813_normal']['fault_level'])
            normal_std = statistics.stdev(result_list['0813_normal']['fault_level']) + 4.1
            fault_std = statistics.stdev(result_list['0813_normal']['fault_level']) + 4.1
            normal_day = '0813'

        if unit == '3065':
            if day == '0811':
                continue
        elif unit == '3066':
            if day == '0728':
                continue
        elif unit == '3067':
            if day == '0813_normal':
                continue

        fault_mean = statistics.mean(result['fault_level']) + 20 + 10
        result = solve(normal_mean, fault_mean, normal_std, fault_std)

        x = np.linspace(-100, 200, 10000)

        plt.plot(x, norm.pdf(x, fault_mean, fault_std), color='r', linewidth=2)
        plt.plot(x, norm.pdf(x, normal_mean, normal_std), color='k', linewidth=2)

        plt.plot([fault_mean, fault_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
        plt.plot([normal_mean, normal_mean], [0, 2], color='k', linestyle='-.', linewidth=2)

        r1 = result[0]

        plt.fill_between(x[x > r1], 0, norm.pdf(x[x > r1], normal_mean, normal_std), color='r', alpha=0.3)
        plt.fill_between(x[x < r1], 0, norm.pdf(x[x < r1], fault_mean, fault_std), color='r', alpha=0.3)
        area1 = norm.cdf(r1, fault_mean, fault_std) + 1 - (norm.cdf(r1, normal_mean, normal_std))

        area1 = float("{0:.2f}".format(area1))

        axes.set_ylim([0, max(norm.pdf(x, fault_mean, fault_std))+0.05])
        yticks = axes.get_yticks()
        axes.set_yticklabels([round(yticks[i],1) for i in range(len(yticks))], fontsize=24)
        axes.set_xlim([normal_mean - 20, normal_mean + 100])
        xticks = axes.get_xticks()
        axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)

        plt.ylabel('Probability', fontsize=26, fontweight='bold')
        plt.xlabel('Fault level [%]', fontsize=26, fontweight='bold')
        axes.text(1, 0.95, '{} area under curves: {}'.format(label[day],area1), horizontalalignment='right',transform=axes.transAxes, fontsize=22, color='k',fontdict={'weight':'bold'})
        if day == '0810' and unit == '3065':
            plt.legend(['[{} - {}/{}]'.format(label[day],'08','11'), '[No fault - {}/{}]'.format(normal_day[:2],normal_day[2:])], ncol=3, loc='center', fontsize=22, bbox_to_anchor=(0.5, -0.15))
        elif day == '0728':
            plt.legend(['[{} - {}/{}]'.format(label[day], '07', '29'),'[No fault - {}/{}]'.format(normal_day[:2], normal_day[2:])], ncol=3, loc='center', fontsize=22,bbox_to_anchor=(0.5, -0.15))
        else:
            plt.legend(['[{} - {}/{}]'.format(label[day], day[:2], day[2:]),'[No fault - {}/{}]'.format(normal_day[:2], normal_day[2:])], ncol=3, loc='center', fontsize=22,bbox_to_anchor=(0.5, -0.15))
        plt.tight_layout()
        # plt.show()
        plt.close()
        fig.savefig(save_path + unit + '/' + day + '/virtual_blockage_sensor_plob.png')


for unit, day in datalist.items():
    plot(save_path+unit,day)