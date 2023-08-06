# Sample python script to run an EBSILON model from python
# via the EbsOpen COM API
# Requires pywin32 and a valid EBSILON license with EbsOpen option
# By: Milton Venetos, Wyatt Enterprises, LLC
# Copyright (C) October 18, 2017
# http://www.wyattllc.com
# 注意：引入本文件就需要可用的Ebsilon授权和EbsOpen授权

from enum import Enum
from typing import Optional

import win32com.client

from yangke.common.config import logger

app = None  # ebsilon内部的application类对象，代表了ebsilon软件本身
e_uom: Optional[win32com.client.Constants] = None  # ebsilon的枚举常量集合
# 初始化ebsilon，返回Ebsilon软件内置的Application类对象
try:
    # ebs = win32com.client.dynamic.Dispatch("EbsOpen.Application") #late binding / dynamic dispatch
    app = win32com.client.gencache.EnsureDispatch("EbsOpen.Application")  # early binding / static dispatch
    e_uom = win32com.client.constants
except:
    logger.debug("初始化Ebsilon时发生错误，请检查您的Ebsilon license")
    exit()


class EbsKind(Enum):
    pipe_electric = e_uom.epObjectKindPipeElectric
    comp1 = e_uom.epObjectKindComp1
    comp2 = e_uom.epObjectKindComp2
    comp3 = e_uom.epObjectKindComp3
    comp4 = e_uom.epObjectKindComp4
    comp5 = e_uom.epObjectKindComp5
    comp6 = e_uom.epObjectKindComp6
    comp7 = e_uom.epObjectKindComp7
    comp8 = e_uom.epObjectKindComp8
    comp9 = e_uom.epObjectKindComp9
    comp10 = e_uom.epObjectKindComp10
    comp11 = e_uom.epObjectKindComp11
    comp12 = e_uom.epObjectKindComp12
    comp13 = e_uom.epObjectKindComp13
    comp14 = e_uom.epObjectKindComp14
    comp15 = e_uom.epObjectKindComp15
    comp16 = e_uom.epObjectKindComp16
    comp17 = e_uom.epObjectKindComp17
    comp18 = e_uom.epObjectKindComp18
    comp19 = e_uom.epObjectKindComp19
    comp20 = e_uom.epObjectKindComp20
    comp21 = e_uom.epObjectKindComp21
    comp22 = e_uom.epObjectKindComp22
    comp23 = e_uom.epObjectKindComp23
    comp24 = e_uom.epObjectKindComp24
    comp25 = e_uom.epObjectKindComp25
    comp26 = e_uom.epObjectKindComp26
    comp27 = e_uom.epObjectKindComp27
    comp28 = e_uom.epObjectKindComp28
    comp29 = e_uom.epObjectKindComp29

    comp30 = e_uom.epObjectKindComp30
    comp31 = e_uom.epObjectKindComp31
    comp32 = e_uom.epObjectKindComp32
    comp33 = e_uom.epObjectKindComp33
    comp34 = e_uom.epObjectKindComp34
    comp35 = e_uom.epObjectKindComp35
    comp36 = e_uom.epObjectKindComp36
    comp37 = e_uom.epObjectKindComp37
    comp38 = e_uom.epObjectKindComp38
    comp39 = e_uom.epObjectKindComp39

    comp40 = e_uom.epObjectKindComp40
    comp41 = e_uom.epObjectKindComp41
    comp42 = e_uom.epObjectKindComp42
    comp43 = e_uom.epObjectKindComp43
    comp44 = e_uom.epObjectKindComp44
    comp45 = e_uom.epObjectKindComp45
    comp46 = e_uom.epObjectKindComp46
    comp47 = e_uom.epObjectKindComp47
    comp48 = e_uom.epObjectKindComp48
    comp49 = e_uom.epObjectKindComp49

    comp50 = e_uom.epObjectKindComp50
    comp51 = e_uom.epObjectKindComp51
    comp52 = e_uom.epObjectKindComp52
    comp53 = e_uom.epObjectKindComp53
    comp54 = e_uom.epObjectKindComp54
    comp55 = e_uom.epObjectKindComp55
    comp56 = e_uom.epObjectKindComp56
    comp57 = e_uom.epObjectKindComp57
    comp58 = e_uom.epObjectKindComp58
    comp59 = e_uom.epObjectKindComp59

    comp60 = e_uom.epObjectKindComp60
    comp61 = e_uom.epObjectKindComp61
    comp62 = e_uom.epObjectKindComp62
    comp63 = e_uom.epObjectKindComp63
    comp64 = e_uom.epObjectKindComp64
    comp65 = e_uom.epObjectKindComp65
    comp66 = e_uom.epObjectKindComp66
    comp67 = e_uom.epObjectKindComp67
    comp68 = e_uom.epObjectKindComp68
    comp69 = e_uom.epObjectKindComp69

    comp70 = e_uom.epObjectKindComp70
    comp71 = e_uom.epObjectKindComp71
    comp72 = e_uom.epObjectKindComp72
    comp73 = e_uom.epObjectKindComp73
    comp74 = e_uom.epObjectKindComp74
    comp75 = e_uom.epObjectKindComp75
    comp76 = e_uom.epObjectKindComp76
    comp77 = e_uom.epObjectKindComp77
    comp78 = e_uom.epObjectKindComp78
    comp79 = e_uom.epObjectKindComp79

    comp80 = e_uom.epObjectKindComp80
    comp81 = e_uom.epObjectKindComp81
    comp82 = e_uom.epObjectKindComp82
    comp83 = e_uom.epObjectKindComp83
    comp84 = e_uom.epObjectKindComp84
    comp85 = e_uom.epObjectKindComp85
    comp86 = e_uom.epObjectKindComp86
    comp87 = e_uom.epObjectKindComp87
    comp88 = e_uom.epObjectKindComp88
    comp89 = e_uom.epObjectKindComp89

    comp90 = e_uom.epObjectKindComp90
    comp91 = e_uom.epObjectKindComp91
    comp92 = e_uom.epObjectKindComp92
    comp93 = e_uom.epObjectKindComp93
    comp94 = e_uom.epObjectKindComp94
    comp95 = e_uom.epObjectKindComp95
    comp96 = e_uom.epObjectKindComp96
    comp97 = e_uom.epObjectKindComp97
    comp98 = e_uom.epObjectKindComp98
    comp99 = e_uom.epObjectKindComp99

    comp100 = e_uom.epObjectKindComp100
    comp101 = e_uom.epObjectKindComp101
    comp102 = e_uom.epObjectKindComp102
    comp103 = e_uom.epObjectKindComp103
    comp104 = e_uom.epObjectKindComp104
    comp105 = e_uom.epObjectKindComp105
    comp106 = e_uom.epObjectKindComp106
    comp107 = e_uom.epObjectKindComp107
    comp108 = e_uom.epObjectKindComp108
    comp109 = e_uom.epObjectKindComp109

    comp110 = e_uom.epObjectKindComp110
    comp111 = e_uom.epObjectKindComp111
    comp112 = e_uom.epObjectKindComp112
    comp113 = e_uom.epObjectKindComp113
    comp114 = e_uom.epObjectKindComp114
    comp115 = e_uom.epObjectKindComp115
    comp116 = e_uom.epObjectKindComp116
    comp117 = e_uom.epObjectKindComp117
    comp118 = e_uom.epObjectKindComp118
    comp119 = e_uom.epObjectKindComp119

    comp120 = e_uom.epObjectKindComp120
    comp121 = e_uom.epObjectKindComp121
    comp122 = e_uom.epObjectKindComp122
    comp123 = e_uom.epObjectKindComp123
    comp124 = e_uom.epObjectKindComp124
    comp125 = e_uom.epObjectKindComp125
    comp126 = e_uom.epObjectKindComp126
    comp127 = e_uom.epObjectKindComp127
    comp128 = e_uom.epObjectKindComp128
    comp129 = e_uom.epObjectKindComp129

    comp130 = e_uom.epObjectKindComp130
    comp131 = e_uom.epObjectKindComp131
    comp132 = e_uom.epObjectKindComp132
    comp133 = e_uom.epObjectKindComp133
    comp134 = e_uom.epObjectKindComp134
    comp135 = e_uom.epObjectKindComp135
    comp136 = e_uom.epObjectKindComp136
    comp137 = e_uom.epObjectKindComp137
    comp138 = e_uom.epObjectKindComp138
    comp139 = e_uom.epObjectKindComp139

    comp140 = e_uom.epObjectKindComp140
    comp141 = e_uom.epObjectKindComp141
    comp142 = e_uom.epObjectKindComp142
    comp143 = e_uom.epObjectKindComp143
    comp144 = e_uom.epObjectKindComp144
    comp145 = e_uom.epObjectKindComp145
    comp146 = e_uom.epObjectKindComp146
    comp147 = e_uom.epObjectKindComp147
    comp148 = e_uom.epObjectKindComp148
    comp149 = e_uom.epObjectKindComp149

    comp150 = e_uom.epObjectKindComp150
    comp151 = e_uom.epObjectKindComp151
    comp152 = e_uom.epObjectKindComp152
    comp153 = e_uom.epObjectKindComp153
    comp154 = e_uom.epObjectKindComp154
    comp155 = e_uom.epObjectKindComp155
    comp156 = e_uom.epObjectKindComp156
    comp157 = e_uom.epObjectKindComp157


class EbsUnits(Enum):
    """
    Ebsilon的单位系统，包含了Ebsilon软件中定义的所有单位常量，在读写组件参数时会用到。参见ebsilon帮助文件EpUnit Enumeration
    """
    global e_uom
    # 流量
    lb_h = e_uom.epUNIT_lb_h  # 磅/小时，流量单位
    kg_s = e_uom.epUNIT_kg_s  # 流量单位kg/s
    # 功率
    MW = e_uom.epUNIT_MW  # 功率单位，MW
    kW = e_uom.epUNIT_kW
    W = e_uom.epUNIT_W
    # 压力
    bar = e_uom.epUNIT_bar
    Pa = e_uom.epUNIT_Pa
    kPa = e_uom.epUNIT_kPa
    MPa = e_uom.epUNIT_MPa
    # 温度
    C = e_uom.epUNIT_C
    K = e_uom.epUNIT_K
    # 能量
    J = e_uom.epUNIT_J
    kJ = e_uom.epUNIT_kJ
    MJ = e_uom.epUNIT_MJ
    GJ = e_uom.epUNIT_GJ
    # 密度
    g_m3 = e_uom.epUNIT_g_m3
    # 转速
    unit_1_min = 17  # 试验测试得到的值
    # 其他
    int = e_uom.epUNIT_INTEGRAL
    text = e_uom.epUNIT_TEXT
    access_actual = e_uom.epUNITACCESS_ACTUAL
    access_si = e_uom.epUNITACCESS_SI
    ACCESS_Imperial = e_uom.epUNITACCESS_Imperial
    ACCESS_USC = e_uom.epUNITACCESS_USC
    # ERROR = e_uom.epUNIT_ERROR
    INVALID = e_uom.epUNIT_INVALID
    NONE = e_uom.epUNIT_NONE
    unit_1 = e_uom.epUNIT_1
    GrdC = e_uom.epUNIT_GrdC
    kJ_kg = e_uom.epUNIT_kJ_kg
    m3_kg = e_uom.epUNIT_m3_kg
    m3_s = e_uom.epUNIT_m3_s
    kmol_kmol = e_uom.epUNIT_kmol_kmol
    kg_kg = e_uom.epUNIT_kg_kg
    kW_K = e_uom.epUNIT_kW_K
    W_m2K = e_uom.epUNIT_W_m2K
    kJ_kWh = e_uom.epUNIT_kJ_kWh
    kJ_m3 = e_uom.epUNIT_kJ_m3
    kJ_m3K = e_uom.epUNIT_kJ_m3K
    kg_m3 = e_uom.epUNIT_kg_m3
    m = e_uom.epUNIT_m
    kJ_kgK_cp = e_uom.epUNIT_kJ_kgK_cp
    m2 = e_uom.epUNIT_m2
    kJ_kgK = e_uom.epUNIT_kJ_kgK
    kg_kg_x = e_uom.epUNIT_kg_kg_x
    kg_kg_xg = e_uom.epUNIT_kg_kg_xg
    kg_kmol = e_uom.epUNIT_kg_kmol
    kJ_kg_ncv = e_uom.epUNIT_kJ_kg_ncv
    m_s = e_uom.epUNIT_m_s
    kg_kg_x_rg = e_uom.epUNIT_kg_kg_x_rg
    FTYP_8 = e_uom.epUNIT_FTYP_8
    FTYP_9 = e_uom.epUNIT_FTYP_9
    mg_Nm3 = e_uom.epUNIT_mg_Nm3
    EUR_h = e_uom.epUNIT_EUR_h
    kW_kg = e_uom.epUNIT_kW_kg
    _1_m6 = e_uom.epUNIT_1_m6
    A = e_uom.epUNIT_A
    EUR_kWh = e_uom.epUNIT_EUR_kWh
    EUR_kg = e_uom.epUNIT_EUR_kg
    V = e_uom.epUNIT_V
    m3_m3 = e_uom.epUNIT_m3_m3
    kg = e_uom.epUNIT_kg
    EUR = e_uom.epUNIT_EUR
    m3 = e_uom.epUNIT_m3
    ph = e_uom.epUNIT_ph
    m2K_W = e_uom.epUNIT_m2K_W
    W_m2 = e_uom.epUNIT_W_m2
    TEXT = e_uom.epUNIT_TEXT
    Grd = e_uom.epUNIT_Grd
    m_geopot = e_uom.epUNIT_m_geopot
    t_h = e_uom.epUNIT_t_h
    GrdF = e_uom.epUNIT_GrdF
    Prz = e_uom.epUNIT_Prz
    psia = e_uom.epUNIT_psia
    btu_lb = e_uom.epUNIT_btu_lb
    klb_h = e_uom.epUNIT_klb_h
    ft3_lb = e_uom.epUNIT_ft3_lb
    Mft3_h = e_uom.epUNIT_Mft3_h
    R = e_uom.epUNIT_R
    lb_lb = e_uom.epUNIT_lb_lb
    kbtu_hF = e_uom.epUNIT_kbtu_hF
    btu_ft2hF = e_uom.epUNIT_btu_ft2hF
    lb_ft3 = e_uom.epUNIT_lb_ft3
    btu_lbF = e_uom.epUNIT_btu_lbF
    btu_kWh = e_uom.epUNIT_btu_kWh
    btu_ft3 = e_uom.epUNIT_btu_ft3
    btu_ft3F = e_uom.epUNIT_btu_ft3F
    ft = e_uom.epUNIT_ft
    rpm = e_uom.epUNIT_rpm
    hp = e_uom.epUNIT_hp
    ft2 = e_uom.epUNIT_ft2
    m3_h = e_uom.epUNIT_m3_h
    btu_lbF_cp = e_uom.epUNIT_btu_lbF_cp
    mbar = e_uom.epUNIT_mbar
    lb_lb_x = e_uom.epUNIT_lb_lb_x
    lb_lb_xg = e_uom.epUNIT_lb_lb_xg
    lb_kmol = e_uom.epUNIT_lb_kmol
    btu_lb_ncv = e_uom.epUNIT_btu_lb_ncv
    ft_s = e_uom.epUNIT_ft_s
    lb_lb_x_rg = e_uom.epUNIT_lb_lb_x_rg
    CENT_min = e_uom.epUNIT_CENT_min
    DM_h = e_uom.epUNIT_DM_h
    PFENNIG_min = e_uom.epUNIT_PFENNIG_min
    Prz_x = e_uom.epUNIT_Prz_x
    Prz_xg = e_uom.epUNIT_Prz_xg
    g_mol = e_uom.epUNIT_g_mol
    ppm = e_uom.epUNIT_ppm
    ppm_xg = e_uom.epUNIT_ppm_xg
    MW_kg = e_uom.epUNIT_MW_kg
    hp_lb = e_uom.epUNIT_hp_lb
    mg_m3 = e_uom.epUNIT_mg_m3
    _1_ft6 = e_uom.epUNIT_1_ft6
    kg_h = e_uom.epUNIT_kg_h
    mA = e_uom.epUNIT_mA
    t_s = e_uom.epUNIT_t_s
    EUR_MWh = e_uom.epUNIT_EUR_MWh
    CENT_kWh = e_uom.epUNIT_CENT_kWh
    EUR_t = e_uom.epUNIT_EUR_t
    CENT_kg = e_uom.epUNIT_CENT_kg
    kV = e_uom.epUNIT_kV
    g_kg = e_uom.epUNIT_g_kg
    mg_kg = e_uom.epUNIT_mg_kg
    Prz_vol = e_uom.epUNIT_Prz_vol
    ppm_vol = e_uom.epUNIT_ppm_vol
    ft3_ft3 = e_uom.epUNIT_ft3_ft3
    t = e_uom.epUNIT_t
    g = e_uom.epUNIT_g
    mg = e_uom.epUNIT_mg
    lb = e_uom.epUNIT_lb
    klb = e_uom.epUNIT_klb
    CENT = e_uom.epUNIT_CENT
    DM = e_uom.epUNIT_DM
    Pfennig = e_uom.epUNIT_Pfennig
    l_min = e_uom.epUNIT_l_min
    l_h = e_uom.epUNIT_l_h
    mV = e_uom.epUNIT_mV
    mm = e_uom.epUNIT_mm
    cm = e_uom.epUNIT_cm
    km = e_uom.epUNIT_km
    yd = e_uom.epUNIT_yd
    inch = e_uom.epUNIT_in
    mi = e_uom.epUNIT_mi
    mm2 = e_uom.epUNIT_mm2
    cm2 = e_uom.epUNIT_cm2
    L = e_uom.epUNIT_l
    km2 = e_uom.epUNIT_km2
    yd2 = e_uom.epUNIT_yd2
    in2 = e_uom.epUNIT_in2
    mi2 = e_uom.epUNIT_mi2
    ft3 = e_uom.epUNIT_ft3
    mm3 = e_uom.epUNIT_mm3
    cm3 = e_uom.epUNIT_cm3
    km3 = e_uom.epUNIT_km3
    yd3 = e_uom.epUNIT_yd3
    in3 = e_uom.epUNIT_in3
    mi3 = e_uom.epUNIT_mi3
    gal = e_uom.epUNIT_gal
    kg_Nm3 = e_uom.epUNIT_kg_Nm3
    tm3_h = e_uom.epUNIT_tm3_h
    Mm3_h = e_uom.epUNIT_Mm3_h
    mmWS = e_uom.epUNIT_mmWS
    mWS = e_uom.epUNIT_mWS
    kA = e_uom.epUNIT_kA
    l_s = e_uom.epUNIT_l_s
    Hz = e_uom.epUNIT_Hz
    mmHg = e_uom.epUNIT_mmHg
    mg_l = e_uom.epUNIT_mg_l
    at = e_uom.epUNIT_at
    kcal_kg = e_uom.epUNIT_kcal_kg
    kcal_kg_ncv = e_uom.epUNIT_kcal_kg_ncv
    kcal_kgK = e_uom.epUNIT_kcal_kgK
    kcal_kgK_cp = e_uom.epUNIT_kcal_kgK_cp
    kW_m2 = e_uom.epUNIT_kW_m2
    kcal_m2h = e_uom.epUNIT_kcal_m2h
    Nm_kg = e_uom.epUNIT_Nm_kg
    kVA = e_uom.epUNIT_kVA
    MVA = e_uom.epUNIT_MVA
    VA = e_uom.epUNIT_VA
    kVAr = e_uom.epUNIT_kVAr
    MVAr = e_uom.epUNIT_MVAr
    VAr = e_uom.epUNIT_VAr
    atm = e_uom.epUNIT_atm
    g_s = e_uom.epUNIT_g_s
    kg_ms = e_uom.epUNIT_kg_ms
    W_mK = e_uom.epUNIT_W_mK
    inHg = e_uom.epUNIT_inHg
    ft_geopot = e_uom.epUNIT_ft_geopot
    km_geopot = e_uom.epUNIT_km_geopot
    yd_geopot = e_uom.epUNIT_yd_geopot
    mi_geopot = e_uom.epUNIT_mi_geopot
    rad = e_uom.epUNIT_rad
    _1_Grd = e_uom.epUNIT_1_Grd
    _1_Grd2 = e_uom.epUNIT_1_Grd2
    _1_Grd3 = e_uom.epUNIT_1_Grd3
    _1_Grd4 = e_uom.epUNIT_1_Grd4
    _1_Grd5 = e_uom.epUNIT_1_Grd5
    _1_rad = e_uom.epUNIT_1_rad
    _1_rad2 = e_uom.epUNIT_1_rad2
    _1_rad3 = e_uom.epUNIT_1_rad3
    _1_rad4 = e_uom.epUNIT_1_rad4
    _1_rad5 = e_uom.epUNIT_1_rad5
    _1_K = e_uom.epUNIT_1_K
    _1_K2 = e_uom.epUNIT_1_K2
    _1_K3 = e_uom.epUNIT_1_K3
    _1_K4 = e_uom.epUNIT_1_K4
    _1_R = e_uom.epUNIT_1_R
    _1_R2 = e_uom.epUNIT_1_R2
    _1_R3 = e_uom.epUNIT_1_R3
    _1_R4 = e_uom.epUNIT_1_R4
    W_m = e_uom.epUNIT_W_m
    kW_m = e_uom.epUNIT_kW_m
    kcal_mh = e_uom.epUNIT_kcal_mh
    GrdK = e_uom.epUNIT_GrdK
    s = e_uom.epUNIT_s
    min = e_uom.epUNIT_min
    h = e_uom.epUNIT_h
    d = e_uom.epUNIT_d
    K_m = e_uom.epUNIT_K_m
    kJ_kgm = e_uom.epUNIT_kJ_kgm
    K_cm = e_uom.epUNIT_K_cm
    K_mm = e_uom.epUNIT_K_mm
    K_km = e_uom.epUNIT_K_km
    K_ft = e_uom.epUNIT_K_ft
    K_yd = e_uom.epUNIT_K_yd
    R_ft = e_uom.epUNIT_R_ft
    R_yd = e_uom.epUNIT_R_yd
    btu_lbft = e_uom.epUNIT_btu_lbft
    datetime = e_uom.epUNIT_datetime
    kW_kgK = e_uom.epUNIT_kW_kgK
    W_kgK = e_uom.epUNIT_W_kgK
    W_gK = e_uom.epUNIT_W_gK
    kbtu_lbhF = e_uom.epUNIT_kbtu_lbhF
    bar_m = e_uom.epUNIT_bar_m
    mbar_m = e_uom.epUNIT_mbar_m
    mbar_cm = e_uom.epUNIT_mbar_cm
    psia_ft = e_uom.epUNIT_psia_ft
    kt = e_uom.epUNIT_kt
    Mt = e_uom.epUNIT_Mt
    mN_m = e_uom.epUNIT_mN_m
    N_m = e_uom.epUNIT_N_m
    W_mK2 = e_uom.epUNIT_W_mK2
    W_mK3 = e_uom.epUNIT_W_mK3
    W_mK4 = e_uom.epUNIT_W_mK4
    m_K = e_uom.epUNIT_m_K
    m_K2 = e_uom.epUNIT_m_K2
    m2_s = e_uom.epUNIT_m2_s
    ft2_s = e_uom.epUNIT_ft2_s
    mm2_s = e_uom.epUNIT_mm2_s
    cm2_s = e_uom.epUNIT_cm2_s
    in2_s = e_uom.epUNIT_in2_s
    Pas = e_uom.epUNIT_Pas
    mPas = e_uom.epUNIT_mPas
    kWh = e_uom.epUNIT_kWh
    MWh = e_uom.epUNIT_MWh
    Nm3_s = e_uom.epUNIT_Nm3_s
    Nm3_h = e_uom.epUNIT_Nm3_h
    kNm3_h = e_uom.epUNIT_kNm3_h
    kg_m3K = e_uom.epUNIT_kg_m3K
    lb_ft3R = e_uom.epUNIT_lb_ft3R
    g_m3K = e_uom.epUNIT_g_m3K
    kg_lK = e_uom.epUNIT_kg_lK
    g_lK = e_uom.epUNIT_g_lK
    g_cm3K = e_uom.epUNIT_g_cm3K
    kJ_kgK2 = e_uom.epUNIT_kJ_kgK2
    btu_lbR2 = e_uom.epUNIT_btu_lbR2
    kg_l = e_uom.epUNIT_kg_l
    g_l = e_uom.epUNIT_g_l
    g_cm3 = e_uom.epUNIT_g_cm3
    kcal_kWh = e_uom.epUNIT_kcal_kWh
    mrad = e_uom.epUNIT_mrad
    kg2_kJs = e_uom.epUNIT_kg2_kJs
    lb2_btus = e_uom.epUNIT_lb2_btus
    kW_m2K = e_uom.epUNIT_kW_m2K
    INTEGRAL = e_uom.epUNIT_INTEGRAL
    P = e_uom.epUNIT_P
    cP = e_uom.epUNIT_cP
    St = e_uom.epUNIT_St
    cSt = e_uom.epUNIT_cSt
    lb_s = e_uom.epUNIT_lb_s
    klb_s = e_uom.epUNIT_klb_s
    oz_s = e_uom.epUNIT_oz_s
    oz_h = e_uom.epUNIT_oz_h
    y3_s = e_uom.epUNIT_y3_s
    ft3_s = e_uom.epUNIT_ft3_s
    in3_s = e_uom.epUNIT_in3_s
    gal_s = e_uom.epUNIT_gal_s
    y3_h = e_uom.epUNIT_y3_h
    ft3_h = e_uom.epUNIT_ft3_h
    in3_h = e_uom.epUNIT_in3_h
    gal_h = e_uom.epUNIT_gal_h
    kft3_s = e_uom.epUNIT_kft3_s
    kft3_h = e_uom.epUNIT_kft3_h
    m_h = e_uom.epUNIT_m_h
    km_h = e_uom.epUNIT_km_h
    y_s = e_uom.epUNIT_y_s
    in_s = e_uom.epUNIT_in_s
    y_h = e_uom.epUNIT_y_h
    ft_h = e_uom.epUNIT_ft_h
    mi_h = e_uom.epUNIT_mi_h
    W_mGrdC = e_uom.epUNIT_W_mGrdC
    W_mGrdC2 = e_uom.epUNIT_W_mGrdC2
    W_mGrdC3 = e_uom.epUNIT_W_mGrdC3
    W_mGrdC4 = e_uom.epUNIT_W_mGrdC4
    m_GrdC = e_uom.epUNIT_m_GrdC
    m_GrdC2 = e_uom.epUNIT_m_GrdC2
    bars_kg = e_uom.epUNIT_bars_kg
    barkg_kJ = e_uom.epUNIT_barkg_kJ
    barK_kW = e_uom.epUNIT_barK_kW
    ppm_kg = e_uom.epUNIT_ppm_kg
    ppm_x = e_uom.epUNIT_ppm_x
    ppm_x_rg = e_uom.epUNIT_ppm_x_rg
    Prz_kg = e_uom.epUNIT_Prz_kg
    Prz_x_rg = e_uom.epUNIT_Prz_x_rg
    g_kg_x = e_uom.epUNIT_g_kg_x
    mg_kg_x = e_uom.epUNIT_mg_kg_x
    g_kg_xg = e_uom.epUNIT_g_kg_xg
    mg_kg_xg = e_uom.epUNIT_mg_kg_xg
    g_kg_x_rg = e_uom.epUNIT_g_kg_x_rg
    mg_kg_x_rg = e_uom.epUNIT_mg_kg_x_rg
    _1_s = e_uom.epUNIT_1_s
    _1_h = e_uom.epUNIT_1_h
    F = e_uom.epUNIT_F
    inWS = e_uom.epUNIT_inWS
    cmWS = e_uom.epUNIT_cmWS
    kcal = e_uom.epUNIT_kcal
    cal = e_uom.epUNIT_cal
    kcal_h = e_uom.epUNIT_kcal_h
    lb_lbmole = e_uom.epUNIT_lb_lbmole
    lbmole_lbmole = e_uom.epUNIT_lbmole_lbmole
    kmol_lbmole = e_uom.epUNIT_kmol_lbmole
    lbmole_kmol = e_uom.epUNIT_lbmole_kmol
    MJ_m3 = e_uom.epUNIT_MJ_m3
    btu = e_uom.epUNIT_btu
    N = e_uom.epUNIT_N
    kN = e_uom.epUNIT_kN
    mN = e_uom.epUNIT_mN
    lbf = e_uom.epUNIT_lbf
    kp = e_uom.epUNIT_kp
    PS = e_uom.epUNIT_PS
    Torr = e_uom.epUNIT_Torr
    unit_1_m = e_uom.epUNIT_1_m
    unit_1_ft = e_uom.epUNIT_1_ft
    unit_1_mm = e_uom.epUNIT_1_mm
    unit_1_cm = e_uom.epUNIT_1_cm
    unit_1_km = e_uom.epUNIT_1_km
    unit_1_yd = e_uom.epUNIT_1_yd
    unit_1_in = e_uom.epUNIT_1_in
    unit_1_mi = e_uom.epUNIT_1_mi
    btu_h = e_uom.epUNIT_btu_h
    kbtu_h = e_uom.epUNIT_kbtu_h
    Mbtu_h = e_uom.epUNIT_Mbtu_h
    m2_W = e_uom.epUNIT_m2_W
    kJ_Nm3 = e_uom.epUNIT_kJ_Nm3
    MJ_Nm3 = e_uom.epUNIT_MJ_Nm3
    MJ_SCM = e_uom.epUNIT_MJ_SCM
    btu_SCF = e_uom.epUNIT_btu_SCF
    oz = e_uom.epUNIT_oz
    gr = e_uom.epUNIT_gr
    mg_SCM = e_uom.epUNIT_mg_SCM
    gr_SCF = e_uom.epUNIT_gr_SCF
    SCM_s = e_uom.epUNIT_SCM_s
    SCF_s = e_uom.epUNIT_SCF_s
    PATH = e_uom.epUNIT_PATH
    FOLDER = e_uom.epUNIT_FOLDER
    KERNELEXPRESSION = e_uom.epUNIT_KERNELEXPRESSION
    unit_1_kg = e_uom.epUNIT_1_kg
    kg_kg_1xg = e_uom.epUNIT_kg_kg_1xg
    mol_mol = e_uom.epUNIT_mol_mol
    mol_prz = e_uom.epUNIT_mol_prz
    mass_prz = e_uom.epUNIT_mass_prz
    mol_ppm = e_uom.epUNIT_mol_ppm
    ftH2O = e_uom.epUNIT_ftH2O
    mTorr = e_uom.epUNIT_mTorr
    oz_in2 = e_uom.epUNIT_oz_in2
    hPa = e_uom.epUNIT_hPa
    cmHg = e_uom.epUNIT_cmHg
    kg_cm2 = e_uom.epUNIT_kg_cm2
    g_cm2 = e_uom.epUNIT_g_cm2
    shton_s = e_uom.epUNIT_shton_s
    shton_h = e_uom.epUNIT_shton_h
    lgton_s = e_uom.epUNIT_lgton_s
    lgton_h = e_uom.epUNIT_lgton_h
    DOLLAR_h = e_uom.epUNIT_DOLLAR_h
    POUND_h = e_uom.epUNIT_POUND_h
    YEN_h = e_uom.epUNIT_YEN_h
    DOLLAR_kWh = e_uom.epUNIT_DOLLAR_kWh
    POUND_kWh = e_uom.epUNIT_POUND_kWh
    YEN_kWh = e_uom.epUNIT_YEN_kWh
    DOLLAR_kg = e_uom.epUNIT_DOLLAR_kg
    POUND_kg = e_uom.epUNIT_POUND_kg
    YEN_kg = e_uom.epUNIT_YEN_kg
    DOLLAR = e_uom.epUNIT_DOLLAR
    POUND = e_uom.epUNIT_POUND
    YEN = e_uom.epUNIT_YEN
    DOLLAR_s = e_uom.epUNIT_DOLLAR_s
    POUND_s = e_uom.epUNIT_POUND_s
    YEN_s = e_uom.epUNIT_YEN_s
    EUR_s = e_uom.epUNIT_EUR_s
    CENT_s = e_uom.epUNIT_CENT_s
    CENT_h = e_uom.epUNIT_CENT_h
    kNm3_s = e_uom.epUNIT_kNm3_s
    kJ_mol = e_uom.epUNIT_kJ_mol
    J_mol = e_uom.epUNIT_J_mol
    btu_mol = e_uom.epUNIT_btu_mol
    kcal_mol = e_uom.epUNIT_kcal_mol
    gal_min = e_uom.epUNIT_gal_min
    mSQRT_K_W = e_uom.epUNIT_mSQRT_K_W
    mSQRT_K_kW = e_uom.epUNIT_mSQRT_K_kW
    ftSQRT_Rk_W = e_uom.epUNIT_ftSQRT_Rk_W
    impgal = e_uom.epUNIT_impgal
    impgal_s = e_uom.epUNIT_impgal_s
    impgal_min = e_uom.epUNIT_impgal_min
    impgal_h = e_uom.epUNIT_impgal_h
    impgal_d = e_uom.epUNIT_impgal_d
    Mimpgal_d = e_uom.epUNIT_Mimpgal_d
    A_K = e_uom.epUNIT_A_K
    mA_K = e_uom.epUNIT_mA_K
    V_K = e_uom.epUNIT_V_K
    mV_K = e_uom.epUNIT_mV_K
    A_F = e_uom.epUNIT_A_F
    mA_F = e_uom.epUNIT_mA_F
    V_F = e_uom.epUNIT_V_F
    mV_F = e_uom.epUNIT_mV_F
    Ohm = e_uom.epUNIT_Ohm
    kOhm = e_uom.epUNIT_kOhm
    MOhm = e_uom.epUNIT_MOhm
    Farad = e_uom.epUNIT_Farad
    mFarad = e_uom.epUNIT_mFarad
    muFarad = e_uom.epUNIT_muFarad
    nFarad = e_uom.epUNIT_nFarad
    pFarad = e_uom.epUNIT_pFarad
    Henry = e_uom.epUNIT_Henry
    mHenry = e_uom.epUNIT_mHenry
    kHenry = e_uom.epUNIT_kHenry
    muHenry = e_uom.epUNIT_muHenry
    kJ_kgs = e_uom.epUNIT_kJ_kgs
    kJ_kgh = e_uom.epUNIT_kJ_kgh
    kWs_kg = e_uom.epUNIT_kWs_kg
    kWh_kg = e_uom.epUNIT_kWh_kg
    kWs_m3 = e_uom.epUNIT_kWs_m3
    kWh_m3 = e_uom.epUNIT_kWh_m3
    GrdR = e_uom.epUNIT_GrdR
    Nm = e_uom.epUNIT_Nm
    kNm = e_uom.epUNIT_kNm
    lbf_ft = e_uom.epUNIT_lbf_ft
    ozf_in = e_uom.epUNIT_ozf_in
    lbf_in = e_uom.epUNIT_lbf_in
    ozf_ft = e_uom.epUNIT_ozf_ft
    dynm = e_uom.epUNIT_dynm
    Wh = e_uom.epUNIT_Wh
    Wh_kg = e_uom.epUNIT_Wh_kg
    Wh_m3 = e_uom.epUNIT_Wh_m3
    kJ_m2 = e_uom.epUNIT_kJ_m2
    kWh_m2 = e_uom.epUNIT_kWh_m2
    Wh_m2 = e_uom.epUNIT_Wh_m2
    btu_ft2 = e_uom.epUNIT_btu_ft2
    W_m3 = e_uom.epUNIT_W_m3
    kW_m3 = e_uom.epUNIT_kW_m3
    m2K_kW = e_uom.epUNIT_m2K_kW
    ft2hF_btu = e_uom.epUNIT_ft2hF_btu
    MJ_kg = e_uom.epUNIT_MJ_kg
    GJ_kg = e_uom.epUNIT_GJ_kg
    J_kg = e_uom.epUNIT_J_kg
    MJ_kWh = e_uom.epUNIT_MJ_kWh
    GJ_kWh = e_uom.epUNIT_GJ_kWh
    J_kWh = e_uom.epUNIT_J_kWh
    GJ_m3 = e_uom.epUNIT_GJ_m3
    J_m3 = e_uom.epUNIT_J_m3
    MJ_m3K = e_uom.epUNIT_MJ_m3K
    GJ_m3K = e_uom.epUNIT_GJ_m3K
    J_m3K = e_uom.epUNIT_J_m3K
    MJ_kgK_cp = e_uom.epUNIT_MJ_kgK_cp
    GJ_kgK_cp = e_uom.epUNIT_GJ_kgK_cp
    J_kgK_cp = e_uom.epUNIT_J_kgK_cp
    MJ_kgK = e_uom.epUNIT_MJ_kgK
    GJ_kgK = e_uom.epUNIT_GJ_kgK
    J_kgK = e_uom.epUNIT_J_kgK
    MJ_kg_ncv = e_uom.epUNIT_MJ_kg_ncv
    GJ_kg_ncv = e_uom.epUNIT_GJ_kg_ncv
    J_kg_ncv = e_uom.epUNIT_J_kg_ncv
    MJ_kgm = e_uom.epUNIT_MJ_kgm
    GJ_kgm = e_uom.epUNIT_GJ_kgm
    J_kgm = e_uom.epUNIT_J_kgm
    GW = e_uom.epUNIT_GW
    TW = e_uom.epUNIT_TW
    GJ_h = e_uom.epUNIT_GJ_h
    MJ_h = e_uom.epUNIT_MJ_h
    kJ_h = e_uom.epUNIT_kJ_h
    J_h = e_uom.epUNIT_J_h
    J_s = e_uom.epUNIT_J_s
    mg_s = e_uom.epUNIT_mg_s
    g_h = e_uom.epUNIT_g_h
    mg_h = e_uom.epUNIT_mg_h
    mug_s = e_uom.epUNIT_mug_s
    mug_h = e_uom.epUNIT_mug_h
    mug = e_uom.epUNIT_mug
    mum = e_uom.epUNIT_mum
    ml = e_uom.epUNIT_ml
    ml_s = e_uom.epUNIT_ml_s
    cm3_s = e_uom.epUNIT_cm3_s
    mm3_s = e_uom.epUNIT_mm3_s
    kW_mK = e_uom.epUNIT_kW_mK
    l_kg = e_uom.epUNIT_l_kg
    btu_hftK = e_uom.epUNIT_btu_hftK
    W_mm = e_uom.epUNIT_W_mm
    W_cm = e_uom.epUNIT_W_cm
    btu_hft = e_uom.epUNIT_btu_hft
    W_ft = e_uom.epUNIT_W_ft
    W_cm2 = e_uom.epUNIT_W_cm2
    btu_hft2 = e_uom.epUNIT_btu_hft2
    W_ft2 = e_uom.epUNIT_W_ft2
    MW_m3 = e_uom.epUNIT_MW_m3
    btu_hft3 = e_uom.epUNIT_btu_hft3
    W_ft3 = e_uom.epUNIT_W_ft3
    W_kg = e_uom.epUNIT_W_kg
    ms = e_uom.epUNIT_ms
    mus = e_uom.epUNIT_mus
    Promille = e_uom.epUNIT_Promille
    Promille_x = e_uom.epUNIT_Promille_x
    Promille_xg = e_uom.epUNIT_Promille_xg
    Promille_vol = e_uom.epUNIT_Promille_vol
    Promille_kg = e_uom.epUNIT_Promille_kg
    Promille_x_rg = e_uom.epUNIT_Promille_x_rg
    mol_promille = e_uom.epUNIT_mol_promille
    mass_promille = e_uom.epUNIT_mass_promille
    unit_1_W = e_uom.epUNIT_1_W
    unit_1_V = e_uom.epUNIT_1_V


class EbsApp:
    def __init__(self, ebsilon=None):
        """
        Ebsilon软件对象，参见EbsOpen.Application帮助文件，为空则会自动创建该对象。

        :param ebsilon:
        """
        if ebsilon is None:
            ebsilon = app
        self.app = ebsilon
        self.about = ebsilon.AboutString
        self.com_class_id = ebsilon.COMCLSID
        self.com_progress_id = ebsilon.COMProgID
        self.computation_tool = ebsilon.ComputationTool
        self.configuration = ebsilon.Configuration
        self.ebsilon_professional_flag = ebsilon.EbsilonProfessionalFlag
        self.ebsilon_professional_license_values_layout2 = ebsilon.EbsilonProfessionalLicenseValuesLayout2
        self.ebsilon_professional_license_values_layout2_marshal_array = \
            ebsilon.EbsilonProfessionalLicenseValuesLayout2MarshalArrayAsVariant
        self.ebs_open_demo_mode = ebsilon.EbsOpenDemoMode
        # self.events = ebsilon.Events  # 初始化时报错，可能是个动态变量
        self.intel_mkl_cnr_cbwr = ebsilon.Intel_MKL_CNR_CBWR
        self.is_dll = ebsilon.IsDll
        self.isProcess = ebsilon.IsProcess
        self.module_filename = ebsilon.ModuleFileName
        self.object_caster = ObjectCaster(ebsilon.ObjectCaster)
        self.position = ebsilon.Position
        self.version_string = ebsilon.ProductVersionString
        self.version_major = ebsilon.ProductVersionMajor
        self.version_minor = ebsilon.ProductVersionMinor
        self.version_serialization = ebsilon.SerializationVersion
        self.unit_converter = ebsilon.UnitConverter

    def open(self, filename, on_error_return_null: bool = True):
        model: EbsModel = EbsModel(self.app.Open(filename, on_error_return_null))
        if not model.exists():
            logger.debug(f"打开模型文件时出错，检查文件路径是否存在：{filename}")
            exit(0)
        return model

    def get_active_model(self):
        return EbsModel(self.app.ActiveModel)

    def get_models(self):
        models = []
        for m in self.app.Models:
            models.append(EbsModel(m))
        return models

    def show_window(self, show=None):
        if show is None:
            show = e_uom.epShowWindowShowNormal
        result: bool = self.app.ShowWindow(show)
        return result

    def get_application_string(self):
        return self.app.ApplicationString

    def describe(self):
        logger.info(self.get_application_string())


class EbsModel:
    def __init__(self, model):
        """
        Ebsilon软件的模型类，考虑到动态更新成员变量和循环引用，将源对象的成员变量更改为对应的成员方法模式获取

        :param model: Ebsilon软件待封装的模型对象
        """
        self.model = model

    def set_value(self, component, abbr, value, unit=None):
        """
        设置模型中某个组件中的参数

        :param component: 组件名
        :param abbr: 参数名，缩写
        :param value: 参数数值
        :param unit: 单位，EbsUnits对象
        :return:
        """
        com = self.object_by_context(component)  # 不能使用get_object
        com.set_value(abbr=abbr, value=value, unit=unit)

    def get_active_profile(self):
        return EbsProfile(self.model.ActiveProfile)

    def get_compression_level(self):
        return self.model.CompressionLevel

    def get_compression_method(self):
        return self.model.CompressionMethod

    def has_calculation_equations(self):
        return self.model.HasCalculationEquations

    def get_calculation_equations(self):
        return self.model.CalculationEquations

    def has_calculation_errors(self):
        return self.model.HasCalculationErrors

    def get_calculation_errors(self):
        return self.model.CalculationErrors

    def has_validation_ebsilon_entries(self):
        return self.model.HasValidationEbsilonEntries

    def get_validation_ebsilon_entries(self):
        return self.model.ValidationEbsilonEntries

    def get_statistics(self):
        return self.model.Statistics

    def get_doa(self):
        return self.model.DOA

    def get_toa(self):
        return self.model.TOA

    def get_context(self):
        return self.model.Context

    def get_objects(self):
        """
        获取模型中的所有组件列表

        :return:
        """
        objects = []
        for obj in self.model.Objects:
            objects.append(EbsObject(obj))
        return objects

    def get_position(self):
        return self.model.Position

    def get_path(self):
        return self.model.Path

    def get_root_profile(self):
        return self.model.RootProfile

    def get_summary(self):
        return self.model.Summary

    def get_name(self):
        return str(self.model.Name)

    def get_configuration(self):
        return self.model.Configuration

    def get_events(self):
        return self.model.Events

    def get_app(self):  # 不能定义为成员变量self.app，否则和EbsApp的构造方法循环引用
        return EbsApp(self.model.Application)

    def activate(self):
        self.model.Activate()

    def activate_profile(self, name_or_id: "str or int"):
        """
        激活指定的Profile

        :param name_or_id:
        :return:
        """
        result: bool = self.model.ActivateProfile(name_or_id)
        return result

    def get_profile(self, name_or_id: "str or int" = None, waring=True):
        """
        获取模型中指定的Profile，如果不存在指定的profile，则返回None

        :param name_or_id:
        :param waring: 不存在时是否报警告
        :return:
        """
        if name_or_id is None:
            return EbsProfile(self.model.ActiveProfile)
        else:
            _tuple = self.model.GetProfile(name_or_id)
            if _tuple[0]:
                return EbsProfile(_tuple[1])
            else:
                if waring:
                    logger.warning(f"不存在指定的profile：{name_or_id}")
                return None

    def get_all_profiles(self):
        profiles = []
        i = 0
        _ = self.get_profile(i, waring=False)
        while _ is not None:
            profiles.append(_)
            i = i + 1
            _ = self.get_profile(i, waring=False)
        return profiles

    def get_position1(self, from_current_context: bool = True):
        return self.model.getPosition(from_current_context)

    def get_object(self, name: str, on_not_found_return_null=True):
        """
        根据组件名获取组件对象，该方法会获取到具体的组件对象，而不是统一的EbsObject类对象

        :param name:
        :param on_not_found_return_null:
        :return:
        """
        obj: EbsObject = self.object_by_context(name, on_not_found_return_null)
        if not obj.exists():  # 查找的组件不存在
            return None
        result = obj.cast_to_component()  # 将当前组件转换为对应的组件类对象
        return result

    def object_by_context(self, name: str, on_not_found_return_null=True):
        result: EbsObject = EbsObject(self.model.ObjectByContext(name, on_not_found_return_null))
        if not result.exists():
            logger.warning(f"不存在名为{name}的组件")
        return result

    def save(self):
        result: bool = self.model.Save()
        return result

    def save_as(self, filepath: str):
        """
        保存一个当前模型的副本，当前打开的模型变更为新保存的模型

        :param filepath:
        :return:
        """
        result: bool = self.model.SaveAs(filepath)
        return result

    def save_copy_as(self, filepath: str):
        """
        保存一个当前模型的副本，当前打开的模型不变
        :param filepath:
        :return:
        """
        result: bool = self.model.SaveCopyAs(filepath)
        return result

    def simulate(self):
        result = self.model.Simulate()
        return result

    def simulate2(self):
        """
        提示信息更丰富，推荐使用

        :return:
        """
        result = self.model.Simulate2()
        result = ebs_err_code2_msg(result)
        return result

    def simulate_new(self):
        result = self.model.SimulateNew()
        result = ebs_err_code2_msg(result)
        return result

    def describe(self, print_objects=False):
        logger.info(f"模型路径：{self.get_path()}")
        profiles = self.get_all_profiles()
        logger.info("该模型包含以下Profiles：")
        for prof in profiles:
            logger.info(f"id: {prof.get_profile_id()}，Name: {prof.get_name()}")
        if print_objects:
            objects = self.get_objects()
            objects = sorted(objects, key=lambda o: o.get_kind(), reverse=True)
            logger.info(f"该模型共包含{len(objects)}个组件，如下所示：")
            logger.info(f"{'name':^35}|{'type':^10}")
            for obj in objects:
                logger.info(f"{obj.get_name():^35}|{obj.get_kind():^10}")

    def exists(self):
        """
        当前模型是否存在

        :return:
        """
        if self.model is None:
            return False
        else:
            return True


class EbsProfile:
    def __init__(self, profile):
        """
        Ebsilon软件的Profile类，其中，考虑到循环引用和动态更新的问题，将成员变量更改为相应的成员方法
        :param profile:
        """
        self.profile = profile

    def get_configuration(self):
        return self.profile.Configuration

    def has_new_nominal_values(self):
        return self.profile.HasNewNominalValues

    def has_parent(self):
        return bool(self.profile.HasParent)

    def get_profile_id(self):
        return self.profile.ProfileId

    def is_active(self):
        return bool(self.profile.IsActive)

    def get_name(self):
        return str(self.profile.Name)

    def get_parent(self):
        # 不能定义为成员变量self.parent，否则和EbsApp类的构造方法循环引用
        return EbsProfile(self.profile.Parent)

    def get_app(self):
        # 不能定义为成员变量self.app，否则和EbsApp类的构造方法循环引用
        return EbsApp(self.profile.Application)

    def get_model(self):
        # 不能定义为成员变量，否则和EbsModel类的构造方法循环引用
        return EbsModel(self.profile.Model)

    def activate(self):
        result: bool = self.profile.Activate()
        return result

    def change_name(self, new_name: str):
        result: str = self.profile.ChangeName(new_name, allow_modify=True, check_only=False)
        return result

    def get_children(self):
        children = self.profile.Children
        result = []
        for child in children:
            result.append(EbsProfile(child))
        return result

    def copy(self, copied_profile, deep=True, parent_of_copied_profile=None):
        """
        方法未调试

        :param copied_profile:
        :param deep:
        :param parent_of_copied_profile:
        :return:
        """
        result: bool = self.profile.Copy(copied_profile, deep, parent_of_copied_profile)
        return result

    def delete(self):
        result: bool = self.profile.Delete()
        return result

    def make_to_root(self):
        result: bool = self.profile.MakeToRoot()
        return result

    def new_child(self):
        result: EbsProfile = EbsProfile(self.profile.NewChild())
        return result

    def saturate(self, profile: Optional["EbsProfile"]):
        """
        可能是全屏操作

        :param profile:
        :return:
        """
        result: bool = self.profile.Saturate(profile)
        return result

    def take_over_nominal_values(self):
        result: bool = self.profile.TakeOverNominalValues()
        return result


class ObjectCaster:
    def __init__(self, caster):
        self.caster = caster

    def cast_to_component(self, component_id: int, obj):
        """
        将IObject类型转换为具体的类型
        :param component_id: 因为Ebsilon有157个不同类型的组件，因此component_id≥1，≤157
        :return:
        """
        _ = self.caster
        obj = obj.obj
        expression = f"_.CastToComp{component_id}(obj)"
        result = eval(expression)
        return result

    def cast_to_data(self, obj):
        """
        将EbsObject类型转换为数据包类型，便于进一步提取组件中的数据

        :param obj:
        :return:
        """
        if isinstance(obj, EbsObject):
            obj = obj.obj
        result = self.caster.CastToData(obj)
        return result


class EbsObject:
    def __init__(self, obj):
        """
        Ebsilon软件的Object类

        :param obj: Ebsilon软件的Object类对象
        """
        self.obj = obj

    def get_data_object(self):
        return self.obj.DataObject

    def get_description(self):
        return self.obj.Description

    def get_description2(self):
        return self.obj.Description2

    def get_description3(self):
        return self.obj.Description3

    def get_description4(self):
        return self.obj.Description4

    def get_name(self):
        return self.obj.Name

    def get_fullname(self):
        return self.obj.FullName

    def get_font(self):
        return self.obj.Font

    def get_font_color(self):
        return self.obj.FontColor

    def get_model(self):
        return EbsModel(self.obj.Model)

    def get_kind(self):
        return self.obj.Kind

    def get_组件号(self, warning=True):
        组件号 = self.get_kind() - 10000
        if 1 <= 组件号 <= 157:
            return 组件号
        else:
            if warning:
                logger.warning(f"未知组件号：{self.get_kind()}")
                return -1
            else:
                return 组件号 + 10000

    def cast_to_object(self):
        return self.obj.CastToObject()

    def cast_to_component(self):
        """
        将Object对象转换为具体的组件类对象，如果是文本、管道等非组件类对象，则原样返回

        :return:
        """
        组件号 = self.get_组件号()
        if 组件号 == -1:
            return self
        ebs_app = self.get_model().get_app()
        caster = ebs_app.object_caster
        result = caster.cast_to_component(组件号, self)  # 将当前组件转换为对应的组件类对象
        return result

    def change_name(self, new_name: str, allow_modify=True, check_only=False):
        new_name: str = self.obj.ChangeName(new_name, allow_modify, check_only)
        return new_name

    def exists(self):
        if self.obj is None:
            return False
        else:
            return True

    def get_values(self):
        """
        获取部件所有参数的名称、数值和单位

        :return:
        """
        data_obj = ObjectCaster(app.ObjectCaster).cast_to_data(self)
        parameters = data_obj.EbsValues
        values = []
        for para in parameters:
            values.append((para.Name, para.Value, EbsUnits(para.Unit).name))
        return values

    def get_value(self, abbr: str, unit: EbsUnits = None):
        """
        获取指定参数的值

        :param abbr: 参数名称缩写
        :param unit: 参数的单位，参考EbsUnits中的枚举量，可以取默认
        :return:
        """
        data_obj = ObjectCaster(app.ObjectCaster).cast_to_data(self)
        value = data_obj.EbsValues(abbr)
        if value is None:
            logger.warning(f"未知参数名：{self.get_name()}.{abbr}")
            return None
        value = value.GetValueInUnit(unit.value)
        return value

    def set_value(self, abbr: str, value, unit: EbsUnits = None, save_flag=True):
        """
        设置指定参数的值

        :param abbr:
        :param value:
        :param unit:
        :param save_flag: 为真则设置参数值后保存模型
        :return:
        """
        data_obj = ObjectCaster(app.ObjectCaster).cast_to_data(self)
        para = data_obj.EbsValues(abbr)
        if para is None:
            logger.warning(f"未知参数名：{self.get_name()}.{abbr}")
            return None
        if unit is None:
            unit = EbsUnits(para.GetUnitValue()[1].Unit)  # 该语句可以查看当前变量的单位
        bret_val = para.SetValueInUnit(value, unit.value)
        if bret_val and save_flag:
            self.get_model().save()

        return bret_val


def ebs_err_code2_msg(ebs_calc_result_code: int):
    # Function to translate EBSILON Calculation Result Codes to text
    ebs_err_code_txt = "Unknown Error Code"
    if ebs_calc_result_code == 0:
        ebs_err_code_txt = "Simulation Successful"
    if ebs_calc_result_code == 1:
        ebs_err_code_txt = "Simulation Successful With Comments"
    if ebs_calc_result_code == 2:
        ebs_err_code_txt = "Simulation Successful With Warnings"
    if ebs_calc_result_code == 3:
        ebs_err_code_txt = "Simulation Failed With Errors"
    if ebs_calc_result_code == 4:
        ebs_err_code_txt = "Simulation Failed with Errors before Calculation - Check Model set up"
    if ebs_calc_result_code == 5:
        ebs_err_code_txt = "Simulation Failed - Fatal Error"
    if ebs_calc_result_code == 6:
        ebs_err_code_txt = "Simulation Failed - Maximum Number of Iterations Reached"
    if ebs_calc_result_code == 7:
        ebs_err_code_txt = "Simulation Failed - Maximum Number of Iterations Reached With Warnings"
    if ebs_calc_result_code == 8:
        ebs_err_code_txt = "Simulation Failed - Maximum Simulation Duration Time Exceeded"
    if ebs_calc_result_code == 9:
        ebs_err_code_txt = "Simulation Failed - Maximum Number of Iterations Reached With Errors"
    if ebs_calc_result_code == 10:
        ebs_err_code_txt = "Simulation Failed - License Error"
    if ebs_calc_result_code == 11:
        ebs_err_code_txt = "Simulation Failed- Already In Simulation Error"
    if ebs_calc_result_code == 12:
        ebs_err_code_txt = "Simulation Failed - Internal Error"

    return ebs_err_code_txt


def is_type(obj, type_str: str):
    actual_type_str = str(type(obj)).replace("'>", "")
    if actual_type_str.endswith(type_str):
        return True
    else:
        return False
