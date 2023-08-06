function PT(p, T, V, U, S, H, CP, CV, W) {
    if (T >= 273.15 && p <= 100) {
        let Ps = PSK(T)
        if (p > Ps && p <= 100) {
            PT_1(p, T, V, U, S, H, CP, CV, W)
        } else if (p >= 0 && p <= Ps) {
            PT_2(p, T, V, U, S, H, CP, CV, W)
        }
    } else if (T >= 623.15 && T <= 863.15) {
        let P23;
        P23 = P_B23(T);
        if (p >= P23 && p <= 100) {
            PT_3(p, T, V, U, S, H, CP, CV, W)
        } else if (p >= 0 && p <= P23) {
            PT_2(p, T, V, U, S, H, CP, CV, W)
        }
    } else if (T >= 863.15 && T <= 1073.15) {
        if (p >= 0 && p <= 100) {
            PT_2(p, T, V, U, S, H, CP, CV, W)
        }
    } else if (T >= 1073.15 && T <= 2073.15) {
        if (p > 0 && p <= 10) {
            PT_5(p, T, V, U, S, H, CP, CV, W)
        }
    }
}

// 'Calculate Saturation Pressure Ps from Ts(由饱和温度计算饱和压力).
// 'Ts [K], Valid for 273.15 K --- 647.096 K
// 'Ps [MPa]
// 'Input parameters:  T-the specific temperature
// 'Output parameters:  P-the saturation pressure corresponding to the specific temperature
// '*************************************
function PSK(T) {
    let A, B, C, AN
    AN = [0, 1167.0521452767, -724213.16703206, -17.073846940092, 12020.82470247, -3232555.0322333, 14.91510861353,
        -4823.2657361591, 405113.40542057, -0.23855557567849, 650.17534844798]
    let TCT = 1;
    if (T > 273.15 && T < 647.096) {
        let ZT = T / TCT;
        ZT = ZT + AN[8] / (ZT - AN[9]);
        A = ZT ^ 2 + AN[0] * ZT + AN[1]
        B = AN[2] * ZT ^ 2 + AN[3] * ZT + AN[4]
        C = AN[5] * ZT ^ 2 + AN[6] * ZT + AN[7]
        let result;
        result = 2 * C / (Sqr(B * B - 4 * A * C) - B);
        result = result ^ 4;
        return result
    }
}

// 'Calculate Saturation Temperature Ts from Ps(由饱和压力计算饱和温度,饱和温度线方程).
// 'Ps [MPa], Valid for 611.213 Pa --- 22.064 MPa
// 'Ts [K]
// 'Checked By Li, April 17, 2007
function TSK(p) {
    let AN;
    AN = [0, 1167.0521452767, -724213.16703206, -17.073846940092, 12020.82470247, -3232555.0322333, 14.91510861353,
        -4823.2657361591, 405113.40542057, -0.23855557567849, 650.17534844798]
    let PCT = 1;

    if (p > 0.000611213 && p < 22.064) {
        let ZP = (p / PCT) ^ 0.25;
        let E = ZP ^ 2 + AN[2] * ZP + AN[5]
        let F = AN[0] * ZP ^ 2 + AN[3] * ZP + AN[6];
        let G = AN[1] * ZP ^ 2 + AN[4] * ZP + AN[7];
        let D = 2 * G / (-F - Sqr(F * F - 4 * E * G))
        let TSK = AN[9] + D - Sqr((AN[9] + D) ^ 2 - 4 * (AN[8] + AN[9] * D))
        return TSK / 2;
    }
}