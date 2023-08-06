# 设置模型路径
import numpy as np
import pandas as pd

from yangke.common.config import logger
from yangke.ebsilon.ebsilon import EbsUnits, EbsApp, EbsModel, EbsObject

model_path = r"F:\电站性能技术部\Desktop\重庆两江燃机\冷端优化2_14版不使用燃机库_100%设计工况.ebs"
# data_path = r"C:\Users\杨可\Documents\WPS Cloud Files\217145378\6科研项目\2021\华能重庆两江燃机发电有限责任公司\重庆两江批量计算.xlsx"
data_path = r"F:\电站性能技术部\Desktop\重庆两江燃机\重庆两江批量计算.xlsx"


class Condition:
    def __init__(self, name):
        self.name = name
        self.data = []

    def append_parameters(self, component, variable, value, unit, profile=None):
        self.data.append({"component": component, "variable": variable, "value": value, "unit": unit})


def init_ebsilon():
    """
    初始化ebsilon
    :return:
    """
    ebsilon = EbsApp()
    ebsilon.describe()
    return ebsilon


def read_data_from_xlsx(filename: str):
    """
    读取xlsx文件中的数据，并组装为Conditions字典
    :param filename:
    :return:
    """
    sheet_data: pd.DataFrame = pd.read_excel(filename)
    sheet_data.dropna(subset=["变量名", "组件名"], inplace=True)  # 删除变量名和组件名为空的行
    sheet_data.dropna(axis=1, how="all")
    conditions = {}
    for name in sheet_data.columns[4:]:
        conditions.update({name: Condition(name)})
    for i, row in sheet_data.iterrows():
        component_name = row["组件名"]
        variable_name = row["变量名"]
        unit = row["单位"].replace("/", "_")
        try:
            unit = unit.replace("℃", "C")
            if unit == "_":
                unit = EbsUnits.unit_1  # 没有单位，例如湿度
            else:
                unit = eval(f"EbsUnits.{unit}")
        except:
            unit = None

        for col in row[4:].iteritems():
            conditions.get(col[0]).append_parameters(component_name, variable_name, col[1], unit)
    return conditions


def solve(ebsilon, condition):
    model_path_test = f"{model_path[:-4]}_{condition}.ebs"

    # 打开模型文件，并激活design的profile
    model: EbsModel = ebsilon.open(model_path)
    model.activate_profile("design")  # 激活当前操作的Profile，后续操作均在激活的Profile上进行

    # 设置组件参数
    for para in condition.data:
        comp = para.get("component")
        var = para.get("variable")
        value = para.get("value")
        unit = para.get("unit")
        model.set_value(comp, var, value, unit)

    # 获取模型中的参数值
    p_fgh_gas_in = pnt_p_fgh_gas_in.get_value("MEASM", EbsUnits.MPa)
    power1 = generator1.get_value("QREAL", EbsUnits.MW)

    model.save_as(model_path_test)  # 另存一份模型，后续在新模型上更改
    ebsilon.show_window()

    value = 4
    pnt_p_fgh_gas_in.set_value("MEASM", value, EbsUnits.MPa)
    ebs_calc_result = model.simulate_new()
    logger.info(ebs_calc_result)

    p_fgh_gas_in = pnt_p_fgh_gas_in.get_value("MEASM", EbsUnits.MPa)
    power1 = generator1.get_value("QREAL", EbsUnits.MW)
    logger.info(f"燃气入口压力为{p_fgh_gas_in} MPa")
    logger.info(f"燃机发电机功率为{power1} MW")

    model.save()


data: dict = read_data_from_xlsx(data_path)
ebs = init_ebsilon()
for key, condition in data.items():
    solve(ebs, condition)
