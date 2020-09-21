from decimal import Decimal
# 用于定制线条颜色
from cycler import cycler

import mplfinance as mpf
import pandas as pd
from pandas import DataFrame

from CoinAnalyze import ppa_algorithm, base_api

# from CoinAnalyze.mock import klines

data = {'Date': [], 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Volume': [],
        '收盘时间': [], '成交额': [], '成交笔数': [], '主动买入成交量': [], '主动买入成交额': [],
        "Support2": [], "Support1": [], "PivotPoint": [], "Resistance1": [], "Resistance2": [],
        }
klines = base_api.get_klines('UNIUSDT', interval='3m', limit=500)

for k in klines:
    开盘时间, 开盘价, 最高价, 最低价, 收盘价, 成交量, 收盘时间, 成交额, 成交笔数, 主动买入成交量, 主动买入成交额, ignore = k
    Support2, Support1, PivotPoint, Resistance1, Resistance2 = ppa_algorithm.ppaWoodie(Decimal(最高价), Decimal(最低价),
                                                                                       Decimal(收盘价))
    data['Date'].append(开盘时间)
    data['Open'].append(float(开盘价))
    data['High'].append(float(最高价))
    data['Low'].append(float(最低价))
    data['Close'].append(float(收盘价))
    data['Volume'].append(float(成交量))
    data['Support2'].append(float(Support2))
    data['Support1'].append(float(Support1))
    data['PivotPoint'].append(float(PivotPoint))
    data['Resistance1'].append(float(Resistance1))
    data['Resistance2'].append(float(Resistance2))
    data['收盘时间'].append(收盘时间)
    data['成交额'].append(成交额)
    data['成交笔数'].append(成交笔数)
    data['主动买入成交量'].append(主动买入成交量)
    data['主动买入成交额'].append(主动买入成交额)
    # print(ppa)
# print(klines)
df = DataFrame(data,
               columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume',
                        'Support2', 'Support1', 'PivotPoint', 'Resistance1', 'Resistance2',
                        '收盘时间', '成交额', '成交笔数', '主动买入成交量',
                        '主动买入成交额', ], )
print()

# print(df)
df.index = pd.DatetimeIndex(pd.to_datetime(df['Date'], unit='ms'))

# 设置基本参数
# type 绘制图形的类型，有candle, renko, ohlc, line等
# 此处选择candle,即K线图
# mav(moving average):均线类型,此处设置7,30,60日线
# volume:布尔类型，设置是否显示成交量，默认False
# title:设置标题
# y_label_lower:设置成交量图一栏的标题
# figratio:设置图形纵横比
# figscale:设置图形尺寸(数值越大图像质量越高)
kwargs = dict(
    type='renko',
    mav=(7, 30, 60),
    volume=True,
    title='\nA_stock candle_line', ylabel='OHLC Candles',
    ylabel_lower='Shares\nTraded Volume',
    figratio=(15, 10),
    figscale=5)

mc = mpf.make_marketcolors(
    up='green',
    down='red',
    edge='i',
    wick='i',
    volume='in',
    inherit=True)
# 设置图形风格
# gridaxis:设置网格线位置
# gridstyle:设置网格线线型
# y_on_right:设置y轴位置是否在右
s = mpf.make_mpf_style(
    gridaxis='both',
    gridstyle='-.',
    y_on_right=False,
    marketcolors=mc)

mpf.plot(df, **kwargs, style=s)
