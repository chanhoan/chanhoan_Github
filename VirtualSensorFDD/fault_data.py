import pandas as pd
import datetime as dt
import os


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)

month = '08'
date = '11'
unit = '3065'
experiment_count = 1
layer = '40Mesh'
layer_depth = 4
start_time = ['2021-{}-{} 12:40:00'.format(month,date), '2021-{}-{} 14:24:00'.format(month,date), '2021-{}-{} 17:10:00'.format(month,date)]
finish_time = ['2021-{}-{} 13:57:00'.format(month,date),'2021-{}-{} 15:14:00'.format(month,date), '2021-{}-{} 17:59:00'.format(month,date)]

temp_index = [51,52,53,54,55,56,57,58,59,60,43,45,47,49,42,44,46,48]

iot = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung'
                  r'\Compressor map data\2021-11-17\{}{}\outdoor_{}.csv'.format(month,date,unit))
temp = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung'
                   r'\Compressor map data\2021-11-17\{}{}\{}{} temp.csv'.format(month,date,month,date)).fillna(method='ffill')
flow = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung'
                   r'\Compressor map data\2021-11-17\{}{}\{}{} flow.csv'.format(month,date,month,date)).fillna(method='ffill')


temp_time = ['2021-{}-{} '.format(month,date)+temp['Time'][i] for i in range(len(temp['Time']))]
temp.index = temp_time
flow_time = ['2021-{}-{} '.format(month,date)+flow['Time'][i] for i in range(len(flow['Time']))]
flow.index = flow_time

iot_time = pd.date_range(iot['updated_time'][0],iot['updated_time'][len(iot)-1],freq=dt.timedelta(minutes=1))
temp_time = pd.date_range('2021-{}-{} '.format(month,date)+temp['Time'][0],'2021-{}-{} '.format(month,date)+temp['Time'][len(temp)-1],freq=dt.timedelta(seconds=2))
flow_time = pd.date_range('2021-{}-{} '.format(month,date)+flow['Time'][0],'2021-{}-{} '.format(month,date)+flow['Time'][len(flow)-1],freq=dt.timedelta(seconds=2))

iot_df = pd.DataFrame(iot_time,columns=['Time']).set_index('Time')
iot.index = iot_time

temp_df = pd.DataFrame(index=temp_time)
temp_df['Time'] = [temp_df.index[i].strftime('%Y-%m-%d %H:%M:%S') for i in range(len(temp_df))]
temp_df = temp_df.set_index('Time')

flow_df = pd.DataFrame(index=flow_time)
flow_df['Time'] = [flow_df.index[i].strftime('%Y-%m-%d %H:%M:%S') for i in range(len(flow_df))]
flow_df = flow_df.set_index('Time')

for i in range(len(iot.columns)):
    if iot.columns[i] == 'Unnamed: 0' or iot.columns[i] == 'Time':
        continue
    else:
        iot_df = pd.concat([iot_df,iot[iot.columns[i]]],axis=1)

for i in range(len(temp_index)):
    temp_df = pd.concat([temp_df,temp['point {}'.format(temp_index[i])]],axis=1)
temp_time = pd.date_range('2021-{}-{} '.format(month,date)+temp['Time'][0],'2021-{}-{} '.format(month,date)+temp['Time'][len(temp)-1],freq=dt.timedelta(seconds=2))
temp_df.index = temp_time

flow_df['Standard Velocity (Matrix)'] = flow['Standard Velocity (Matrix)']
flow_time = pd.date_range('2021-{}-{} '.format(month,date)+flow['Time'][0],'2021-{}-{} '.format(month,date)+flow['Time'][len(flow)-1],freq=dt.timedelta(seconds=2))
flow_df.index = flow_time

temp_resample = pd.DataFrame()
flow_resample = pd.DataFrame()

for i in range(len(temp_index)):
    temp_resample['point {}'.format(temp_index[i])] = temp_df['point {}'.format(temp_index[i])].resample('1T').mean()

flow_resample['Standard Velocity (Matrix)'] = flow_df['Standard Velocity (Matrix)'].resample('1T').mean()

iot_start = 0
iot_finish = 0
temp_start = 0
temp_finish = 0
flow_start = 0
flow_finish = 0
for i in range(experiment_count):
    for k in range(len(iot_df)):
        if start_time[i] == str(iot_df.index[k]):
            iot_start = k
        elif finish_time[i] == str(iot_df.index[k]):
            iot_finish = k

    for k in range(len(temp_resample)):
        if start_time[i] == str(temp_resample.index[k]):
            temp_start = k
        elif finish_time[i] == str(temp_resample.index[k]):
            temp_finish = k

    for k in range(len(flow_resample)):
        if start_time[i] == str(flow_resample.index[k]):
            flow_start = k
        elif finish_time[i] == str(flow_resample.index[k]):
            flow_finish = k

    iot_cut = iot_df.iloc[iot_start:iot_finish,:]
    temp_cut = temp_resample.iloc[temp_start:temp_finish,:]
    flow_cut = flow_resample.iloc[flow_start:flow_finish,:]

    save = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Dataset\{}\{}{}\experiment {}'.format(unit,month,date,i+1)
    create_folder(save)
    overall = pd.concat([iot_cut,temp_cut,flow_cut],axis=1)
    overall.to_csv(save+'\Outdoor{}_{}{}_{}_{}.csv'.format(unit,month,date,layer,i+1))