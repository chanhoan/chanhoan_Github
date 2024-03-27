import pandas as pd
import numpy as np
import datetime as dt
import os
import CoolProp as CP


class comp_model(object):
    def __init__(self, model, file_path, date, freq, unit):
        self.unit = unit
        self.model = model
        self.date = date
        for i in os.listdir(file_path):
            if 'outdoor' in i:
                path = file_path + '/' + i
                print(path)
        self.data = pd.read_csv(path)
        self.file_path = file_path + '/'
        self.freq = freq
        if self.freq == 1:
            self.f = self.data['comp_current_frequency1']
        elif self.freq == 2:
            self.f = self.data['comp_current_frequency2']
        self.P_dis = self.data['high_pressure']
        self.P_suc = self.data['low_pressure']
        self.T_suc = self.data['suction_temp1']
        self.dis_t1 = self.data['discharge_temp1']
        self.dis_t2 = self.data['discharge_temp2']
        self.cond_o_t = self.data['cond_out_temp1']
        self.liq_t = self.data['double_tube_temp']
        self.Tc, self.Te = self.Tsat()

        if model == 'GB052':
            # m_dot_rated coefficient
            self.a0 = 1.34583367e+0
            self.a1 = 1.30612964e+0
            self.a2 = 8.16473285e-2
            self.a3 = 6.64829686e-5
            self.a4 = 1.71071419e+1
            self.a5 = -3.2517798e-1
            self.a6 = 2.0076971000e-3
            self.a7 = 3.35711090e-1
            self.a8 = -3.11725301e-3
            self.a9 = 6.35877854e-4
            self.a10 = 2.06143118e-13
            # w_dot_rated coefficient
            self.b0 = 3.51846146e+0
            self.b1 = 3.57686903e+0
            self.b2 = 6.43560572e-1
            self.b3 = 1.50045118e-5
            self.b4 = 3.07724735e+1
            self.b5 = 1.96728924e+0
            self.b6 = -1.55914878e-2
            self.b7 = -4.89411467e-2
            self.b8 = -7.434599943e-4
            self.b9 = -9.79711966e-3
            self.b10 = 2.82415926e-12
            # m_dot_pred coefficient
            self.c0 = 9.98623382E-1 * 0.30
            self.c1 = 1.70178410E-2 * 0.30
            self.c2 = -1.85413544E-5 * 0.30
            # w_dot_pred coefficient
            self.d0 = 9.99818595E-01 * 0.30
            self.d1 = 2.11652803E-02 * 0.30
            self.d2 = 1.17252618E-04 * 0.30

        elif model == 'GB066':
            # m_dot_rated coefficient
            self.a0 = 1.91778583E+0
            self.a1 = 3.28857174E+0
            self.a2 = 1.84065620E-1
            self.a3 = 7.14011551E-5
            self.a4 = 2.10278731E+1
            self.a5 = -3.92042237E-1
            self.a6 = 2.38168548E-3
            self.a7 = 3.65647991E-1
            self.a8 = -3.43302726E-3
            self.a9 = -5.06182999E-4
            self.a10 = -1.49453769E-13
            # w_dot_rated coefficient
            self.b0 = 4.68221681E+0
            self.b1 = 2.89315135E+1
            self.b2 = 5.08822631E-1
            self.b3 = -2.52904377E-6
            self.b4 = 3.72538174E+1
            self.b5 = 2.52480352E+0
            self.b6 = -1.98829304E-2
            self.b7 = -6.79818927E-1
            self.b8 = 1.96893378E-3
            self.b9 = -3.26935360E-3
            self.b10 = -2.85508042E-12
            # m_dot_pred coefficient
            self.c0 = 9.90958566E-1
            self.c1 = 1.66658435E-2
            self.c2 = -1.91782998E-5
            # w_dot_pred coefficient
            self.d0 = 6.5629020e-02
            self.d1 = 1.3365647e-03
            self.d2 = 3.4921488e-06

        elif model == 'GB070':
            # m_dot_rated coefficient
            self.a0 = 3.45223093E+0
            self.a1 = 9.58731730E+0
            self.a2 = 2.65999052E-1
            self.a3 = 4.99983074E-5
            self.a4 = 2.61357700E+1
            self.a5 = -4.95946275E-1
            self.a6 = 3.07594686E-3
            self.a7 = 2.45668661E-1
            self.a8 = -2.42475689E-3
            self.a9 = -1.05368068E-3
            self.a10 = -3.92888272E-13
            # w_dot_rated coefficient
            self.b0 = 4.68221681E+0
            self.b1 = 2.89315135E+1
            self.b2 = 5.08822631E-1
            self.b3 = -2.52904377E-6
            self.b4 = 3.72538174E+1
            self.b5 = 2.52480352E+0
            self.b6 = -1.98829304E-2
            self.b7 = -6.79818927E-1
            self.b8 = 1.96893378E-3
            self.b9 = -3.26935360E-3
            self.b10 = -2.85508042E-12
            # m_dot_pred coefficient
            self.c0 = 8.73877476E-1 * 0.24
            self.c1 = 1.42782414E-2 * 0.24
            self.c2 = -1.66033155E-5 * 0.24
            # w_dot_pred coefficient
            self.d0 = 1.03655761E+0 * 0.24
            self.d1 = 2.18790914E-02 * 0.24
            self.d2 = 1.20530958E-04 * 0.24

        elif model == 'GB080':
            # m_dot_rated coefficient
            self.a0 = 2.94692558E+0
            self.a1 = 8.09167658E+0
            self.a2 = 2.62344701E-1
            self.a3 = 5.32184444E-5
            self.a4 = 2.59520736E+1
            self.a5 = -4.81374673E-1
            self.a6 = 2.88635012E-3
            self.a7 = 2.94984013E-1
            self.a8 = -2.80522711E-3
            self.a9 = -1.41173400E-3
            self.a10 = 1.58730325E-13
            # w_dot_rated coefficient
            self.b0 = 2.65608412E+0
            self.b1 = 2.81012263E+1
            self.b2 = -2.82198326E-0
            self.b3 = -2.80384826E-4
            self.b4 = 2.81501305E+1
            self.b5 = 3.50317115E+0
            self.b6 = -2.70107151E-2
            self.b7 = -6.07810636E-1
            self.b8 = 2.41499759E-3
            self.b9 = 6.42414150E-3
            self.b10 = 3.60750696E-12
            # m_dot_pred coefficient
            self.c0 = 1.00362719E-0
            self.c1 = 1.75723734E-2
            self.c2 = -6.37848299E-5
            # w_dot_pred coefficient
            self.d0 = 9.97164782E-1 * 0.24
            self.d1 = 2.10053578E-2 * 0.24
            self.d2 = 6.99834241E-5 * 0.24

    def Density(self):
        D = []
        T_suc = self.T_suc
        P_suc = self.P_suc
        for i in range(len(self.data)):
            D.append(CP.CoolProp.PropsSI('D', 'P', P_suc[i] * 98.0665 * 1000, 'T', T_suc[i] + 273, 'R410A'))
        return D

    def Tsat(self):
        T_c = []
        T_e = []
        P_dis = self.P_dis
        P_suc = self.P_suc
        for i in range(len(self.data)):
            T_c.append(CP.CoolProp.PropsSI('T', 'P', P_dis[i] * 98.0665 * 1000, 'Q', 0.5, 'R410A') - 273.15)
            T_e.append(CP.CoolProp.PropsSI('T', 'P', P_suc[i] * 98.0665 * 1000, 'Q', 0.5, 'R410A') - 273.15)
        return T_c, T_e

    def m_dot_rated(self):
        m_dot_rated = []
        Density = self.Density()
        for i in range(len(self.data)):
            m_dot_rate = (self.a0 + self.a1 * self.Te[i] + self.a2 * pow(self.Te[i], 2) +
                          self.a3 * pow(self.Te[i], 3) + self.a4 * self.Tc[i] +
                          self.a5 * pow(self.Tc[i], 2) + self.a6 * pow(self.Tc[i], 3) +
                          self.a7 * self.Te[i] * self.Tc[i] + self.a8 * self.Te[i] * pow(self.Tc[i], 2) +
                          self.a9 * pow(self.Te[i], 2) * self.Tc[i] +
                          self.a10 * pow(self.Te[i], 2) * pow(self.Tc[i], 2))
            m_dot_rated.append(m_dot_rate)
        return m_dot_rated

    def w_dot_rated(self):
        w_dot_rated = []
        Density = self.Density()
        for i in range(len(self.data)):
            w_dot_rate = Density[i] * (self.b0 + self.b1 * self.Te[i] + self.b2 * pow(self.Te[i], 2) +
                                       self.b3 * pow(self.Te[i], 3) + self.b4 * self.Tc[i] +
                                       self.b5 * pow(self.Tc[i], 2) + self.b6 * pow(self.Tc[i], 3) +
                                       self.b7 * self.Te[i] * self.Tc[i] + self.b8 * self.Te[i] * pow(self.Tc[i], 2) +
                                       self.b9 * pow(self.Te[i], 2) * self.Tc[i] +
                                       self.b10 * pow(self.Te[i], 2) * pow(self.Tc[i], 2))
            w_dot_rated.append(w_dot_rate)
        return w_dot_rated

    def fre(self):
        fre = []
        for i in range(len(self.data)):
            fre_ = self.f[i] - 58
            fre.append(fre_)
        return fre

    def k_mp(self):
        k_m = []
        k_p = []
        m_dot = self.data['m_dot']
        w_dot = self.data['w_dot']
        m_dot_rated = self.m_dot_rated()
        w_dot_rated = self.w_dot_rated()
        for i in range(len(self.data)):
            k_m.append(m_dot[i] / m_dot_rated[i])
            k_p.append(w_dot[i] / w_dot_rated[i])
        return k_m, k_p

    def m_dot_pred(self):
        m_dot_pred = []
        fre = self.fre()
        m_dot_rated = self.m_dot_rated()
        for i in range(len(self.data)):
            m_dot_pred_ = (self.c0 + self.c1 * fre[i] + self.c2 * pow(fre[i], 2)) * m_dot_rated[i]
            if m_dot_pred_ < 0:
                m_dot_pred_ = 0
            m_dot_pred.append(m_dot_pred_ / 3600)
        return m_dot_pred

    def w_dot_pred(self):
        w_dot_pred = []
        fre = self.fre()
        w_dot_rated = self.w_dot_rated()
        for i in range(len(self.data)):
            w_dot_pred_ = (self.d0 + self.d1 * fre[i] + self.d2 * pow(fre[i], 2)) * w_dot_rated[i]
            if w_dot_pred_ < 0:
                w_dot_pred_ = 0
            w_dot_pred.append(w_dot_pred_)
        return w_dot_pred

    def Qcond(self,):
        dis_t = []
        delta_h = []
        dis_t1 = self.dis_t1
        dis_t2 = self.dis_t2
        cond_o_t = self.cond_o_t
        high_p = self.P_dis
        m_dot = self.m_dot_pred()
        for i in range(len(self.data)):
            if dis_t1[i] > dis_t2[i]:
                dis_t.append(dis_t1[i])
            elif dis_t2[i] > dis_t1[i]:
                dis_t.append(dis_t2[i])
            else:
                dis_t.append(dis_t1[i])
            try:
                h_dis = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', dis_t[i] + 273.15, 'R410A')
                h_cond = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273.15, 'R410A')
            except:
                h_dis = 0
                h_cond = 0
            delta_h.append((h_dis - h_cond) / 1000)
        Q_cond = pd.DataFrame([x * y for x, y in zip(delta_h, m_dot)], columns=['Qcond'])
        return Q_cond

    def Qevap(self,):
        delta_h = []
        suc_t1 = self.T_suc
        cond_o_t = self.liq_t
        low_p = self.P_suc
        m_dot = self.m_dot_pred()
        for i in range(len(self.data)):
            h_suc = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', suc_t1[i] + 273.15, 'R410A')
            h_evap = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273.15, 'R410A')
            delta_h.append(abs((h_evap - h_suc) / 1000))
        Q_evap = pd.DataFrame([x * y for x, y in zip(delta_h, m_dot)], columns=['Qevap'])
        return Q_evap

    def RMSE(self):
        m_dot = self.data['m_dot']
        w_dot = self.data['w_dot']
        m_dot_pred = self.m_dot_pred()
        w_dot_pred = self.w_dot_pred()
        m_dot_error = []
        w_dot_error = []
        for i in range(len(self.data)):
            m_dot_error.append(pow(m_dot[i] - m_dot_pred[i], 2))
            w_dot_error.append(pow(w_dot[i] - w_dot_pred[i], 2))
        m_dot_error = np.sqrt(sum(m_dot_error) / len(m_dot_error))
        w_dot_error = np.sqrt(sum(w_dot_error) / len(w_dot_error))
        return print("{}: m_dot_error RMSE - {}".format(self.model, m_dot_error)), print(
            "{}: w_dot_error RMSE - {}".format(self.model, w_dot_error))

    def create_folder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: creating directory. ' + directory)

    def concat(self):
        f = self.f
        Tc = self.Tc
        Te = self.Te
        fre = self.fre()
        # m_dot = self.data['m_dot']
        # w_dot = self.data['w_dot']
        m_dot_pred = self.m_dot_pred()
        w_dot_pred = self.w_dot_pred()
        m_dot_rated = self.m_dot_rated()
        w_dot_rated = self.w_dot_rated()
        Qcond = self.Qcond()
        Qevap = self.Qevap()
        time = self.data['updated_time']
        # k_m,k_p = self.k_mp()
        columns = ['Time', 'frequency', 'Condensing Temp', 'Evaporating Temp', 'frequency rated',
                   'm_dot_rated', 'w_dot_rated', 'm_dot_pred', 'w_dot_pred','Qcond','Qevap']
        overall_data = pd.DataFrame(
            np.column_stack([time, f, Tc, Te, fre, m_dot_rated, w_dot_rated, m_dot_pred, w_dot_pred,Qcond,Qevap]),
            columns=columns).set_index('Time')
        # today = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        # folder_name = today[0:10]
        directory = self.file_path + '/freq{}/'.format(self.freq)
        # self.RMSE()
        self.create_folder(directory=directory)
        return overall_data.to_csv(directory + '{}_{}.csv'.format(self.model, self.unit))


path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2022-02-14/'

file = {'3069/': ['0214']}

k = 0
for key, value in file.items():
    for j in value:
        dic = path + key + j + '/'
        comp = comp_model(model='GB066', file_path=dic, date=j, freq=1, unit=key[:-1])
        comp.concat()
        comp2 = comp_model(model='GB066', file_path=dic, date=j, freq=2, unit=key[:-1])
        comp2.concat()
        k += 1
