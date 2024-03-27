import CoolProp as CP
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import statistics
from scipy.stats import norm


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


year = '2022'
month = '02'
day = '21'

unit = '3069'

path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Experiment/Data/{}-{}-{}/'.format(year, month, day)
save_path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/VAF/{}/{}-{}-{}'.format(unit, year, month, day)
comp_model = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python\samsung/Compressor map data/{}-{}-{}/{}/{}{}'.format(year,month,day,unit,month,day)

create_folder(save_path)

c_p = 1.005
air_specific_volume = 1 / 1.225


def airflow_sensor_outdoor(path):
    cond_in_h = []
    cond_out_h = []
    data = pd.DataFrame()
    for i in os.listdir(path):
        if 'outdoor' in i:
            df_outdoor = pd.read_csv(path + '/' + i)
            data['updated_time'] = df_outdoor['updated_time']
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
                        data.loc[j, 'discharge_temp1'] = data.loc[j, 'discharge_temp2']
                for j in range(len(data)):
                    if data['comp2'][j] == 0:
                        data.loc[j, 'discharge_temp2'] = data.loc[j, 'discharge_temp1']

                data['cond_in_ref'] = (data['discharge_temp1'] + data['discharge_temp2']) / 2
            else:
                data['cond_in_ref'] = data['discharge_temp1']
            data['cond_out_ref'] = df_outdoor['cond_out_temp1']
            data['high_pressure'] = df_outdoor['high_pressure']

    m_dot_freq1 = pd.read_csv(comp_model + '/freq1/GB066_{}.csv'.format(unit))['m_dot_pred']
    m_dot_freq2 = pd.read_csv(comp_model + '/freq2/GB066_{}.csv'.format(unit))['m_dot_pred']
    data['m_dot_ref'] = m_dot_freq1 + m_dot_freq2

    data = data.dropna(axis=0)
    for j in range(len(data)):
        try:
            cond_in_h.append(CP.CoolProp.PropsSI('H', 'P', data['high_pressure'][j] * 98.0665 * 1000, 'T',data['cond_in_ref'][j] + 273, 'R410A') / 1000)
        except:
            cond_in_h.append(None)
    for j in range(len(data)):
        try:
            cond_out_h.append(CP.CoolProp.PropsSI('H', 'P', data['high_pressure'][j] * 98.0665 * 1000, 'T',data['cond_out_ref'][j] + 273, 'R410A') / 1000)
        except:
            cond_out_h.append(None)

    data['cond_in_h'] = cond_in_h
    data['cond_out_h'] = cond_out_h

    data['cond_in_h'] = data['cond_in_h'].fillna(method='bfill').fillna(method='ffill')
    data['cond_out_h'] = data['cond_out_h'].fillna(method='bfill').fillna(method='ffill')

    df_temp = pd.read_csv(path + '\{}{} temp.csv'.format(month, day), engine='python').fillna(method='bfill').fillna(method='ffill')
    df_temp['updated_time'] = df_temp['Date'] + ' ' + df_temp['Time']

    df_temp.index = pd.to_datetime(df_temp['updated_time'])
    df_temp.drop(['updated_time','Date','Time','sec'], inplace=True, axis=1)
    df_temp = df_temp.resample('1T').mean()
    for col in df_temp.columns:
        df_temp[col] = df_temp[col].apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')

    df_temp['cond_in_air'] = df_temp.filter(regex='point').min(axis=1)
    df_temp['cond_out_air'] = df_temp.filter(regex='condout').max(axis=1)

    data.index = pd.to_datetime(data['updated_time'])
    data.drop(['updated_time'], inplace=True, axis=1)
    data = data.loc[df_temp.index[0]:df_temp.index[len(df_temp) - 1], :]

    index = data.index

    df_temp = df_temp.reset_index().drop('updated_time',axis=1)
    data = data.reset_index().drop('updated_time', axis=1)

    data = pd.concat([data,df_temp[['cond_in_air','cond_out_air']]],axis=1)

    data['m_dot_air'] = air_specific_volume * (data['m_dot_ref'] * (data['cond_in_h'] - data['cond_out_h'])) / (c_p * (data['cond_out_air'] - data['cond_in_air']))

    data['m_dot_air'] = data['m_dot_air'].apply(lambda x: None if x < 0 else x)
    data['m_dot_air'] = data['m_dot_air'].apply(lambda x: None if x > 100 else x)

    data['m_dot_air'] = data['m_dot_air'].fillna(method='bfill')
    data['updated_time'] = index

    data['rated_m_dot_air'] = data['freq_avg'] * 0.51408 / 6
    data.to_csv(save_path+'/VAF_data_ODU.csv')
    print(data)

    return data


def airflow_sensor_indoor(path):
    cond_in_h = []
    cond_out_h = []
    data = pd.DataFrame()
    indoor = pd.DataFrame()
    for i in os.listdir(path):
        if 'outdoor' in i:
            df_outdoor = pd.read_csv(path + '/' + i)
            data['updated_time'] = df_outdoor['updated_time']
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
                        data.loc[j, 'discharge_temp1'] = data.loc[j, 'discharge_temp2']
                for j in range(len(data)):
                    if data['comp2'][j] == 0:
                        data.loc[j, 'discharge_temp2'] = data.loc[j, 'discharge_temp1']

                data['cond_in_ref'] = (data['discharge_temp1'] + data['discharge_temp2']) / 2
            else:
                data['cond_in_ref'] = data['discharge_temp1']
            data['cond_out_ref'] = df_outdoor['cond_out_temp1']
            data['high_pressure'] = df_outdoor['high_pressure']
            data['low_pressure'] = df_outdoor['low_pressure']
        elif 'indoor' in i:
            df = pd.read_csv(path + '/' + i)
            indoor['evapin_temp{}'.format(i)] = df['evain_temp']
            indoor['evapout_temp{}'.format(i)] = df['evaout_temp']

    m_dot_freq1 = pd.read_csv(comp_model + '/freq1/GB066_{}.csv'.format(unit))['m_dot_pred']
    m_dot_freq2 = pd.read_csv(comp_model + '/freq2/GB066_{}.csv'.format(unit))['m_dot_pred']
    data['m_dot_ref'] = m_dot_freq1 + m_dot_freq2

    data['evapin_temp'] = indoor.filter(regex='evapin_temp').mean(axis=1)
    data['evapout_temp'] = indoor.filter(regex='evapout_temp').mean(axis=1)

    data = data.dropna(axis=0)
    for j in range(len(data)):
        try:
            cond_in_h.append(CP.CoolProp.PropsSI('H', 'P', data['high_pressure'][j] * 98.0665 * 1000, 'T',data['evapin_temp'][j] + 273, 'R410A') / 1000)
        except:
            cond_in_h.append(None)
    for j in range(len(data)):
        try:
            cond_out_h.append(CP.CoolProp.PropsSI('H', 'P', data['high_pressure'][j] * 98.0665 * 1000, 'T',data['evapout_temp'][j] + 273, 'R410A') / 1000)
        except:
            cond_out_h.append(None)

    data['cond_in_h'] = cond_in_h
    data['cond_out_h'] = cond_out_h

    data['cond_in_h'] = data['cond_in_h'].fillna(method='bfill').fillna(method='ffill')
    data['cond_out_h'] = data['cond_out_h'].fillna(method='bfill').fillna(method='ffill')

    df_temp = pd.read_csv(path + '\{}{} temp2.csv'.format(month, day), engine='python').fillna(method='bfill').fillna(method='ffill')
    df_temp['updated_time'] = df_temp['Date'] + ' ' + df_temp['Time']

    df_temp.index = pd.to_datetime(df_temp['updated_time'])
    df_temp.drop(['updated_time','Date','Time','sec'], inplace=True, axis=1)
    df_temp = df_temp.resample('1T').mean()
    for col in df_temp.columns:
        df_temp[col] = df_temp[col].apply(lambda x: None if x < 10 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')

    df_temp['cond_in_air'] = df_temp.filter(regex='point').min(axis=1)
    df_temp['cond_out_air'] = df_temp.filter(regex='condout').max(axis=1)

    data.index = pd.to_datetime(data['updated_time'])
    data.drop(['updated_time'], inplace=True, axis=1)
    data = data.loc[df_temp.index[0]:df_temp.index[len(df_temp) - 1], :]

    index = data.index

    df_temp = df_temp.reset_index().drop('updated_time',axis=1)
    data = data.reset_index().drop('updated_time', axis=1)

    data = pd.concat([data,df_temp[['cond_in_air','cond_out_air']]],axis=1)


    data['m_dot_air'] = air_specific_volume * (data['m_dot_ref'] * (data['cond_in_h'] - data['cond_out_h'])) / (c_p * (data['cond_in_air'] - data['cond_out_air']))

    data['m_dot_air'] = data['m_dot_air'].apply(lambda x: None if x < 0 else x)
    data['m_dot_air'] = data['m_dot_air'].apply(lambda x: None if x > 10 else x)

    data['m_dot_air'] = data['m_dot_air'].fillna(method='bfill')
    data['updated_time'] = index

    data['rated_m_dot_air'] = data['freq_avg'] * 0.51408 / 15
    data.to_csv(save_path+'/VAF_data_IDU.csv')
    print(data)

    return data


def day_result(df):
    time = 'updated_time'
    fig, ax1 = plt.subplots(figsize=(12, 5))
    fault_timestamp = pd.to_datetime(df[time])
    test_data = df.set_index(fault_timestamp)
    test_data = test_data.resample('15T').mean()
    test_data.fillna(0, inplace=True)

    test_data['rated_m_dot_air'] = test_data['rated_m_dot_air'].apply(lambda x: 0 if x <= 0 else x)
    test_data.dropna(inplace=True)

    xtick = list(str(test_data.index[i]) for i in range(len(test_data)))
    xtick = [xtick[i][:10]+'\n'+xtick[i][11:] for i in range(len(xtick))]


    ax1.step(xtick, test_data['rated_m_dot_air'], label='Rated airflow - {:.1f}$m^3/s$'.format(statistics.mean(test_data['rated_m_dot_air'])))
    ax1.step(xtick, test_data['m_dot_air'], label='Airflow based on VAF sensor - {:.1f}$m^3/s$'.format(statistics.mean(test_data['m_dot_air'])))

    # ax1.set_ylim(0,120)
    ax1.set_ylim(0,10)
    yticks = ax1.get_yticks()
    ax1.set_yticklabels([int(yticks[i]) for i in range(len(yticks))],fontsize=20)
    ax1.set_xticks([xtick[i] for i in range(len(xtick)) if i % 4 == 0])
    ax1.set_xticklabels([xtick[i] for i in range(len(xtick)) if i % 4 == 0],fontsize=20)

    ax1.set_ylabel('Airflow [$m^3/s$]',fontsize=18)

    ax1.set_xlabel('Time', fontsize=18)

    plt.legend(loc='upper right', ncol=2, fontsize=18)
    plt.grid(linestyle=':')
    # plt.ylabel('Temperature [C]')
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=15)

    plt.tight_layout()
    return fig.savefig(save_path + '/realtime_result_ODU.png')
    # plt.show()


def probability(x, mean_base, std_base, mean_fault, std_fault, result1,):
    fig2, ax = plt.subplots(figsize=(10, 9))

    plt.plot(x, norm.pdf(x, mean_fault, std_fault), color='r', linewidth=2)
    plt.plot(x, norm.pdf(x, mean_base, std_base), color='k', linewidth=2)

    plt.plot([mean_fault, mean_fault], [0, 2], color='r', linestyle='-.', linewidth=2)
    plt.plot([mean_base, mean_base], [0, 2], color='k', linestyle='-.', linewidth=2)

    r1 = result1[0]

    if mean_fault > mean_base:
        plt.fill_between(x[x > r1], 0, norm.pdf(x[x > r1], mean_base, std_base), color='red', alpha=0.3)
        plt.fill_between(x[x < r1], 0, norm.pdf(x[x < r1], mean_fault, std_fault), color='red', alpha=0.3)
        area1 = norm.cdf(r1, mean_fault, std_fault) + 1-(norm.cdf(r1, mean_base, std_base))
    else:
        plt.fill_between(x[x < r1], 0, norm.pdf(x[x < r1], mean_base, std_base), color='red', alpha=0.3)
        plt.fill_between(x[x > r1], 0, norm.pdf(x[x > r1], mean_fault, std_fault), color='red', alpha=0.3)
        area1 = 1-norm.cdf(r1, mean_fault, std_fault) + (norm.cdf(r1, mean_base, std_base))

    area1 = float("{0:.2f}".format(area1))
    print("Normal distribution area under curves ", area1)

    axes = plt.gca()
    axes.set_ylim([0, max(norm.pdf(x, mean_base, std_base)) + 0.05])
    yticks = axes.get_yticks()
    axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
    axes.set_xlim([mean_base - 10, mean_base + 10])
    # axes.set_xlim([mean_base - 5, mean_base + 5])
    xticks = axes.get_xticks()
    axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
    plt.ylabel('Probability', fontsize=26, fontweight='bold')
    plt.xlabel('Airflow [kg/s]', fontsize=26, fontweight='bold')
    axes.text(1, 0.95, 'area under curves: {}'.format(area1), horizontalalignment='right',transform=axes.transAxes, fontsize=22, color='k', fontdict={'weight': 'bold'})
    legend = plt.legend(['[Rated airflow]','[Airflow based on VAF]'],ncol=3, loc='center',fontsize=22, bbox_to_anchor=(0.5, -0.15))
    plt.tight_layout()
    # plt.show()
    return fig2.savefig(save_path + './probability_ODU.png', bbox_extra_artists=(legend,), bbox_inches='tight')



data = airflow_sensor_outdoor(path=path)
# data = airflow_sensor_indoor(path=path)
day_result(data)
#
line_x = np.linspace(-100, 200, 10000)
normal_mean = statistics.mean(data['m_dot_air'])
normal_std = statistics.stdev(data['m_dot_air'])

fault_mean1 = statistics.mean(data['rated_m_dot_air'])
# fault_std1 = statistics.stdev(data['rated_m_dot_air'])
fault_std1 = normal_std
result1 = solve(normal_mean, fault_mean1, normal_std, fault_std1)

print(normal_mean)
print(normal_std)
print(fault_mean1)
print(fault_std1)

probability(line_x,normal_mean,normal_std,fault_mean1,fault_std1,result1)