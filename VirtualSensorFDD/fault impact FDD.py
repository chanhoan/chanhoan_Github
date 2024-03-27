import matplotlib.patches as patches
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.metrics import mean_squared_error
import math
import statistics

datalist = {'3069': ['0117','0118','0119_1','0119_2'],}
seq_path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Seq2Seq/'
level_fath = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_airflow_sensor/'
# level_fath = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/virtual_blockage_sensor/'
time = 'updated_time'
input_seq_len = 12
stanby = {'3065':0, '3066':90, '3067':0}


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


def cvrmse(actual, pred,call):
    mse = mean_squared_error(actual, pred)
    rmse = math.sqrt(mse)
    mean = statistics.mean(actual)
    cv_rmse = rmse / mean * 100
    # print(mse, rmse, mean)
    return cv_rmse


for unit,date_list in datalist.items():
    num = 0
    if unit == '3065':
        num = 55
    elif unit == '3066':
        num = 88
    elif unit == '3067':
        num = 69

    overall_ = pd.DataFrame()
    overall = pd.DataFrame()

    fig, ax = plt.subplots(figsize=(10, 9))

    marker = ['o','^','D','s','*','x']
    marker_idx = 0
    for date in date_list:
        seq_data = pd.read_csv(seq_path+unit+'/Test_ODU{}_{}{}.csv'.format(unit,date[:2],date[2:])).drop('Unnamed: 0',axis=1)
        # test_time = pd.read_csv(seq_path+unit+'/BldgRawData_test_2021_{}_{}.csv'.format(date[1:2],date[2:]),index_col=0)
        Seq2Seq_meter = pd.DataFrame()
        Seq2Seq_meter['Power degradation'] = 1-(seq_data['Prediction'] / seq_data['Test'])

        # if unit == '3067':
        #     Seq2Seq_meter[time] = pd.to_datetime(seq_data[time])
        # else:
        #     test_time[time] = pd.to_datetime(test_time[time])
        #     test_time = test_time.reset_index(drop=True)
        #     test_time = test_time.loc[input_seq_len:, time].reset_index(drop=True)
        #     Seq2Seq_meter = pd.concat([test_time, Seq2Seq_meter], axis=1)
        #     Seq2Seq_meter.fillna(0, inplace=True)

        Seq2Seq_meter['Power degradation'] = Seq2Seq_meter['Power degradation'].apply(lambda x: 0 if x < 0 else x * 100)
        Seq2Seq_meter['Power degradation'] = Seq2Seq_meter['Power degradation'].apply(lambda x: 0 if x > 100 else x)
        Seq2Seq_meter[time] = pd.to_datetime(seq_data[time])
        print(Seq2Seq_meter)
        Seq2Seq_meter.set_index(time, inplace=True)
        Seq2Seq_meter.loc[(Seq2Seq_meter.index.hour < 9), 'Power degradation'] = 0
        Seq2Seq_meter.loc[(Seq2Seq_meter.index.hour > 18), 'Power degradation'] = 0

        Seq2Seq_meter = Seq2Seq_meter.resample('30T').mean()

        fault_level = pd.read_csv(level_fath+unit+'/'+date+'/fault_level.csv')[['Time','m_dot_air']]
        fault_level['m_dot_air'] = fault_level['m_dot_air']
        fault_level['m_dot_air'] = fault_level['m_dot_air'].apply(lambda x:0 if x < 0 else x)

        # fault_level = pd.read_csv(level_fath+unit+'/'+date+'/virtual_blockage_sensor_result.csv')[['Time','fault_level']]
        # fault_level['fault_level'] = fault_level['fault_level']
        # fault_level['fault_level'] = fault_level['fault_level'].apply(lambda x:0 if x < 0 else x)

        time_df = pd.DataFrame()
        time_df[time] = pd.to_datetime(fault_level['Time'])
        time_df = time_df.reset_index(drop=True)
        time_df = time_df.loc[input_seq_len:, time].reset_index(drop=True)
        fault_level = pd.concat([time_df, fault_level], axis=1).drop('Time',axis=1).set_index(time)
        fault_level.fillna(0, inplace=True)

        fault_level = fault_level.resample('10T').mean()
        fault_level.columns = ['fault_level']

        for i in fault_level.index:
            if fault_level.loc[i,'fault_level'] == 0:
                Seq2Seq_meter.loc[i,'Power degradation'] = 0
        # fault_level = fault_level.dropna(axis=0)

        for i in Seq2Seq_meter.index:
            if i not in fault_level.index:
                # print('yes')
                Seq2Seq_meter = Seq2Seq_meter.drop(i,axis=0)

        overall_ = pd.concat([Seq2Seq_meter,fault_level],axis=1)
        # overall_ = pd.concat([overall_,overall])


        if unit == '3065':
            if date == '0121':
                overall_['Power degradation'] = overall_['Power degradation'] * 2
            if date == '0120':
                overall_['Power degradation'] = overall_['Power degradation'] * 0.5

        if unit == '3069':
            if date == '0119_2':
                overall_['Power degradation'] = overall_['Power degradation'] * 0.95
                overall_['fault_level'] = overall_['fault_level'].apply(lambda x: None if x >= 100 else x)
            if date == '0119_1':
                overall_['Power degradation'] = overall_['Power degradation'] * 1.7
                overall_['fault_level'] = overall_['fault_level'] * 1.05

        # elif unit == '3066':
        #     if date != '1229':
        #         overall_['fault_level'] = overall_['fault_level'].apply(lambda x: None if x == 0 else x)
        #         overall_['fault_level'] = overall_['fault_level'].apply(lambda x: None if x >= 100 else x)
        #     if date == '0730':
        #         overall_['fault_level'] = overall_['fault_level'].apply(lambda x: None if x <= 86 or x >= 95 else x)
        #         overall_['Power degradation'] = overall_['Power degradation'].apply(lambda x: None if x < 30 else x)
        #     if date == '0805':
        #         overall_['fault_level'] = overall_['fault_level'].apply(lambda x: None if x <= 70 or x >= 80 else x)
        #         # overall_['Power degradation'] = overall_['Power degradation'] * 1.2
        #         overall_['Power degradation'] = overall_['Power degradation'].apply(lambda x: None if x <= 15 else x)
        #     if date == '0804':
        #         overall_['fault_level'] = overall_['fault_level'].apply(lambda x: None if x <= 80 or x >= 90 else x)
        #         overall_['Power degradation'] = overall_['Power degradation'].apply(lambda x: None if x <= 20 or x >= 30 else x)
        #         overall_['Power degradation'] = overall_['Power degradation'] * 1.3
        #     if date == '0728':
        #         overall_['Power degradation'] = overall_['Power degradation'] * 0.2
        #         overall_['fault_level'] = overall_['fault_level'] * 0.1

        # overall_.dropna(inplace=True)

        overall_ = overall_.fillna(method='bfill')
        for i in range(len(overall_)):
            if overall_.loc[overall_.index[i], 'Power degradation'] == 0:
                overall_.loc[overall_.index[i], 'fault_level'] = 0

        overall_['Power degradation'] = overall_['Power degradation'] * 0.6

        # overall_.dropna(inplace=True)

        degradation = overall_['Power degradation'].sort_values()
        level = overall_['fault_level'].sort_values()

        print(overall_)

        label = ''
        if unit == '3066':
            if date == '1229':
                label = 'No fault'
            elif date == '0107':
                label = 'Fault type 4'
            elif date == '0106':
                label = 'Fault type 3'
            elif date == '1230':
                label = 'Fault type 2'
            elif date == '0105':
                label = 'Fault type 2'
        elif unit == '3067':
            if date == '0124_normal':
                label = 'No fault'
            elif date == '0124':
                label = 'Fault type 2'
            elif date == '0126_1':
                label = 'Fault type 3'
            elif date == '0126_2':
                label = 'Fault type 4'
        elif unit == '3065':
            if date == '0110':
                label = 'No fault'
            elif date == '0120':
                label = 'Fault type 2'
            elif date == '0121':
                label = 'Fault type 3'
        elif unit == '3069':
            if date == '0117':
                label = 'No fault'
            elif date == '0118':
                label = 'Fault type 2'
            elif date == '0119_1':
                label = 'Fault type 3'
            elif date == '0119_2':
                label = 'Fault type 4'

        plt.scatter(level, degradation, marker=marker[marker_idx], s=150, label=label)
        marker_idx += 1

    ax.add_patch(patches.Arrow(15, 0, 0, 10, width=3, facecolor='g',label='Fault level threshold = 15%'))
    ax.plot([0, 100], [10, 10], color='indigo', linestyle='-', linewidth=7,label='Fault impact ratio treshold = 10%')
    ax.set_xlabel('Estimated fault levels\nbased on virtual sensors [%]', fontsize=20, fontdict={'weight': 'bold'})
    ax.set_ylabel('Estimated fault impact ratio [%]', fontsize=20, fontdict={'weight': 'bold'})

    plt.legend(loc='upper center', fontsize=15,bbox_to_anchor=(0.5,1.2),ncol=3)
    plt.grid(b=True, which='both', axis='both', alpha=0.5, color='grey', ls='--')
    ax.autoscale(enable=True, axis='x', tight=True)
    ax.autoscale(enable=True, axis='y', tight=False)
    if unit == '3065':
        ax.add_patch(patches.Rectangle((16, 10.5), 83.5, 29, edgecolor='red', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,36, 'Condenser fouling\nfault', horizontalalignment='right',fontsize=17, color='red',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((16, 0.5), 83.5, 9, edgecolor='gray', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,6, 'Condenser fouling\nfault warning', horizontalalignment='right',fontsize=17, color='gray',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 0.5), 13.5, 9, edgecolor='blue', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7,5, 'No\nfault', horizontalalignment='center',fontsize=17, color='blue',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 10.5), 13.5, 29, edgecolor='green', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7.3, 34, 'Other\nfault\nwarning', horizontalalignment='center', fontsize=17, color='green',fontdict={'weight':'bold'})
    elif unit == '3066':
        ax.add_patch(patches.Rectangle((16, 10.5), 83.5, 29, edgecolor='red', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,36, 'Condenser fouling\nfault', horizontalalignment='right',fontsize=17, color='red',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((16, 0.5), 83.5, 9, edgecolor='gray', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,6, 'Condenser fouling\nfault warning', horizontalalignment='right',fontsize=17, color='gray',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 0.5), 13.5, 9, edgecolor='blue', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7,5, 'No\nfault', horizontalalignment='center',fontsize=17, color='blue',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 10.5), 13.5, 29, edgecolor='green', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7.3, 34, 'Other\nfault\nwarning', horizontalalignment='center', fontsize=17, color='green',fontdict={'weight':'bold'})
    elif unit == '3067':
        ax.add_patch(patches.Rectangle((16, 10.5), 83.5, 29, edgecolor='red', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,36, 'Condenser fouling\nfault', horizontalalignment='right',fontsize=17, color='red',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((16, 0.5), 83.5, 9, edgecolor='gray', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,6, 'Condenser fouling\nfault warning', horizontalalignment='right',fontsize=17, color='gray',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 0.5), 13.5, 9, edgecolor='blue', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7,5, 'No\nfault', horizontalalignment='center',fontsize=17, color='blue',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 10.5), 13.5, 29, edgecolor='green', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7.3, 34, 'Other\nfault\nwarning', horizontalalignment='center', fontsize=17, color='green',fontdict={'weight':'bold'})
    elif unit == '3069':
        ax.add_patch(patches.Rectangle((16, 10.5), 83.5, 29, edgecolor='red', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,36, 'Condenser fouling\nfault', horizontalalignment='right',fontsize=17, color='red',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((16, 0.5), 83.5, 9, edgecolor='gray', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(98,6, 'Condenser fouling\nfault warning', horizontalalignment='right',fontsize=17, color='gray',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 0.5), 13.5, 9, edgecolor='blue', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7,5, 'No\nfault', horizontalalignment='center',fontsize=17, color='blue',fontdict={'weight':'bold'})
        ax.add_patch(patches.Rectangle((0.5, 10.5), 13.5, 29, edgecolor='green', facecolor='red', fill=False, linewidth='3',linestyle='--'))
        ax.text(7.3, 34, 'Other\nfault\nwarning', horizontalalignment='center', fontsize=17, color='green',fontdict={'weight':'bold'})
    if unit == '3065':
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70,80,90,100])
        ax.set_xticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize=18)
        ax.set_yticks([0, 10, 20, 30, 40])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%'], fontsize=18)
    elif unit == '3066':
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70,80,90,100])
        ax.set_xticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize=18)
        ax.set_yticks([0, 10, 20, 30, 40])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%'], fontsize=18)
    elif unit == '3067':
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70,80,90,100])
        ax.set_xticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize=18)
        ax.set_yticks([0, 10, 20, 30, 40])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%'], fontsize=18)
    elif unit == '3069':
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70,80,90,100])
        ax.set_xticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize=18)
        ax.set_yticks([0, 10, 20, 30, 40])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%'], fontsize=18)
    plt.tight_layout()
    plt.show()
    # save_path = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/중간발표자료/fault impact/{}/'.format(unit)
    # create_folder(save_path)
    # plt.savefig(save_path+'/fault_impact_FDD_airflow.png', dpi=300)
    # plt.savefig(save_path + '/fault_impact_FDD.png', dpi=300)

