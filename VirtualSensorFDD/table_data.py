import pandas as pd
import statistics
import CoolProp as CP


def Tsat(high_p,low_p,power):
    T_c = []
    T_e = []
    P_dis = high_p
    P_suc = low_p
    for i in range(len(power)):
        T_c.append(CP.CoolProp.PropsSI('T', 'P', P_dis[i] * 98.0665 * 1000, 'Q', 0.5, 'R410A') - 273.15)
        T_e.append(CP.CoolProp.PropsSI('T', 'P', P_suc[i] * 98.0665 * 1000, 'Q', 0.5, 'R410A') - 273.15)
    return T_c, T_e


data_point = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-02\point_time_side.csv')
power = pd.read_csv(
    r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2021-08-02\outdoor_02_3069.csv')
normal = data_point['nolayer']
low = data_point['lowlevel']
high = data_point['highlevel']
normal_finish = data_point['nolayer_finish']
low_finish = data_point['lowlevel_finish']
high_finish = data_point['highlevel_finish']

freq1 = power['comp_current_frequency1']
freq2 = power['comp_current_frequency2']
oat = power['outdoor_temperature']
high_p = power['high_pressure']
low_p = power['low_pressure']
T_c, T_e = Tsat(high_p,low_p,power)

for i in range(len(power)):
    high_p[i] = high_p[i] * 98.0665
    low_p[i] = low_p[i] * 98.0665

print(data_point)
normal_index = []
low_index = []
high_index = []
normal_finish_index = []
low_finish_index = []
high_finish_index = []

power_index = []
power_finish = []
power_index_low = []
power_finish_low = []
power_index_high = []
power_finish_high = []


for i in range(len(power)):
    for j in range(len(data_point)):
        if power['Time'][i] == normal_finish[j][0:5] + ':00':
            power_finish.append(i)
        elif power['Time'][i] == normal[j][0:5] + ':00':
            power_index.append(i)
        elif power['Time'][i] == low_finish[j][0:5] + ':00':
            power_finish_low.append(i)
        elif power['Time'][i] == low[j][0:5] + ':00':
            power_index_low.append(i)
        elif power['Time'][i] == high[j][0:5] + ':00':
            power_index_high.append(i)
        elif power['Time'][i] == high_finish[j][0:5] + ':00':
            power_finish_high.append(i)

print(power_index)
print(power_finish)
print(power_index_low)
print(power_finish_low)
print(power_index_high)
print(power_finish_high)

k = 0
try:
    print('Experiment 1: frequency 1 mean = {}'.format(statistics.mean(freq1[power_index[k]:power_finish[k-1]])))
    print('Experiment 1: frequency 2 mean = {}'.format(statistics.mean(freq2[power_index[k]:power_finish[k-1]])))
    print('Experiment 1: OAT mean = {}'.format(statistics.mean(oat[power_index[k]:power_finish[k-1]])))
    print('Experiment 1: High pressure mean = {}'.format(statistics.mean(high_p[power_index[k]:power_finish[k-1]])))
    print('Experiment 1: Low pressure mean = {}'.format(statistics.mean(low_p[power_index[k]:power_finish[k-1]])))
    print('Experiment 1: condenser temp mean = {}'.format(statistics.mean(T_c[power_index[k]:power_finish[k-1]])))
    print('Experiment 1: Evaporator temp mean = {}'.format(statistics.mean(T_e[power_index[k]:power_finish[k-1]])))
    print('\n')
except:
    pass

try:
    print('Experiment 2: frequency 1 mean = {}'.format(statistics.mean(freq1[power_index_low[k]:power_finish_low[k-1]])))
    print('Experiment 2: frequency 2 mean = {}'.format(statistics.mean(freq2[power_index_low[k]:power_finish_low[k-1]])))
    print('Experiment 2: OAT mean = {}'.format(statistics.mean(oat[power_index_low[k]:power_finish_low[k-1]])))
    print('Experiment 2: High pressure mean = {}'.format(statistics.mean(high_p[power_index_low[k]:power_finish_low[k-1]])))
    print('Experiment 2: Low pressure mean = {}'.format(statistics.mean(low_p[power_index_low[k]:power_finish_low[k-1]])))
    print('Experiment 2: condenser temp mean = {}'.format(statistics.mean(T_c[power_index_low[k]:power_finish_low[k-1]])))
    print('Experiment 2: Evaporator temp mean = {}'.format(statistics.mean(T_e[power_index_low[k]:power_finish_low[k-1]])))
    print('\n')
except:
    pass

try:
    print('Experiment 3: frequency 1 mean = {}'.format(statistics.mean(freq1[power_index_high[k]:power_finish_high[k-1]])))
    print('Experiment 3: frequency 2 mean = {}'.format(statistics.mean(freq2[power_index_high[k]:power_finish_high[k-1]])))
    print('Experiment 3: OAT mean = {}'.format(statistics.mean(oat[power_index_high[k]:power_finish_high[k-1]])))
    print('Experiment 3: High pressure mean = {}'.format(statistics.mean(high_p[power_index_high[k]:power_finish_high[k-1]])))
    print('Experiment 3: Low pressure mean = {}'.format(statistics.mean(low_p[power_index_high[k]:power_finish_high[k-1]])))
    print('Experiment 3: condenser temp mean = {}'.format(statistics.mean(T_c[power_index_high[k]:power_finish_high[k-1]])))
    print('Experiment 3: Evaporator temp mean = {}'.format(statistics.mean(T_e[power_index_high[k]:power_finish_high[k-1]])))
except:
    pass
