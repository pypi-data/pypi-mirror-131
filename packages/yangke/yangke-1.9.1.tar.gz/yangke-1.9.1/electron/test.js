function 流量_标准孔板_拟合公式(计算公式系数, 孔板直径d_mm, 膨胀系数ε, 流量系数α, 差压_kPa, 工况密度ρ) {
    // 标准孔边计算公式，该公式没有ISO 5167计算的准确
    let d = 孔板直径d_mm;
    let m = 计算公式系数 * d * d * 流量系数α * 膨胀系数ε * Math.sqrt(差压_kPa * 1000 * 工况密度ρ);
    return m / 1000;
}


function 流量_标准孔板(取压方式, 工质状态, P, T, dp, D1_20, D2_20, Alfa1, Alfa2, K) {
    // '********************************************ISO 5167-2-2003(标准孔板)*********************************
    // 取压方式=1,D&D/2 取压; KBtype=2,角接取压;KBtype=3,法兰取压
    // 工质状态=水蒸汽;水;
    // 'P--工作压力(MPa);  T--工作温度(℃);    DP--差压(kPa);
    // 'D1--管道内径(m);   D2--孔板内径(m);
    // 'Alfa1--管道膨胀系数(mm/(mm*℃*1.0e-6));    Alfa2--孔板膨胀系数;
    // 'k--等熵指数;       Dlnd--动力粘度(Pa*s);   Pf--密度(kg/m3);
    // 'C--流出系数;       Y--可膨胀性系数；   Beta--开孔直径比；
    // 'RD1--雷诺数(D);    RD2--雷诺数(d);     Q--流量；
    // 'X-- 迭代循环变量1; Delta-迭代循环变量2;

    let L1 = 0;
    let L2 = 0;
    let M2 = 0;
    let D1 = 0;
    let D2 = 0;
    let Beta = 0;
    let 流量 = 0;
    // 计算试验条件下的管道和孔板内径、Beta值;
    D1 = D1_20 * (1 + Alfa1 * 0.000001 * (T - 20))
    D2 = D2_20 * (1 + Alfa2 * 0.000001 * (T - 20))
    Beta = D2 / D1

    // '求动力粘度;
    let DLND = DLND_PT(P, T)

    // 判断流量是否为0
    if (dp === 0) {
        return 流量;
    }

    let Density = 0;
    // '求密度；
    // '通过比容的倒数计算,求对应压力下的饱和温度，
    // '当蒸汽温度低于对应压力下的饱和温度时，其密度等于饱和状态下的密度；
    // '当工质为水时，也可以用V_PT()来求密度;
    // 考虑到温度测量仪表的精度，工质状态不能单纯通过T和TW_P来判断，需要由用户输入
    if (工质状态 === "水蒸汽") {  // 水蒸气，可能是过热蒸汽或湿蒸汽
        if (T < TW_P(P)) {  // 说明是湿蒸汽
            Density = 1 / VW_T(T)  // 水的密度
        } else {  // 说明是过热蒸汽
            Density = 1 / V_PT(P, T)
        }
    } else {  // 工质为水
        Density = 1 / V_PT(P, T)
    }

    // 计算可膨胀性系数;
    // 注意单位，DP的输入单位是KPa，P的输入单位是MPa,因此要给P乘以1000；
    // 该标准中规定，此公式只适用于P2/P1>=0.75的情况;
    let y = 1;
    if ((P - dp / 1000) / P >= 0.75) {
        if (工质状态 === "水蒸汽") {
            y = 1 - (0.351 + 0.256 * Beta ^ 4 + 0.93 * Beta ^ 8) * (1 - ((P - dp / 1000) / P) ^ (1 / K));
        }
    } else {
        return "P2/P1<0.75，该公式不可用"
    }

    // '计算迭代变量
    let a = y * D2 * D2 * Math.sqrt(2 * (dp * 1000) * Density / (1 - Beta ^ 4)) / DLND / D1

    // '假设流出系数的C，取最大值Cmax;
    let Cmax = 0.5959 + 0.0312 * Beta ^ 2.1 - 0.184 * Beta ^ 8
    let C = Cmax
    let I = 0
    let WuCha = 1

    // '************************迭代循环******************************
    while (WuCha > 0.00000000000001) {
        // '计算雷诺数Re
        let re = a * C;
        if (取压方式 === "D&D/2") {
            L1 = 1
            L2 = 0.47
        } else if (取压方式 === "角接取压" || 取压方式 === "角接") {
            // '角接取压
            L1 = 0
            L2 = 0
        } else if (取压方式 === "法兰取压" || 取压方式 === "法兰") {
            // '法兰取压
            L1 = 25.4 / D1 / 1000
            L2 = 25.4 / D1 / 1000
        }
        M2 = 2 * L2 / (1 - Beta)
        let AA = (19000 * Beta / Re) ^ 0.8;
         C = 0.5961 + 0.0261 * Beta ^ 2 - 0.216 * Beta ^ 8 + 0.000521 * (1000000 * Beta / Re) ^ 0.7
            + (0.0188 + 0.0063 * AA) * Beta ^ 3.5 * (1000000 / Re) ^ 0.3
            + (0.043 + 0.08 * Math.exp(-10 * L1) - 0.123 * Math.exp(-7 * L1))
            * (1 - 0.11 * AA) * Beta ^ 4 / (1 - Beta ^ 4)
            - 0.031 * (M2 - 0.8 * M2 ^ 1.1) * Beta ^ 1.3
        if (D1_20 < 71.12 / 1000) {
            C = C + 0.011 * (0.75 - Beta) * (2.8 - D1 * 1000 / 25.4)
        }
        I = I + 1
        // '计算误差
        WuCha = Math.abs((a - Re / C) / a)
    }

    // ************************输出结果******************************
    let Q = 3.1415926 * DLND * D1 * Re / 4;
    return Q * 3.6;

}


// '********************************************(非标准多孔孔板)*********************************
// 'KBtype=1,D&D/2 取压; KBtype=2,角接取压;KBtype=3,法兰取压
// 'LTtype=1,蒸汽;     LTtype=2,水;
// 'P--工作压力(MPa);  T--工作温度(℃);    DP--差压(kPa);
// 'D1--管道内径(m);   D2--孔板内径(m);
// 'Alfa1--管道膨胀系数(mm/(mm*℃*1.0e-6));    Alfa2--孔板膨胀系数;
// 'k--等熵指数;       Dlnd--动力粘度(Pa*s);   Pf--密度(kg/m3);
// 'C--流出系数;       Y--可膨胀性系数；   Beta--开孔直径比；
// 'RD1--雷诺数(D);    RD2--雷诺数(d);     Q--流量；
// 'X-- 迭代循环变量1; Delta-迭代循环变量2;
// Public Function LL_DKKB(KBtype As Integer, LTtype As Integer, P As Double, T As Double, dp As Double, D1_20 As Double, _
//                        D2_20 As Double, Alfa1 As Double, Alfa2 As Double, K As Double, CC As Double)
// Dim Beta, D1, D2, L1, L2, M2, AA As Double
// Dim DLND, Re, Density As Double
// Dim WuCha, a As Double
// Dim y, C, Cmax As Double
// Dim I As Integer
// L1 = 0
// L2 = 0
// M2 = 0
// D1 = 0
// D2 = 0
// Beta = 0
// '计算试验条件下的管道和孔板内径、Beta值;
// D1 = D1_20 * (1 + Alfa1 * 0.000001 * (T - 20))
// D2 = D2_20 * (1 + Alfa2 * 0.000001 * (T - 20))
// Beta = D2 / D1
//
// '求动力粘度;
// DLND = DLND_PT(P, T)
//
// '判断流量是否为0
// If dp = 0 Then
//     LL_DKKB = 0
//     Exit Function
// End If
//
// '求密度；
// '通过比容的倒数计算,求对应压力下的饱和温度，
// '当蒸汽温度低于对应压力下的饱和温度时，其密度等于饱和状态下的密度；
// '当工质为水时，也可以用V_PT()来求密度;
// If LTtype = 1 Then
//     If TW_P(P) > T Then
//       Density = 1 / VW_T(T)
//     Else
//       Density = 1 / V_PT(P, T)
//     End If
// Else
//     Density = 1 / V_PT(P, T)
// End If
//
// '计算可膨胀性系数;
// '注意单位，DP的输入单位是KPa，P的输入单位是MPa,因此要给P乘以1000；
// '该标准中规定，此公式只适用于P2/P1>=0.75的情况;
// If (P - dp / 1000) / P >= 0.75 Then
//     If LTtype = 1 Then
//         y = 1 - (0.351 + 0.256 * Beta ^ 4 + 0.93 * Beta ^ 8) * (1 - ((P - dp / 1000) / P) ^ (1 / K))
//     Else
//         y = 1
//     End If
// Else
//
//     Exit Function
// End If
//
// '计算迭代变量
// C = CC
// '************************输出结果******************************
// Q = 0.1264465 * C / ((1 - Beta ^ 4) ^ 0.5) * (D2 * 1000) ^ 2 * y * (Density * dp) ^ 0.5
//
// LL_DKKB = Q / 1000
// End Function
//
// '********************************************ISO 5167-2-2003(ISA1932喷嘴)*********************************
// 'P--工作压力(MPa);  T--工作温度(℃);    DP--差压(kPa);
// 'LTtype=1,蒸汽;     LTtype=2,水;
// 'D1--管道内径(m);   D2--孔板内径(m);
// 'Alfa1--管道膨胀系数(mm/(mm*℃*1.0e-6));    Alfa2--孔板膨胀系数;
// 'k--等熵指数;       Dlnd--动力粘度(Pa*s);   Density--密度(kg/m3);
// 'C--流出系数;       Y--可膨胀性系数；   Beta--开孔直径比；
// 'Re--雷诺数(D);     Q--流量；
// 'X-- 迭代循环变量1; Delta-迭代循环变量2;
// 'TAO--压比;
//
// Public Function ISA(LTtype As Integer, P As Double, T As Double, dp As Double, D1_20 As Double, _
//                        D2_20 As Double, Alfa1 As Double, Alfa2 As Double, K As Double)
// Dim Beta, D1, D2, TAO As Double
// Dim DLND, Re, Density As Double
// Dim WuCha, a As Double
// Dim y, C, Cmax As Double
// Dim I As Integer
// D1 = 0
// D2 = 0
// Beta = 0
// TAO = 0
// '计算试验条件下的管道和孔板内径、Beta值;
// D1 = D1_20 * (1 + Alfa1 * 0.000001 * (T - 20))
// D2 = D2_20 * (1 + Alfa2 * 0.000001 * (T - 20))
// Beta = D2 / D1
//
// '求动力粘度;
// DLND = DLND_PT(P, T)
//
// '判断流量是否为0
// If dp = 0 Then
//     ISA = 0
//     Exit Function
// End If
//
// '求密度；
// '通过比容的倒数计算,求对应压力下的饱和温度，
// '当蒸汽温度低于对应压力下的饱和温度时，其密度等于饱和状态下的密度；
// '当工质为水时，也可以用V_PT()来求密度;
// If LTtype = 1 Then
//     If TW_P(P) > T Then
//       Density = 1 / VW_T(T)
//     Else
//       Density = 1 / V_PT(P, T)
//     End If
// Else
//     Density = 1 / V_PT(P, T)
// End If
//
// '计算可膨胀性系数;
// '注意单位，DP的输入单位是KPa，P的输入单位是MPa,因此要给P乘以1000；
// '该标准中规定，此公式只适用于P2/P1>=0.75的情况;
// TAO = (P - dp / 1000) / P
//
// If TAO >= 0.75 Then
//     If LTtype = 1 Then
//         y = K * TAO ^ (2 / K) / (K - 1)
//         y = y * (1 - Beta ^ 4) / (1 - Beta ^ 4 * TAO ^ (2 / K))
//         y = y * (1 - TAO ^ ((K - 1) / K)) / (1 - TAO)
//         y = y ^ 0.5
//     Else
//         y = 1
//     End If
// Else
//     ISA = MsgBox("ISA1932喷嘴前后压比不满足标准要求")
//     ISA = TAO
//     Exit Function
// End If
//
// '计算迭代变量
// a = y * D2 ^ 2 * Sqr(2 * (dp * 1000) * Density / (1 - Beta ^ 4)) / DLND / D1
//
// '假设流出系数的C，取最大值Cmax;
// Cmax = 0.5959 + 0.0312 * Beta ^ 2.1 - 0.184 * Beta ^ 8
// C = Cmax
// I = 0
// WuCha = 1
//
// '************************迭代循环******************************
// Do While (WuCha > 0.00000000000001)
//
// '计算雷诺数Re
// Re = a * C
//
// C = 0.99 - 0.2262 * Beta ^ 4.1 - (0.00175 * Beta ^ 2 - 0.0033 * Beta ^ 4.15) * (1000000 / Re) ^ 1.15
// I = I + 1
// '计算误差
// WuCha = Abs((a - Re / C) / a)
//
// Loop
// '************************输出结果******************************
// Q = 3.1415926 * DLND * D1 * Re / 4
//
// ISA = Q * 3.6
// End Function
//
//
// '********************************************ISO 5167-2-2003(长颈喷嘴)*********************************
// 'LTtype=1,蒸汽;     LTtype=2,水;
// 'P--工作压力(MPa);  T--工作温度(℃);    DP--差压(kPa);
// 'D1--管道内径(m);   D2--孔板内径(m);
// 'Alfa1--管道膨胀系数(mm/(mm*℃*1.0e-6));    Alfa2--孔板膨胀系数;
// 'k--等熵指数;       Dlnd--动力粘度(Pa*s);   Density--密度(kg/m3);
// 'C--流出系数;       Y--可膨胀性系数；   Beta--开孔直径比；
// 'Re--雷诺数(D);     Q--流量；
// 'X-- 迭代循环变量1; Delta-迭代循环变量2;
// 'TAO--压比;
//
// Public Function L_radius(LTtype As Double, P As Double, T As Double, dp As Double, D1_20 As Double, _
//                        D2_20 As Double, Alfa1 As Double, Alfa2 As Double, K As Double)
// Dim Beta, D1, D2, TAO As Double
// Dim DLND, Re, Density As Double
// Dim WuCha, a As Double
// Dim y, C, Cmax As Double
// Dim I As Integer
// D1 = 0
// D2 = 0
// Beta = 0
// Beta_20 = 0
// a = 0
// C = 0
// '计算试验条件下的管道和孔板内径、Beta值;
// D1 = D1_20 * (1 + Alfa1 * 0.000001 * (T - 20))
// D2 = D2_20 * (1 + Alfa2 * 0.000001 * (T - 20))
// Beta = D2 / D1
// If D1 < 0.05 Or D1 > 0.63 Then
//     L_radius = MsgBox("D超限")
//     Exit Function
// End If
// If Beta < 0.2 Or Beta > 0.8 Then
//     L_radius = MsgBox("Beta超限")
//     Exit Function
// End If
//
// '求动力粘度;
// DLND = DLND_PT(P, T)
//
// '判断流量是否为0
// If dp = 0 Then
//     L_radius = 0
//     Exit Function
// End If
//
//
// '求密度，工质为水时，用V_PT()来求密度;
// Density = 1 / V_PT(P, T)
//
// '计算可膨胀性系数;
// '注意单位，DP的输入单位是KPa，P的输入单位是MPa,因此要给P乘以1000；
// '该标准中规定，此公式只适用于P2/P1>=0.75的情况;
// TAO = (P - dp / 1000) / P
//
// If TAO >= 0.75 Then
//     If LTtype = 1 Then
//         y = K * TAO ^ (2 / K) / (K - 1)
//         y = y * (1 - Beta ^ 4) / (1 - Beta ^ 4 * TAO ^ (2 / K))
//         y = y * (1 - TAO ^ ((K - 1) / K)) / (1 - TAO)
//         y = y ^ 0.5
//     Else
//         y = 1
//     End If
// Else
//     L_radius = MsgBox("L_radius喷嘴前后压比不满足标准要求")
//     L_radius = TAO
//     Exit Function
// End If
//
//
//
// '计算迭代变量
// a = y * D2 ^ 2 * Sqr(2 * (dp * 1000) * Density / (1 - Beta ^ 4)) / DLND / D1
//
// '假设流出系数的C，取最大值Cmax;
// Cmax = 0.5959 + 0.0312 * Beta ^ 2.1 - 0.184 * Beta ^ 8
// C = Cmax
// I = 0
// WuCha = 1
//
// '************************迭代循环******************************
// Do While (WuCha > 0.00000000000001)
//
// '计算雷诺数Re
// Re = a * C
//
// C = 0.9965 - 0.00653 * Sqr(1000000 * Beta / Re)
// I = I + 1
// '计算误差
// WuCha = Abs((a - Re / C) / a)
//
// Loop
// '************************输出结果******************************
// Q = 3.1415926 * DLND * D1 * Re / 4
//
// L_radius = Q * 3.6
// 'L_radius = i
// End Function
//
// '********************************************ISO 5167-2-2003(文丘里管)*********************************
// 'P--工作压力(MPa);  T--工作温度(℃);    DP--差压(kPa);
// 'D1--管道内径(m);   D2--孔板内径(m);
// 'Alfa1--管道膨胀系数(mm/(mm*℃*1.0e-6));    Alfa2--孔板膨胀系数;
// 'k--等熵指数;       Dlnd--动力粘度(Pa*s);   Density--密度(kg/m3);
// 'C--流出系数;       Y--可膨胀性系数；   Beta--开孔直径比；
// 'Re--雷诺数(D);     Q--流量；
// 'X-- 迭代循环变量1; Delta-迭代循环变量2;
// 'TAO--压比;
//
// Public Function Venturi(P As Double, T As Double, dp As Double, D1_20 As Double, _
//                        D2_20 As Double, Alfa1 As Double, Alfa2 As Double, K As Double)
// Dim Beta, D1, D2, TAO As Double
// Dim DLND, Re, Density As Double
// Dim WuCha, a As Double
// Dim y, C, Cmax As Double
// Dim I As Integer
// D1 = 0
// D2 = 0
// Beta = 0
// Beta_20 = 0
// a = 0
// C = 0
// '计算试验条件下的管道和孔板内径、Beta值;
// D1 = D1_20 * (1 + Alfa1 * 0.000001 * (T - 20))
// D2 = D2_20 * (1 + Alfa2 * 0.000001 * (T - 20))
// Beta = D2 / D1
// If D1 < 0.065 Or D1 > 0.5 Then
//     L_radius = MsgBox("D超限")
//     Exit Function
// End If
// If D2 < 0.05 Then
//     L_radius = MsgBox("d超限")
//     Exit Function
// End If
// If Beta < 0.316 Or Beta > 0.775 Then
//     L_radius = MsgBox("Beta超限")
//     Exit Function
// End If
//
//
// '求动力粘度;
// DLND = DLND_PT(P, T)
//
// '判断流量是否为0
// If dp = 0 Then
//     Venturi = 0
//     Exit Function
// End If
//
//
// '求密度，工质为水时，用V_PT()来求密度;
// Density = 1 / V_PT(P, T)
//
// '计算可膨胀性系数;
// '注意单位，DP的输入单位是KPa，P的输入单位是MPa,因此要给P乘以1000；
// '该标准中规定，此公式只适用于P2/P1>=0.75的情况;
// TAO = (P - dp) / P
//
// If TAO >= 0.75 Then
//     If LTtype = 1 Then
//         y = K * TAO ^ (2 / K) / (K - 1)
//         y = y * (1 - Beta ^ 4) / (1 - Beta ^ 4 * TAO ^ (2 / K))
//         y = y * (1 - TAO ^ ((K - 1) / K)) / (1 - TAO)
//         y = y ^ 0.5
//     Else
//         y = 1
//     End If
// Else
//     Venturi = MsgBox("ISA1932喷嘴前后压比不满足标准要求")
//     Exit Function
// End If
// '文丘里管的流出系数不用迭代，直接可以计算，与雷诺数无关；
// C = 0.9858 - 0.196 * Beta ^ 4.5
//
// '************************输出结果******************************
// Q = 3.1415926 / 4 * D2 ^ 2 * C * Sqr(2 * dp * Density) * y / Sqr(1 - Beta ^ 4)
//
// Venturi = Q * 3.6
// End Function
//
// '******************************ASME 低β值喉部取压长径喷嘴*****************************************
// 'P--工作压力(MPa);  T--工作温度(℃);    DP--差压(kPa);
// 'D1--管道内径(m);   D2--孔板内径(m);    DC--(Cxavg-1.0054)
// 'Alfa1--管道膨胀系数(mm/(mm*℃*1.0e-6));    Alfa2--孔板膨胀系数;
// 'k--等熵指数;       Dlnd--动力粘度(Pa*s);   Density--密度(kg/m3);
// 'C--流出系数;       Y--可膨胀性系数；   Beta--开孔直径比；
// 'Re--雷诺数(D);     Q--流量；
// 'X-- 迭代循环变量1; Delta-迭代循环变量2;
// Public Function LL_ASME(P As Double, T As Double, dC As Double, dp As Double, D1_20 As Double, _
//                        D2_20 As Double, Alfa1 As Double, Alfa2 As Double)
// Dim Beta, D1, D2, TAO As Double
// Dim DLND, Re, Density As Double
// Dim WuCha, a As Double
// Dim y, C, Cmax As Double
// Dim I As Integer
// D1 = 0
// D2 = 0
// Beta = 0
// Beta_20 = 0
// a = 0
// C = 0
// '计算试验条件下的管道和孔板内径、Beta值;
// D1 = D1_20 * (1 + Alfa1 * 0.000001 * (T - 20))
// D2 = D2_20 * (1 + Alfa2 * 0.000001 * (T - 20))
// Beta = D2 / D1
// '求动力粘度;
// DLND = DLND_PT(P, T)
//
// '判断流量是否为0
// If dp = 0 Then
//     LL_ASME = 0
//     Exit Function
// End If
//
//
// '求密度，工质为水时，用V_PT()来求密度;
// Density = 1 / V_PT(P, T)
//
// '计算可膨胀性系数;
// '注意单位，DP的输入单位是KPa，P的输入单位是MPa,因此要给P乘以1000；
// '该标准中规定，此公式只适用于P2/P1>=0.75的情况;
// y = 1
//
// '计算迭代变量,其中：ASME低Beta喉部取压长颈喷嘴的流出系数迭代中用的雷诺数是以喷嘴中的小d为特征长度的；
// a = y * D2 ^ 2 * Sqr(2 * (dp * 1000) * Density / (1 - Beta ^ 4)) / DLND / D2
//
// '假设流出系数的C，取最大值Cmax;
// Cmax = 0.5959 + 0.0312 * Beta ^ 2.1 - 0.184 * Beta ^ 8
// C = Cmax
// I = 0
// WuCha = 1
//
// '************************迭代循环******************************
// Do While (WuCha > 0.00000000000001)
//
// '计算雷诺数Re
// Re = a * C
//
// C = 1.0054 + dC - 0.185 * Re ^ (-0.2) * (1 - 361239 / Re) ^ 0.8
// I = I + 1
// '计算误差
// WuCha = Abs((a - Re / C) / a)
//
// Loop
// '************************输出结果******************************
// Q = 3.1415926 * DLND * D2 * Re / 4
//
// LL_ASME = Q * 3.6
// End Function



