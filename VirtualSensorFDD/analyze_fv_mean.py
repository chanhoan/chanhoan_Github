import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import statistics
import numpy as np
import collections
import itertools
import os


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]
directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Analyze\Data\{}\analyze.csv'.format(folder_name)
directory2 = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Analyze\Data\{}\analyze2.csv'.format(folder_name)

data_28 = pd.read_csv(directory)
data_29 = pd.read_csv(directory)
data_30 = pd.read_csv(directory)
data_04 = pd.read_csv(directory)
data_05 = pd.read_csv(directory)
time_28 = pd.read_csv(directory2)['28Time'].dropna()
time_29 = pd.read_csv(directory2)['29Time'].dropna()
time_30 = pd.read_csv(directory2)['30Time'].dropna()
time_04 = pd.read_csv(directory2)['04Time'].dropna()
time_05 = pd.read_csv(directory2)['05Time'].dropna()
v_28 = pd.read_csv(directory2)['velocity_28'].dropna()
v_29 = pd.read_csv(directory2)['velocity_29'].dropna()
v_30 = pd.read_csv(directory2)['velocity_30'].dropna()
v_04 = pd.read_csv(directory2)['velocity_04'].dropna()
v_05 = pd.read_csv(directory2)['velocity_05'].dropna()

time28_dt = []
time29_dt = []
time30_dt = []
time04_dt = []
time05_dt = []

for i in range(len(time_28)):
    time28_dt.append(dt.datetime.strptime(time_28[i],'%Y-%m-%d %H:%M:%S'))
for i in range(len(time_29)):
    time29_dt.append(dt.datetime.strptime(time_29[i],'%Y-%m-%d %H:%M:%S'))
for i in range(len(time_30)):
    time30_dt.append(dt.datetime.strptime(time_30[i],'%Y-%m-%d %H:%M:%S'))
for i in range(len(time_04)):
    time04_dt.append(dt.datetime.strptime(time_04[i],'%Y-%m-%d %H:%M:%S'))
for i in range(len(time_05)):
    time05_dt.append(dt.datetime.strptime(time_05[i],'%Y-%m-%d %H:%M:%S'))

df28 = pd.concat([pd.DataFrame(time28_dt,columns=['28Time']),v_28],axis=1).set_index('28Time')
df29 = pd.concat([pd.DataFrame(time29_dt,columns=['29Time']),v_29],axis=1).set_index('29Time')
df30 = pd.concat([pd.DataFrame(time30_dt,columns=['30Time']),v_30],axis=1).set_index('30Time')
df04 = pd.concat([pd.DataFrame(time04_dt,columns=['04Time']),v_04],axis=1).set_index('04Time')
df05 = pd.concat([pd.DataFrame(time05_dt,columns=['05Time']),v_05],axis=1).set_index('05Time')

time28_compo = []
time29_compo = []
time30_compo = []
time04_compo = []
time05_compo = []
for i in range(len(time_28)):
    if time_28[i][11:16] not in time28_compo:
        time28_compo.append(time_28[i][11:16])
for i in range(len(time_29)):
    if time_29[i][11:16] not in time29_compo:
        time29_compo.append(time_29[i][11:16])
for i in range(len(time_30)):
    if time_30[i][11:16] not in time30_compo:
        time30_compo.append(time_30[i][11:16])
for i in range(len(time_04)):
    if time_04[i][11:16] not in time04_compo:
        time04_compo.append(time_04[i][11:16])
for i in range(len(time_05)):
    if time_05[i][11:16] not in time05_compo:
        time05_compo.append(time_05[i][11:16])

drop_idx_28 = []
drop_idx_29 = []
drop_idx_30 = []
drop_idx_04 = []
drop_idx_05 = []

for i in range(len(data_28)):
    if data_28['Time'][i][0:5] not in time28_compo:
        drop_idx_28.append(i)
for i in range(len(data_29)):
    if data_29['Time'][i][0:5] not in time29_compo:
        drop_idx_29.append(i)
for i in range(len(data_30)):
    if data_30['Time'][i][0:5] not in time30_compo:
        drop_idx_30.append(i)
for i in range(len(data_04)):
    if data_04['Time'][i][0:5] not in time04_compo:
        drop_idx_04.append(i)
for i in range(len(data_05)):
    if data_05['Time'][i][0:5] not in time05_compo:
        drop_idx_05.append(i)

data_28 = data_28.drop(drop_idx_28,axis=0).reset_index()
data_29 = data_29.drop(drop_idx_29,axis=0).reset_index()
data_30 = data_30.drop(drop_idx_30,axis=0).reset_index()
data_04 = data_04.drop(drop_idx_04,axis=0).reset_index()
data_05 = data_05.drop(drop_idx_05,axis=0).reset_index()

fs_28 = data_28['fan_step_28'].dropna()
fs_29 = data_29['fan_step_29'].dropna()
fs_30 = data_30['fan_step_30'].dropna()
fs_04 = data_04['fan_step_04'].dropna()
fs_05 = data_05['fan_step_05'].dropna()

fs_28_compo = []
fs_29_compo = []
fs_30_compo = []
fs_04_compo = []
fs_05_compo = []

for i in range(len(fs_28)):
    if fs_28[i] not in fs_28_compo and fs_28[i] != 0:
        fs_28_compo.append(fs_28[i])
for i in range(len(fs_29)):
    if fs_29[i] not in fs_29_compo and fs_29[i] != 0:
        fs_29_compo.append(fs_29[i])
for i in range(len(fs_30)):
    if fs_30[i] not in fs_30_compo and fs_30[i] != 0:
        fs_30_compo.append(fs_30[i])
for i in range(len(fs_04)):
    if fs_04[i] not in fs_04_compo and fs_04[i] != 0:
        fs_04_compo.append(fs_04[i])
for i in range(len(fs_05)):
    if fs_05[i] not in fs_05_compo and fs_05[i] != 0:
        fs_05_compo.append(fs_05[i])

print(sorted(fs_28_compo))
print(sorted(fs_29_compo))
print(sorted(fs_30_compo))
print(sorted(fs_04_compo))
print(sorted(fs_05_compo))

fs_28_idx = {key:[] for key in fs_28_compo}
fs_29_idx = {key:[] for key in fs_29_compo}
fs_30_idx = {key:[] for key in fs_30_compo}
fs_04_idx = {key:[] for key in fs_04_compo}
fs_05_idx = {key:[] for key in fs_05_compo}

df28_mean = pd.DataFrame()
df29_mean = pd.DataFrame()
df30_mean = pd.DataFrame()
df04_mean = pd.DataFrame()
df05_mean = pd.DataFrame()

df28_mean['velocity_28'] = df28['velocity_28'].resample('1T').mean().dropna()
df29_mean['velocity_29'] = df29['velocity_29'].resample('1T').mean().dropna()
df30_mean['velocity_30'] = df30['velocity_30'].resample('1T').mean().dropna()
df04_mean['velocity_04'] = df04['velocity_04'].resample('1T').mean().dropna()
df05_mean['velocity_05'] = df05['velocity_05'].resample('1T').mean().dropna()

for key in fs_28:
    for i in range(len(fs_28)):
        if fs_28[i] == key and key != 0:
            fs_28_idx[key].append(df28_mean['velocity_28'][i])
for key in fs_29:
    for i in range(len(fs_29)):
        if fs_29[i] == key and key != 0:
            fs_29_idx[key].append(df29_mean['velocity_29'][i])
for key in fs_30:
    for i in range(len(fs_30)):
        if fs_30[i] == key and key != 0:
            fs_30_idx[key].append(df30_mean['velocity_30'][i])
for key in fs_04:
    for i in range(len(fs_04)):
        if fs_04[i] == key and key != 0:
            fs_04_idx[key].append(df04_mean['velocity_04'][i])
for key in fs_05:
    for i in range(len(fs_05)):
        if fs_05[i] == key and key != 0:
            fs_05_idx[key].append(df05_mean['velocity_05'][i])

fs_28_idx = sorted(fs_28_idx.items())
fs_29_idx = sorted(fs_29_idx.items())
fs_30_idx = sorted(fs_30_idx.items())
fs_04_idx = sorted(fs_04_idx.items())
fs_05_idx = sorted(fs_05_idx.items())


def xyl(dict):
    k = 0
    x = []
    y = []
    l = []
    for key, value in dict:
        x.append(key)
        y.append(statistics.mean(value))
        l.append(key)
        k+=1
    return x,y,l


fs_28_x, fs_28_y, fs_28_l = xyl(fs_28_idx)
fs_29_x, fs_29_y, fs_29_l = xyl(fs_29_idx)
fs_30_x, fs_30_y, fs_30_l = xyl(fs_30_idx)
fs_04_x, fs_04_y, fs_04_l = xyl(fs_04_idx)
fs_05_x, fs_05_y, fs_05_l = xyl(fs_05_idx)

print(fs_28_x)
print(fs_28_y)
print(fs_29_x)
print(fs_29_y)


def plotting(x1,y1,x2,y2,l,comp_num,cond1,cond2,date1,date2):
    fig, ax1 = plt.subplots(figsize=(12,10))
    ax1.set_title('Air velocity and Fan step ({} / {})'.format(cond1,cond2),fontsize=16)
    ax1.step(x1,y1,c='b',where='mid')
    ax1.step(x2,y2,c='r',where='mid')
    ax1.set_xticks(x1)
    ax1.set_xlim([0,max(x2)+3])
    ax1.set_xticks([i for i in range(max(x2)+3)])
    ax1.set_xlabel('Fan step'.format(comp_num),fontsize=14)
    ax1.set_ylabel('Air velocity [m/s]',fontsize=14)
    # ax2.set_ylabel('Air velocity [m/s]', fontsize=14)
    ax1.legend(['{}'.format(cond1)],fontsize='large')
    ax1.legend(['{}'.format(cond2)],fontsize='large')
    plt.tight_layout()
    today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = today[0:10]
    fig_save_dir = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Analyze\Result\{}'.format(folder_name)
    create_folder(fig_save_dir)
    plt.savefig(fig_save_dir+'\Air velocity and Fan step_({}vs{})_mean.png'.format(date1,date2))


plotting(fs_28_x,fs_28_y,fs_29_x,fs_29_y,fs_28_l,1,'No fault','Mesh layer','0728','0729')
plotting(fs_28_x,fs_28_y,fs_30_x,fs_30_y,fs_28_l,1,'No fault','kitchen towel','0728','0730')
plotting(fs_28_x,fs_28_y,fs_04_x,fs_04_y,fs_28_l,1,'No fault','kitchen towel','0728','0804')
plotting(fs_28_x,fs_28_y,fs_05_x,fs_05_y,fs_28_l,1,'No fault','kitchen towel','0728','0805')