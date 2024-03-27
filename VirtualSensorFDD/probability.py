import pandas as pd
import statistics
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from scipy.stats import norm
import os


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


year = '2022'
month = '01'
day = '19'
unit = '3069'

if len(month) == 1:
    month = '0' + month
if len(day) == 1:
    day = '0' + day

temp = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\{}{} temp2.csv'.format(year,month, day, month, day), engine='python').fillna(method='bfill').fillna(method='ffill')
flow = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\{}{} flow2.csv'.format(year,month, day, month, day), engine='python').fillna(method='bfill').fillna(method='ffill')
volume = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\{}{} volume2.csv'.format(year,month, day, month, day), engine='python').fillna(method='bfill').fillna(method='ffill')
data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\{}-{}-{}\outdoor_{}.csv'.format(year,month, day,unit))

temp['updated_time'] = temp['Date'] + ' ' + temp['Time']
flow['updated_time'] = temp['Date'] + ' ' + flow['Time1']
volume['updated_time'] = temp['Date'] + ' ' + volume['Time']
flow['flow1'] = flow.filter(regex='velocity1').mean(axis=1)
flow['flow2'] = flow.filter(regex='velocity2').mean(axis=1)
flow['flow3'] = flow.filter(regex='velocity3').mean(axis=1)
flow['flow4'] = flow.filter(regex='velocity4').mean(axis=1)
flow['flow5'] = flow.filter(regex='velocity5').mean(axis=1)
flow['flow6'] = flow.filter(regex='velocity6').mean(axis=1)
volume['flow'] = flow.filter(regex='volume').mean(axis=1)
data['freq'] = data.filter(regex='comp_current_frequency').mean(axis=1)

temp.index = pd.to_datetime(temp['updated_time'])
temp.drop('updated_time', inplace=True, axis=1)
side_temp = temp.side_temp.resample('1T').mean().apply(lambda x: None if x < -20 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
upper_temp = temp.upper_temp.resample('1T').mean().apply(lambda x: None if x < -20 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')

flow.index = pd.to_datetime(flow['updated_time'])
flow.drop('updated_time', inplace=True, axis=1)
flow = flow.flow.resample('1T').mean().apply(lambda x: None if x < 0 else x).fillna(method='bfill').fillna(method='ffill')

volume.index = pd.to_datetime(volume['updated_time'])
volume.drop('updated_time', inplace=True, axis=1)
volume = volume.volume.resample('1T').mean().apply(lambda x: None if x < 0 else x).fillna(method='bfill').fillna(method='ffill')

data.index = pd.to_datetime(data['updated_time'])
power = data.loc[side_temp.index[0]:side_temp.index[len(side_temp)-1],'value'].apply(lambda x: -x if x<0 else x)
fan = data.loc[side_temp.index[0]:side_temp.index[len(side_temp)-1],'fan_step']
freq = data.loc[side_temp.index[0]:side_temp.index[len(side_temp)-1],'freq']

side_temp_mean = statistics.mean(side_temp)
upper_temp_mean = statistics.mean(upper_temp)
velocity_mean = statistics.mean(flow)
volume_mean = statistics.mean(volume)
power_mean = statistics.mean(power)
fan_mean = statistics.mean(fan)
freq_mean = statistics.mean(freq)

side_temp_stdev = statistics.stdev(side_temp)
upper_temp_stdev = statistics.stdev(upper_temp)
velocity_stdev = statistics.stdev(flow)
volume_stdev = statistics.stdev(volume)
power_stdev = statistics.stdev(power)
fan_stdev = statistics.stdev(fan)
freq_stdev = statistics.stdev(freq)

fig_save = r'C:\Users\com\Desktop\samsung\Experiment\probability\{}-{}-{}'.format(year,month,day)
create_folder(fig_save)

#side_temp
x = np.linspace(-100, 200, 10000)
plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, side_temp_mean, side_temp_stdev), color='r', linewidth=2)
plt.plot([side_temp_mean, side_temp_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, side_temp_mean, side_temp_stdev)) + 0.05])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([side_temp_mean - 10, side_temp_mean + 10])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Inlet temperature [C]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.savefig(fig_save+'/side_temperature.png')
# plt.show()

#upper_temp
x = np.linspace(-100, 200, 10000)
plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, upper_temp_mean, upper_temp_stdev), color='r', linewidth=2)
plt.plot([upper_temp_mean, upper_temp_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, upper_temp_mean, upper_temp_stdev)) + 0.05])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([upper_temp_mean - 10, upper_temp_mean + 10])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Outlet temperature [C]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.savefig(fig_save+'/upper_temperature.png')
# plt.show()

#velocity
x = np.linspace(-100, 200, 10000)
plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, velocity_mean, velocity_stdev), color='r', linewidth=2)
plt.plot([velocity_mean, velocity_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, velocity_mean, velocity_stdev)) + 0.05])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([velocity_mean - 10, velocity_mean + 10])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Velocity [m/s]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.savefig(fig_save+'/velocity.png')
# plt.show()

#volume
x = np.linspace(-10000, 10000, 100000)
plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, volume_mean, volume_stdev), color='r', linewidth=2)
plt.plot([volume_mean, volume_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, volume_mean, volume_stdev)) + 0.05])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([volume_mean - 5000, volume_mean + 5000])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Volume [$m^3/h$]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.savefig(fig_save+'/volume.png')
# plt.show()

#power
x = np.linspace(-10000, 10000, 100000)
plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, power_mean, power_stdev), color='r', linewidth=2)
plt.plot([power_mean, power_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, power_mean, power_stdev)) + 0.05])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([power_mean - 5000, power_mean + 5000])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Power [W]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.savefig(fig_save+'/power.png')
# plt.show()

#fan
x = np.linspace(-100, 200, 100000)
plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, fan_mean, fan_stdev), color='r', linewidth=2)
plt.plot([fan_mean, fan_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, fan_mean, fan_stdev)) + 0.05])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([fan_mean - 20, fan_mean + 20])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Fan step [step]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.savefig(fig_save+'/fan.png')
# plt.show()

#freq
x = np.linspace(-100, 200, 100000)
plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, freq_mean, freq_stdev), color='r', linewidth=2)
plt.plot([freq_mean, freq_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, freq_mean, freq_stdev)) + 0.05])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([freq_mean - 20, freq_mean + 20])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Freq [Hz]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.savefig(fig_save+'/freq.png')
# plt.show()

print('{}/{}'.format(month,day))
print('side temperature mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(side_temp),statistics.stdev(side_temp)))
print('upper temperature mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(upper_temp),statistics.stdev(upper_temp)))
print('velocity mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(flow),statistics.stdev(flow)))
print('volume mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(volume),statistics.stdev(volume)))
print('power mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(power),statistics.stdev(power)))
print('fan step mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(fan),statistics.stdev(fan)))
print('freq mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(freq),statistics.stdev(freq)))

f = open(fig_save+'/text.txt'.format(month+day,unit), 'w')
f.write('{}/{}'.format(month,day))
f.write('\n')
f.write('side temperature mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(side_temp),statistics.stdev(side_temp)))
f.write('\n')
f.write('upper temperature mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(upper_temp),statistics.stdev(upper_temp)))
f.write('\n')
f.write('velocity mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(flow),statistics.stdev(flow)))
f.write('\n')
f.write('volume mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(volume),statistics.stdev(volume)))
f.write('\n')
f.write('power mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(power),statistics.stdev(power)))
f.write('\n')
f.write('fan step mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(fan),statistics.stdev(fan)))
f.write('\n')
f.write('freq mean : {:.1f}, stdev : {:.1f}'.format(statistics.mean(freq),statistics.stdev(freq)))
f.close()
