import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


file = {'3065/': ['0810','0811'],
        '3066/': ['0728','0729','0730','0804','0805', '0810', '0811'],
        '3067/': ['0813']}

for key, date_list in file.items():
    unit = key[:-1]
    for date in date_list:
        dir = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Performance degradation/EPM/{}/{}/'.format(unit, date)
        testlist = os.listdir(dir)
        Seq2Seq_compMap = []
        Seq2Seq_meter = []
        EPM_compMap = []
        EPM_meter = []
        compMap_meter = []
        for test in testlist:
            EPM = pd.read_csv(dir+test+'/EPM.csv')['Prediction']
            Seq = pd.read_csv(dir+test + '/Seq2Seq.csv')['Prediction']
            meter = pd.read_csv(dir+test+'/Seq2Seq.csv')['Test']
            MAP = pd.read_csv(dir+test+'/Map.csv')['value_prediction'] * 0.8

            for i in range(len(Seq)):
                Seq2Seq_meter.append(Seq[i]/meter[i])
                Seq2Seq_compMap.append(Seq[i]/MAP[i])
            for i in range(len(EPM)):
                EPM_compMap.append(EPM[i]/meter[i])
                EPM_meter.append(EPM[i]/MAP[i])
            for i in range(len(MAP)):
                compMap_meter.append(meter[i]/MAP[i])

        Seq2Seq_compMap = pd.DataFrame(Seq2Seq_compMap,columns=['Power_degradation'])
        Seq2Seq_meter = pd.DataFrame(Seq2Seq_meter, columns=['Power_degradation'])
        EPM_compMap = pd.DataFrame(EPM_compMap, columns=['Power_degradation'])
        EPM_meter = pd.DataFrame(EPM_meter, columns=['Power_degradation'])
        compMap_meter = pd.DataFrame(compMap_meter, columns=['Power_degradation'])

        save_dir = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Performance degradation/degradation/{}/{}/{}'.format(unit,date,test)
        create_folder(save_dir)
        Seq2Seq_compMap.to_csv(save_dir+'/Seq2Seq_compMap_{}.csv'.format(unit))
        Seq2Seq_meter.to_csv(save_dir + '/Seq2Seq_meter_{}.csv'.format(unit))
        EPM_compMap.to_csv(save_dir + '/EPM_compMap_{}.csv'.format(unit))
        EPM_meter.to_csv(save_dir + '/EPM_meter_{}.csv'.format(unit))
        compMap_meter.to_csv(save_dir + '/compMap_meter_{}.csv'.format(unit))

        Seq2Seq_compMap = Seq2Seq_compMap['Power_degradation'].apply(lambda x: None if x > 1.2 else x*100)
        Seq2Seq_meter = Seq2Seq_meter['Power_degradation'].apply(lambda x: None if x > 1.2 else x*100)
        EPM_compMap = EPM_compMap['Power_degradation'].apply(lambda x: None if x > 1.2 else x*100)
        EPM_meter = EPM_meter['Power_degradation'].apply(lambda x: None if x > 1.2 else x*100)
        compMap_meter = compMap_meter['Power_degradation'].apply(lambda x: None if x > 1.2 or x < 0.8 else x*100)



        def EER():
            plt.cla()
            plt.clf()
            fig, ax = plt.subplots(figsize=(12, 8))
            plt.scatter(compMap_meter, Seq2Seq_compMap, color='b', marker='o', s=70, label='Seq2Seq vs Compressor Map')
            plt.scatter(compMap_meter, Seq2Seq_meter, color='c', marker='X', s=70, label='Seq2Seq vs Power meter')
            plt.scatter(compMap_meter, EPM_compMap, color='m', marker='s', s=70, label='EPM vs Compressor Map')
            plt.scatter(compMap_meter, EPM_meter, color='y', marker='D', s=70, label='EPM vs Power meter')
            ax.set_xlabel('Current power consumption ratio based on\ncompressor map [%]', fontsize=18)
            ax.set_ylabel('Expected power consumption ratio based on\nexpected performance model [%]', fontsize=18)
            plt.grid(b=True, which='both', axis='both', alpha=0.5, color='grey', ls='-')
            ax.set_xticks([20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
            ax.set_xticklabels(['20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', '110%', '120%'],fontsize=14)
            ax.set_yticks([20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
            ax.set_yticklabels(['20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', '110%', '120%'],fontsize=14)
            legend = plt.legend(ncol=3, loc='lower center', fontsize=14, framealpha=1)
            plt.setp(legend.texts)
            ax.autoscale(enable=True, axis='x', tight=True)
            ax.autoscale(enable=True, axis='y', tight=True)
            ax.text(100, 110, '+10%\nerror', horizontalalignment='right', fontsize=16, color='black')
            ax.text(120, 93, '+10%\nerror', horizontalalignment='right', fontsize=16, color='black')
            ax.plot([20, 120], [20, 120], color='indigo', linestyle='-', linewidth=2)
            ax.plot([30, 120], [20, 110], color='red', linestyle='--', linewidth=2)
            ax.plot([20, 110], [30, 120], color='red', linestyle='--', linewidth=2)
            plt.tight_layout()
            # plt.show()
            fig_dir = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Performance degradation/figure/{}/{}/'.format(unit,date)
            create_folder(fig_dir)
            plt.savefig(fig_dir+'/Performance degradation.png')

        # EER()