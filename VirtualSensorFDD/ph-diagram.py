import CoolProp as CP
import pandas as pd
import CoolProp
from CoolProp.Plots import PropertyPlot
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\b.IOT\디지털도서관\0721\outdoor(1min)_디지털도서관_0721.csv')
time = data['updated_time']

low_p = data['low_pressure']
high_p = data['high_pressure']
dis_t1 = data['discharge_temp1']
dis_t2 = data['discharge_temp2']
cond_t_o = data['double_tube_temp']
evap_t_i = data['double_tube_temp'] #isenthalpic process through expansion valve
suc_t = data['suction_temp1']
dis_t = []

dis_h = []
cond_h_o = []
evap_h_i = []
suc_h = []

for i in range(len(data)):
    if dis_t1[i] > dis_t2[i]:
        dis_t.append(dis_t1[i])
    elif dis_t2[i] > dis_t1[i]:
        dis_t.append(dis_t2[i])
    else:
        dis_t.append(dis_t1[i])

for i in range(len(data)):
    dis_h.append(CP.CoolProp.PropsSI('H','P',high_p[i]*98.0665*1000,'T',dis_t[i]+273.15,'R410A')/1000)
    cond_h_o.append(CP.CoolProp.PropsSI('H','P',high_p[i]*98.0665*1000,'T',cond_t_o[i]+273.15,'R410A')/1000)
    evap_h_i.append(CP.CoolProp.PropsSI('H','P',high_p[i]*98.0665*1000,'T',cond_t_o[i]+273.15,'R410A')/1000)
    suc_h.append(CP.CoolProp.PropsSI('H', 'P', low_p[i]*98.0665*1000, 'T', suc_t[i]+273.15, 'R410A')/1000)
    # print(high_p[i]*1000)

enthalpy = pd.DataFrame(np.column_stack([dis_h,cond_h_o,evap_h_i,suc_h]),columns=['Discharge','Condenser Outlet','Evaporator Inlet','Suction'])

for i in range(len(data)):
    if dis_h[i] < suc_h[i]:
        continue
    elif cond_h_o[i] > 400:
        continue
    if i == 0:
        pass
    if dis_h[i] == dis_h[i-1]:
        continue

    print(time[i][0:16])
    plt.cla()
    plt.clf()
    pp = PropertyPlot('R410A', 'PH')
    pp.calc_isolines(CoolProp.iT)
    pp.calc_isolines(CoolProp.iQ, num=11)
    plt.xticks([100,200,300,400,500,600])
    plt.scatter(dis_h[i],high_p[i]*98,marker='o',color='r')
    plt.scatter(cond_h_o[i], high_p[i] * 98.0665, marker='o', color='r')
    plt.scatter(evap_h_i[i], low_p[i] * 98.0665, marker='o', color='r')
    plt.scatter(suc_h[i], low_p[i] * 98.0665, marker='o', color='r')
    plt.plot([cond_h_o[i],dis_h[i]],[high_p[i]*98.0665,high_p[i]*98.0665],color='r')
    plt.plot([cond_h_o[i], evap_h_i[i]], [high_p[i]* 98.0665,low_p[i]* 98.0665], color='r')
    plt.plot([evap_h_i[i],suc_h[i]],[low_p[i] * 98.0665, low_p[i] * 98.0665], color='r')
    plt.plot([dis_h[i],suc_h[i]], [high_p[i] * 98.0665, low_p[i] * 98.0665], color='r')
    plt.text(dis_h[i]+10,high_p[i]*98.0665,'Compressor outlet')
    plt.text(cond_h_o[i]-50,high_p[i]*98.0665+250,'Condenser outlet')
    plt.text(evap_h_i[i]-50, low_p[i] * 98.0665-200, 'Evaporator inlet')
    plt.text(suc_h[i]+10, low_p[i] * 98.0665, 'Compressor inlet')
    plt.tight_layout()
    plt.title('PH-Diagram of DVM S')
    plt.text(450,9000,'Date/Time:{}'.format(time[i][0:16]))
    pp.savefig(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\b.IOT\디지털도서관\0721\ph-Diagram\ph-Diagram_{}-{}.png'.format(time[i][11:13],time[i][14:16]))

