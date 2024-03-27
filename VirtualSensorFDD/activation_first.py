from fouling_FDD import FDD2
from SEER import FixedSpeedCompressor
import pandas as pd
import CoolProp as CP

diretory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\Data\2021-10-15'
data_list = ['\Cooling_RTU_1_evaluator.csv','\Cooling_RTU_2_evaluator.csv','\Cooling_RTU_3_evaluator.csv',
             '\Cooling_RTU_4_evaluator.csv','\Cooling_Split_1_evaluator.csv','\Cooling_Split_2_evaluator.csv',
             '\Cooling_Split_3_evaluator.csv','\Cooling_Split_4_evaluator.csv','\Cooling_Split_5_evaluator.csv']
save = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\Result\2021-10-15'


for i in range(len(data_list)):
    seer = []
    cost = []
    data = pd.read_csv(diretory+data_list[i], encoding='euc-kr')
    capacity = data['Q_ref'].fillna(0) * 1000
    input_power = data['Power'].fillna(0)

    if data_list[i] == '\Cooling_RTU_1_evaluator.csv' or data_list[i] == '\Cooling_RTU_4_evaluator.csv':
        product_capacity = 17600
    elif data_list[i] == '\Cooling_RTU_2_evaluator.csv':
        product_capacity = 17600/2
    else:
        product_capacity = 10550

    for j in range(len(capacity)):
        VSC = FixedSpeedCompressor(capacity=capacity[j],input_power=input_power[j],product_capacity=product_capacity)
        seer_ = VSC.SEER()
        cost_ = VSC.AnnualCostOfPower()
        seer.append(seer_)
        cost.append(cost_)
        data['SEER'] = pd.DataFrame(seer).round(2)
        data['COST'] = pd.DataFrame(cost).round(2)
    data.to_csv(save+data_list[i])

    if data_list[i] == '\Cooling_RTU_1_evaluator.csv':
        pass
    else:
        Q_air = data['Q_air'].fillna(method='ffill')
        T_air_ce = data['T_air_ce'].fillna(method='ffill')
        P_suc = data['P_suc'].fillna(method='ffill')
        P_dis = data['P_dischg'].fillna(method='ffill')
        m_ref = data['m_ref'].fillna(method='ffill') / 60
        T_dis = data['T_dischg'].fillna(method='ffill')
        T_suc = data['T_suc'].fillna(method='ffill')
        T_air_ci = data['T_amb'].fillna(method='ffill')
        T_oa = data['T_amb'].fillna(method='ffill')
        T_co = data['T_LL'].fillna(method='ffill')
        P_ll = data['P_LL'].fillna(method='ffill')
        Q_ref = data['Q_ref'].fillna(method='ffill')
        T_RA = data['T_RA'].fillna(method='ffill')
        T_SA = data['T_SA'].fillna(method='ffill')

        if data_list[i] == '\Cooling_RTU_2_evaluator.csv' or data_list[i] == '\Cooling_RTU_3_evaluator.csv' \
                or data_list[i] == '\Cooling_Split_1_evaluator.csv' or data_list[i] == '\Cooling_Split_2_evaluator.csv' \
                or data_list[i] == '\Cooling_Split_3_evaluator.csv':
            ref = 'R410a'
        elif data_list[i] == '\Cooling_RTU_4_evaluator.csv':
            ref = 'R407c'
        elif data_list[i] == '\Cooling_Split_4_evaluator.csv' or data_list[i] == '\Cooling_Split_5_evaluator.csv':
            ref = 'R22'
        FDD = FDD2(m_dot=m_ref,P_high=P_suc, cond_in_temp=T_dis, cond_out_temp=T_co, cond_in_air=T_air_ci,
                   cond_out_air=T_air_ce,outdoor_temp=T_oa,low_pressure=P_suc,suction_temp=T_suc,ref=ref,
                   P_ll=P_ll,T_ll=T_co,Q_ref=Q_ref,Q_air=Q_air,evap_out_temp=T_suc,evap_out_air=T_SA,evap_in_air=T_RA)

        pred_airflow_cond1 = FDD.condenser_air_flow1()
        pred_airflow_cond2 = FDD.condenser_air_flow2()
        pred_airflow_cond3 = FDD.condenser_air_flow3()
        pred_airflow_cond4 = FDD.condenser_air_flow4()

        data['Condenser airflow prediction 1 [kg/s]'] = pd.DataFrame(pred_airflow_cond1).round(3)
        data['Condenser airflow prediction 2 [kg/s]'] = pd.DataFrame(pred_airflow_cond2).round(3)
        data['Condenser airflow prediction 3 [kg/s]'] = pd.DataFrame(pred_airflow_cond3).round(3)
        data['Condenser airflow prediction 4 [kg/s]'] = pd.DataFrame(pred_airflow_cond4).round(3)

        pred_airflow_evap1 = FDD.evaporator_air_flow1()
        pred_airflow_evap2 = FDD.evaporator_air_flow2()
        pred_airflow_evap3 = FDD.evaporator_air_flow3()
        data['Evaporator airflow prediction 1 [kg/s]'] = pd.DataFrame(pred_airflow_evap1).round(3)
        data['Evaporator airflow prediction 2 [kg/s]'] = pd.DataFrame(pred_airflow_evap2).round(3)
        data['Evaporator airflow prediction 3 [kg/s]'] = pd.DataFrame(pred_airflow_evap3).round(3)

        # fault_level = FDD.faultLevel(pred=pred_airflow_cond1, actual=actual_airflow_cond)
        # data['fault_level'] = pd.DataFrame(fault_level)


        # pred_ref_charge = FDD.refrigerant_charge_sensor()
        # data['Refrigerant charge [%]'] = pd.DataFrame(pred_ref_charge)

    print(data_list[i])
    data.to_csv(save+data_list[i])