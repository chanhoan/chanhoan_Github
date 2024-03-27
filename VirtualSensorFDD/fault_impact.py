import pandas as pd
import matplotlib.pyplot as plt
import statistics
import os


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


data = {'3065': ['0810','0811'],
        '3066': ['0728','0729','0730','0804','0805','0810','0811'],
        '3067': ['0813']}

model = ['EPM_meter','Seq2Seq_meter']

dir = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Performance degradation'

for unit, date_list in data.items():
    for date in date_list:
        for m in model:
            globals()[m,date] = pd.read_csv(dir+'\degradation\{}\{}\{}_{}.csv'.format(unit,date,m,unit)).drop('Unnamed: 0',axis=1)['COP_degradation'] * 100
        print(unit,date)
        globals()['compMap_meter',date] = pd.read_csv(dir+'\degradation\{}\compMap_meter_{}.csv'.format(date,unit)).drop('Unnamed: 0',axis=1)['COP_degradation'] * 100

marker = ['o','D','^','s']


def EER():
    for unit, date_list in data.items():
        for date in date_list:
            k = 0
            fig, ax = plt.subplots(figsize=(12, 8))
            for m in model:
                for i in range(len(globals()[m,date])):
                    if globals()[m,date][i] <= 0 or globals()[m,date][i] >= 120:
                        globals()[m, date][i] = None
                    if globals()['compMap_meter',date][i] <= 0 or globals()['compMap_meter',date][i] >= 120:
                        globals()['compMap_meter', date][i] = None
                plt.scatter(globals()['compMap_meter',date],globals()[m,date], s=70, marker=marker[k], label='{}_{}'.format(date,m))
                k += 1
            ax.set_ylabel('Energy efficiency ratio based on\nvirtual sensor [%]', fontsize=18)
            ax.set_xlabel('Energy efficiency ratio based on\nexpected performance model [%]', fontsize=18)
            plt.grid(b=True, which='both', axis='both', alpha=0.5, color='grey', ls='-')
            ax.set_xticks([0,10,20,30,40,50,60,70,80,90,100,110,120])
            ax.set_xticklabels(['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%','110%','120%'], fontsize=14)
            ax.set_yticks([0,10,20,30,40,50,60,70,80,90,100,110,120])
            ax.set_yticklabels(['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%','110%','120%'], fontsize=14)
            legend = plt.legend(ncol=3, loc='lower center', fontsize=15,framealpha=1)
            ax.autoscale(enable=True, axis='x', tight=True)
            ax.autoscale(enable=True, axis='y', tight=True)
            ax.text(100, 110, '-10%\nerror', horizontalalignment='right', fontsize=16, color='black')
            ax.text(120, 93, '+10%\nerror', horizontalalignment='right', fontsize=16, color='black')
            ax.plot([0, 120], [0, 120], color='indigo', linestyle='-', linewidth=2)
            ax.plot([10, 120], [0, 110], color='red', linestyle='--', linewidth=2)
            ax.plot([0, 110], [10, 120], color='red', linestyle='--', linewidth=2)
            plt.tight_layout()
            # plt.show()
            create_folder(dir+'\{}\{}'.format('figure',date))
            plt.savefig(dir+'\{}\{}\{}.png'.format('figure',date,unit))


EER()