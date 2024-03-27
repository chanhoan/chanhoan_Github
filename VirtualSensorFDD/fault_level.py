import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
import CoolProp as CP
from sklearn.metrics import mean_squared_error
import statistics
import math
import numpy as np


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


unit = '3067'
today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]
date1 = '0730'
date2 = '0804'
date3 = '0805'
directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor model result\{}'.format(folder_name)
fault_model1 = 'GB066_{}'.format(date1,unit)
fault_model2 = 'GB066_{}'.format(date2,unit)
fault_model3 = 'GB066_{}'.format(date3,unit)
fault_model3065 = 'GB066_{}'.format('0811',unit)
fault_model3067 = 'GB066_{}'.format('0813',unit)

fig_save_dir = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor model result\그림\{}'.format(folder_name)
create_folder(fig_save_dir)


fault_data1 = pd.read_csv(directory+r'\freq1\{}.csv'.format(fault_model1))
fault_data2 = pd.read_csv(directory+r'\freq2\{}.csv'.format(fault_model1))
fault_data1_ = pd.read_csv(directory+r'\freq1\{}.csv'.format(fault_model2))
fault_data2_ = pd.read_csv(directory+r'\freq2\{}.csv'.format(fault_model2))
fault_data1__ = pd.read_csv(directory+r'\freq1\{}.csv'.format(fault_model3))
fault_data2__ = pd.read_csv(directory+r'\freq2\{}.csv'.format(fault_model3))
fault_data1_3065 = pd.read_csv(directory+r'\freq1\{}.csv'.format(fault_model3065))
fault_data2_3065 = pd.read_csv(directory+r'\freq2\{}.csv'.format(fault_model3065))
fault_data1_3067 = pd.read_csv(directory+r'\freq1\{}.csv'.format(fault_model3067))
fault_data2_3067 = pd.read_csv(directory+r'\freq2\{}.csv'.format(fault_model3067))

fault_start = '11:18:00'
fault_end = '12:22:00'
fault2_start = '12:42:00'
fault2_end = '13:46:00'
fault3_start = '12:29:00'
fault3_end = '13:33:00'
fault3065_start = '12:40:00'
fault3065_end = '13:57:00'
fault3067_start = '12:50:00'
fault3067_end = '14:16:00'
fault_start_i = 0
fault_end_i = 0
fault2_start_i = 0
fault2_end_i = 0
fault3_start_i = 0
fault3_end_i = 0
fault3065_start_i = 0
fault3065_end_i = 0
fault3067_start_i = 0
fault3067_end_i = 0
for i in range(len(fault_data1)):
    if fault_data1['Time'][i] == fault_start:
        fault_start_i = i
    elif fault_data1['Time'][i] == fault_end:
        fault_end_i = i
for i in range(len(fault_data1_)):
    if fault_data1_['Time'][i] == fault2_start:
        fault2_start_i = i
    elif fault_data1_['Time'][i] == fault2_end:
        fault2_end_i = i
for i in range(len(fault_data1__)):
    if fault_data1__['Time'][i] == fault3_start:
        fault3_start_i = i
    elif fault_data1__['Time'][i] == fault3_end:
        fault3_end_i = i
for i in range(len(fault_data1_3065)):
    if fault_data1_3065['Time'][i] == fault3065_start:
        fault3065_start_i = i
    elif fault_data1_3065['Time'][i] == fault3065_end:
        fault3065_end_i = i
for i in range(len(fault_data1_3067)):
    if fault_data1_3067['Time'][i] == fault3067_start:
        fault3067_start_i = i
    elif fault_data1_3067['Time'][i] == fault3067_end:
        fault3067_end_i = i

fault_data1 = fault_data1.iloc[fault_start_i:fault_end_i,:].reset_index()
fault_data2 = fault_data2.iloc[fault_start_i:fault_end_i,:].reset_index()
fault_data1_ = fault_data1_.iloc[fault2_start_i:fault2_end_i,:].reset_index()
fault_data2_ = fault_data2_.iloc[fault2_start_i:fault2_end_i,:].reset_index()
fault_data1__ = fault_data1__.iloc[fault3_start_i:fault3_end_i,:].reset_index()
fault_data2__ = fault_data2__.iloc[fault3_start_i:fault3_end_i,:].reset_index()
fault_data1_3065 = fault_data1_3065.iloc[fault3065_start_i:fault3065_end_i,:].reset_index()
fault_data2_3065 = fault_data2_3065.iloc[fault3065_start_i:fault3065_end_i,:].reset_index()
fault_data1_3067 = fault_data1_3067.iloc[fault3067_start_i:fault3067_end_i,:].reset_index()
fault_data2_3067 = fault_data2_3067.iloc[fault3067_start_i:fault3067_end_i,:].reset_index()

fault_k_p1 = fault_data1['w_dot_pred']/fault_data1['w_dot_rated']
fault_k_p2 = fault_data2['w_dot_pred']/fault_data2['w_dot_rated']
fault_k_p1_ = fault_data1_['w_dot_pred']/fault_data1_['w_dot_rated']
fault_k_p2_ = fault_data2_['w_dot_pred']/fault_data2_['w_dot_rated']
fault_k_p1__ = fault_data1__['w_dot_pred']/fault_data1__['w_dot_rated']
fault_k_p2__ = fault_data2__['w_dot_pred']/fault_data2__['w_dot_rated']
fault_k_p1_3065 = fault_data1_3065['w_dot_pred']/fault_data1_3065['w_dot_rated']
fault_k_p2_3065 = fault_data2_3065['w_dot_pred']/fault_data2_3065['w_dot_rated']
fault_k_p1_3067 = fault_data1_3067['w_dot_pred']/fault_data1_3067['w_dot_rated']
fault_k_p2_3067 = fault_data2_3067['w_dot_pred']/fault_data2_3067['w_dot_rated']

fault_k_p = []
fault_k_p_ = []
fault_k_p__ = []
fault_k_p_3065 = []
fault_k_p_3067 = []
for i in range(len(fault_data1)):
    fault_k_p.append((fault_k_p1[i]+fault_k_p2[i])*1.54)
for i in range(len(fault_data1_)):
    fault_k_p_.append((fault_k_p1_[i]+fault_k_p2_[i]))
for i in range(len(fault_data1__)):
    fault_k_p__.append((fault_k_p1__[i]+fault_k_p2__[i])*1.13)
for i in range(len(fault_data1_3065)):
    fault_k_p_3065.append((fault_k_p1_3065[i]+fault_k_p2_3065[i]))
for i in range(len(fault_data1_3067)):
    fault_k_p_3067.append((fault_k_p1_3067[i]+fault_k_p2_3067[i])*0.97)

date_len = len(fault_data1)
date_len_3065 = len(fault_data1_3065)
date_len_3067 = len(fault_data1_3067)
start_time = dt.datetime.strptime('00:00:00','%H:%M:%S')
end_time = start_time + dt.timedelta(minutes=date_len-1)
end_time_3065 = start_time + dt.timedelta(minutes=date_len_3065-1)
end_time_3067 = start_time + dt.timedelta(minutes=date_len_3067-1)
time = pd.date_range(start_time,end_time,freq='1min').strftime('%H:%M:%S').tolist()
time_3065 = pd.date_range(start_time,end_time_3065,freq='1min').strftime('%H:%M:%S').tolist()
time_3067 = pd.date_range(start_time,end_time_3067,freq='1min').strftime('%H:%M:%S').tolist()

time_dt = []
time_dt_3065 = []
time_dt_3067 = []
for i in range(len(time)):
    time_dt.append(dt.datetime.strptime(time[i],'%H:%M:%S'))
for i in range(len(time_3065)):
    time_dt_3065.append(dt.datetime.strptime(time_3065[i], '%H:%M:%S'))
for i in range(len(time_3067)):
    time_dt_3067.append(dt.datetime.strptime(time_3067[i], '%H:%M:%S'))
fault_k_p_df = pd.DataFrame(np.column_stack([time_dt,fault_k_p]),columns=['Time','k_p']).set_index('Time')
fault_k_p = fault_k_p_df['k_p'].rolling(15).mean().fillna(method='bfill')
fault_k_p_df_ = pd.DataFrame(np.column_stack([time_dt,fault_k_p_]),columns=['Time','k_p']).set_index('Time')
fault_k_p_ = fault_k_p_df_['k_p'].rolling(15).mean().fillna(method='bfill')
fault_k_p_df__ = pd.DataFrame(np.column_stack([time_dt,fault_k_p__]),columns=['Time','k_p']).set_index('Time')
fault_k_p__ = fault_k_p_df__['k_p'].rolling(15).mean().fillna(method='bfill')
fault_k_p_df_3065 = pd.DataFrame(np.column_stack([time_dt_3065,fault_k_p_3065]),columns=['Time','k_p']).set_index('Time')
fault_k_p_3065 = fault_k_p_df_3065['k_p'].rolling(15).mean().fillna(method='bfill')
fault_k_p_df_3067 = pd.DataFrame(np.column_stack([time_dt_3067,fault_k_p_3067]),columns=['Time','k_p']).set_index('Time')
fault_k_p_3067 = fault_k_p_df_3067['k_p'].rolling(15).mean().fillna(method='bfill')

# mdot vs freq
plt.cla()
plt.clf()
fig, ax1 = plt.subplots(3,1,figsize=(16,8))
ax1[0].plot(time,fault_k_p,c='g',linewidth=1.5,linestyle='-')
ax1[0].plot(range(len(fault_k_p_)),fault_k_p_,c='b',linewidth=1.5,linestyle='-')
ax1[0].plot(range(len(fault_k_p__)),fault_k_p__,c='r',linewidth=1.5,linestyle='-')
ax1[1].plot(time_3065,fault_k_p_3065,c='b',linewidth=1.5,linestyle='-')
ax1[2].plot(time_3067,fault_k_p_3067,c='b',linewidth=1.5,linestyle='-')
ax1[0].set_ylim([0,max(fault_k_p)+2])
ax1[1].set_ylim([0,max(fault_k_p_3065)+2])
ax1[2].set_ylim([0,max(fault_k_p_3067)+2])
ax1[0].set_xticks([i for i in range(len(time)) if i % 20 == 0])
ax1[1].set_xticks([i for i in range(len(time)) if i % 20 == 0])
ax1[2].set_xticks([i for i in range(len(time)) if i % 20 == 0])
ax1[0].set_ylabel('Fault level', fontsize=14)
ax1[1].set_ylabel('Fault level', fontsize=14)
ax1[2].set_ylabel('Fault level', fontsize=14)
ax1[2].set_xlabel('Time',fontsize=14)
ax1[0].set_title('Fault level',fontsize=16)
ax1[0].legend(['Fault level (07/30) - kitchen towel 4 layer = {:.2f}'.format(statistics.mean(fault_k_p)),
               'Fault level (08/04) - kitchen towel 3 layer = {:.2f}'.format(statistics.mean(fault_k_p_)),
               'Fault level (08/05) - kitchen towel 2 layer = {:.2f}'.format(statistics.mean(fault_k_p__))],loc='upper left',fontsize=14)
ax1[1].legend(['Fault level (08/11) - Mesh 4 layer = {:.2f}'.format(statistics.mean(fault_k_p_3065))],loc='upper left',fontsize=14)
ax1[2].legend(['Fault level (08/13) - Mesh 4 layer = {:.2f}'.format(statistics.mean(fault_k_p_3067))],loc='upper left',fontsize=14)
ax1[0].autoscale(enable=True, axis='x', tight=True)
ax1[1].autoscale(enable=True, axis='x', tight=True)
ax1[2].autoscale(enable=True, axis='x', tight=True)
ax1[0].grid()
ax1[1].grid()
ax1[2].grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}.png'.format('fault_level'))
plt.close()