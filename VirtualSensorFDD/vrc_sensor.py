import pandas as pd


class VRC(object):
    def __init__(self, T_sh, T_sc):
        self.T_sh = T_sh
        self.T_sc = T_sc

        self.T_sh_rated = 8.783
        self.T_sc_rated = 6.504
        self.T_sh_diff = []
        self.T_sc_diff = []
        self.VRC = []

        self.a0 = 0.04847089
        self.a1 = -0.01401478

    def refrigerant_charge_sensor(self):
        self.T_sc_diff = []
        self.T_sh_diff = []
        self.VRC = []
        for i in range(len(self.T_sh)):
            self.T_sc_diff.append(self.T_sc[i] - self.T_sc_rated)
            self.T_sh_diff.append(self.T_sh[i] - self.T_sh_rated)
        for i in range(len(self.T_sh)):
            vrc = self.T_sc_diff[i] * self.a0 + self.T_sh_diff[i] * self.a1
            self.VRC.append((1 + round(vrc, 2)) * 100)
        return self.VRC


diretory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\Data\2021-11-21'
data_name = '\RTU_Lab1.csv'
save = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\Result\2021-10-15'

data = pd.read_csv(diretory+data_name)

T_sh = data['T_sh'].fillna(method='ffill')
T_sc = data['T_sc'].fillna(method='ffill')

VRC = VRC(T_sh=T_sh, T_sc=T_sc)

pred_ref_charge = VRC.refrigerant_charge_sensor()
data['Refrigerant charge [%]'] = pd.DataFrame(pred_ref_charge)

# data.to_csv(save + data_name)
print(data['Refrigerant charge [%]'])