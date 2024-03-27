import pandas as pd
import matplotlib.pyplot as plt
import os


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


unit = 'RTU_Split'

path = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\0315\{} data\SEER'.format(unit)
save_path = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\0315\result\{}'.format(unit)

fault = 'charge'

dic = path + '\{}'.format(fault)

marker = ['o','v','^','s','D','*','D']
edge = ['r','b','g','m','tab:cyan','y']


def SEER_plot():
    count = 0
    fig, ax = plt.subplots(figsize=(12, 10))
    for i in os.listdir(dic):
        print(i)
        data = pd.read_csv(dic+'/'+i).dropna(axis=0,inplace=False)
        fault_level = data['Fault_level']
        SEER = data['SEER']

        plt.scatter(fault_level,SEER,s=200,label=i[:-4],marker=marker[count],facecolors='none',edgecolors=edge[count],linewidths=2)
        count += 1

    if fault == 'charge':
        ax.set_xlabel('Refrigerant charge [%]', fontsize=20, fontdict={'weight': 'bold'})
    else:
        ax.set_xlabel('Air flow rate ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    ax.set_ylabel('SEER ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    if fault == 'charge':
        xticks = [20, 40, 60, 80, 100, 120, 140]
        yticks = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140]
    else:
        xticks = [40, 50, 60, 70, 80, 90, 100, 110]
        yticks = [40, 50, 60, 70, 80, 90, 100, 110, 120,]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, fontsize=20)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=20)
    ax.grid(linestyle=':', color='dimgray')
    # plt.autoscale(enable=True, axis='x', tight=True)
    # plt.autoscale(enable=True, axis='y', tight=True)
    if fault == 'charge':
        if unit == 'RTU_Lab1':
            plt.legend(loc='lower center', fontsize=14.3,ncol=2)
        else:
            plt.legend(loc='lower center', fontsize=20, ncol=2)
    else:
        if unit == 'RTU_Lab1':
            plt.legend(loc='lower center', fontsize=14.3,ncol=2)
        else:
            plt.legend(loc='lower center', fontsize=20, ncol=2)
    plt.tight_layout()
    # plt.show()

    create_folder(save_path+'/{}'.format(fault))
    fig.savefig(save_path + '/{}/SEER.png'.format(fault))


def COP_plot():
    count = 0
    fig, ax = plt.subplots(figsize=(12, 10))
    for i in os.listdir(dic):
        print(i)
        data = pd.read_csv(dic+'/'+i).dropna(axis=0,inplace=False)
        fault_level = data['Fault_level']
        COP = data['COP']

        plt.scatter(fault_level,COP,s=200,label=i[:-4],marker=marker[count],facecolors='none',edgecolors=edge[count],linewidths=2)
        count += 1

    if fault == 'charge':
        ax.set_xlabel('Refrigerant charge [%]', fontsize=20, fontdict={'weight': 'bold'})
    else:
        ax.set_xlabel('Air flow rate ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    ax.set_ylabel('Coefficient of performance ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    if fault == 'charge':
        xticks = [20, 40, 60, 80, 100, 120, 140]
        yticks = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140]
    else:
        xticks = [40, 50, 60, 70, 80, 90, 100, 110]
        yticks = [40, 50, 60, 70, 80, 90, 100, 110, 120,]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, fontsize=20)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=20)
    ax.grid(linestyle=':', color='dimgray')
    # plt.autoscale(enable=True, axis='x', tight=True)
    # plt.autoscale(enable=True, axis='y', tight=True)
    if fault == 'charge':
        if unit == 'RTU_Lab1':
            plt.legend(loc='lower center', fontsize=14.3, ncol=2)
        else:
            plt.legend(loc='lower center', fontsize=20, ncol=2)
    else:
        if unit == 'RTU_Lab1':
            plt.legend(loc='lower center', fontsize=14.3,ncol=2)
        else:
            plt.legend(loc='lower center', fontsize=20, ncol=2)
    plt.tight_layout()
    # plt.show()

    create_folder(save_path+'/{}'.format(fault))
    fig.savefig(save_path + '/{}/COP.png'.format(fault))


def Q_ref_plot():
    count = 0
    fig, ax = plt.subplots(figsize=(12, 10))
    for i in os.listdir(dic):
        print(i)
        data = pd.read_csv(dic+'/'+i).dropna(axis=0,inplace=False)
        fault_level = data['Fault_level']
        Q_ref = data['Q_ref']

        plt.scatter(fault_level,Q_ref,s=200,label=i[:-4],marker=marker[count],facecolors='none',edgecolors=edge[count],linewidths=2)
        count += 1

    if fault == 'charge':
        ax.set_xlabel('Refrigerant charge [%]', fontsize=20, fontdict={'weight': 'bold'})
    else:
        ax.set_xlabel('Air flow rate ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    ax.set_ylabel('Cooling capacity ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    if fault == 'charge':
        xticks = [20, 40, 60, 80, 100, 120, 140]
        yticks = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140]
    else:
        xticks = [40, 50, 60, 70, 80, 90, 100, 110]
        yticks = [40, 50, 60, 70, 80, 90, 100, 110, 120,]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, fontsize=20)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=20)
    ax.grid(linestyle=':', color='dimgray')
    # plt.autoscale(enable=True, axis='x', tight=True)
    # plt.autoscale(enable=True, axis='y', tight=True)
    if fault == 'charge':
        if unit == 'RTU_Lab1':
            plt.legend(loc='lower center', fontsize=14.3, ncol=2)
        else:
            plt.legend(loc='lower center', fontsize=20, ncol=2)
    else:
        if unit == 'RTU_Lab1':
            plt.legend(loc='lower center', fontsize=14.3,ncol=2)
        else:
            plt.legend(loc='lower center', fontsize=20, ncol=2)
    plt.tight_layout()
    # plt.show()

    create_folder(save_path+'/{}'.format(fault))
    fig.savefig(save_path + '/{}/Q_ref.png'.format(fault))


def COST_plot():
    count = 0
    fig, ax = plt.subplots(figsize=(12, 10))
    for i in os.listdir(dic):
        print(i)
        data = pd.read_csv(dic+'/'+i).dropna(axis=0,inplace=False)
        fault_level = data['Fault_level']
        COST = data['COST']

        plt.scatter(fault_level,COST,s=200,label=i[:-4],marker=marker[count],facecolors='none',edgecolors=edge[count],linewidths=2)
        count += 1

    if fault == 'charge':
        ax.set_xlabel('Refrigerant charge [%]', fontsize=20, fontdict={'weight': 'bold'})
    else:
        ax.set_xlabel('Air flow rate ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    ax.set_ylabel('Annual operating cost ratio [%]', fontsize=20, fontdict={'weight': 'bold'})
    if fault == 'charge':
        xticks = [20,40,60, 80, 100, 120, 140]
        yticks = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340]
    else:
        xticks = [40, 50, 60, 70, 80, 90, 100, 110]
        yticks = [80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, fontsize=20)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=20)
    ax.grid(linestyle=':', color='dimgray')
    # plt.autoscale(enable=True, axis='x', tight=True)
    # plt.autoscale(enable=True, axis='y', tight=True)
    if fault == 'charge':
        if unit == 'RTU_Lab1':
            plt.legend(loc='upper center', fontsize=14.3, ncol=2)
        else:
            plt.legend(loc='upper center', fontsize=20, ncol=2)
    else:
        if unit == 'RTU_Lab1':
            plt.legend(loc='upper center', fontsize=14.3,ncol=2)
        else:
            plt.legend(loc='upper center', fontsize=20, ncol=2)
    plt.tight_layout()
    # plt.show()

    create_folder(save_path+'/{}'.format(fault))
    fig.savefig(save_path + '/{}/COST.png'.format(fault))


SEER_plot()
COP_plot()
Q_ref_plot()
COST_plot()
