class FixedSpeedCompressor(object):
    def __init__(self, capacity, input_power, product_capacity):
        self.capacity = capacity
        self.input_power = input_power
        self.product_capacity = product_capacity
        self.low_temp_capacity = self.capacity * 1.077
        self.low_temp_input_power = self.input_power * 0.914
        self.standard_COP = self.capacity / self.input_power
        self.low_temp_COP = self.low_temp_capacity / self.low_temp_input_power
        self.standard_SEER = self.standard_COP * 3.412
        self.low_temp_SEER = self.low_temp_COP * 3.412

        self.temperature_range = 15
        self.outdoor_temp = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
        self.occuring_hour = [182, 164, 196, 165, 105, 104, 86, 80, 42, 31, 15, 5, 5, 4, 0]

        self.coefficient_degradation = 0.25

        self.unit_size = self.product_capacity/0.293
        self.total_occur = sum(self.occuring_hour)

        self.CoolingBuildingLoad = []
        self.CoolingCapacity = []
        self.PowerInput = []
        self.OperationFactor = []
        self.PLF = []
        self.cooling_capacity = []
        self.cooling_input_power = []
        self.capacity_during_cooling = []
        self.input_during_cooling = []
        self.COP = []
        self.CSPF = []
        self.CoolingSeasongCapacity = []
        self.CoolingSeasonInputPower = []

    def BL_c(self):
        for i in range(self.temperature_range):
            BL_c = self.product_capacity * (self.outdoor_temp[i] - 20) / (35 - 20)
            self.CoolingBuildingLoad.append(BL_c)
        return self.CoolingBuildingLoad

    def Capacity_c(self):
        for i in range(self.temperature_range):
            Capa_c = self.capacity + ((self.low_temp_capacity - self.capacity) / (35 - 29)) * (
                        35 - self.outdoor_temp[i])
            self.CoolingCapacity.append(Capa_c)
        return self.CoolingCapacity

    def Power_i(self):
        for i in range(self.temperature_range):
            P_input = self.input_power + ((self.low_temp_input_power - self.input_power) / (35 - 29)) * (
                        35 - self.outdoor_temp[i])
            self.PowerInput.append(P_input)
        return self.PowerInput

    def factor_oper(self):
        cooling_building_load = self.BL_c()
        cooling_capacity = self.Capacity_c()
        for i in range(self.temperature_range):
            factor = cooling_building_load[i] / cooling_capacity[i]
            if factor <= 1:
                factor = factor
            else:
                factor = 1
            self.OperationFactor.append(factor)
        return self.OperationFactor

    def PLF_(self):
        factor = self.factor_oper()
        for i in range(self.temperature_range):
            plf = 1 - self.coefficient_degradation * (1 - factor[i])
            self.PLF.append(plf)
        return self.PLF

    def CoolingCapacity_(self):
        rated_cooling_capa = self.Capacity_c()
        factor = self.factor_oper()
        for i in range(self.temperature_range):
            cc = rated_cooling_capa[i] * factor[i]
            self.cooling_capacity.append(cc)
        return self.cooling_capacity

    def CoolingInputPower_(self):
        Power_i = self.Power_i()
        factor = self.factor_oper()
        PLF = self.PLF_()
        for i in range(self.temperature_range):
            cip = factor[i] * Power_i[i] / PLF[i]
            self.cooling_input_power.append(cip)
        return self.cooling_input_power

    def CapacityDuringCooling_(self):
        Cooling_c = self.CoolingCapacity_()
        hour = self.occuring_hour
        for i in range(self.temperature_range):
            cdc = Cooling_c[i] * hour[i] / 1000
            self.capacity_during_cooling.append(cdc)
        return self.capacity_during_cooling

    def InputDuringCooling_(self):
        Cooling_p = self.CoolingInputPower_()
        hour = self.occuring_hour
        for i in range(self.temperature_range):
            idc = Cooling_p[i] * hour[i] / 1000
            self.input_during_cooling.append(idc)
        return self.input_during_cooling

    def COP_(self):
        Cooling_p = self.CoolingInputPower_()
        Cooling_c = self.CoolingCapacity_()
        for i in range(self.temperature_range):
            cop = Cooling_c[i] / Cooling_p[i]
            self.COP.append(cop)
        return self.COP

    def CSPF(self):
        capacity = sum(self.CapacityDuringCooling_())
        power = sum(self.InputDuringCooling_())
        for i in range(self.temperature_range):
            cspf = capacity[i] / power[i]
            self.CSPF.append(cspf)
            self.CoolingSeasongCapacity.append(capacity)
            self.CoolingSeasonInputPower.append(power)

    def SEER(self):
        capacity = sum(self.CapacityDuringCooling_())
        power = sum(self.InputDuringCooling_())
        return capacity * 3.412 / power

    def AnnualCostOfPower(self):
        self.cost = (self.unit_size * self.total_occur * 0.12) / (self.SEER() * 1000)
        return self.cost


class VariableSpeedCompressor(object):
    def __init__(self, capacity, input_power):
        self.capacity = capacity
        self.input_power = input_power

        self.Fraction_of_total = [0.214, 0.231, 0.216, 0.161, 0.104, 0.052, 0.018, 0.004]
        self.temperature_range = 8
        self.bin_temperature = [67, 72, 77, 82, 87, 92, 97, 102]
        self.coefficient_degradation = 0.25

        self.L1 = 0
        self.K1 = 0
        self.K2 = 0
        self.T1 = 0
        self.T2 = 0
        self.Tv = 0
        self.NQ = 0
        self.NE = 0
        self.MQ = 0
        self.ME = 0
        self.EER_T1 = 0
        self.EER_T2 = 0
        self.EER_Tv = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0

        self.E1 = 0
        self.E2 = 0
        self.Qc_1 = 0
        self.Ec_1 = 0
        self.Qc_2 = 0
        self.Ec_2 = 0
        self.Qc_v = 0
        self.Ec_v = 0

        self.BuildingLoad = []
        self.Qc_k1 = []
        self.Ec_k1 = []
        self.Qc_k2 = []
        self.Ec_k2 = []
        self.Qc_kv = []
        self.Ec_kv = []
        self.region = [1, 1, 1, 2, 2, 2, 2, 3]

        self.X = []
        self.PLF = []
        self.EER_Ki = []
        self.qc_N = []
        self.ec_N = []
        self.EER = []
        self.InputPower = []
        self.SEER = 0

    def L1_(self):
        self.L1 = self.capacity[0] / ((95 - 65) * 1.1)
        return self.L1

    def K1_(self):
        self.K1 = (self.capacity[3]-self.capacity[4]) / (87 - 67)
        return self.K1

    def K2_(self):
        self.K2 = (self.capacity[0]-self.capacity[1]) / (95 - 82)
        return self.K2

    def T1_(self):
        self.T1 = (self.capacity[4] + 65 * self.L1_() - 67 * self.K1_()) / (self.L1_() - self.K1_())
        return self.T1

    def T2_(self):
        self.T2 = (self.capacity[1] + 65 * self.L1_() - 82 * self.K2_()) / (self.L1_() - self.K2_())
        return self.T2

    def Tv_(self):
        self.Tv = (self.capacity[2] - self.MQ_() * 87 + 65 * self.L1_()) / (self.L1_() - self.MQ_())
        return self.Tv

    def EER_T1_(self):
        self.EER_T1 = self.Qc_1_() / self.Ec_1_()
        return self.EER_T1

    def EER_T2_(self):
        self.EER_T2 = self.Qc_2_() / self.Ec_2_()
        return self.EER_T2

    def EER_Tv_(self):
        self.EER_Tv = self.Qc_v_() / self.Ec_v_()
        return self.EER_Tv

    def NQ_(self):
        self.NQ = (self.capacity[2] - self.Qc_k1_()[4]) / (self.Qc_k2_()[4] - self.Qc_k1_()[4])
        return self.NQ

    def NE_(self):
        self.NE = (self.input_power[2] - self.Ec_k1_()[4]) / (self.Ec_k2_()[4] - self.Ec_k1_()[4])
        return self.NE

    def MQ_(self):
        self.MQ = (self.capacity[3] - self.capacity[4]) * (1 - self.NQ_()) / (82 - 67) + self.NQ_() * (self.capacity[0] - self.capacity[1]) / (95 - 82)
        return self.MQ

    def ME_(self):
        self.ME = (self.input_power[3] - self.input_power[4]) * (1 - self.NE_()) / (82 - 67) + self.NE_() * (self.input_power[0] - self.input_power[1]) / (95 - 82)
        return self.ME

    def A_(self):
        self.A = self.EER_T2_() - self.B_() * self.T2_() - self.C_() * self.T2_() * self.T2_()
        return self.A

    def B_(self):
        self.B = (self.EER_T1_() - self.EER_T2_() - self.D_() * (self.EER_T1_() - self.EER_Tv_())) / (self.T1_() - self.T2_() - self.D_() * (self.T1_() - self.Tv_()))
        return self.B

    def C_(self):
        self.C = (self.EER_T1_() - self.EER_T2_() - self.B_() * (self.T1_() - self.T2_())) / (self.T1_() * self.T1_() - self.T2_() * self.T2_())
        return self.C

    def D_(self):
        self.D = (self.T2_() * self.T2_() - self.T1_() * self.T1_()) / (self.Tv_() * self.Tv_() - self.T1_() * self.T1_())
        return self.D

    def E1_(self):
        self.E1 = (self.input_power[3] - self.input_power[4]) / (82 - 67)
        return self.E1

    def E2_(self):
        self.E2 = (self.input_power[0] - self.input_power[1]) / (95 - 82)
        return self.E2

    def Qc_1_(self):
        self.Qc_1 = self.capacity[4] + (self.capacity[3] - self.capacity[4]) * (self.T1_() - 67) / (82 - 67)
        return self.Qc_1

    def Ec_1_(self):
        self.Ec_1 = self.input_power[4] + (self.input_power[3] - self.input_power[4]) * (self.T1_() - 67) / (82 - 67)
        return self.Ec_1

    def Qc_2_(self):
        self.Qc_2 = self.capacity[1] + (self.capacity[0] - self.capacity[1]) * (self.T2_() - 82) / (95 - 82)
        return self.Qc_2

    def Ec_2_(self):
        self.Ec_2 = self.input_power[1] + (self.input_power[0] - self.input_power[1]) * (self.T2_() - 82) / (95 - 82)
        return self.Ec_2

    def Qc_v_(self):
        self.Qc_v = self.capacity[2] + self.MQ_() * (self.Tv_() - 87)
        return self.Qc_v

    def Ec_v_(self):
        self.Ec_v = self.input_power[2] + self.ME_() * (self.Tv_() - 87)
        return self.Ec_v

    def BuildingLoad_(self):
        self.BuildingLoad = []
        for i in range(self.temperature_range):
            bl = ((self.bin_temperature[i] - 65) / (95 - 65)) * (self.capacity[0] / 1.1)
            self.BuildingLoad.append(bl)
        return self.BuildingLoad

    def Qc_k1_(self):
        self.Qc_k1 = []
        for i in range(self.temperature_range):
            qc_k1 = self.capacity[4] + (self.capacity[3] - self.capacity[4]) * (self.bin_temperature[i] - 67) / (82 - 67)
            self.Qc_k1.append(qc_k1)
        return self.Qc_k1

    def Ec_k1_(self):
        self.Ec_k1 = []
        for i in range(self.temperature_range):
            ec_k1 = self.input_power[4] + (self.input_power[3] - self.input_power[4]) * (self.bin_temperature[i] - 67) / (82 - 67)
            self.Ec_k1.append(ec_k1)
        return self.Ec_k1

    def Qc_k2_(self):
        self.Qc_k2 = []
        for i in range(self.temperature_range):
            qc_k2 = self.capacity[1] + (self.capacity[0] - self.capacity[1]) * (self.bin_temperature[i] - 82) / (95 - 82)
            self.Qc_k2.append(qc_k2)
        return self.Qc_k2

    def Ec_k2_(self):
        self.Ec_k2 = []
        for i in range(self.temperature_range):
            ec_k2 = self.input_power[1] + (self.input_power[0] - self.input_power[1]) * (self.bin_temperature[i] - 82) / (95 - 82)
            self.Ec_k2.append(ec_k2)
        return self.Ec_k2

    def Qc_kv_(self):
        self.Qc_kv = []
        for i in range(self.temperature_range):
            qc_kv = self.capacity[2] + self.MQ_() * (self.bin_temperature[i] - 87)
            self.Qc_kv.append(qc_kv)
        return self.Qc_kv

    def Ec_kv_(self):
        self.Ec_kv = []
        for i in range(self.temperature_range):
            ec_kv = self.capacity[2] + self.ME_() * (self.bin_temperature[i] - 87)
            self.Ec_kv.append(ec_kv)
        return self.Ec_kv

    def X_(self):
        self.X = []
        for i in range(self.temperature_range):
            if self.region[i] == 1:
                x = self.BuildingLoad_()[i] / self.Qc_k1_()[i]
            else:
                x = 0
            self.X.append(x)
        return self.X

    def PLF_(self):
        self.PLF = []
        for i in range(self.temperature_range):
            if self.region[i] == 1:
                plf = 1 - self.coefficient_degradation * (1 - self.X_()[i])
            else:
                plf = 0
            self.PLF.append(plf)
        return self.PLF

    def EER_Ki_(self):
        self.EER_Ki = []
        for i in range(self.temperature_range):
            if self.region[i] == 2:
                eer_ki = self.A_() + self.B_() * self.bin_temperature[i] + self.C_() * self.bin_temperature[i] * self.bin_temperature[i]
            else:
                eer_ki = 0
            self.EER_Ki.append(eer_ki)
        return self.EER_Ki

    def qc_N_(self):
        self.qc_N = []
        for i in range(self.temperature_range):
            if self.region[i] == 1:
                qc_n = self.X_()[i] * self.Qc_k1_()[i] * self.Fraction_of_total[i]
                self.qc_N.append(qc_n)
            elif self.region[i] == 2:
                qc_n = self.BuildingLoad_()[i] * self.Fraction_of_total[i]
                self.qc_N.append(qc_n)
            elif self.region[i] == 3:
                qc_n = self.Qc_k2_()[i] * self.Fraction_of_total[i]
                self.qc_N.append(qc_n)
        return self.qc_N

    def ec_N_(self):
        self.ec_N = []
        for i in range(self.temperature_range):
            if self.region[i] == 1:
                ec_n = self.X_()[i] * self.Ec_k1_()[i] * self.Fraction_of_total[i] / self.PLF_()[i]
                self.ec_N.append(ec_n)
            elif self.region[i] == 2:
                ec_n = self.qc_N_()[i] / self.EER_Ki_()[i]
                self.ec_N.append(ec_n)
            elif self.region[i] == 3:
                ec_n = self.Ec_k2_()[i] * self.Fraction_of_total[i]
                self.ec_N.append(ec_n)
        return self.ec_N

    def EER_(self):
        for i in range(self.temperature_range):
            eer = self.qc_N_()[i] / self.ec_N_()[i]
            self.EER.append(eer)
        return self.EER

    def InputPower_(self):
        for i in range(self.temperature_range):
            ip = self.ec_N_()[i] / self.Fraction_of_total[i]
            self.InputPower.append(ip)

    def SEER_(self):
        return sum(self.qc_N_()) / sum(self.ec_N_())


