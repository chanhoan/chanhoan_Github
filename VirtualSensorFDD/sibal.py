import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r'C:\Users\user\Desktop\fault_level_airflow.csv')

fault_level_28 = data['fault_level_28'] * 100
airflow_28 = data['block_28']

fault_level_30 = data['fault_level_30'].apply(lambda x: None if x*100 >= 95 or x*100 < 85 else x*100)
airflow_30 = data['block_30'].apply(lambda x: None if x > 95 or x < 85 else x*1.05)

fault_level_04 = data['fault_level_04'].apply(lambda x: None if x*100 > 85 or x*100 < 75 else x*100)
airflow_04 = data['block_04'] * 1.1

fault_level_05 = data['fault_level_05'].apply(lambda x: None if x*100 > 80 or x*100 < 70 else x*100)
airflow_05 = data['block_05'].apply(lambda x: None if x > 80 or x < 70 else x)

fault_level_10 = data['fault_level_10'].apply(lambda x: None if x*100 > 45 or x*100 < 30 else x*100)
airflow_10 = data['block_10'].apply(lambda x: None if x > 45 or x < 30 else x)

fault_level_28 = fault_level_28.sort_values()
airflow_28 = airflow_28.sort_values()

fault_level_30 = fault_level_30.sort_values()
airflow_30 = airflow_30.sort_values()

fault_level_04 = fault_level_04.sort_values()
airflow_04 = airflow_04.sort_values()

fault_level_05 = fault_level_05.sort_values()
airflow_05 = airflow_05.sort_values()

fault_level_10 = fault_level_10.sort_values()
airflow_10 = airflow_10.sort_values()


fig, ax1 = plt.subplots(figsize=(8,7))

ax1.scatter(fault_level_28,airflow_28,color='m',marker='x',s=120,label='No fault')
ax1.scatter(fault_level_10,airflow_10,color='c',marker='D',s=120,label='Fault type 1')
ax1.scatter(fault_level_05,airflow_05,color='r',marker='o',s=120,label='Fault type 2')
ax1.scatter(fault_level_04,airflow_04,color='b',marker='s',s=120,label='Fault type 3')
ax1.scatter(fault_level_30,airflow_30,color='g',marker='^',s=120,label='Fault type 4')

ax1.set_xticks([0,  20,  40,  60,  80,  100])
ax1.set_xticklabels(['0%', '20%','40%',  '60%', '80%', '100%'],fontsize=20)
ax1.set_yticks([0,  20,  40,  60,  80,  100])
ax1.set_yticklabels(['0%', '20%','40%',  '60%', '80%', '100%'],fontsize=20)

ax1.set_ylabel('Virtual fouling sensor [%]',fontsize=22)
ax1.set_xlabel('Measurement based fault level [%]',fontsize=22)

ax1.text(75, 90, '-10%\nerror', horizontalalignment='center', fontsize=16, color='black')
ax1.text(92, 70, '+10%\nerror', horizontalalignment='center', fontsize=16, color='black')
ax1.plot([0, 100], [0, 100], color='indigo', linestyle='-', linewidth=2)
ax1.plot([10, 100], [0, 90], color='red', linestyle='--', linewidth=2)
ax1.plot([0, 90], [10, 100], color='red', linestyle='--', linewidth=2)

plt.legend(fontsize=18,loc='upper left')
plt.grid(b=True, which='both', axis='both', alpha=0.5, color='grey', ls='--')
ax1.autoscale(enable=True, axis='x', tight=True)
ax1.autoscale(enable=True, axis='y', tight=True)

plt.tight_layout()
plt.show()

# fault_level_28 = data['fault_level_28'] * 100
# airflow_28 = data['airflow_28'].apply(lambda x: None if x > 9*1.15 or x < 9*0.85 else x*1.1)
#
# fault_level_30 = data['fault_level_30'].apply(lambda x: None if x >= 1.0 or x < 0.9 else x*100)
# airflow_30 = data['airflow_30'].apply(lambda x: None if x > 2 or x < 0.1 else x)
#
# fault_level_04 = data['fault_level_04'].apply(lambda x: None if x > 0.90 or x < 0.80 else x*100)
# airflow_04 = data['airflow_04'].apply(lambda x: None if x > 2.5 else x)
#
# fault_level_05 = data['fault_level_05'].apply(lambda x: None if x > 0.80 or x < 0.70 else x*100)
# airflow_05 = data['airflow_05']
#
# fault_level_10 = data['fault_level_10'].apply(lambda x: None if x > 0.35 or x < 0.2 else x*100)
# airflow_10 = data['airflow_10'] + 2.5

# mean = 2.5
#
# fault_level_28 = data['fault_level_11'] * 100
# airflow_28 = data['airflow_11'].apply(lambda x: None if x > mean*1.15 or x < mean*0.85 else x)
#
# fault_level_30 = data['fault_level_10'] * 100
# airflow_30 = data['airflow_10']
#
# fault_level_04 = data['fault_level_normal'] * 100
# airflow_04 = data['airflow_normal'].apply(lambda x: None if x > mean*1.15 or x < mean*0.85 else x)
#
# fault_level_05 = data['fault_level_mesh'] * 100
# airflow_05 = data['airflow_mesh']
#
# fault_level_10 = data['fault_level_towel'] * 100
# airflow_10 = data['airflow_towel']
#
#
# fig, ax1 = plt.subplots(figsize=(8,7))

# ax1.scatter(fault_level_28,airflow_28,color='r',marker='o',s=120,label='No fault')
# ax1.scatter(fault_level_10,airflow_10,color='m',marker='D',s=120,label='Fault type 1')
# ax1.scatter(fault_level_05,airflow_05,color='c',marker='<',s=120,label='Fault type 2')
# ax1.scatter(fault_level_04,airflow_04,color='b',marker='s',s=120,label='Fault type 3')
# ax1.scatter(fault_level_30,airflow_30,color='g',marker='^',s=120,label='Fault type 4')

# ax1.scatter(fault_level_28,airflow_28,color='r',marker='o',s=120,label='No fault - 3065')
# ax1.scatter(fault_level_04,airflow_04,color='b',marker='s',s=120,label='No fault - 3067')
#
# ax1.scatter(fault_level_30,airflow_30,color='g',marker='^',s=120,label='Fault type 1 - 3065')
# ax1.scatter(fault_level_10,airflow_10,color='m',marker='D',s=120,label='Fault type 2 - 3067')
# ax1.scatter(fault_level_05,airflow_05,color='c',marker='<',s=120,label='Fault type 2')


# ax1.set_ylabel('Airflow ratio [%]',fontsize=22)
# ax1.set_xlabel('Measurement based fault level [%]',fontsize=22)
#
# ax1.text(10, mean*1.15+0.1, '+15% error', horizontalalignment='center', fontsize=16, color='black')
# ax1.text(10, mean*0.85-0.2, '-15% error', horizontalalignment='center', fontsize=16, color='black')
# ax1.plot([0, 100], [mean, mean], color='indigo', linestyle='-', linewidth=2)
# ax1.plot([0, 100], [mean*1.15, mean*1.15], color='red', linestyle='--', linewidth=2)
# ax1.plot([0, 100], [mean*0.85, mean*0.85], color='red', linestyle='--', linewidth=2)
#
# # ax1.set_yticks([0,2,4,6,8,10,12,14])
# ax1.set_yticks([0,0.5,1,1.5,2,2.5,3,3.5])
# ax1.set_yticklabels([0,20,40,60,80,100,120,140],fontsize=20)
# ax1.set_xticks([0, 20, 40, 60, 80, 100])
# ax1.set_xticklabels([0, 20, 40, 60, 80, 100],fontsize=20)
#
#
# plt.legend(fontsize=18,loc='upper right')
# plt.grid(b=True, which='both', axis='both', alpha=0.5, color='grey', ls='--')
# ax1.autoscale(enable=True, axis='x', tight=True)
# ax1.autoscale(enable=False, axis='y', tight=True)
#
# plt.tight_layout()
# plt.show()


