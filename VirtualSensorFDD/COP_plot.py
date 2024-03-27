import pandas as pd
import matplotlib.pyplot as plt
import os

path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/SEER/Result/2021-10-15/'
savepath = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/SEER/Result/2021-10-15/'

filename = 'Multiple_Cost_Lab1.csv'

device_list = ['110F','95F','75F']
dict = {}

column_name = ['Air flow Rate','Virtual sensor','Virtual sensor [%]','Q_ref','COP','SEER','COST','Ratio_Q_ref','Ratio_COP','Ratio_SEER','Ratio_COST']

target = 'Ratio_COP'

data = pd.read_csv(path+filename,encoding='cp949')
column_number = []
for i in range(len(data.columns)):
    if data.columns[i] in device_list:
        column_number.append(i)

for i in column_number:
    dict[data.columns[i]] = data.iloc[0:,i:i+11]
    dict[data.columns[i]] = dict[data.columns[i]].drop(1,axis=0)
    dict[data.columns[i]].columns = column_name
    dict[data.columns[i]] = dict[data.columns[i]].drop(0, axis=0)
    dict[data.columns[i]] = dict[data.columns[i]].dropna(axis=0)

marker = ['o','v','^','s','x','*','D']
i = 0
fig, ax1 = plt.subplots(figsize=(8,7))
for device, data in dict.items():
    xdata = dict[device]['Virtual sensor [%]'].apply(lambda x: int(x[:-1]))
    ydata = dict[device][target].apply(lambda x: int(x[:-1]))
    ax1.scatter(xdata,ydata,label=device,s=100,marker=marker[i])
    i += 1

xticks = [20,40,60,80,100,120]
yticks = [20,40,60,80,100,120]
ax1.set_xticks(xticks)
ax1.set_xticklabels(xticks,fontsize=14)
ax1.set_yticks(yticks)
ax1.set_yticklabels(yticks,fontsize=14)
ax1.set_xlabel('Ratio of airflow [%]',fontsize=16,fontdict={'weight':'bold'})
ax1.set_ylabel('Ratio of COP [%]',fontsize=16,fontdict={'weight':'bold'})
ax1.legend(loc='lower left',fontsize=12,ncol=1)
ax1.grid(linestyle=':', color='dimgray')

plt.tight_layout()
plt.show()
fig.savefig(savepath+'/{}.png'.format(target))