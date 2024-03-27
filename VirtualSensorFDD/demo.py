import pandas as pd
import matplotlib.pyplot as plt
import statistics

data = pd.read_csv(r'C:\Users\user\Desktop\accident.csv')

print(data)

Time10 = data['Time20']
Time12 = data['Time21']

High_P10 = data['High_P20']* 98.0665
High_P12 = data['High_P21']* 98.0665


Low_P10 = data['Low_P20']* 98.0665
Low_P12 = data['Low_P21']* 98.0665

suction_10 = data['suction_20']
suction_12 = data['suction_21']

discharge_10 = data['discharge_20']
discharge_12 = data['discharge_21']

cond_out_10 = data['cond_out_20']
cond_out_12 = data['cond_out_21']

frequency_10 = data['frequency_20']
frequency_12 = data['frequency_21']

xticklist = []
for i in range(len(Time12)):
    if i % 10 == 0:
        xticklist.append(Time12[i][:10] + '\n' + Time12[i][11:])

lim = 20

fig, ax1 = plt.subplots(1, 1, figsize=(12, 4))

ax1.set_ylim(-20,lim)
ax1.set_xticks([i for i in range(len(Time12)) if i % 10 == 0])
# ax1.set_xticklabels([xticklist[i] for i in range(len(xticklist)) if i % 10 == 0])
ax1.set_xticklabels(xticklist,fontsize=12)
# ax1.set_ylabel('High Pressure [kPa]', fontsize=14)
# ax1.set_ylabel('Low Pressure [kPa]', fontsize=14)
# ax1.set_ylabel('Suction Temperature [C]', fontsize=14)
# ax1.set_ylabel('Discharge Temperature [C]', fontsize=14)
ax1.set_ylabel('Condenser Outlet Temperature [C]', fontsize=14)
# ax1.set_ylabel('Average Compressor Frequency [Hz]', fontsize=14)

ax1.plot(range(len(frequency_10)), cond_out_10, label='01/20', linewidth=2)
ax1.plot(range(len(frequency_12)), cond_out_12,label='01/21', linewidth=2)

# plt.axvspan(120, 180, facecolor='skyblue', alpha=0.5)

ax1.legend(loc='upper right', ncol = 2,fontsize=12)
ax1.grid(linestyle="--", color='lightgray')
# ax1.set_ylabel('PowerConsumption [kW]', fontsize=14)

plt.show()
