import CoolProp as CP
import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
from scipy.stats import norm


# 유닛에 따라 나누어 처리
class FDD1(object):
    def __init__(self, data, unit):
        # condenser air volume flow parameter
        self.condenser_3065 = ['m_dot_3065', 'high_pressure_3065', 'cond_in_temp_3065', 'cond_out_temp_3065',
                               'cond_in_air_3065', 'cond_out_air_3065', 'outdoor_temp_3065']
        self.condenser_3066 = ['m_dot_3066', 'high_pressure_3066', 'cond_in_temp_3066', 'cond_out_temp_3066',
                               'cond_in_air_3066', 'cond_out_air_3066', 'outdoor_temp_3066']
        self.condenser_3067 = ['m_dot_3067', 'high_pressure_3067', 'cond_in_temp_3067', 'cond_out_temp_3067',
                               'cond_in_air_3067', 'cond_out_air_3067', 'outdoor_temp_3067']
        self.condenser_3069 = ['m_dot_3069', 'high_pressure_3069', 'cond_in_temp_3069', 'cond_out_temp_3069',
                               'cond_in_air_3069', 'cond_out_air_3069', 'outdoor_temp_3069']
        self.c_pa = 1.005

        # evaporator air volume flow parameter
        self.evaporator_3065 = ['low_pressure_3065', 'suction_temp_3065']
        self.evaporator_3066 = ['low_pressure_3066', 'suction_temp_3066']
        self.evaporator_3067 = ['low_pressure_3067', 'suction_temp_3067']
        self.evaporator_3069 = ['low_pressure_3069', 'suction_temp_3069']

        # import data and set variable with unit number
        self.data = data
        self.unit = unit
        if self.unit == '3065':
            self.m_dot = self.data[self.condenser_3065[0]]
            self.high_pressure = self.data[self.condenser_3065[1]]
            self.cond_in_temp = self.data[self.condenser_3065[2]]
            self.cond_out_temp = self.data[self.condenser_3065[3]]
            self.cond_in_air = self.data[self.condenser_3065[4]]
            self.cond_out_air = self.data[self.condenser_3065[5]]
            self.outdoor_temp = self.data[self.condenser_3065[6]]
            self.low_pressure = self.data[self.evaporator_3065[0]]
            self.suction_temp = self.data[self.evaporator_3065[1]]
        elif self.unit == '3066':
            self.m_dot = self.data[self.condenser_3066[0]]
            self.high_pressure = self.data[self.condenser_3066[1]]
            self.cond_in_temp = self.data[self.condenser_3066[2]]
            self.cond_out_temp = self.data[self.condenser_3066[3]]
            self.cond_in_air = self.data[self.condenser_3066[4]]
            self.cond_out_air = self.data[self.condenser_3066[5]]
            self.outdoor_temp = self.data[self.condenser_3066[6]]
            self.low_pressure = self.data[self.evaporator_3066[0]]
            self.suction_temp = self.data[self.evaporator_3066[1]]
        elif self.unit == '3067':
            self.m_dot = self.data[self.condenser_3067[0]]
            self.high_pressure = self.data[self.condenser_3067[1]]
            self.cond_in_temp = self.data[self.condenser_3067[2]]
            self.cond_out_temp = self.data[self.condenser_3067[3]]
            self.cond_in_air = self.data[self.condenser_3067[4]]
            self.cond_out_air = self.data[self.condenser_3067[5]]
            self.outdoor_temp = self.data[self.condenser_3067[6]]
            self.low_pressure = self.data[self.evaporator_3067[0]]
            self.suction_temp = self.data[self.evaporator_3067[1]]
        elif self.unit == '3069':
            self.m_dot = self.data[self.condenser_3069[0]]
            self.high_pressure = self.data[self.condenser_3069[1]]
            self.cond_in_temp = self.data[self.condenser_3069[2]]
            self.cond_out_temp = self.data[self.condenser_3069[3]]
            self.cond_in_air = self.data[self.condenser_3069[4]]
            self.cond_out_air = self.data[self.condenser_3069[5]]
            self.outdoor_temp = self.data[self.condenser_3069[6]]
            self.low_pressure = self.data[self.evaporator_3069[0]]
            self.suction_temp = self.data[self.evaporator_3069[1]]

        self.h = []
        self.v = []
        self.V_AFC = []
        self.V_AFE = []

        self.air_specific_volume = self.specific_volume(self.outdoor_temp, 'Air')
        self.cond_in_h = self.enthalpy(self.high_pressure, self.cond_in_temp, 'R410A')
        self.cond_out_h = self.enthalpy(self.high_pressure, self.cond_out_temp, 'R410A')
        self.evap_out_h = self.enthalpy(self.low_pressure, self.suction_temp, 'R410A')

        self.AirFlowCond = self.condenser_air_flow()
        self.AirFlowEvap = self.evaporator_air_flow()

        self.mean = 0
        self.std = 0
        self.aa = 0
        self.b = 0
        self.cc = 0

        self.AirFlowCond_mean, self.AirFlowCond_std = self.get_mean_std(self.AirFlowCond)
        self.AirFlowEvap_mean, self.AirFlowEvap_std = self.get_mean_std(self.AirFlowEvap)

        self.AirFlowCond_mean_base = 0
        self.AirFlowCond_std_base = 0
        self.AirFlowEvap_mean_base = 0
        self.AirFlowEvap_std_base = 0

        self.cond_fouling_threshold = 0
        self.evap_fouling_threshold = 0

        self.x = np.linspace(0, 50, 1000)
        self.result = self.solve(self.AirFlowCond_mean_base, self.AirFlowCond_mean, self.AirFlowCond_std_base,
                                 self.AirFlowCond_std)

    def enthalpy(self, pressure, temperature, material):
        self.h = []
        for i in range(len(pressure)):
            self.h.append(
                CP.CoolProp.PropsSI('H', 'P', pressure[i] * 100000, 'T', temperature[i] + 273.15, material))
        return self.h

    def specific_volume(self, temperature, material):
        self.v = []
        for i in range(len(temperature)):
            self.v.append(CP.CoolProp.PropsSI('D', 'P', 101325, 'T', temperature[i] + 273.15, material))
        return self.v

    def condenser_air_flow(self):
        self.V_AFC = []
        for i in range(len(self.data)):
            v = (self.m_dot[i] * (self.cond_in_h[i] - self.cond_out_h[i]) * self.air_specific_volume[i]) / (
                    self.c_pa * (self.cond_out_air[i] - self.cond_in_air[i]))
            self.V_AFC.append(v)
        return self.V_AFC

    def evaporator_air_flow(self):
        self.V_AFE = []
        for i in range(len(self.data)):
            v = (self.m_dot[i] * (self.cond_out_h[i] - self.evap_out_h[i]) * self.air_specific_volume[i]) / (
                    self.c_pa * (self.cond_in_air[i] - self.cond_out_air[i]))
            self.V_AFE.append(v)
        return self.V_AFE

    def get_mean_std(self, data):
        self.mean = statistics.mean(data)
        self.std = statistics.stdev(data)
        return self.mean, self.std

    def solve(self, m1, m2, std1, std2):
        self.aa = 1 / (2 * std1 ** 2) - 1 / (2 * std2 ** 2)
        self.b = m2 / (std2 ** 2) - m1 / (std1 ** 2)
        self.cc = m1 ** 2 / (2 * std1 ** 2) - m2 ** 2 / (2 * std2 ** 2) - np.log(std2 / std1)
        return np.roots([self.aa, self.b, self.cc])

    def condenser_fouling(self):
        fig, ax1 = plt.subplots(figsize=(12, 8))
        plt.title('Condenser Fouling Detection', fontsize=24, fontweight='bold')
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowCond_mean_base, self.AirFlowCond_std_base), color='b',
                 linewidth=2)
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowCond_mean, self.AirFlowCond_std), color='r', linewidth=2)
        plt.plot([self.AirFlowCond_mean_base, self.AirFlowCond_mean_base], [0, 2], color='b', linestyle='-.',
                 linewidth=2)
        plt.plot([self.AirFlowCond_mean, self.AirFlowCond_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
        r = self.result[0]
        if self.AirFlowCond_mean > self.AirFlowCond_mean_base:
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowCond_mean_base,
                                                             self.AirFlowCond_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowCond_mean,
                                                             self.AirFlowCond_std), color='red', alpha=0.3)
            area = norm.cdf(r, self.AirFlowCond_mean, self.AirFlowCond_std) + \
                   1 - (norm.cdf(r, self.AirFlowCond_mean_base, self.AirFlowCond_std_base))
            area = float("{0:.5f}".format(area))
        else:
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowCond_mean_base,
                                                             self.AirFlowCond_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowCond_mean,
                                                             self.AirFlowCond_std), color='red', alpha=0.3)
            area = 1 - norm.cdf(r, self.AirFlowCond_mean, self.AirFlowCond_std) + \
                   (norm.cdf(r, self.AirFlowCond_mean_base, self.AirFlowCond_std_base))
        print("volumetric air flow normal distribution area under curves ", area)
        axes = plt.gca()
        axes.set_ylim([0, 1.0])
        axes.set_xlim([self.AirFlowCond_mean_base - 10, self.AirFlowCond_mean_base + 20])
        plt.ylabel('Probability', fontsize=22, fontweight='bold')
        plt.xlabel('Volumetric air flow [m]', fontsize=22, fontweight='bold')
        axes.text(1, 0.95, 'Area under curves: {}'.format(area), horizontalalignment='right', transform=axes.transAxes,
                  fontsize=16, color='black')
        if area < self.cond_fouling_threshold:
            axes.text(1, 0.85, 'Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16, color='red')
        else:
            axes.text(1, 0.85, 'No Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16,
                      color='blue')
        legend = plt.legend(['Normal Distribution of Virtual Sensor Prediction [Normal Condition]',
                             'Normal Distribution of Virtual Sensor Prediction [Fault Condition]'], loc='upper left',
                            fontsize=14, bbox_to_anchor=(0.1, -0.1))
        plt.show()
        return fig.savefig('./CondenserFouling.png', bbox_extra_artists=(legend,), bbox_inches='tight')

    def evaporator_fouling(self):
        fig, ax1 = plt.subplots(figsize=(12, 8))
        plt.title('Evaporator Fouling Detection', fontsize=24, fontweight='bold')
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowEvap_mean_base, self.AirFlowEvap_std_base), color='b',
                 linewidth=2)
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowEvap_mean, self.AirFlowEvap_std), color='r', linewidth=2)
        plt.plot([self.AirFlowEvap_mean_base, self.AirFlowEvap_mean_base], [0, 2], color='b', linestyle='-.',
                 linewidth=2)
        plt.plot([self.AirFlowEvap_mean, self.AirFlowEvap_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
        r = self.result[0]
        if self.AirFlowEvap_mean > self.AirFlowEvap_mean_base:
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowEvap_mean_base,
                                                             self.AirFlowEvap_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowEvap_mean,
                                                             self.AirFlowEvap_std), color='red', alpha=0.3)
            area = norm.cdf(r, self.AirFlowEvap_mean, self.AirFlowEvap_std) + \
                   1 - (norm.cdf(r, self.AirFlowEvap_mean_base, self.AirFlowEvap_std_base))
            area = float("{0:.5f}".format(area))
        else:
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowEvap_mean_base,
                                                             self.AirFlowEvap_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowEvap_mean,
                                                             self.AirFlowEvap_std), color='red', alpha=0.3)
            area = 1 - norm.cdf(r, self.AirFlowEvap_mean, self.AirFlowEvap_std) + \
                   (norm.cdf(r, self.AirFlowEvap_mean_base, self.AirFlowEvap_std_base))
        print("volumetric air flow normal distribution area under curves ", area)
        axes = plt.gca()
        axes.set_ylim([0, 1.0])
        axes.set_xlim([self.AirFlowEvap_mean_base - 10, self.AirFlowEvap_mean_base + 20])
        plt.ylabel('Probability', fontsize=22, fontweight='bold')
        plt.xlabel('Temperature [C]', fontsize=22, fontweight='bold')
        axes.text(1, 0.95, 'Area under curves: {}'.format(area), horizontalalignment='right', transform=axes.transAxes,
                  fontsize=16, color='black')
        if area < self.evap_fouling_threshold:
            axes.text(1, 0.85, 'Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16, color='red')
        else:
            axes.text(1, 0.85, 'No Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16,
                      color='blue')
        legend = plt.legend(['Normal Distribution of Virtual Sensor Prediction [Normal Evapition]',
                             'Normal Distribution of Virtual Sensor Prediction [Fault Evapition]'], loc='upper left',
                            fontsize=14, bbox_to_anchor=(0.1, -0.1))
        plt.show()
        return fig.savefig('./EvapenserFouling.png', bbox_extra_artists=(legend,), bbox_inches='tight')


# 유닛 나누지 않고 처리
class FDD2(object):
    def __init__(self, m_dot, P_high, cond_in_temp, cond_out_temp, cond_in_air,cond_out_air,outdoor_temp,low_pressure,suction_temp,ref,P_ll,T_ll,Q_ref,Q_air,
                 evap_out_temp,evap_out_air,evap_in_air,T_sh,T_sc):
        self.data = m_dot
        self.m_dot = m_dot
        self.high_pressure = P_high
        self.ll_pressure = P_ll
        self.cond_in_temp = cond_in_temp
        self.cond_out_temp = cond_out_temp
        self.cond_in_air = cond_in_air
        self.cond_out_air = cond_out_air
        self.outdoor_temp = outdoor_temp
        self.low_pressure = low_pressure
        self.suction_temp = suction_temp
        self.Q_ref = Q_ref
        self.c_pa = 1.005
        self.ref = ref
        self.liquid_temp = T_ll
        self.Q_air = Q_air
        self.evap_out_temp = evap_out_temp
        self.evap_in_air = evap_in_air
        self.evap_out_air = evap_out_air
        self.T_sh = T_sh
        self.T_sc = T_sc

        self.h = []
        self.v = []
        self.V_AFC = []
        self.V_AFE = []

        self.air_specific_volume = self.specific_volume(self.outdoor_temp, 'Air')
        self.cond_in_h = self.enthalpy(self.high_pressure, self.cond_in_temp, self.ref)
        self.cond_out_h1 = self.enthalpy(self.high_pressure, self.cond_out_temp, self.ref)
        self.cond_out_h2 = self.enthalpy(self.ll_pressure, self.liquid_temp, self.ref)
        self.evap_out_h = self.enthalpy(self.low_pressure, self.evap_out_temp, self.ref)
        self.evap_in_h = self.enthalpy(self.high_pressure, self.cond_out_temp, self.ref)

        # self.AirFlowCond = self.condenser_air_flow()
        # self.AirFlowEvap = self.evaporator_air_flow()

        self.mean = 0
        self.std = 0
        self.aa = 0
        self.b = 0
        self.cc = 0

        # self.AirFlowCond_mean, self.AirFlowCond_std = self.get_mean_std(self.AirFlowCond)
        # self.AirFlowEvap_mean, self.AirFlowEvap_std = self.get_mean_std(self.AirFlowEvap)

        self.AirFlowCond_mean_base = 1
        self.AirFlowCond_std_base = 1
        self.AirFlowEvap_mean_base = 1
        self.AirFlowEvap_std_base = 1

        self.cond_fouling_threshold = 0
        self.evap_fouling_threshold = 0

        self.x = np.linspace(0, 50, 1000)
        # self.result = self.solve(self.AirFlowCond_mean_base, self.AirFlowCond_mean, self.AirFlowCond_std_base,
        #                          self.AirFlowCond_std)

        self.fault_level = []

        self.T_sh_rated = 8.783
        self.T_sc_rated = 6.504
        self.T_sh_diff = []
        self.T_sc_diff = []
        self.VRC = []

        self.a0 = 0.04847089
        self.a1 = -0.01401478

    def Tsat(self,P_dis,P_suc,ref):
        T_c = []
        T_e = []
        for i in range(len(self.data)):
            T_c.append(CP.CoolProp.PropsSI('T','P',P_dis[i]*1000,'Q',0.5,ref)-273.15)
            T_e.append(CP.CoolProp.PropsSI('T','P',P_suc[i]*1000,'Q',0.5,ref)-273.15)
        return T_c,T_e

    def enthalpy(self, pressure, temperature, material):
        self.h = []
        for i in range(len(pressure)):
            try:
                self.h.append(CP.CoolProp.PropsSI('H', 'P', pressure[i] * 1000, 'T', temperature[i] + 273, material)/1000)
            except:
                self.h.append(None)
        return self.h

    def specific_volume(self, temperature, material):
        self.v = []
        for i in range(len(temperature)):
            self.v.append(1/CP.CoolProp.PropsSI('D', 'P', 101325, 'T', temperature[i] + 273, material))
        return self.v

    def condenser_air_flow1(self):
        self.V_AFC = []
        for i in range(len(self.data)):
            v = (self.m_dot[i] * (self.cond_in_h[i] - self.cond_out_h1[i])) / (self.c_pa * (self.cond_out_air[i] - self.cond_in_air[i]))
            self.V_AFC.append(v)
        return self.V_AFC

    def condenser_air_flow2(self):
        self.V_AFC = []
        for i in range(len(self.data)):
            try:
                v = (self.m_dot[i] * (self.cond_in_h[i] - self.cond_out_h2[i])) / (self.c_pa * (self.cond_out_air[i] - self.cond_in_air[i]))
            except:
                v = None
            self.V_AFC.append(v)
        return self.V_AFC

    def condenser_air_flow3(self):
        self.V_AFC = []
        for i in range(len(self.data)):
            try:
                v = (self.m_dot[i] * (self.cond_in_h[i] - self.cond_out_h2[i])) / (self.c_pa * (self.liquid_temp[i] - self.cond_in_air[i]))
            except:
                v = None
            self.V_AFC.append(v)
        return self.V_AFC

    def evaporator_air_flow1(self):
        self.V_AFE = []
        for i in range(len(self.data)):
            v = (self.m_dot[i] * abs(self.evap_out_h[i] - self.evap_in_h[i])) / (self.c_pa * abs(self.evap_out_air[i] - self.evap_in_air[i]))
            self.V_AFE.append(v)
        return self.V_AFE

    def evaporator_air_flow2(self):
        self.V_AFE = []
        for i in range(len(self.data)):
            v = (self.Q_ref[i] / (self.c_pa * abs(self.evap_out_air[i] - self.evap_in_air[i])))
            self.V_AFE.append(v)
        return self.V_AFE

    def evaporator_air_flow3(self):
        self.V_AFE = []
        for i in range(len(self.data)):
            v = (self.Q_air[i] / (self.c_pa * abs(self.evap_out_air[i] - self.evap_in_air[i])))
            self.V_AFE.append(v)
        return self.V_AFE

    def refrigerant_charge_sensor(self):
        self.T_sc_diff = []
        self.T_sh_diff = []
        self.VRC = []
        for i in range(len(self.data)):
            self.T_sc_diff.append(self.T_sc[i] - self.T_sc_rated)
            self.T_sh_diff.append(self.T_sh[i] - self.T_sh_rated)
        for i in range(len(self.data)):
            vrc = self.T_sc_diff[i]*self.a0 + self.T_sh_diff[i]*self.a1
            self.VRC.append((1+round(vrc,2))*100)
        return self.VRC

    def get_mean_std(self, data):
        self.mean = statistics.mean(data)
        self.std = statistics.stdev(data)
        return self.mean, self.std

    def solve(self, m1, m2, std1, std2):
        self.aa = 1 / (2 * std1 ** 2) - 1 / (2 * std2 ** 2)
        self.b = m2 / (std2 ** 2) - m1 / (std1 ** 2)
        self.cc = m1 ** 2 / (2 * std1 ** 2) - m2 ** 2 / (2 * std2 ** 2) - np.log(std2 / std1)
        return np.roots([self.aa, self.b, self.cc])

    def faultLevel(self, pred, actual):
        self.fault_level = []
        for i in range(len(pred)):
            fl = 100*abs(pred[i]-actual[i])/actual[i]
            if fl >= 100:
                fl = 100
            self.fault_level.append(fl)
        return self.fault_level

    def condenser_fouling(self):
        fig, ax1 = plt.subplots(figsize=(12, 8))
        plt.title('Condenser Fouling Detection', fontsize=24, fontweight='bold')
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowCond_mean_base, self.AirFlowCond_std_base),
                 color='b', linewidth=2)
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowCond_mean, self.AirFlowCond_std), color='r', linewidth=2)
        plt.plot([self.AirFlowCond_mean_base, self.AirFlowCond_mean_base], [0, 2], color='b', linestyle='-.',
                 linewidth=2)
        plt.plot([self.AirFlowCond_mean, self.AirFlowCond_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
        r = self.result[0]
        if self.AirFlowCond_mean > self.AirFlowCond_mean_base:
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowCond_mean_base,
                                                             self.AirFlowCond_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowCond_mean,
                                                             self.AirFlowCond_std), color='red', alpha=0.3)
            area = norm.cdf(r, self.AirFlowCond_mean, self.AirFlowCond_std) + \
                   1 - (norm.cdf(r, self.AirFlowCond_mean_base, self.AirFlowCond_std_base))
            area = float("{0:.5f}".format(area))
        else:
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowCond_mean_base,
                                                             self.AirFlowCond_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowCond_mean,
                                                             self.AirFlowCond_std), color='red', alpha=0.3)
            area = 1 - norm.cdf(r, self.AirFlowCond_mean, self.AirFlowCond_std) + \
                   (norm.cdf(r, self.AirFlowCond_mean_base, self.AirFlowCond_std_base))
        print("volumetric air flow normal distribution area under curves ", area)
        axes = plt.gca()
        axes.set_ylim([0, 1.0])
        axes.set_xlim([self.AirFlowCond_mean_base - 10, self.AirFlowCond_mean_base + 20])
        plt.ylabel('Probability', fontsize=22, fontweight='bold')
        plt.xlabel('Volumetric air flow [m]', fontsize=22, fontweight='bold')
        axes.text(1, 0.95, 'Area under curves: {}'.format(area), horizontalalignment='right', transform=axes.transAxes,
                  fontsize=16, color='black')
        if area < self.cond_fouling_threshold:
            axes.text(1, 0.85, 'Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16, color='red')
        else:
            axes.text(1, 0.85, 'No Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16,
                      color='blue')
        legend = plt.legend(['Normal Distribution of Virtual Sensor Prediction [Normal Condition]',
                             'Normal Distribution of Virtual Sensor Prediction [Fault Condition]'], loc='upper left',
                            fontsize=14, bbox_to_anchor=(0.1, -0.1))
        # plt.show()
        return fig.savefig('./CondenserFouling.png', bbox_extra_artists=(legend,), bbox_inches='tight')

    def evaporator_fouling(self):
        fig, ax1 = plt.subplots(figsize=(12, 8))
        plt.title('Evaporator Fouling Detection', fontsize=24, fontweight='bold')
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowEvap_mean_base, self.AirFlowEvap_std_base), color='b',
                 linewidth=2)
        plt.plot(self.x, norm.pdf(self.x, self.AirFlowEvap_mean, self.AirFlowEvap_std), color='r', linewidth=2)
        plt.plot([self.AirFlowEvap_mean_base, self.AirFlowEvap_mean_base], [0, 2], color='b', linestyle='-.',
                 linewidth=2)
        plt.plot([self.AirFlowEvap_mean, self.AirFlowEvap_mean], [0, 2], color='r', linestyle='-.', linewidth=2)
        r = self.result[0]
        if self.AirFlowEvap_mean > self.AirFlowEvap_mean_base:
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowEvap_mean_base,
                                                             self.AirFlowEvap_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowEvap_mean,
                                                             self.AirFlowEvap_std), color='red', alpha=0.3)
            area = norm.cdf(r, self.AirFlowEvap_mean, self.AirFlowEvap_std) + \
                   1 - (norm.cdf(r, self.AirFlowEvap_mean_base, self.AirFlowEvap_std_base))
            area = float("{0:.5f}".format(area))
        else:
            plt.fill_between(self.x[self.x < r], 0, norm.pdf(self.x[self.x < r], self.AirFlowEvap_mean_base,
                                                             self.AirFlowEvap_std_base), color='red', alpha=0.3)
            plt.fill_between(self.x[self.x > r], 0, norm.pdf(self.x[self.x > r], self.AirFlowEvap_mean,
                                                             self.AirFlowEvap_std), color='red', alpha=0.3)
            area = 1 - norm.cdf(r, self.AirFlowEvap_mean, self.AirFlowEvap_std) + \
                   (norm.cdf(r, self.AirFlowEvap_mean_base, self.AirFlowEvap_std_base))
        print("volumetric air flow normal distribution area under curves ", area)
        axes = plt.gca()
        axes.set_ylim([0, 1.0])
        axes.set_xlim([self.AirFlowEvap_mean_base - 10, self.AirFlowEvap_mean_base + 20])
        plt.ylabel('Probability', fontsize=22, fontweight='bold')
        plt.xlabel('Temperature [C]', fontsize=22, fontweight='bold')
        axes.text(1, 0.95, 'Area under curves: {}'.format(area), horizontalalignment='right', transform=axes.transAxes,
                  fontsize=16, color='black')
        if area < self.evap_fouling_threshold:
            axes.text(1, 0.85, 'Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16, color='red')
        else:
            axes.text(1, 0.85, 'No Fault', horizontalalignment='right', transform=axes.transAxes, fontsize=16,
                      color='blue')
        legend = plt.legend(['Normal Distribution of Virtual Sensor Prediction [Normal Evapition]',
                             'Normal Distribution of Virtual Sensor Prediction [Fault Evapition]'], loc='upper left',
                            fontsize=14, bbox_to_anchor=(0.1, -0.1))
        plt.show()
        return fig.savefig('./EvapenserFouling.png', bbox_extra_artists=(legend,), bbox_inches='tight')
