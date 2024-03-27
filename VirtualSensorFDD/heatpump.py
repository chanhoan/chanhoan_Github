import CoolProp as CP
import pandas as pd
import CoolProp
from CoolProp.Plots import PropertyPlot
import matplotlib.pyplot as plt

# suc_t = 31.49472
# dis_t = 90.33776
# cond_t_o = -14.83008
# high_p = 2.7*2
# low_p = 0.80032*2
#
# dis_h = CP.CoolProp.PropsSI('H', 'P', high_p * 100000, 'T', dis_t + 273.15, 'R404A') / 1000
# cond_h_o = CP.CoolProp.PropsSI('H', 'P', high_p * 100000, 'T', cond_t_o + 273.15, 'R404A') / 1000
# evap_h_i = CP.CoolProp.PropsSI('H', 'P', high_p * 100000, 'T', cond_t_o + 273.15, 'R404A') / 1000
# suc_h = CP.CoolProp.PropsSI('H', 'P', low_p * 100000, 'T', suc_t + 273.15, 'R404A') / 1000
# evap_t_i = CP.CoolProp.PropsSI('T', 'P', low_p * 100000, 'H', evap_h_i*1000, 'R404A') -273.15
#
# plt.cla()
# plt.clf()
# pp = PropertyPlot('R410A', 'PH')
# pp.calc_isolines(CoolProp.iT)
# pp.calc_isolines(CoolProp.iQ, num=11)
# # plt.xticks([100, 200, 300, 400, 500, 600])
# plt.scatter(dis_h, high_p * 100, marker='o', color='r')
# plt.scatter(cond_h_o, high_p * 100, marker='o', color='r')
# plt.scatter(evap_h_i, low_p * 100, marker='o', color='r')
# plt.scatter(suc_h, low_p * 100, marker='o', color='r')
# plt.plot([cond_h_o, dis_h], [high_p * 100, high_p * 100], color='r')
# plt.plot([cond_h_o, evap_h_i], [high_p * 100, low_p * 100], color='r')
# plt.plot([evap_h_i, suc_h], [low_p * 100, low_p * 100], color='r')
# plt.plot([dis_h, suc_h], [high_p * 100, low_p * 100], color='r')
# plt.text(dis_h, high_p * 100, '2')
# plt.text(cond_h_o, high_p * 100, '3')
# plt.text(evap_h_i, low_p * 100, '4')
# plt.text(suc_h, low_p * 100, '1')
# plt.tight_layout()
# plt.title('PH-Diagram of Cooling mode')
# pp.savefig('./cooling_mode.png')
#
# Qevap = abs(evap_h_i-suc_h)
# Wcomp = abs(dis_h-suc_h)
# COP = Qevap/Wcomp
#
# print("Evaporator inlet temperature : {:.2f} C".format(evap_t_i))
# print("Evaporator capacity : {:.2f} kJ/kg".format(Qevap))
# print("Compressor power : {:.2f} kJ/kg".format(Wcomp))
# print("COP : {}".format(COP))
#
# print('\n')

suc_t = 38.84633385
dis_t = 102.5960998
cond_t_o = -17.8773791
high_p = 3.0*2
low_p = 0.8*2

dis_h = CP.CoolProp.PropsSI('H', 'P', high_p * 100000, 'T', dis_t + 273.15, 'R404A') / 1000
cond_h_o = CP.CoolProp.PropsSI('H', 'P', high_p * 100000, 'T', cond_t_o + 273.15, 'R404A') / 1000
evap_h_i = CP.CoolProp.PropsSI('H', 'P', high_p * 100000, 'T', cond_t_o + 273.15, 'R404A') / 1000
suc_h = CP.CoolProp.PropsSI('H', 'P', low_p * 100000, 'T', suc_t + 273.15, 'R404A') / 1000
evap_t_i = CP.CoolProp.PropsSI('T', 'P', low_p * 100000, 'H', evap_h_i*1000, 'R404A') -273.15

plt.cla()
plt.clf()
pp = PropertyPlot('R410A', 'PH')
pp.calc_isolines(CoolProp.iT)
pp.calc_isolines(CoolProp.iQ, num=11)
# plt.xticks([100, 200, 300, 400, 500, 600])
plt.scatter(dis_h, high_p * 100, marker='o', color='r')
plt.scatter(cond_h_o, high_p * 100, marker='o', color='r')
plt.scatter(evap_h_i, low_p * 100, marker='o', color='r')
plt.scatter(suc_h, low_p * 100, marker='o', color='r')
plt.plot([cond_h_o, dis_h], [high_p * 100, high_p * 100], color='r')
plt.plot([cond_h_o, evap_h_i], [high_p * 100, low_p * 100], color='r')
plt.plot([evap_h_i, suc_h], [low_p * 100, low_p * 100], color='r')
plt.plot([dis_h, suc_h], [high_p * 100, low_p * 100], color='r')
plt.text(dis_h, high_p * 100, '2')
plt.text(cond_h_o, high_p * 100, '3')
plt.text(evap_h_i, low_p * 100, '4')
plt.text(suc_h, low_p * 100, '1')
plt.tight_layout()
plt.title('PH-Diagram of Heating mode')
pp.savefig('./heating_mode.png')

Qevap = abs(evap_h_i-suc_h)
Wcomp = abs(dis_h-suc_h)
COP = Qevap/Wcomp

print("Evaporator inlet temperature : {:.2f} C".format(evap_t_i))
print("Evaporator capacity : {:.2f} kJ/kg".format(Qevap))
print("Compressor power : {:.2f} kJ/kg".format(Wcomp))
print("COP : {}".format(COP))