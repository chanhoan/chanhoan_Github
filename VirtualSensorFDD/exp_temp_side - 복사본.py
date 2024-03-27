import matplotlib.pyplot as plt
import CoolProp as CP
import datetime as dt
import numpy as np
import pandas as pd
import collections
import itertools
import os
import statistics
import datetime

# month = str(datetime.datetime.today().month)
# day = str(datetime.datetime.today().day)
month = '02'
day = '22'

if len(month) == 1:
    month = '0' + month
if len(day) == 1:
    day = '0' + day

data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\{}{} temp.csv'.format(month, day, month, day), engine='python').fillna(method='bfill').fillna(method='ffill')
power = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data\2022-{}-{}\outdoor_3069.csv'.format(month, day))

# data['Date'] + ' ' +
data['updated_time'] = data['Time']

print(data)

y1 = data[['updated_time', 'point1']]
y2 = data[['updated_time', 'point2']]
y3 = data[['updated_time', 'point3']]
y4 = data[['updated_time', 'point4']]
y5 = data[['updated_time', 'point5']]
y6 = data[['updated_time', 'point6']]
y7 = data[['updated_time', 'point7']]
y8 = data[['updated_time', 'point8']]
y9 = data[['updated_time', 'point9']]
y10 = data[['updated_time', 'point10']]
y11 = data[['updated_time', 'point11']]
y12 = data[['updated_time', 'point12']]
y13 = data[['updated_time', 'point13']]
y14 = data[['updated_time', 'point14']]
y15 = data[['updated_time', 'point15']]
y16 = data[['updated_time', 'point16']]
y17 = data[['updated_time', 'point17']]
y18 = data[['updated_time', 'point18']]
y19 = data[['updated_time', 'point19']]
y20 = data[['updated_time', 'point20']]
y21 = data[['updated_time', 'point21']]
y22 = data[['updated_time', 'point22']]
y23 = data[['updated_time', 'point23']]
y24 = data[['updated_time', 'point24']]
y25 = data[['updated_time', 'point25']]
y26 = data[['updated_time', 'point26']]
y27 = data[['updated_time', 'point27']]
y28 = data[['updated_time', 'point28']]
y29 = data[['updated_time', 'point29']]
y30 = data[['updated_time', 'point30']]
y31 = data[['updated_time', 'point31']]
y32 = data[['updated_time', 'point32']]
y33 = data[['updated_time', 'point33']]
y34 = data[['updated_time', 'point34']]
y35 = data[['updated_time', 'point35']]
y36 = data[['updated_time', 'point36']]
y37 = data[['updated_time', 'point37']]
y38 = data[['updated_time', 'point38']]
y39 = data[['updated_time', 'point39']]
y40 = data[['updated_time', 'point40']]
# y41 = data[['updated_time', 'point41']]
# y42 = data[['updated_time', 'point42']]
# y43 = data[['updated_time', 'point43']]
# y44 = data[['updated_time', 'point44']]
# y45 = data[['updated_time', 'point45']]
# y46 = data[['updated_time', 'point46']]
# y47 = data[['updated_time', 'point47']]
# y48 = data[['updated_time', 'point48']]
# y49 = data[['updated_time', 'point49']]
# y50 = data[['updated_time', 'point50']]
# y51 = data[['updated_time', 'point51']]
# y52 = data[['updated_time', 'point52']]

y1.index = pd.to_datetime(y1['updated_time'])
y1.drop('updated_time', inplace=True, axis=1)
y1 = y1.point1.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y2.index = pd.to_datetime(y2['updated_time'])
y2.drop('updated_time', inplace=True, axis=1)
y2 = y2.point2.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y3.index = pd.to_datetime(y3['updated_time'])
y3.drop('updated_time', inplace=True, axis=1)
y3 = y3.point3.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y4.index = pd.to_datetime(y4['updated_time'])
y4.drop('updated_time', inplace=True, axis=1)
y4 = y4.point4.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y5.index = pd.to_datetime(y5['updated_time'])
y5.drop('updated_time', inplace=True, axis=1)
y5 = y5.point5.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y6.index = pd.to_datetime(y6['updated_time'])
y6.drop('updated_time', inplace=True, axis=1)
y6 = y6.point6.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y7.index = pd.to_datetime(y7['updated_time'])
y7.drop('updated_time', inplace=True, axis=1)
y7 = y7.point7.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y8.index = pd.to_datetime(y8['updated_time'])
y8.drop('updated_time', inplace=True, axis=1)
y8 = y8.point8.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y9.index = pd.to_datetime(y9['updated_time'])
y9.drop('updated_time', inplace=True, axis=1)
y9 = y9.point9.resample('1T').mean().apply(lambda x: None if x < 20 or x > 55 else x).fillna(method='bfill').fillna(method='ffill')
y10.index = pd.to_datetime(y10['updated_time'])
y10.drop('updated_time', inplace=True, axis=1)
y10 = y10.point10.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y11.index = pd.to_datetime(y11['updated_time'])
y11.drop('updated_time', inplace=True, axis=1)
y11 = y11.point11.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y12.index = pd.to_datetime(y12['updated_time'])
y12.drop('updated_time', inplace=True, axis=1)
y12 = y12.point12.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y13.index = pd.to_datetime(y13['updated_time'])
y13.drop('updated_time', inplace=True, axis=1)
y13 = y13.point13.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y14.index = pd.to_datetime(y14['updated_time'])
y14.drop('updated_time', inplace=True, axis=1)
y14 = y14.point14.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y15.index = pd.to_datetime(y15['updated_time'])
y15.drop('updated_time', inplace=True, axis=1)
y15 = y15.point15.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y16.index = pd.to_datetime(y16['updated_time'])
y16.drop('updated_time', inplace=True, axis=1)
y16 = y16.point16.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y17.index = pd.to_datetime(y17['updated_time'])
y17.drop('updated_time', inplace=True, axis=1)
y17 = y17.point17.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y18.index = pd.to_datetime(y18['updated_time'])
y18.drop('updated_time', inplace=True, axis=1)
y18 = y18.point18.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y19.index = pd.to_datetime(y19['updated_time'])
y19.drop('updated_time', inplace=True, axis=1)
y19 = y19.point19.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y20.index = pd.to_datetime(y20['updated_time'])
y20.drop('updated_time', inplace=True, axis=1)
y20 = y20.point20.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y21.index = pd.to_datetime(y21['updated_time'])
y21.drop('updated_time', inplace=True, axis=1)
y21 = y21.point21.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y22.index = pd.to_datetime(y22['updated_time'])
y22.drop('updated_time', inplace=True, axis=1)
y22 = y22.point22.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y23.index = pd.to_datetime(y23['updated_time'])
y23.drop('updated_time', inplace=True, axis=1)
y23 = y23.point23.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y24.index = pd.to_datetime(y24['updated_time'])
y24.drop('updated_time', inplace=True, axis=1)
y24 = y24.point24.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y25.index = pd.to_datetime(y25['updated_time'])
y25.drop('updated_time', inplace=True, axis=1)
y25 = y25.point25.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y26.index = pd.to_datetime(y26['updated_time'])
y26.drop('updated_time', inplace=True, axis=1)
y26 = y26.point26.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y27.index = pd.to_datetime(y27['updated_time'])
y27.drop('updated_time', inplace=True, axis=1)
y27 = y27.point27.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y28.index = pd.to_datetime(y28['updated_time'])
y28.drop('updated_time', inplace=True, axis=1)
y28 = y28.point28.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y29.index = pd.to_datetime(y29['updated_time'])
y29.drop('updated_time', inplace=True, axis=1)
y29 = y29.point29.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y30.index = pd.to_datetime(y30['updated_time'])
y30.drop('updated_time', inplace=True, axis=1)
y30 = y30.point30.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y31.index = pd.to_datetime(y31['updated_time'])
y31.drop('updated_time', inplace=True, axis=1)
y31 = y31.point31.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y32.index = pd.to_datetime(y32['updated_time'])
y32.drop('updated_time', inplace=True, axis=1)
y32 = y32.point32.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y33.index = pd.to_datetime(y33['updated_time'])
y33.drop('updated_time', inplace=True, axis=1)
y33 = y33.point33.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y34.index = pd.to_datetime(y34['updated_time'])
y34.drop('updated_time', inplace=True, axis=1)
y34 = y34.point34.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y35.index = pd.to_datetime(y35['updated_time'])
y35.drop('updated_time', inplace=True, axis=1)
y35 = y35.point35.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y36.index = pd.to_datetime(y36['updated_time'])
y36.drop('updated_time', inplace=True, axis=1)
y36 = y36.point36.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y37.index = pd.to_datetime(y37['updated_time'])
y37.drop('updated_time', inplace=True, axis=1)
y37 = y37.point37.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y38.index = pd.to_datetime(y38['updated_time'])
y38.drop('updated_time', inplace=True, axis=1)
y38 = y38.point38.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y39.index = pd.to_datetime(y39['updated_time'])
y39.drop('updated_time', inplace=True, axis=1)
y39 = y39.point39.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
y40.index = pd.to_datetime(y40['updated_time'])
y40.drop('updated_time', inplace=True, axis=1)
y40 = y40.point40.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y41.index = pd.to_datetime(y41['updated_time'])
# y41.drop('updated_time', inplace=True, axis=1)
# y41 = y41.point41.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y42.index = pd.to_datetime(y42['updated_time'])
# y42.drop('updated_time', inplace=True, axis=1)
# y42 = y42.point42.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y43.index = pd.to_datetime(y43['updated_time'])
# y43.drop('updated_time', inplace=True, axis=1)
# y43 = y43.point43.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y44.index = pd.to_datetime(y44['updated_time'])
# y44.drop('updated_time', inplace=True, axis=1)
# y44 = y44.point44.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y45.index = pd.to_datetime(y45['updated_time'])
# y45.drop('updated_time', inplace=True, axis=1)
# y45 = y45.point45.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y46.index = pd.to_datetime(y46['updated_time'])
# y46.drop('updated_time', inplace=True, axis=1)
# y46 = y46.point46.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y47.index = pd.to_datetime(y47['updated_time'])
# y47.drop('updated_time', inplace=True, axis=1)
# y47 = y47.point47.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y48.index = pd.to_datetime(y48['updated_time'])
# y48.drop('updated_time', inplace=True, axis=1)
# y48 = y48.point48.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y49.index = pd.to_datetime(y49['updated_time'])
# y49.drop('updated_time', inplace=True, axis=1)
# y49 = y49.point49.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y50.index = pd.to_datetime(y50['updated_time'])
# y50.drop('updated_time', inplace=True, axis=1)
# y50 = y50.point50.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y51.index = pd.to_datetime(y51['updated_time'])
# y51.drop('updated_time', inplace=True, axis=1)
# y51 = y51.point51.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')
# y52.index = pd.to_datetime(y52['updated_time'])
# y52.drop('updated_time', inplace=True, axis=1)
# y52 = y52.point52.resample('1T').mean().apply(lambda x: None if x < -10 or x > 15 else x).fillna(method='bfill').fillna(method='ffill')

 # y41, y42,
#                      y43, y44, y45, y46, y47, y48, y49, y50,y51, y52
overall = pd.concat([y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22,
                     y23, y24, y25, y26, y27, y28, y29, y30, y31, y32, y33, y34, y35, y36, y37, y38, y39, y40,], axis=1).to_csv('./temp_resample_side.csv')

power.index = pd.to_datetime(power['updated_time'])
power = power.loc[y1.index[0]:y1.index[len(y1) - 1], 'value']

# print(statistics.mean([statistics.mean(y1), statistics.mean(y2), statistics.mean(y3), statistics.mean(y4),
#                        statistics.mean(y5), statistics.mean(y6), statistics.mean(y7),statistics.mean(y8),
#                        statistics.mean(y9), statistics.mean(y8), statistics.mean(y10), statistics.mean(y11),
#                        statistics.mean(y12), statistics.mean(y13), statistics.mean(y14), statistics.mean(y15),
#                        statistics.mean(y16), statistics.mean(y17), statistics.mean(y18), statistics.mean(y19),
#                        statistics.mean(y20), statistics.mean(y21), statistics.mean(y22), statistics.mean(y23), statistics.mean(y24)]))
# print(statistics.mean(power))

x = []
zero = dt.datetime.strptime('00:00', '%H:%M')
for i in range(len(y1)):
    x.append(zero.strftime("%H:%M"))
    zero = zero + dt.timedelta(minutes=1)

fig, ax1 = plt.subplots(4, 10, figsize=(16, 12))
# ax1[0, 0].plot(range(len(x)), y1, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 1].plot(range(len(x)), y2, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 2].plot(range(len(x)), y3, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 3].plot(range(len(x)), y4, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 4].plot(range(len(x)), y5, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 5].plot(range(len(x)), y6, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 6].plot(range(len(x)), y7, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 7].plot(range(len(x)), y8, color='b', linewidth=1.5, linestyle='-')
#
# ax1[0, 8].plot(range(len(x)), y9, color='b', linewidth=1.5, linestyle='-')

ax1[0, 9].plot(range(len(x)), y10, color='b', linewidth=1.5, linestyle='-')

# ax1[0, 10].plot(range(len(x)), y35, color='b', linewidth=1.5, linestyle='-')

# ax1[0, 11].plot(range(len(x)), y36, color='b', linewidth=1.5, linestyle='-')

# ax1[0, 12].plot(range(len(x)), y37, color='b', linewidth=1.5, linestyle='-')

ax1[1, 0].plot(range(len(x)), y11, color='b', linewidth=1.5, linestyle='-')

ax1[1, 1].plot(range(len(x)), y12, color='b', linewidth=1.5, linestyle='-')

ax1[1, 2].plot(range(len(x)), y13, color='b', linewidth=1.5, linestyle='-')

ax1[1, 3].plot(range(len(x)), y14, color='b', linewidth=1.5, linestyle='-')

ax1[1, 4].plot(range(len(x)), y15, color='b', linewidth=1.5, linestyle='-')

ax1[1, 5].plot(range(len(x)), y16, color='b', linewidth=1.5, linestyle='-')

ax1[1, 6].plot(range(len(x)), y17, color='b', linewidth=1.5, linestyle='-')

ax1[1, 7].plot(range(len(x)), y18, color='b', linewidth=1.5, linestyle='-')

ax1[1, 8].plot(range(len(x)), y19, color='b', linewidth=1.5, linestyle='-')

ax1[1, 9].plot(range(len(x)), y20, color='b', linewidth=1.5, linestyle='-')

# ax1[1, 10].plot(range(len(x)), y40, color='b', linewidth=1.5, linestyle='-')

# ax1[1, 11].plot(range(len(x)), y41, color='b', linewidth=1.5, linestyle='-')

# ax1[1, 12].plot(range(len(x)), y42, color='b', linewidth=1.5, linestyle='-')

ax1[2, 0].plot(range(len(x)), y21, color='b', linewidth=1.5, linestyle='-')

ax1[2, 1].plot(range(len(x)), y22, color='b', linewidth=1.5, linestyle='-')

ax1[2, 2].plot(range(len(x)), y23, color='b', linewidth=1.5, linestyle='-')

ax1[2, 3].plot(range(len(x)), y24, color='b', linewidth=1.5, linestyle='-')

ax1[2, 4].plot(range(len(x)), y25, color='b', linewidth=1.5, linestyle='-')

ax1[2, 5].plot(range(len(x)), y26, color='b', linewidth=1.5, linestyle='-')

ax1[2, 6].plot(range(len(x)), y27, color='b', linewidth=1.5, linestyle='-')

ax1[2, 7].plot(range(len(x)), y28, color='b', linewidth=1.5, linestyle='-')

ax1[2, 8].plot(range(len(x)), y29, color='b', linewidth=1.5, linestyle='-')

ax1[2, 9].plot(range(len(x)), y30, color='b', linewidth=1.5, linestyle='-')

# ax1[2, 10].plot(range(len(x)), y45, color='b', linewidth=1.5, linestyle='-')

# ax1[2, 11].plot(range(len(x)), y46, color='b', linewidth=1.5, linestyle='-')

# ax1[2, 12].plot(range(len(x)), y47, color='b', linewidth=1.5, linestyle='-')

ax1[3, 0].plot(range(len(x)), y31, color='b', linewidth=1.5, linestyle='-')

ax1[3, 1].plot(range(len(x)), y32, color='b', linewidth=1.5, linestyle='-')

ax1[3, 2].plot(range(len(x)), y33, color='b', linewidth=1.5, linestyle='-')

ax1[3, 3].plot(range(len(x)), y34, color='b', linewidth=1.5, linestyle='-')

ax1[3, 4].plot(range(len(x)), y35, color='b', linewidth=1.5, linestyle='-')

ax1[3, 5].plot(range(len(x)), y36, color='b', linewidth=1.5, linestyle='-')

ax1[3, 6].plot(range(len(x)), y37, color='b', linewidth=1.5, linestyle='-')

ax1[3, 7].plot(range(len(x)), y38, color='b', linewidth=1.5, linestyle='-')

ax1[3, 8].plot(range(len(x)), y39, color='b', linewidth=1.5, linestyle='-')

ax1[3, 9].plot(range(len(x)), y40, color='b', linewidth=1.5, linestyle='-')

# ax1[3, 10].plot(range(len(x)), y50, color='b', linewidth=1.5, linestyle='-')

# ax1[3, 11].plot(range(len(x)), y51, color='b', linewidth=1.5, linestyle='-')

# ax1[3, 12].plot(range(len(x)), y52, color='b', linewidth=1.5, linestyle='-')


for i in range(4):
    for j in range(10):
        ax1[i, j].set_yticks([-20,-10,0,10,20])
        ax1[i, 0].set_ylabel('Temperature [C]', fontsize=12)
        ax1[i, j].set_xticks([0, (len(x) // 2), len(x)])
        ax1[i, j].set_xticklabels([x[n] for n in range(len(x)) if n % (len(x) // 2) == 0 or x[n] == x[-1]])
        ax1[i, j].grid(linestyle="--", color='lightgray')

plt.tight_layout()
plt.show()
