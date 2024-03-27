import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os
import statistics


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


time = 'updated_time'

# month = str(datetime.datetime.today().month)
# day = str(datetime.datetime.today().day)
year = '2022'
month = '02'
day = '03'
unit = '3065'

fan_limit = {'3065': 10, '3066': 20, '3067': 20, '3069': 20}

if len(month) == 1:
    month = '0' + month
if len(day) == 1:
    day = '0' + day

temp = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\{}{} temp.csv'.format(
        year, month, day, month, day), engine='python').fillna(method='bfill').fillna(method='ffill')
volume = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\{}{} volume.csv'.format(
        year,month, day, month, day), engine='python')
velocity = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\{}{} flow.csv'.format(
        year, month, day, month, day), engine='python')
power = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(
        year, month, day, unit))
comp = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(
        year, month, day, unit))
fan = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(
        year, month, day, unit))
Psuc = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(
        year, month, day, unit))
Pdis = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(
        year, month, day, unit))
Tsuc = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(
        year, month, day, unit))
Tdis = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(
        year, month, day, unit))

date = temp['Date']

volume_time = date + ' ' + volume['Time']
velocity_time1 = date + ' ' + velocity['Time1']
velocity_time2 = date + ' ' + velocity['Time2']
velocity_time3 = date + ' ' + velocity['Time3']
velocity_time4 = date + ' ' + velocity['Time4']
velocity_time5 = date + ' ' + velocity['Time5']
velocity_time6 = date + ' ' + velocity['Time6']
velocity_time7 = date + ' ' + velocity['Time7']
velocity_time8 = date + ' ' + velocity['Time8']

velocity = velocity.dropna()

volume_time = volume_time.dropna()
velocity_time1 = velocity_time1.dropna()
velocity_time2 = velocity_time2.dropna()
velocity_time3 = velocity_time3.dropna()
velocity_time4 = velocity_time4.dropna()
velocity_time5 = velocity_time5.dropna()
velocity_time6 = velocity_time6.dropna()
velocity_time7 = velocity_time7.dropna()
velocity_time8 = velocity_time8.dropna()

velocity1 = velocity['velocity1']
velocity1.index = pd.to_datetime(velocity_time1)
velocity1 = velocity.velocity1.resample('1T').mean()
velocity1 = velocity1.apply(lambda x: 0 if x < 0 else x)
velocity2 = velocity['velocity2']
velocity2.index = pd.to_datetime(velocity_time2)
velocity2 = velocity.velocity2.resample('1T').mean()
velocity2 = velocity2.apply(lambda x: 0 if x < 0 else x)
velocity3 = velocity['velocity3']
velocity3.index = pd.to_datetime(velocity_time3)
velocity3 = velocity.velocity3.resample('1T').mean()
velocity3 = velocity3.apply(lambda x: 0 if x < 0 else x)
velocity4 = velocity['velocity4']
velocity4.index = pd.to_datetime(velocity_time4)
velocity4 = velocity.velocity4.resample('1T').mean()
velocity4 = velocity4.apply(lambda x: 0 if x < 0 else x)
velocity5 = velocity['velocity5']
velocity5.index = pd.to_datetime(velocity_time5)
velocity5 = velocity.velocity5.resample('1T').mean()
velocity5 = velocity5.apply(lambda x: 0 if x < 0 else x)
velocity6 = velocity['velocity6']
velocity6.index = pd.to_datetime(velocity_time6)
velocity6 = velocity.velocity6.resample('1T').mean()
velocity6 = velocity6.apply(lambda x: 0 if x < 0 else x)
velocity7 = velocity['velocity7']
velocity7.index = pd.to_datetime(velocity_time7)
velocity7 = velocity.velocity7.resample('1T').mean()
velocity7 = velocity7.apply(lambda x: 0 if x < 0 else x)
velocity8 = velocity['velocity8']
velocity8.index = pd.to_datetime(velocity_time8)
velocity8 = velocity.velocity8.resample('1T').mean()
velocity8 = velocity8.apply(lambda x: 0 if x < 0 else x)

volume.index = pd.to_datetime(volume_time)
volume = volume.volume.resample('1T').mean()
volume = volume.apply(lambda x: 0 if x < 0 else x).apply(lambda x: -x if x < 0 else x)

fan.index = pd.to_datetime(fan[time])
fan1 = fan.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan2 = fan.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan3 = fan.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan4 = fan.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan5 = fan.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan6 = fan.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan7 = fan.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan8 = fan.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)
fan_v = fan.loc[volume.index[0]:volume.index[len(volume)-1],'fan_step'].apply(lambda x: None if x < fan_limit[unit] else x)

power.index = pd.to_datetime(power[time])
power1 = power.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power2 = power.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power3 = power.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power4 = power.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power5 = power.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power6 = power.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power7 = power.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power8 = power.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)
power_v = power.loc[volume.index[0]:volume.index[len(volume)-1],'value'].apply(lambda x: -x if x < 0 else x).apply(lambda x: None if x < 1000 else x/1000)

Psuc.index = pd.to_datetime(Psuc[time])
Psuc1 = Psuc.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc2 = Psuc.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc3 = Psuc.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc4 = Psuc.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc5 = Psuc.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc6 = Psuc.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc7 = Psuc.loc[velocity7.index[0]:velocity7.index[len(velocity8)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc8 = Psuc.loc[velocity8.index[0]:velocity8.index[len(velocity7)-1],'low_pressure'].apply(lambda x: x * 98.0665)
Psuc_v = Psuc.loc[volume.index[0]:volume.index[len(volume)-1],'low_pressure'].apply(lambda x: x * 98.0665)

Tsuc.index = pd.to_datetime(Tsuc[time])
Tsuc1 = Tsuc.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'suction_temp1']
Tsuc2 = Tsuc.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'suction_temp1']
Tsuc3 = Tsuc.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'suction_temp1']
Tsuc4 = Tsuc.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'suction_temp1']
Tsuc5 = Tsuc.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'suction_temp1']
Tsuc6 = Tsuc.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'suction_temp1']
Tsuc7 = Tsuc.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'suction_temp1']
Tsuc8 = Tsuc.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'suction_temp1']
Tsuc_v = Tsuc.loc[volume.index[0]:volume.index[len(volume)-1],'suction_temp1']

Pdis.index = pd.to_datetime(Pdis[time])
Pdis1 = Pdis.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis2 = Pdis.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis3 = Pdis.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis4 = Pdis.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis5 = Pdis.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis6 = Pdis.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis7 = Pdis.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis8 = Pdis.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'high_pressure'].apply(lambda x: x * 98.0665)
Pdis_v = Pdis.loc[volume.index[0]:volume.index[len(volume)-1],'high_pressure'].apply(lambda x: x * 98.0665)

Tdis['T_dis'] = (Tdis['discharge_temp1'] + Tdis['discharge_temp2']) / 2
Tdis.index = pd.to_datetime(Tdis[time])
Tdis1 = Tdis.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'T_dis']
Tdis2 = Tdis.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'T_dis']
Tdis3 = Tdis.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'T_dis']
Tdis4 = Tdis.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'T_dis']
Tdis5 = Tdis.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'T_dis']
Tdis6 = Tdis.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'T_dis']
Tdis7 = Tdis.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'T_dis']
Tdis8 = Tdis.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'T_dis']
Tdis_v = Tdis.loc[volume.index[0]:volume.index[len(volume)-1],'T_dis']

comp['comp_freq'] = comp.filter(regex='comp_current_freq').mean(axis=1)
comp.index = pd.to_datetime(comp[time])
comp1 = comp.loc[velocity1.index[0]:velocity1.index[len(velocity1)-1],'comp_freq']
comp2 = comp.loc[velocity2.index[0]:velocity2.index[len(velocity2)-1],'comp_freq']
comp3 = comp.loc[velocity3.index[0]:velocity3.index[len(velocity3)-1],'comp_freq']
comp4 = comp.loc[velocity4.index[0]:velocity4.index[len(velocity4)-1],'comp_freq']
comp5 = comp.loc[velocity5.index[0]:velocity5.index[len(velocity5)-1],'comp_freq']
comp6 = comp.loc[velocity6.index[0]:velocity6.index[len(velocity6)-1],'comp_freq']
comp7 = comp.loc[velocity7.index[0]:velocity7.index[len(velocity7)-1],'comp_freq']
comp8 = comp.loc[velocity8.index[0]:velocity8.index[len(velocity8)-1],'comp_freq']
comp_v = comp.loc[volume.index[0]:volume.index[len(volume)-1],'comp_freq']

velocity1 = pd.concat([velocity1, fan1, power1, comp1, Psuc1, Tsuc1, Pdis1, Tdis1],axis=1).dropna()
velocity2 = pd.concat([velocity2, fan2, power2, comp2, Psuc2, Tsuc2, Pdis2, Tdis2],axis=1).dropna()
velocity3 = pd.concat([velocity3, fan3, power3, comp3, Psuc3, Tsuc3, Pdis3, Tdis3],axis=1).dropna()
velocity4 = pd.concat([velocity4, fan4, power4, comp4, Psuc4, Tsuc4, Pdis4, Tdis4],axis=1).dropna()
velocity5 = pd.concat([velocity5, fan5, power5, comp5, Psuc5, Tsuc5, Pdis5, Tdis5],axis=1).dropna()
velocity6 = pd.concat([velocity6, fan6, power6, comp6, Psuc6, Tsuc6, Pdis6, Tdis6],axis=1).dropna()
velocity7 = pd.concat([velocity7, fan7, power7, comp7, Psuc7, Tsuc7, Pdis7, Tdis7],axis=1).dropna()
velocity8 = pd.concat([velocity8, fan8, power8, comp8, Psuc8, Tsuc8, Pdis8, Tdis8],axis=1).dropna()
volume = pd.concat([volume, fan_v, power_v, comp_v, Psuc_v, Tsuc_v, Pdis_v, Tdis_v],axis=1).dropna()

fan = pd.concat([velocity1['fan_step'], velocity2['fan_step'], velocity3['fan_step'], velocity4['fan_step'], velocity5['fan_step'], velocity6['fan_step'], velocity7['fan_step'], velocity8['fan_step'], volume['fan_step']])
power = pd.concat([velocity1['value'], velocity2['value'], velocity3['value'], velocity4['value'], velocity5['value'], velocity6['value'], velocity7['value'], velocity8['value'], volume['value']])
comp = pd.concat([velocity1['comp_freq'], velocity2['comp_freq'], velocity3['comp_freq'], velocity4['comp_freq'], velocity5['comp_freq'], velocity6['comp_freq'], velocity7['comp_freq'], velocity8['comp_freq'], volume['comp_freq']])
Psuc = pd.concat([velocity1['low_pressure'], velocity2['low_pressure'], velocity3['low_pressure'], velocity4['low_pressure'], velocity5['low_pressure'], velocity6['low_pressure'], velocity7['low_pressure'], velocity8['low_pressure'], volume['low_pressure']])
Tsuc = pd.concat([velocity1['suction_temp1'], velocity2['suction_temp1'], velocity3['suction_temp1'], velocity4['suction_temp1'], velocity5['suction_temp1'], velocity6['suction_temp1'], velocity7['suction_temp1'], velocity8['suction_temp1'], volume['suction_temp1']])
Pdis = pd.concat([velocity1['high_pressure'], velocity2['high_pressure'], velocity3['high_pressure'], velocity4['high_pressure'], velocity5['high_pressure'], velocity6['high_pressure'], velocity7['high_pressure'], velocity8['high_pressure'], volume['high_pressure']])
Tdis = pd.concat([velocity1['T_dis'], velocity2['T_dis'], velocity3['T_dis'], velocity4['T_dis'], velocity5['T_dis'], velocity6['T_dis'], velocity7['T_dis'], velocity8['T_dis'], volume['T_dis']])
# fan = pd.concat([velocity1['fan_step'], velocity2['fan_step'], velocity3['fan_step'], volume['fan_step']])
# power = pd.concat([velocity1['value'], velocity2['value'], velocity3['value'], volume['value']])
# comp = pd.concat([velocity1['comp_freq'], velocity2['comp_freq'], velocity3['comp_freq'], volume['comp_freq']])

""" *******************************Compressur frequency range******************************* """
volume['freq'] = pd.cut(volume['comp_freq'],np.arange(0,max(volume['comp_freq'])+10,step=10))
volume_ = volume.groupby(['freq'], as_index=True)['volume'].describe().dropna()

velocity1['freq'] = pd.cut(velocity1['comp_freq'],np.arange(0,max(velocity1['comp_freq'])+10,step=10))
velocity2['freq'] = pd.cut(velocity2['comp_freq'],np.arange(0,max(velocity2['comp_freq'])+10,step=10))
velocity3['freq'] = pd.cut(velocity3['comp_freq'],np.arange(0,max(velocity3['comp_freq'])+10,step=10))
velocity4['freq'] = pd.cut(velocity4['comp_freq'],np.arange(0,max(velocity4['comp_freq'])+10,step=10))
velocity5['freq'] = pd.cut(velocity5['comp_freq'],np.arange(0,max(velocity5['comp_freq'])+10,step=10))
velocity6['freq'] = pd.cut(velocity6['comp_freq'],np.arange(0,max(velocity6['comp_freq'])+10,step=10))
velocity7['freq'] = pd.cut(velocity7['comp_freq'],np.arange(0,max(velocity7['comp_freq'])+10,step=10))
velocity8['freq'] = pd.cut(velocity8['comp_freq'],np.arange(0,max(velocity8['comp_freq'])+10,step=10))

velocity1_ = velocity1.groupby(['freq'], as_index=True)['velocity1'].describe().dropna()
velocity2_ = velocity2.groupby(['freq'], as_index=True)['velocity2'].describe().dropna()
velocity3_ = velocity3.groupby(['freq'], as_index=True)['velocity3'].describe().dropna()
velocity4_ = velocity4.groupby(['freq'], as_index=True)['velocity4'].describe().dropna()
velocity5_ = velocity5.groupby(['freq'], as_index=True)['velocity5'].describe().dropna()
velocity6_ = velocity6.groupby(['freq'], as_index=True)['velocity6'].describe().dropna()
velocity7_ = velocity7.groupby(['freq'], as_index=True)['velocity7'].describe().dropna()
velocity8_ = velocity8.groupby(['freq'], as_index=True)['velocity8'].describe().dropna()
velocity1_mean = velocity1_['mean']
velocity1_std = velocity1_['std']
velocity2_mean = velocity2_['mean']
velocity2_std = velocity2_['std']
velocity3_mean = velocity3_['mean']
velocity3_std = velocity3_['std']
velocity4_mean = velocity4_['mean']
velocity4_std = velocity4_['std']
velocity5_mean = velocity5_['mean']
velocity5_std = velocity5_['std']
velocity6_mean = velocity6_['mean']
velocity6_std = velocity6_['std']
velocity7_mean = velocity7_['mean']
velocity7_std = velocity7_['std']
velocity8_mean = velocity8_['mean']
velocity8_std = velocity8_['std']
asdf = pd.concat([velocity1_mean,velocity2_mean,velocity3_mean,velocity4_mean,velocity5_mean,velocity6_mean,velocity7_mean,velocity8_mean],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
mean_of_velocity = pd.DataFrame()
for i in range(len(asdf)):
    mean_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
asdf = pd.concat([velocity1_std,velocity2_std,velocity3_std,velocity4_std,velocity5_std,velocity6_std,velocity7_std,velocity8_std],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
std_of_velocity = pd.DataFrame()
for i in range(len(asdf)):
    std_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

Psuc1_ = velocity1.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc2_ = velocity2.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc3_ = velocity3.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc4_ = velocity4.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc5_ = velocity5.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc6_ = velocity6.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc7_ = velocity7.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc8_ = velocity8.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psucv_ = volume.groupby(['freq'], as_index=True)['low_pressure'].describe().dropna()
Psuc1_mean = Psuc1_['mean']
Psuc1_std = Psuc1_['std']
Psuc2_mean = Psuc2_['mean']
Psuc2_std = Psuc2_['std']
Psuc3_mean = Psuc3_['mean']
Psuc3_std = Psuc3_['std']
Psuc4_mean = Psuc4_['mean']
Psuc4_std = Psuc4_['std']
Psuc5_mean = Psuc5_['mean']
Psuc5_std = Psuc5_['std']
Psuc6_mean = Psuc6_['mean']
Psuc6_std = Psuc6_['std']
Psuc7_mean = Psuc7_['mean']
Psuc7_std = Psuc7_['std']
Psuc8_mean = Psuc8_['mean']
Psuc8_std = Psuc8_['std']
Psucv_mean = Psucv_['mean']
Psucv_std = Psucv_['std']
asdf = pd.concat([Psuc1_mean,Psuc2_mean,Psuc3_mean,Psuc4_mean,Psuc5_mean,Psuc6_mean,Psuc7_mean,Psuc8_mean,Psucv_mean],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
mean_of_Psuc = pd.DataFrame()
for i in range(len(asdf)):
    mean_of_Psuc[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
asdf = pd.concat([Psuc1_std,Psuc2_std,Psuc3_std,Psuc4_std,Psuc5_std,Psuc6_std,Psuc7_std,Psuc8_std,Psucv_std],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
std_of_Psuc = pd.DataFrame()
for i in range(len(asdf)):
    std_of_Psuc[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

Tsuc1_ = velocity1.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc2_ = velocity2.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc3_ = velocity3.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc4_ = velocity4.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc5_ = velocity5.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc6_ = velocity6.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc7_ = velocity7.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc8_ = velocity8.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsucv_ = volume.groupby(['freq'], as_index=True)['suction_temp1'].describe().dropna()
Tsuc1_mean = Tsuc1_['mean']
Tsuc1_std = Tsuc1_['std']
Tsuc2_mean = Tsuc2_['mean']
Tsuc2_std = Tsuc2_['std']
Tsuc3_mean = Tsuc3_['mean']
Tsuc3_std = Tsuc3_['std']
Tsuc4_mean = Tsuc4_['mean']
Tsuc4_std = Tsuc4_['std']
Tsuc5_mean = Tsuc5_['mean']
Tsuc5_std = Tsuc5_['std']
Tsuc6_mean = Tsuc6_['mean']
Tsuc6_std = Tsuc6_['std']
Tsuc7_mean = Tsuc7_['mean']
Tsuc7_std = Tsuc7_['std']
Tsuc8_mean = Tsuc8_['mean']
Tsuc8_std = Tsuc8_['std']
Tsucv_mean = Tsucv_['mean']
Tsucv_std = Tsucv_['std']
asdf = pd.concat([Tsuc1_mean,Tsuc2_mean,Tsuc3_mean,Tsuc4_mean,Tsuc5_mean,Tsuc6_mean,Tsuc7_mean,Tsuc8_mean,Tsucv_mean],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
mean_of_Tsuc = pd.DataFrame()
for i in range(len(asdf)):
    mean_of_Tsuc[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
asdf = pd.concat([Tsuc1_std,Tsuc2_std,Tsuc3_std,Tsuc4_std,Tsuc5_std,Tsuc6_std,Tsuc7_std,Tsuc8_std,Tsucv_std],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
std_of_Tsuc = pd.DataFrame()
for i in range(len(asdf)):
    std_of_Tsuc[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

Power1_ = velocity1.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power2_ = velocity2.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power3_ = velocity3.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power4_ = velocity4.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power5_ = velocity5.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power6_ = velocity6.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power7_ = velocity7.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power8_ = velocity8.groupby(['freq'], as_index=True)['value'].describe().dropna()
Powerv_ = volume.groupby(['freq'], as_index=True)['value'].describe().dropna()
Power1_mean = Power1_['mean']
Power1_std = Power1_['std']
Power2_mean = Power2_['mean']
Power2_std = Power2_['std']
Power3_mean = Power3_['mean']
Power3_std = Power3_['std']
Power4_mean = Power4_['mean']
Power4_std = Power4_['std']
Power5_mean = Power5_['mean']
Power5_std = Power5_['std']
Power6_mean = Power6_['mean']
Power6_std = Power6_['std']
Power7_mean = Power7_['mean']
Power7_std = Power7_['std']
Power8_mean = Power8_['mean']
Power8_std = Power8_['std']
Powerv_mean = Powerv_['mean']
Powerv_std = Powerv_['std']
asdf = pd.concat([Power1_mean,Power2_mean,Power3_mean,Power4_mean,Power5_mean,Power6_mean,Power7_mean,Power8_mean,Powerv_mean],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
mean_of_Power = pd.DataFrame()
for i in range(len(asdf)):
    mean_of_Power[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
asdf = pd.concat([Power1_std,Power2_std,Power3_std,Power4_std,Power5_std,Power6_std,Power7_std,Power8_std,Powerv_std],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('freq',axis=1)
std_of_Power = pd.DataFrame()
for i in range(len(asdf)):
    std_of_Power[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

# asdf = pd.concat([velocity1_mean,velocity2_mean,velocity3_mean],axis=1)
# index = asdf.index
# asdf = asdf.reset_index().drop('freq',axis=1)
# mean_of_velocity = pd.DataFrame()
# for i in range(len(asdf)):
#     mean_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
#
# asdf = pd.concat([velocity1_std,velocity2_std,velocity3_std],axis=1)
# index = asdf.index
# asdf = asdf.reset_index().drop('freq',axis=1)
# std_of_velocity = pd.DataFrame()
# for i in range(len(asdf)):
#     std_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]


print('{}-{}-{}'.format(year,month,day))
print('Suction pressure mean : {}'.format(mean_of_Psuc.transpose()))
print('Suction pressure stdev : {}'.format(std_of_Psuc.transpose()))
print('Suction temperature mean : {}'.format(mean_of_Tsuc.transpose()))
print('Suction temperature stdev : {}'.format(std_of_Tsuc.transpose()))
print('Power mean : {}'.format(mean_of_Power.transpose()))
print('Power stdev : {}'.format(std_of_Power.transpose()))

""" *******************************Fan step range******************************* """
volume['step'] = pd.cut(volume['fan_step'],np.arange(0,max(volume['fan_step'])+5,step=5))
volume_ = volume.groupby(['step'], as_index=True)['volume'].describe().dropna()

mean_of_volume = volume_['mean']
std_of_volume = volume_['std']

velocity1['step'] = pd.cut(velocity1['fan_step'],np.arange(0,max(velocity1['fan_step'])+5,step=5))
velocity2['step'] = pd.cut(velocity2['fan_step'],np.arange(0,max(velocity2['fan_step'])+5,step=5))
velocity3['step'] = pd.cut(velocity3['fan_step'],np.arange(0,max(velocity3['fan_step'])+5,step=5))
velocity4['step'] = pd.cut(velocity4['fan_step'],np.arange(0,max(velocity4['fan_step'])+5,step=5))
velocity5['step'] = pd.cut(velocity5['fan_step'],np.arange(0,max(velocity5['fan_step'])+5,step=5))
velocity6['step'] = pd.cut(velocity6['fan_step'],np.arange(0,max(velocity6['fan_step'])+5,step=5))
velocity7['step'] = pd.cut(velocity7['fan_step'],np.arange(0,max(velocity7['fan_step'])+5,step=5))
velocity8['step'] = pd.cut(velocity8['fan_step'],np.arange(0,max(velocity8['fan_step'])+5,step=5))


velocity1_ = velocity1.groupby(['step'], as_index=True)['velocity1'].describe().dropna()
velocity2_ = velocity2.groupby(['step'], as_index=True)['velocity2'].describe().dropna()
velocity3_ = velocity3.groupby(['step'], as_index=True)['velocity3'].describe().dropna()
velocity4_ = velocity4.groupby(['step'], as_index=True)['velocity4'].describe().dropna()
velocity5_ = velocity5.groupby(['step'], as_index=True)['velocity5'].describe().dropna()
velocity6_ = velocity6.groupby(['step'], as_index=True)['velocity6'].describe().dropna()
velocity7_ = velocity7.groupby(['step'], as_index=True)['velocity7'].describe().dropna()
velocity8_ = velocity8.groupby(['step'], as_index=True)['velocity8'].describe().dropna()
velocity1_mean = velocity1_['mean']
velocity1_std = velocity1_['std']
velocity2_mean = velocity2_['mean']
velocity2_std = velocity2_['std']
velocity3_mean = velocity3_['mean']
velocity3_std = velocity3_['std']
velocity4_mean = velocity4_['mean']
velocity4_std = velocity4_['std']
velocity5_mean = velocity5_['mean']
velocity5_std = velocity5_['std']
velocity6_mean = velocity6_['mean']
velocity6_std = velocity6_['std']
velocity7_mean = velocity7_['mean']
velocity7_std = velocity7_['std']
velocity8_mean = velocity8_['mean']
velocity8_std = velocity8_['std']
asdf = pd.concat([velocity1_mean,velocity2_mean,velocity3_mean,velocity4_mean,velocity5_mean,velocity6_mean,velocity7_mean,velocity8_mean],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('step',axis=1)
mean_of_velocity = pd.DataFrame()
for i in range(len(asdf)):
    mean_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
asdf = pd.concat([velocity1_std,velocity2_std,velocity3_std,velocity4_std,velocity5_std,velocity6_std,velocity7_std,velocity8_std],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('step',axis=1)
std_of_velocity = pd.DataFrame()
for i in range(len(asdf)):
    std_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

Pdis1_ = velocity1.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis2_ = velocity2.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis3_ = velocity3.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis4_ = velocity4.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis5_ = velocity5.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis6_ = velocity6.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis7_ = velocity7.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis8_ = velocity8.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdisv_ = volume.groupby(['step'], as_index=True)['high_pressure'].describe().dropna()
Pdis1_mean = Pdis1_['mean']
Pdis1_std = Pdis1_['std']
Pdis2_mean = Pdis2_['mean']
Pdis2_std = Pdis2_['std']
Pdis3_mean = Pdis3_['mean']
Pdis3_std = Pdis3_['std']
Pdis4_mean = Pdis4_['mean']
Pdis4_std = Pdis4_['std']
Pdis5_mean = Pdis5_['mean']
Pdis5_std = Pdis5_['std']
Pdis6_mean = Pdis6_['mean']
Pdis6_std = Pdis6_['std']
Pdis7_mean = Pdis7_['mean']
Pdis7_std = Pdis7_['std']
Pdis8_mean = Pdis8_['mean']
Pdis8_std = Pdis8_['std']
Pdisv_mean = Pdisv_['mean']
Pdisv_std = Pdisv_['std']
asdf = pd.concat([Pdis1_mean,Pdis2_mean,Pdis3_mean,Pdis4_mean,Pdis5_mean,Pdis6_mean,Pdis7_mean,Pdis8_mean,Pdisv_mean],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('step',axis=1)
mean_of_Pdis = pd.DataFrame()
for i in range(len(asdf)):
    mean_of_Pdis[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
asdf = pd.concat([Pdis1_std,Pdis2_std,Pdis3_std,Pdis4_std,Pdis5_std,Pdis6_std,Pdis7_std,Pdis8_std,Pdisv_std],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('step',axis=1)
std_of_Pdis = pd.DataFrame()
for i in range(len(asdf)):
    std_of_Pdis[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

Tdis1_ = velocity1.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis2_ = velocity2.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis3_ = velocity3.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis4_ = velocity4.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis5_ = velocity5.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis6_ = velocity6.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis7_ = velocity7.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis8_ = velocity8.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdisv_ = volume.groupby(['step'], as_index=True)['T_dis'].describe().dropna()
Tdis1_mean = Tdis1_['mean']
Tdis1_std = Tdis1_['std']
Tdis2_mean = Tdis2_['mean']
Tdis2_std = Tdis2_['std']
Tdis3_mean = Tdis3_['mean']
Tdis3_std = Tdis3_['std']
Tdis4_mean = Tdis4_['mean']
Tdis4_std = Tdis4_['std']
Tdis5_mean = Tdis5_['mean']
Tdis5_std = Tdis5_['std']
Tdis6_mean = Tdis6_['mean']
Tdis6_std = Tdis6_['std']
Tdis7_mean = Tdis7_['mean']
Tdis7_std = Tdis7_['std']
Tdis8_mean = Tdis8_['mean']
Tdis8_std = Tdis8_['std']
Tdisv_mean = Tdisv_['mean']
Tdisv_std = Tdisv_['std']
asdf = pd.concat([Tdis1_mean,Tdis2_mean,Tdis3_mean,Tdis4_mean,Tdis5_mean,Tdis6_mean,Tdis7_mean,Tdis8_mean,Tdisv_mean],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('step',axis=1)
mean_of_Tdis = pd.DataFrame()
for i in range(len(asdf)):
    mean_of_Tdis[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
asdf = pd.concat([Tdis1_std,Tdis2_std,Tdis3_std,Tdis4_std,Tdis5_std,Tdis6_std,Tdis7_std,Tdis8_std,Tdisv_std],axis=1)
index = asdf.index
asdf = asdf.reset_index().drop('step',axis=1)
std_of_Tdis = pd.DataFrame()
for i in range(len(asdf)):
    std_of_Tdis[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

# asdf = pd.concat([velocity1_mean,velocity2_mean,velocity3_mean],axis=1)
# index = asdf.index
# asdf = asdf.reset_index().drop('freq',axis=1)
# mean_of_velocity = pd.DataFrame()
# for i in range(len(asdf)):
#     mean_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]
#
# asdf = pd.concat([velocity1_std,velocity2_std,velocity3_std],axis=1)
# index = asdf.index
# asdf = asdf.reset_index().drop('freq',axis=1)
# std_of_velocity = pd.DataFrame()
# for i in range(len(asdf)):
#     std_of_velocity[str(index[i])] = [round(asdf.loc[i,:].sum()/asdf.loc[i,:].count(),1)]

print('{}-{}-{}'.format(year,month,day))
print('Air velocity mean : {}'.format(mean_of_velocity.transpose()))
print('Air velocity stdev : {}'.format(std_of_velocity.transpose()))
print('Air volume mean : {}'.format(mean_of_volume.transpose()))
print('Air volume stdev : {}'.format(std_of_volume.transpose()))
print('High pressure mean : {}'.format(mean_of_Pdis.transpose()))
print('High pressure stdev : {}'.format(std_of_Pdis.transpose()))
print('Discharge temperature mean : {}'.format(mean_of_Tdis.transpose()))
print('Discharge temperature stdev : {}'.format(std_of_Tdis.transpose()))
# print('{}-{}-{}'.format(year,month,day))
# print('Air velocity mean : {}'.format((velocity1_mean+velocity2_mean+velocity3_mean)/3))
# print('Air velocity stdev : {}'.format((velocity1_std+velocity2_std+velocity3_std)/3))
# print('Air volume mean : {}'.format(statistics.mean(volume['volume'])))
# print('Air volume stdev : {}'.format(statistics.stdev(volume['volume'])))
# print('Fan step mean : {}'.format(statistics.mean(fan)))
# print('Fan step stdev : {}'.format(statistics.stdev(fan)))
# print('Comp freq mean : {}'.format(statistics.mean(comp)))
# print('Comp freq stdev : {}'.format(statistics.stdev(comp)))
# print('Power mean : {}'.format(statistics.mean(power)))
# print('Power stdev : {}'.format(statistics.stdev(power)))

fig_save = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\probability\{}\{}-{}-{}'.format(unit,year,month,day)
create_folder(fig_save)

x_velocity = np.linspace(-100, 100, 10000)
x_volume = np.linspace(-10000, 10000, 1000000)
x_power = np.linspace(-100, 100, 10000)
x_fan = np.linspace(-100, 100, 10000)
x_comp = np.linspace(-100, 200, 10000)

# #velocity1
# max1 = []
# plt.subplots(figsize=(10, 9))
# for i in range(len(velocity1)):
#     plt.plot(x_velocity, norm.pdf(x_velocity, velocity1['mean'][i], velocity1['std'][i]), linewidth=2, label='{} - mean : {:.2f}, std : {:.2f}'.format(velocity1.index[i],velocity1['mean'][i],velocity1['std'][i]))
#     plt.plot([velocity1['mean'][i], velocity1['mean'][i]], [0, 2], color='r', linestyle='-.', linewidth=2)
#     max1.append(max(norm.pdf(x_velocity, velocity1['mean'][i], velocity1['std'][i])))
# axes = plt.gca()
# axes.set_ylim([0, 4])
# yticks = axes.get_yticks()
# axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# axes.set_xlim([max(velocity1['mean']) - 10, max(velocity1['mean']) + 10])
# xticks = axes.get_xticks()
# axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# plt.ylabel('Probability', fontsize=26, fontweight='bold')
# plt.xlabel('Air velocity [m/s]', fontsize=26, fontweight='bold')
# # axes.text(1, 0.95, 'Mean = {0:.1f}'.format(velocity1_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(velocity1_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# plt.tight_layout()
# plt.legend(fontsize=14)
# # plt.show()
# plt.savefig(fig_save+'/velocity1.png')
#
# #velocity2
# max2 = []
# plt.subplots(figsize=(10, 9))
# for i in range(len(velocity2)):
#     plt.plot(x_velocity, norm.pdf(x_velocity, velocity2['mean'][i], velocity2['std'][i]), linewidth=2, label='{} - mean : {:.2f}, std : {:.2f}'.format(velocity2.index[i],velocity2['mean'][i],velocity2['std'][i]))
#     plt.plot([velocity2['mean'][i], velocity2['mean'][i]], [0, 2], color='r', linestyle='-.', linewidth=2)
#     max2.append(max(norm.pdf(x_velocity, velocity2['mean'][i], velocity2['std'][i])))
# axes = plt.gca()
# axes.set_ylim([0, max(max2) + 0.1])
# yticks = axes.get_yticks()
# axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# axes.set_xlim([max(velocity2['mean']) - 10, max(velocity2['mean']) + 10])
# xticks = axes.get_xticks()
# axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# plt.ylabel('Probability', fontsize=26, fontweight='bold')
# plt.xlabel('Air velocity [m/s]', fontsize=26, fontweight='bold')
# # axes.text(1, 0.95, 'Mean = {0:.1f}'.format(velocity2_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(velocity2_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# plt.tight_layout()
# plt.legend(fontsize=14,loc='upper right')
# # plt.show()
# plt.savefig(fig_save+'/velocity2.png')
#
# #velocity3
# max3 = []
# plt.subplots(figsize=(10, 9))
# for i in range(len(velocity3)):
#     plt.plot(x_velocity, norm.pdf(x_velocity, velocity3['mean'][i], velocity3['std'][i]), linewidth=2, label='{} - mean : {:.2f}, std : {:.2f}'.format(velocity3.index[i],velocity3['mean'][i],velocity3['std'][i]))
#     plt.plot([velocity3['mean'][i], velocity3['mean'][i]], [0, 2], color='r', linestyle='-.', linewidth=2)
#     max3.append(max(norm.pdf(x_velocity, velocity3['mean'][i], velocity3['std'][i])))
# axes = plt.gca()
# axes.set_ylim([0, max(max3) + 0.1])
# yticks = axes.get_yticks()
# axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# axes.set_xlim([max(velocity3['mean']) - 10, max(velocity3['mean']) + 10])
# xticks = axes.get_xticks()
# axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# plt.ylabel('Probability', fontsize=26, fontweight='bold')
# plt.xlabel('Air velocity [m/s]', fontsize=26, fontweight='bold')
# # axes.text(1, 0.95, 'Mean = {0:.1f}'.format(velocity3_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(velocity3_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# plt.tight_layout()
# plt.legend(fontsize=14)
# # plt.show()
# plt.savefig(fig_save+'/velocity3.png')
#
# # # #velocity4
# # max4 = []
# # plt.subplots(figsize=(10, 9))
# # for i in range(len(velocity4)):
# #     plt.plot(x_velocity, norm.pdf(x_velocity, velocity4['mean'][i], velocity4['std'][i]), linewidth=2, label='{} - mean : {:.2f}, std : {:.2f}'.format(velocity4.index[i],velocity4['mean'][i],velocity4['std'][i]))
# #     plt.plot([velocity4['mean'][i], velocity4['mean'][i]], [0, 2], color='r', linestyle='-.', linewidth=2)
# #     max4.append(max(norm.pdf(x_velocity, velocity4['mean'][i], velocity4['std'][i])))
# # axes = plt.gca()
# # axes.set_ylim([0, max(max4) + 0.1])
# # yticks = axes.get_yticks()
# # axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# # axes.set_xlim([max(velocity4['mean']) - 10, max(velocity4['mean']) + 10])
# # xticks = axes.get_xticks()
# # axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# # plt.ylabel('Probability', fontsize=26, fontweight='bold')
# # plt.xlabel('Air velocity [m/s]', fontsize=26, fontweight='bold')
# # # axes.text(1, 0.95, 'Mean = {0:.1f}'.format(velocity4_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # # axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(velocity4_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # plt.tight_layout()
# # plt.legend(fontsize=14)
# # # plt.show()
# # plt.savefig(fig_save+'/velocity4.png')
# # #
# # # #velocity5
# # max5 = []
# # plt.subplots(figsize=(10, 9))
# # for i in range(len(velocity5)):
# #     plt.plot(x_velocity, norm.pdf(x_velocity, velocity5['mean'][i], velocity5['std'][i]), linewidth=2, label='{} - mean : {:.2f}, std : {:.2f}'.format(velocity5.index[i],velocity5['mean'][i],velocity5['std'][i]))
# #     plt.plot([velocity5['mean'][i], velocity5['mean'][i]], [0, 2], color='r', linestyle='-.', linewidth=2)
# #     max5.append(max(norm.pdf(x_velocity, velocity5['mean'][i], velocity5['std'][i])))
# # axes = plt.gca()
# # axes.set_ylim([0, max(max5) + 0.1])
# # yticks = axes.get_yticks()
# # axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# # axes.set_xlim([max(velocity5['mean']) - 10, max(velocity5['mean']) + 10])
# # xticks = axes.get_xticks()
# # axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# # plt.ylabel('Probability', fontsize=26, fontweight='bold')
# # plt.xlabel('Air velocity [m/s]', fontsize=26, fontweight='bold')
# # # axes.text(1, 0.95, 'Mean = {0:.1f}'.format(velocity5_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # # axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(velocity5_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # plt.tight_layout()
# # plt.legend(fontsize=14)
# # # plt.show()
# # plt.savefig(fig_save+'/velocity5.png')
# # #
# # # #velocity6
# # max6 = []
# # plt.subplots(figsize=(10, 9))
# # for i in range(len(velocity6)):
# #     plt.plot(x_velocity, norm.pdf(x_velocity, velocity6['mean'][i], velocity6['std'][i]), linewidth=2, label='{} - mean : {:.2f}, std : {:.2f}'.format(velocity6.index[i],velocity6['mean'][i],velocity6['std'][i]))
# #     plt.plot([velocity6['mean'][i], velocity6['mean'][i]], [0, 2], color='r', linestyle='-.', linewidth=2)
# #     max6.append(max(norm.pdf(x_velocity, velocity6['mean'][i], velocity6['std'][i])))
# # axes = plt.gca()
# # axes.set_ylim([0, max(max6) + 0.1])
# # yticks = axes.get_yticks()
# # axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# # axes.set_xlim([max(velocity6['mean']) - 10, max(velocity6['mean']) + 10])
# # xticks = axes.get_xticks()
# # axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# # plt.ylabel('Probability', fontsize=26, fontweight='bold')
# # plt.xlabel('Air velocity [m/s]', fontsize=26, fontweight='bold')
# # # axes.text(1, 0.95, 'Mean = {0:.1f}'.format(velocity6_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # # axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(velocity6_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # plt.tight_layout()
# # plt.legend(fontsize=14)
# # # plt.show()
# # plt.savefig(fig_save+'/velocity6.png')
#
# #volume
# maxv = []
# plt.subplots(figsize=(10, 9))
# for i in range(len(volume)):
#     plt.plot(x_volume, norm.pdf(x_volume, volume['mean'][i], volume['std'][i]), linewidth=2, label='{} - mean : {:.2f}, std : {:.2f}'.format(volume.index[i],volume['mean'][i],volume['std'][i]))
#     plt.plot([volume['mean'][i], volume['mean'][i]], [0, 2], color='r', linestyle='-.', linewidth=2)
#     maxv.append(max(norm.pdf(x_volume, volume['mean'][i], volume['std'][i])))
# axes = plt.gca()
# axes.set_ylim([0, max(maxv) + 0.0001])
# yticks = axes.get_yticks()
# axes.set_yticklabels([round(yticks[i], 4) for i in range(len(yticks))], fontsize=24)
# axes.set_xlim([max(volume['mean']) - 5000, max(volume['mean']) + 5000])
# xticks = axes.get_xticks()
# axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# plt.ylabel('Probability', fontsize=26, fontweight='bold')
# plt.xlabel('Air velocity [m/s]', fontsize=26, fontweight='bold')
# # axes.text(1, 0.95, 'Mean = {0:.1f}'.format(volume_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# # axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(volume_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# plt.tight_layout()
# plt.legend(fontsize=14)
# # plt.show()
# plt.savefig(fig_save+'/volume.png')
#
# #power
# plt.subplots(figsize=(10, 9))
# plt.plot(x_power, norm.pdf(x_power, power_mean, power_std), color='k', linewidth=2)
# plt.plot([power_mean, power_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
# axes = plt.gca()
# axes.set_ylim([0, max(norm.pdf(x_volume, power_mean, power_std)) + 0.05])
# yticks = axes.get_yticks()
# axes.set_yticklabels([round(yticks[i], 5) for i in range(len(yticks))], fontsize=24)
# axes.set_xlim([power_mean - 20, power_mean + 20])
# xticks = axes.get_xticks()
# axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# plt.ylabel('Probability', fontsize=26, fontweight='bold')
# plt.xlabel('Power [kW]', fontsize=26, fontweight='bold')
# axes.text(1, 0.95, 'Mean = {0:.1f}'.format(power_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# axes.text(1, 0.90, 'Stdev = {0:.1f}'.format(power_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
#
# plt.tight_layout()
# # plt.show()
# plt.savefig(fig_save+'/power.png')
#
# #fan
# plt.subplots(figsize=(10, 9))
# plt.plot(x_fan, norm.pdf(x_fan, fan_mean, fan_std), color='k', linewidth=2)
# plt.plot([fan_mean, fan_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
# axes = plt.gca()
# axes.set_ylim([0, max(norm.pdf(x_fan, fan_mean, fan_std)) + 0.05])
# yticks = axes.get_yticks()
# axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# axes.set_xlim([fan_mean - 30, fan_mean + 30])
# xticks = axes.get_xticks()
# axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# plt.ylabel('Probability', fontsize=26, fontweight='bold')
# plt.xlabel('Fan step [step]', fontsize=26, fontweight='bold')
# axes.text(1, 0.95, 'Mean = {0:.0f}'.format(fan_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# axes.text(1, 0.90, 'Stdev = {0:.0f}'.format(fan_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# plt.tight_layout()
# # plt.show()
# plt.savefig(fig_save+'/fanstep.png')
#
# #comp
# plt.subplots(figsize=(10, 9))
# plt.plot(x_comp, norm.pdf(x_comp, comp_mean, comp_std), color='k', linewidth=2)
# plt.plot([comp_mean, comp_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
# axes = plt.gca()
# axes.set_ylim([0, max(norm.pdf(x_comp, comp_mean, comp_std)) + 0.05])
# yticks = axes.get_yticks()
# axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
# axes.set_xlim([fan_mean - 60, fan_mean + 100])
# xticks = axes.get_xticks()
# axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
# plt.ylabel('Probability', fontsize=26, fontweight='bold')
# plt.xlabel('Frequency [Hz]', fontsize=26, fontweight='bold')
# axes.text(1, 0.95, 'Mean = {0:.0f}'.format(comp_mean), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# axes.text(1, 0.90, 'Stdev = {0:.0f}'.format(comp_std), horizontalalignment='right',fontsize=22, color='k',fontdict={'weight':'bold'},transform=axes.transAxes,)
# plt.tight_layout()
# # plt.show()
# plt.savefig(fig_save+'/comp.png')