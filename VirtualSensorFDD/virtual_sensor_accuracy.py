import pandas as pd
import matplotlib.pyplot as plt
import os


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


unit = 'RTU_Lab1'

path = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\0315\{} data'.format(unit)
save_path = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\0315\result\{}'.format(unit)

fault = 'charge'

dic = path + '\{}'.format(fault)

marker = ['o','v','^','s','x','*','D']
edge = ['r','b','g','m']


def VRC_accuracy():
    count = 0
    fig, ax = plt.subplots(figsize=(12, 10))
    for i in os.listdir(dic):
        print(i)
        data = pd.read_csv(dic+'/'+i)
        actual_level = data['Actual_fault_level']
        virtual_sensor = data['Virtual_sensor_level']

        for j in range(len(data)):
            actual_level.loc[j] = int(actual_level.loc[j][:-1])

        plt.scatter(actual_level,virtual_sensor,s=200,label=i[:-4],marker=marker[count],facecolors='none',edgecolors=edge[count],linewidths=2)
        count += 1

    plt.plot([40,140],[40,140],color='k',linewidth=1.5)
    plt.plot([50,140],[40,130],color='r',linewidth=1.5,linestyle='--')
    plt.plot([40,130],[50,140],color='r',linewidth=1.5,linestyle='--')
    plt.text(120,100,'-10%\nerror',ha='center',va='center',fontsize=20,fontweight='bold')
    plt.text(100,120,'+10%\nerror',ha='center',va='center',fontsize=20,fontweight='bold')
    ax.set_xlabel('Actual refrigerant charge level [%]',fontsize=20,fontdict={'weight':'bold'})
    ax.set_ylabel('Refrigerant charge level based on VRC sensor [%]',fontsize=20,fontdict={'weight':'bold'})
    xticks = [40,50,60,70,80,90,100,110,120,130,140]
    yticks = [40,50,60,70,80,90,100,110,120,130,140]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks,fontsize=20)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks,fontsize=20)
    ax.grid(linestyle=':', color='dimgray')
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.legend(loc='lower right',fontsize=20)
    plt.tight_layout()
    plt.show()

    create_folder(save_path)
    fig.savefig(save_path+'/VRC.png')


def VAF_accuracy():
    count = 0
    fig, ax = plt.subplots(figsize=(12, 10))
    for i in os.listdir(dic):
        print(i)
        data = pd.read_csv(dic + '/' + i)
        actual_level = data['Actual_fault_level']
        virtual_sensor = data['Virtual_sensor_level']

        for j in range(len(data)):
            actual_level.loc[j] = 100-int(actual_level.loc[j][:-1])
            virtual_sensor.loc[j] = int(virtual_sensor.loc[j][:-1])


        plt.scatter(actual_level, virtual_sensor, s=200, label=i[:-4], marker=marker[count], facecolors='none', edgecolors=edge[count],linewidths=2)
        count += 1

    # plt.plot([40, 110], [40, 110], color='k', linewidth=1.5)
    # plt.plot([50, 110], [40, 100], color='r', linewidth=1.5, linestyle='--')
    # plt.plot([40, 100], [50, 110], color='r', linewidth=1.5, linestyle='--')
    # plt.text(100,80,'-10%\nerror',ha='center',va='center',fontsize=20,fontweight='bold')
    # plt.text(80,100,'+10%\nerror',ha='center',va='center',fontsize=20,fontweight='bold')
    ax.set_xlabel('Condenser heat exchanger block level [%]', fontsize=20, fontdict={'weight': 'bold'})
    ax.set_ylabel('Air mass flow ratio based on VAF sensor [%]', fontsize=20, fontdict={'weight': 'bold'})
    xticks = [0,10,20,30,40,50,60]
    yticks = [40,50,60,70,80,90,100,110]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, fontsize=20)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=20)
    ax.grid(linestyle=':', color='dimgray')
    plt.autoscale(enable=False, axis='x', tight=True)
    # plt.autoscale(enable=True, axis='y', tight=True)
    plt.legend(loc='lower left', fontsize=20)
    plt.tight_layout()
    plt.show()

    create_folder(save_path)
    fig.savefig(save_path + '/VAF.png')


if fault == 'charge':
    VRC_accuracy()
elif fault == 'cond':
    VAF_accuracy()

