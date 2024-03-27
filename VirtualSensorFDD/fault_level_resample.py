import pandas as pd
import datetime as dt
import statistics

path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Dataset2/'
save_path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/virtual air flow sensor/'
datalist = {'3065': ['0810','0811'],
            '3066': ['0728','0729','0730','0804','0805','0811'],
            '3067': ['0813_normal','0813'],}


def airflow(path,datelist):
    result_list = {}
    time_list = {}
    time = []
    max_list = []
    for date in datelist:
        time_list[date] = pd.read_csv(path + '/' + date + '/virtual_airflow_sensor.csv')['Time']
        result_list[date] = pd.read_csv(path+'/'+date+'/virtual_airflow_sensor.csv').reset_index().drop('index',axis=1)
        result_list[date]['m_dot_air'] = result_list[date]['m_dot_air'].rolling(15).mean().fillna(method='bfill')
        result_list[date]['Time'] = [dt.datetime.strptime(result_list[date]['Time'][i],'%Y-%m-%d %H:%M') for i in range(len(result_list[date]))]
        max_list.append(len(result_list[date]))
    max_len = max(max_list)

    for date in datelist:
        # print(result_list[date])
        mean = statistics.mean(result_list[date]['m_dot_air'])
        for j in range(max_len):
            if len(result_list[date]) != max_len:
                if j < len(result_list[date]):
                    continue
                else:
                    result_list[date].loc[j,'m_dot_air'] = None
                    result_list[date].loc[j, 'Time'] = result_list[date].loc[j-1, 'Time'] + dt.timedelta(minutes=1)
        result_list[date]['m_dot_air'] = result_list[date]['m_dot_air'].fillna(mean)
        result_list[date] = result_list[date].fillna(method='ffill')

    level = {}
    for date in datelist:
        # level[date] = pd.DataFrame(index=result_list[date]['Time'])
        if unit == '3065':
            level[date] = 100 * (result_list['0811']['m_dot_air'] - result_list[date]['m_dot_air']) / result_list['0811']['m_dot_air']
            level[date] = level[date].apply(lambda x: 0 if x < 0 else x)
            level[date].index = result_list[date]['Time']
        if unit == '3066':
            level[date] = 100 * (result_list['0728']['m_dot_air'] - result_list[date]['m_dot_air']) / result_list['0728']['m_dot_air']
            level[date] = level[date].apply(lambda x: 0 if x < 0 else x)
            level[date].index = result_list[date]['Time']
        if unit == '3067':
            level[date] = 100 * (result_list['0813_normal']['m_dot_air'] - result_list[date]['m_dot_air']) / result_list['0813_normal']['m_dot_air']
            level[date] = level[date].apply(lambda x: 0 if x < 0 else x)
            level[date].index = result_list[date]['Time']

    dt_range = {}
    for date in datelist:
        timestamp = pd.date_range(time_list[date][0],time_list[date][len(time_list[date])-1],freq=dt.timedelta(minutes=1))
        dt_range[date] = pd.DataFrame(index=timestamp,columns=['fault_level'])
        # result_list[date]['Time'] = time_list[date]
        for i in range(len(dt_range[date])):
            for j in range(len(level[date])):
                if dt_range[date].index[i] == level[date].index[j]:
                    dt_range[date].loc[dt_range[date].index[i],'fault_level'] = level[date][level[date].index[j]]
        print(dt_range[date])
        dt_range[date].to_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\혜빈\{}\{}\fault_level.csv'.format(unit,date))
        dt_range[date] = dt_range[date].dropna(axis=0).astype(float)
        df_resample = dt_range[date]['fault_level'].resample('5T').mean()
        df_resample = df_resample.rolling(3).mean().fillna(method='bfill')
        df_resample.to_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Performance degradation\degradation\{}\{}\airflow_sensor_level.csv'.format(unit,date))
        # print(df_resample)


for unit, day in datalist.items():
    airflow(save_path+unit,day)


def blockage(path, datelist):
    result_list = {}
    time_list = {}
    time = []
    max_list = []
    for date in datelist:
        time_list[date] = pd.read_csv(path + '/' + date + '/virtual_blockage_sensor_result.csv')['Time']
        result_list[date] = pd.read_csv(path + '/' + date + '/virtual_blockage_sensor_result.csv').reset_index().drop('index',axis=1)
        result_list[date]['Time'] = [dt.datetime.strptime(result_list[date]['Time'][i], '%Y-%m-%d %H:%M') for i in range(len(result_list[date]))]
        max_list.append(len(result_list[date]))
    max_len = max(max_list)

    for date in datelist:
        # print(result_list[date])
        mean = statistics.mean(result_list[date]['fault_level'])
        for j in range(max_len):
            if len(result_list[date]) != max_len:
                if j < len(result_list[date]):
                    continue
                else:
                    result_list[date].loc[j,'fault_level'] = None
                    result_list[date].loc[j, 'Time'] = result_list[date].loc[j - 1, 'Time'] + dt.timedelta(minutes=1)
        result_list[date]['fault_level'] = result_list[date]['fault_level'].fillna(mean)
        result_list[date] = result_list[date].fillna(method='ffill')
        result_list[date].index = result_list[date]['Time']
        print(result_list[date])

    dt_range = {}
    for date in datelist:
        timestamp = pd.date_range(time_list[date][0], time_list[date][len(time_list[date]) - 1],
                                  freq=dt.timedelta(minutes=1))
        dt_range[date] = pd.DataFrame(index=timestamp, columns=['fault_level'])
        # result_list[date]['Time'] = time_list[date]
        for i in range(len(dt_range[date])):
            for j in range(len(result_list[date]['fault_level'])):
                if dt_range[date].index[i] == result_list[date].index[j]:
                    dt_range[date].loc[dt_range[date].index[i], 'fault_level'] = result_list[date]['fault_level'][result_list[date].index[j]]
        # print(dt_range[date])
        dt_range[date] = dt_range[date].dropna(axis=0).astype(float)
        df_resample = dt_range[date]['fault_level'].resample('5T').mean()
        df_resample = df_resample.rolling(3).mean().fillna(method='bfill')
        df_resample.to_csv(
            r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Performance degradation\degradation\{}\{}\blockage_sensor_level.csv'.format(
                unit, date))


# for unit, day in datalist.items():
#     blockage(save_path + unit, day)

