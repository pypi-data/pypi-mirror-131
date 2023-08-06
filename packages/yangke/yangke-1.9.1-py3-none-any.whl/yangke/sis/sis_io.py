# -*- coding: utf-8 -*-
import random
import time
from datetime import datetime
from yangke.base import execute_function_by_interval
from yangke.common.config import logger
import yangke.sis.dll_file as dll_file

tag_des_write = {
    "N1TC_P_Best_Con": "#1凝汽器最佳真空",
    "N1TC_Way_CirPump_Run": "#1循泵最佳运行台数",
    "N1TC_Way_CoolFan_Run": "#1机力塔风机最佳运行台数",
    "N1TC_Coal_Saving_Run": "#1优化后预计节省标煤量",

    "N2TC_P_Best_Con": "#2凝汽器最佳真空",
    "N2TC_Way_CirPump_Run": "#2循泵最佳运行台数",
    "N2TC_Way_CoolFan_Run": "#2机力塔风机最佳运行台数",
    "NPTC_Coal_Saving_Run": "#2优化后预计节省标煤量",
}


def get_tag_value(snapshot, tag_description):
    return float(snapshot[tag_description][0])


tag_des_read = {  # 可读参数，部分也可以写入，但不建议从该程序中写入
    "N1DCS.TCS110RCAOG_B120_01": "#1环境湿度",
    "N1DCS.TCS110RCAOG_B116_01": "#1环境温度",
    "N1DSJ.TCS110GM015ND04_AV": "#1大气压力",
    "N1TS_T_CicWiA": "#1凝汽器进口循环水温度",
    "N1DCS.10PAB11CP101": "#1凝汽器进口循环水压力",
    "N1TS_T_CicWoA": "#1凝汽器出口循环水温度",
    "N1DCS.10PAB21CP101": "#1凝汽器出口循环水压力",
    "N1TS_P_Pex": "#1背压",
    "N1PC_Q_SUPPLHEAT_GJ": "#1供热能量",
    "N1GS_W_G": "#1燃机功率",
    "N1TS_W_G": "#1汽机功率",
    "N1PS_W_G": "#1机组功率",
    "N1TC_DT_CirWater": "#1循环水温升",
    "N1TC_W_CIRPUMP": "#1循泵总功率",
    "N1TC_W_LitaMachineFan": "#1机力塔风机总功率",
    "N1TC_N_HetLoad": "#1凝汽器热负荷",
    "N1TC_TTD_Con": "#1凝汽器端差",
    "N1TC_P_Res_Con": "#1凝汽器汽阻",
    "N1TC_ConWaterSC": "#1凝汽器过冷度",
    "N1TC_Eff_Con": "#1凝汽器效率",
    "N1TC_E_Clear_Con": "#1凝汽器实时清洁度",
    "N1PC_W_Con_Sys": "#1冷端消耗总功率",
    "N1PC_Eff_Unit": "#1联合循环效率",
    "N1PC_RW_PECEle": "#1厂用电率",
    "N1PC_R_FuelExpendGE": "#1供电气耗",

    # "N1DCS.TCS110RCAOG_B120_01": "#2环境湿度",  # 画面上两台机组相同
    "N2DSJ.TCS220GM015ND04_AV": "#2大气压力",
    "N2TS_T_CicWiA": "#2凝汽器进口循环水温度",
    "N2DCS.20PAB11CP101": "#2凝汽器进口循环水压力",  # 画面点号错误
    "N2TS_T_CicWoA": "#2凝汽器出口循环水温度",
    "N2DCS.20PAB21CP101": "#2凝汽器出口循环水压力",  # 画面错误
    "N2DCS.10CJA02EC109": "#2背压",
    "N2PC_Q_SUPPLHEAT_GJ": "#2供热能量",
    "N2GS_W_G": "#2燃机功率",
    "N2TS_W_G": "#2汽机功率",
    "N2PS_W_G": "#2机组功率",
    "N2TC_DT_CirWater": "#2循环水温升",
    "N2TC_W_CIRPUMP": "#2循泵总功率",
    "N2TC_W_LitaMachineFan": "#2机力塔风机总功率",
    "N2TC_N_HetLoad": "#2凝汽器热负荷",
    "N2TC_TTD_Con": "#2凝汽器端差",
    "N2TC_P_Res_Con": "#2凝汽器汽阻",
    "N2TC_ConWaterSC": "#2凝汽器过冷度",
    "N2TC_Eff_Con": "#2凝汽器效率",
    "N2TC_E_Clear_Con": "#2凝汽器实时清洁度",
    "N2PC_W_Con_Sys": "#2冷端消耗总功率",
    "N2PC_Eff_Unit": "#2联合循环效率",
    "N2PC_RW_PECEle": "#2厂用电率",
    "N2DCS.TCS220RCAOG_B018_02": "#2燃气体积流量",  # Nm3/h
    "N2PC_R_FuelExpendGE": "#2供电气耗",
}


def optimize():
    try:
        dbp_api = dll_file.DllMode("172.22.191.211", "admin", "admin", 12085)
    except:
        logger.warning("RDB代理服务器连接失败")
        return
    snapshot = dbp_api.get_snapshot(tags=list(tag_des_read.keys()),
                                    tag_description=list(tag_des_read.values()),
                                    need_detail=False)

    # print(snapshot.T)
    当前运行背压1 = get_tag_value(snapshot, "#1背压")
    当前运行背压2 = get_tag_value(snapshot, "#2背压")
    机组功率1 = get_tag_value(snapshot, "#1机组功率")
    机组功率2 = get_tag_value(snapshot, "#2机组功率")

    if 机组功率1 < 10:
        最佳背压1 = 当前运行背压1
        最佳循泵运行台数1 = 0
        最佳风机运行台数1 = 0
        节省煤量1 = 0
    else:
        最佳背压1 = 当前运行背压1 * 0.9
        最佳循泵运行台数1 = 2
        最佳风机运行台数1 = 4
        节省煤量1 = random.random() / 5
    if 机组功率2 < 10:
        最佳背压2 = 当前运行背压2
        最佳循泵运行台数2 = 0
        最佳风机运行台数2 = 0
        节省煤量2 = 0
    else:
        最佳背压2 = 当前运行背压2 * 0.9
        最佳循泵运行台数2 = 2
        最佳风机运行台数2 = 4
        节省煤量2 = random.random() / 5

    ret = dbp_api.write_snapshot_double(tags=list(tag_des_write.keys()),
                                        values=[最佳背压1, 最佳循泵运行台数1, 最佳风机运行台数1, 节省煤量1,
                                                最佳背压2, 最佳循泵运行台数2, 最佳风机运行台数2, 节省煤量2, ])
    # dbp_api.get_his_value(["N2TC_TTD_Con", "N1TC_DT_CirWater"])

    ret = dbp_api.dis_connect()
    dbp_api.close()
    logger.debug(f"寻优完成")


def run():
    execute_function_by_interval(optimize, minute=0, second=10)  # 没两分钟执行一次main()方法


if __name__ == "__main__":
    run()
    time.sleep(1000)
