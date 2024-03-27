from fouling_FDD import FDD2
from SEER import FixedSpeedCompressor
import pandas as pd
import CoolProp as CP

diretory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\Data\2022-03-15'
data_list = ['\RTU_Lab1.csv']
save = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\Result\2022-03-15'

for i in range(len(data_list)):
    seer = []
    cost = []
    data = pd.read_csv(diretory+data_list[i])
    capacity = data['Capa_ref'].fillna(0) * 1000
    input_power = data['P_total'].fillna(0) * 1000
    product_capacity = (2.14 + 0.38 + 0.24) * 1000

    for j in range(len(capacity)):
        VSC = FixedSpeedCompressor(capacity=capacity[j],input_power=input_power[j],product_capacity=product_capacity)
        seer_ = VSC.SEER()
        cost_ = VSC.AnnualCostOfPower()
        seer.append(seer_)
        cost.append(cost_)
        data['SEER'] = pd.DataFrame(seer).round(2)
        data['COST'] = pd.DataFrame(cost).round(2)
    data.to_csv(save+data_list[i])

    Q_air = data['Capa_air'].fillna(method='ffill')
    T_air_ce = data['T_cao'].fillna(method='ffill')
    P_suc = data['P_suc'].fillna(method='ffill')
    P_dis = data['P_dis'].fillna(method='ffill')
    m_ref = data['m_dot_r'].fillna(method='ffill') / 1000
    T_dis = data['T_d'].fillna(method='ffill')
    T_suc = data['T_suc'].fillna(method='ffill')
    T_air_ci = data['T_cai'].fillna(method='ffill')
    T_oa = data['T_oa'].fillna(method='ffill')
    T_co = data['T_eev1_in'].fillna(method='ffill')
    T_ll = data['T_liquid_out'].fillna(method='ffill')
    P_ll = data['P_liquid'].fillna(method='ffill')
    Q_ref = data['Capa_ref'].fillna(method='ffill')
    T_RA = data['T_ai'].fillna(method='ffill')
    T_SA = data['T_ao'].fillna(method='ffill')
    T_evai = data['T_evai'].fillna(method='ffill')
    T_evao = data['T_evao'].fillna(method='ffill')
    T_sh = data['T_sh'].fillna(method='ffill')
    T_sc = data['T_sc'].fillna(method='ffill')
    ref = 'R410A'

    FDD = FDD2(m_dot=m_ref,P_high=P_dis, cond_in_temp=T_dis, cond_out_temp=T_co, cond_in_air=T_air_ci,
               cond_out_air=T_air_ce,outdoor_temp=T_oa,low_pressure=P_suc,suction_temp=T_suc,ref=ref,
               P_ll=P_ll,T_ll=T_ll,Q_ref=Q_ref, Q_air=Q_air,evap_out_temp=T_evao,evap_out_air=T_evao,evap_in_air=T_evai,
               T_sh=T_sh,T_sc=T_sc)

    pred_airflow_cond1 = FDD.condenser_air_flow1()
    pred_airflow_cond2 = FDD.condenser_air_flow2()
    pred_airflow_cond3 = FDD.condenser_air_flow3()
    data['Condenser airflow prediction 1 [kg/s]'] = pd.DataFrame(pred_airflow_cond1).round(3)
    data['Condenser airflow prediction 2 [kg/s]'] = pd.DataFrame(pred_airflow_cond2).round(3)
    data['Condenser airflow prediction 3 [kg/s]'] = pd.DataFrame(pred_airflow_cond3).round(3)

    pred_airflow_evap1 = FDD.evaporator_air_flow1()
    pred_airflow_evap2 = FDD.evaporator_air_flow2()
    pred_airflow_evap3 = FDD.evaporator_air_flow3()
    data['Evaporator airflow prediction 1 [kg/s]'] = pd.DataFrame(pred_airflow_evap1).round(3)
    data['Evaporator airflow prediction 2 [kg/s]'] = pd.DataFrame(pred_airflow_evap2).round(3)
    data['Evaporator airflow prediction 3 [kg/s]'] = pd.DataFrame(pred_airflow_evap3).round(3)

    pred_ref_charge = FDD.refrigerant_charge_sensor()
    data['Refrigerant charge [%]'] = pd.DataFrame(pred_ref_charge)

    print(data_list[i])
    data.to_csv(save+data_list[i])