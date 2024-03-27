import pandas as pd
import matplotlib.pyplot as plt


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


ymd = ['2021-07-28','2021-07-29','2021-07-30','2021-08-04','2021-08-05']
date = ['28','29','30','04','05',]
for i in range(5):
    directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\Data'
    data_28 = pd.read_csv(directory+'\{}\outdoor_{}_3066.csv'.format(ymd[i],date[i]))

    main_eev = data_28['eev1']
    evi_eev = data_28['evi_eev']
    evi_out_temp = data_28['double_tube_temp']
    evi_bypass_valve = data_28['evi_bypass_valve']
    liquid_bypass_valve = data_28['liquid_bypass_valve']
    time = data_28['Time']

    fig, ax1 = plt.subplots(figsize=(14,10))
    ax1.set_title('Vapor injection',fontsize=16)
    ax1.step(time,main_eev,c='b',linewidth=1.5,linestyle='-')
    ax1.step(time,evi_eev,c='c',linewidth=1.5,linestyle='-')
    ax1.set_ylim([0,2500])
    ax2 = ax1.twinx()
    ax2.step(time, liquid_bypass_valve, c='m', linewidth=1.5, linestyle='--')
    ax2.step(time,evi_bypass_valve,c='g',linewidth=1.5,linestyle='-')
    ax2.set_ylim([0,1.5])
    # ax2.step(time,liquid_bypass_valve,c='c',linewidth=1.5,linestyle='-')
    ax3 = ax1.twinx()
    make_patch_spines_invisible(ax3)
    ax3.spines["right"].set_position(("axes", 1.05))
    ax3.spines["right"].set_visible(True)
    ax3.plot(time,evi_out_temp,c='r',linewidth=1.5,linestyle='-')
    ax3.set_ylim([10,65])
    ax1.legend(['Main EEV','EVI EEV'],loc='upper left',fontsize=14)
    ax2.legend(['Liquid bypass valve','EVI bypass valve'],fontsize=14)
    ax3.legend(['Double tube temperature'],loc='upper center',fontsize=14)
    ax1.set_xlabel('Time',fontsize=14)
    ax1.set_ylabel('EEV',fontsize=14)
    ax2.set_ylabel('EVI bypass valve',fontsize=14)
    ax3.set_ylabel('Double tube temperature',fontsize=14)
    ax1.set_xticks([time[i] for i in range(len(time)) if i % 120 == 0])
    # plt.show()
    plt.tight_layout()
    plt.savefig('./{}_vapor_injection.png'.format(ymd[i]))