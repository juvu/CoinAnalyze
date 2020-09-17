from decimal import Decimal

import pandas as pd
from pandas import DataFrame

from CoinAnalyze import ppa_algorithm, indicators, base_api
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.model import *

symbol = 'BANDUSDT'
klines = base_api.get_klines(symbol, interval='3m', limit=500)
sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)

# 计算砖块大小
data = {'Date': [], 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Volume': [],
        '收盘时间': [], '成交额': [], '成交笔数': [], '主动买入成交量': [], '主动买入成交额': [],
        "Support2": [], "Support1": [], "PivotPoint": [], "Resistance1": [], "Resistance2": [],
        }

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

df = DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume',
                              'Support2', 'Support1', 'PivotPoint', 'Resistance1', 'Resistance2',
                              '收盘时间', '成交额', '成交笔数', '主动买入成交量',
                              '主动买入成交额', ], )


def _calculate_atr(atr_length, highs, lows, closes):
    """Calculate the average true range
    atr_length : time period to calculate over
    all_highs : list of highs
    all_lows : list of lows
    all_closes : list of closes
    """
    if atr_length < 1:
        raise ValueError("Specified atr_length may not be less than 1")
    elif atr_length >= len(closes):
        raise ValueError("Specified atr_length is larger than the length of the dataset: " + str(len(closes)))
    atr = 0
    for i in range(len(highs) - atr_length, len(highs)):
        high = highs[i]
        low = lows[i]
        close_prev = closes[i - 1]
        tr = max(abs(high - low), abs(high - close_prev), abs(low - close_prev))
        atr += tr
    return atr / atr_length


brick_size = 0.08
# brick_size = _calculate_atr(14, df['High'], df['Low'], df['Close'])
# 砖块大小
print('砖块大小', brick_size)


def _callback(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
        print("Event ID: ", event)
    elif data_type == SubscribeMessageType.PAYLOAD:
        dfNew = pd.DataFrame([{'Date': event.data.closeTime,
                               'Open': event.data.open,
                               'High': event.data.high,
                               'Low': event.data.low,
                               'Close': event.data.close,
                               'Volume': event.data.volume}]
                             , columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        global df
        # brick_size = _calculate_atr(14, df['High'], df['Low'], df['Close'])
        # 砖块大小
        # print('砖块大小', brick_size)
        df = df.append(dfNew, ignore_index=True)
        renko = indicators.Renko(df)
        print('\n\nRenko box calcuation based on periodic close')
        renko.brick_size = brick_size
        renko.chart_type = indicators.Renko.PERIOD_CLOSE
        data = renko.get_ohlc_data()
        MA10 = df['Close'].rolling(10).mean()
        data['MA10'] = MA10
        print(data.tail(10))
    else:
        print("Unknown Data:")
    print()


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)


sub_client.subscribe_candlestick_event(symbol.lower(), CandlestickInterval.MIN3, _callback, error)
