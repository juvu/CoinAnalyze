def ppaBasic(High, Low, Close):
    """
    典型枢轴点
    枢轴点的计算有多种形式,最常用的一种形式使用5个关键点.包括Pivot Point、Support 1 (支持点1)、Resistance 1 (阻力点1)、Support 2 (支持点2) 、Resistance 2 (阻力点2)。计算公式如下：
    """
    # 枢轴点
    PivotPoint = (High + Low + Close) / 3
    # 阻力位1
    Resistance1 = PivotPoint * 2 - Low
    # 支持位1
    Support1 = PivotPoint * 2 - High
    # 阻力位2
    Resistance2 = PivotPoint + (High - Low)
    # Resistance2 := PivotPoint + (Resistance1-Support1)
    # 支持位2
    Support2 = PivotPoint - (High - Low)
    # Support2 = PivotPoint-(Resistance1-Support1)
    return Support2, Support1, PivotPoint, Resistance1, Resistance2


def ppaWoodie(High, Low, Close):
    """
    伍迪(Woodie)枢轴点

    伍迪枢轴点与经典枢轴点类似，但给予收盘价更大的权重。伍迪枢轴点也是由前一时期的最高价（H）、最低价（L）和收盘价（C）推算出当期的枢轴点
    """
    # 枢轴点
    PivotPoint = (High + Low + 2 * Close) / 4
    # 阻力位1
    Resistance1 = PivotPoint * 2 - Low
    # 阻力位2
    Resistance2 = PivotPoint + (High - Low)  # resistance2 := pivotPoint + (resistance1-support1)
    # 支持位1
    Support1 = PivotPoint * 2 - High
    # 支持位2
    Support2 = PivotPoint - (High - Low)  # support2 = pivotPoint-(resistance1-support1)
    return Support2, Support1, PivotPoint, Resistance1, Resistance2


def ppaCamarilla(High, Low, Close):
    """
    卡玛利拉(Camarilla)枢轴点
    卡玛利拉枢轴点，是由前一时期的最高价（H）、最低价（L）和收盘价（C）推算出来。
    """
    # 枢轴点
    PivotPoint = (High + Low + Close) / 3.0
    # 支持位
    Support1 = Close - (High - Low) * 1.1 / 12
    Support2 = Close - (High - Low) * 1.1 / 6
    Support3 = Close - (High - Low) * 1.1 / 4
    Support4 = Close - (High - Low) * 1.1 / 2
    # 阻力位
    Resistance1 = Close + (High - Low) * 1.1 / 12
    Resistance2 = Close + (High - Low) * 1.1 / 6
    Resistance3 = Close + (High - Low) * 1.1 / 4
    Resistance4 = Close + (High - Low) * 1.1 / 2
    return  Support2, Support1, PivotPoint, Resistance1, Resistance2


def ppaFibonacci(High, Low, Close):
    """
    斐波纳契枢(Fibonacci)轴点
    斐波纳契枢轴点是经典枢轴点与斐波纳契比率的结合。首先，由前一时期的最高价（H）、最低价（L）和收盘价（C）之和除以3，算出后一时期的枢轴点。然后将斐波纳契比率分别加上枢轴点，推算出后一时期的支持位和阻力位:
    """
    #由低到高排序
    # 枢轴点
    PivotPoint = (High + Low + Close) / 3
    # 支持位
    Support3 = PivotPoint + (High+Low)*1.0
    Support2 = PivotPoint + (High+Low)*0.618
    Support1 = PivotPoint + (High+Low)*0.382

    #PivotPoint = (High + Low + Close) /3

    # 阻力位
    Resistance1 = PivotPoint + (High+Low)*0.382
    Resistance2 = PivotPoint + (High+Low)*0.618
    Resistance3 = PivotPoint + (High+Low)*1.0
    return Support3, Support2, Support1, PivotPoint, Resistance1, Resistance2, Resistance3


def ppaDeMark(High, Low, Close, OpenThis):
    """
    汤姆.丹麦枢轴点
    汤姆.丹麦枢轴点是对当期的新最高价和新最低价的预测
    """
    if Close < OpenThis:
        x = High + 2*Low + Close
    elif Close > OpenThis:
        x = 2*High + Low + Close
    else:
        x = High + Low + 2*Close

    HighThis = x/2 - Low
    LowThis = x/2 - High
    return LowThis, HighThis