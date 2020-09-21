import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import warnings
import talib
from tqsdk import TqApi, TqBacktest, TargetPosTask, ta, TqSim

from CoinAnalyze import base_api


def get_pv_df(klines: pd.DataFrame, distance=10):
    xxx = np.arange(len(klines))
    yyy = np.array(klines["close"])

    warnings.filterwarnings("error")

    for i in range(1, 500):
        try:
            z1 = np.polyfit(xxx, yyy, i)
        except Warning:
            z1 = np.polyfit(xxx, yyy, i - 1)
            warnings.filterwarnings("ignore")
            break
    p1 = np.poly1d(z1)
    yvals = p1(xxx)

    # plt.plot(xxx, yyy, '.', label='original values')
    # plt.plot(xxx, yvals, 'r', label='polyfit values')
    # plt.xlabel('x axis')
    # plt.ylabel('y axis')
    # plt.legend(loc=4)
    # plt.title('polyfitting')
    # plt.show()

    num_peak = signal.find_peaks(yvals, distance=distance)
    num_valley = signal.find_peaks(-yvals, distance=distance)

    '''
    num_peak = signal.find_peaks_cwt(yyy, np.arange(1,100), signal.ricker)#小波变换后找峰效果似乎不是很好
    num_valley = signal.find_peaks_cwt(yyy, np.arange(1,100), signal.ricker) #小波变换后找峰效果似乎不是很好
    '''

    # plt.plot(xxx, yyy, '.', label='original values')
    plt.plot(xxx, yvals, 'r', label='polyfit values')
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.legend(loc=4)
    plt.title('polyfitting')
    for ii in range(len(num_peak[0])):
        plt.text(num_peak[0][ii], yvals[num_peak[0][ii]],
                 round(yvals[num_peak[0][ii]], 2),
                 color='m')
    for ii in range(len(num_valley[0])):
        plt.text(num_valley[0][ii], yvals[num_valley[0][ii]],
                 round(yvals[num_valley[0][ii]], 2),
                 color='m')
    plt.show()

    klines_copy = klines.copy()
    # 2为非峰非谷
    klines_copy["pv"] = [2] * len(klines_copy)

    # 1为峰
    for i in num_peak[0]:
        klines_copy.iloc[i, -1] = 1
    # 0为谷
    for i in num_valley[0]:
        klines_copy.iloc[i, -1] = 0

    # 峰谷定位
    df = klines_copy[klines_copy["pv"] != 2].copy()
    df["hv"] = df["close"].diff()
    print(df["hv"])
    return df


data = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': [],
        '收盘时间': [], '成交额': [], '成交笔数': [], '主动买入成交量': [], '主动买入成交额': [],
        "Support2": [], "Support1": [], "PivotPoint": [], "Resistance1": [], "Resistance2": [],
        }
# from CoinAnalyze.mock import klines
klines = base_api.get_klines('KAVAUSDT', interval='6h', limit=500)

for k in klines:
    开盘时间, 开盘价, 最高价, 最低价, 收盘价, 成交量, 收盘时间, 成交额, 成交笔数, 主动买入成交量, 主动买入成交额, ignore = k

    data['date'].append(收盘时间)
    data['open'].append(float(开盘价))
    data['high'].append(float(最高价))
    data['low'].append(float(最低价))
    data['close'].append(float(收盘价))
    data['volume'].append(float(成交量))
    data['收盘时间'].append(收盘时间)
    data['成交额'].append(成交额)
    data['成交笔数'].append(成交笔数)
    data['主动买入成交量'].append(主动买入成交量)
    data['主动买入成交额'].append(主动买入成交额)
    # print(ppa)
# print(klines)
df = pd.DataFrame(data,
                  columns=['date', 'open', 'high', 'low', 'close', 'volume',
                           '收盘时间', '成交额', '成交笔数', '主动买入成交量',
                           '主动买入成交额', ], )
df = get_pv_df(df)
pv = list(df.iloc[-3:]["pv"])
price1 = df.iloc[-3]["close"]
price2 = df.iloc[-2]["close"]
price3 = df.iloc[-1]["close"]

atr = ta.ATR(df, 14).iloc[-1]["atr"]

print(price1, price2, price3)
print(pv)
