import pandas as pd
import CoolProp as CP
import matplotlib.pyplot as plt

directory = r'C:\Users\com\Desktop\samsung\Compressor map data'
fig_save_dir = r'C:\Users\com\Desktop\samsung\Compressor model result'
folder_name = '2021-08-05'
date = '05'
data = pd.read_csv(directory+'\{}\outdoor_{}_3066.csv'.format(folder_name,date))

power = data['value']

low_p = data['low_pressure']
high_p = data['high_pressure']

suc_t = data['suction_temp1']
cond_t = data['double_tube_temp']
dis_t1 = data['discharge_temp1']
dis_t2 = data['discharge_temp2']

dis_t = []
for i in range(len(data)):
    if dis_t1[i] > dis_t2[i]:
        dis_t.append(dis_t1[i])
    elif dis_t2[i] > dis_t1[i]:
        dis_t.append(dis_t2[i])
    else:
        dis_t.append(dis_t1[i])

time = data['Time']
suc_h = []
dis_h = []
cond_h = []
for i in range(len(data)):
    suc_h.append(CP.CoolProp.PropsSI('H','P',low_p[i]*98.0665*1000,'T',suc_t[i]+273.15,'R410A'))
    dis_h.append(CP.CoolProp.PropsSI('H','P',high_p[i]*98.0665*1000,'T',dis_t[i]+273.15,'R410A'))
    cond_h.append(CP.CoolProp.PropsSI('H','P',high_p[i]*98.0665*1000,'T',cond_t[i]+273.15,'R410A'))

print(dis_h)
print(suc_h)

m_dot_calc = []
cond_h_ = []
suc_h_ = []
dis_h_ = []
for i in range(len(data)):
    if dis_h[i]-suc_h[i] < 0:
        continue
    else:
        m_dot_calc.append(power[i]/(dis_h[i]-suc_h[i]))
        cond_h_.append(cond_h[i])
        suc_h_.append(suc_h[i])
        dis_h_.append(dis_h[i])

cond_Q = []
evap_Q = []
for i in range(len(m_dot_calc)):
    cond_Q.append(m_dot_calc[i]*abs(cond_h_[i]-dis_h_[i])/1000)
    evap_Q.append(m_dot_calc[i]*abs(suc_h_[i]-cond_h_[i])/1000)

# mdot_calc
plt.cla()
plt.clf()
fig, ax1 = plt.subplots(figsize=(12,10))
ax1.plot(range(len(m_dot_calc)),m_dot_calc,c='b',linewidth=1.5,linestyle='-')
# ax1.set_yticks([-100,0,100,200,300,400,500,600,700])
ax1.set_xticks([i for i in range(len(time)) if i % 60 == 0])
ax1.set_xticklabels([time[i][0:5] for i in range(len(time)) if i % 60 == 0])
ax1.set_ylabel('m_dot_calc', fontsize=14)
ax1.set_xlabel('Time',fontsize=14)
ax1.set_title('m_dot_calc with energy balance',fontsize=16)
ax1.legend(['m_dot_calc'],loc='upper left',fontsize=14)
plt.autoscale(enable=True, axis='x', tight=True)
ax1.grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}_{}.png'.format('m_dot_calc',date))
plt.close()

# cond_Q
plt.cla()
plt.clf()
fig2, ax1 = plt.subplots(figsize=(12,10))
ax1.plot(range(len(cond_Q)),cond_Q,c='b',linewidth=1.5,linestyle='-')
# ax1.set_yticks([0,2,4,6,8,10,12,14])
ax1.set_xticks([i for i in range(len(time)) if i % 60 == 0])
ax1.set_xticklabels([time[i][0:5] for i in range(len(time)) if i % 60 == 0])
ax1.set_ylabel('Condenser Q [kW]', fontsize=14)
ax1.set_xlabel('Time',fontsize=14)
ax1.set_title('Condensor Q with energy balance',fontsize=16)
ax1.legend(['Condensor Q'],loc='upper left',fontsize=14)
plt.autoscale(enable=True, axis='x', tight=True)
ax1.grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}_{}.png'.format('cond_Q',date))

# evap_Q
plt.cla()
plt.clf()
fig3, ax1 = plt.subplots(figsize=(12,10))
ax1.plot(range(len(evap_Q)),evap_Q,c='b',linewidth=1.5,linestyle='-')
# ax1.set_yticks([0,2,4,6,8,10,12,14])
ax1.set_xticks([i for i in range(len(time)) if i % 60 == 0])
ax1.set_xticklabels([time[i][0:5] for i in range(len(time)) if i % 60 == 0])
ax1.set_ylabel('Evaporator Q [kW]', fontsize=14)
ax1.set_xlabel('Time',fontsize=14)
ax1.set_title('Evaporator Q with energy balance',fontsize=16)
ax1.legend(['Evaporator Q'],loc='upper left',fontsize=14)
plt.autoscale(enable=True, axis='x', tight=True)
ax1.grid()
plt.tight_layout()
plt.savefig(fig_save_dir+'\{}_{}.png'.format('evap_Q',date))