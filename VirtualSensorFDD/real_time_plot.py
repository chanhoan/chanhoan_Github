from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import datetime
from scipy.stats import norm
from glob import glob
from collections import OrderedDict
import math
from sklearn.metrics import mean_squared_error
import statistics

time = 'updated_time'
unit = 3069
date = '0119_2'

fault = pd.read_csv(r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_airflow_sensor/{}/{}/virtual_airflow_sensor.csv'.format(unit,date))[['Time','m_dot_air','freq_avg']]
# fault = pd.read_csv(r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_blockage_sensor/{}/{}/virtual_blockage_sensor_result.csv'.format(unit,date))[['Time','fault_level','freq_avg']]

fault['rated'] = fault['freq_avg'] * 0.51408
# fault['rated'] = fault['freq_avg'] * 0.49993 - 14

fault_timestamp = pd.to_datetime(fault['Time'])

fault.columns = [time,'m_dot_air','freq_avg','rated']
# fault.columns = [time,'fault_level','freq_avg','rated']

# fault.index = fault_timestamp
fault = fault.drop(['freq_avg'],axis=1)

# fault['fault_level'] = fault['fault_level'] + 5
fault['m_dot_air'] = fault['m_dot_air']

save = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_airflow_sensor/'
# save = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_blockage_sensor/'


def day_result(df):
    fig, ax1 = plt.subplots(figsize=(12, 5))
    fault_timestamp = pd.to_datetime(df[time])
    test_data = df.set_index(fault_timestamp)
    test_data = test_data.resample('15T').mean()
    test_data.fillna(0, inplace=True)

    # test_data['fault_level'] = test_data['fault_level'].apply(lambda x: None if x<=0 else x)
    # test_data['fault_level'] = test_data['fault_level'].apply(lambda x: 100 if x > 100 else x)
    test_data['rated'] = test_data['rated'].apply(lambda x: 0 if x <= 0 else x)
    test_data.dropna(inplace=True)

    xtick = list(str(test_data.index[i]) for i in range(len(test_data)))
    # xtick = [datetime_idx[i].strftime('%Y-%m-%d %H:%M:%S') for i in range(len(datetime_idx))]
    xtick = [xtick[i][:10]+'\n'+xtick[i][11:] for i in range(len(xtick))]

    # test_data.loc[test_data.Test == 0, ['Test', 'Prediction', 'shift']]=0
    # test_data.to_csv(Dic+'/reslt.csv')
    # test_data.loc[(test_data['comp_sum'] ==0), ['Test', 'shift']] = 0

    print(statistics.mean(test_data['rated']))

    print(test_data)
    ax1.step(xtick, test_data['rated'], label='Normal state airflow - {:.1f}kg/s'.format(statistics.mean(test_data['rated'])))
    ax1.step(xtick, test_data['m_dot_air'], label='Fault state airflow - {:.1f}kg/s'.format(statistics.mean(test_data['m_dot_air'])))
    # ax1.step(xtick, test_data['rated'], label='Rated fouling - {:.1f}%'.format(statistics.mean(test_data['rated'])))
    # ax1.step(xtick, test_data['fault_level'], label='Virtual fouling sensor - {:.1f}%'.format(statistics.mean(test_data['fault_level'])))

    ax1.set_ylim(0,120)
    yticks = ax1.get_yticks()
    ax1.set_yticklabels([int(yticks[i]) for i in range(len(yticks))],fontsize=20)
    ax1.set_xticks([xtick[i] for i in range(len(xtick)) if i % 4 == 0])
    ax1.set_xticklabels([xtick[i] for i in range(len(xtick)) if i % 4 == 0],fontsize=20)

    ax1.set_ylabel('Virtual airflow prediction [kg/s]',fontsize=18)
    # ax1.set_ylabel('Virtual fouling sensor predict [%]', fontsize=17)

    ax1.set_xlabel('Time', fontsize=18)

    plt.legend(loc='upper right', ncol=2, fontsize=18)
    plt.grid(linestyle=':')
    # plt.ylabel('Temperature [C]')
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=15)

    plt.tight_layout()
    fig.savefig(save + '{}/{}/realtime_result.png'.format(unit,date))
    plt.show()


day_result(fault)