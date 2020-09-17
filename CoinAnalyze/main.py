# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time
from decimal import Decimal

from CoinAnalyze import f_api, base_api


def get_time_stamp(t):
    datetime_obj = time.mktime(time.strptime(t, "%Y-%m-%d %H:%M"))
    return int(round(datetime_obj * 1000))


def get_symbol_price(symbol):
    """
    获取货币当前价格
    :param symbol:
    """
    recent_trade = f_api.get_symbol_price_ticker(symbol=symbol)
    return Decimal(recent_trade[0].price)


def print_hi(symbol,  wait: 'bool' = False, wait_price: 'Decimal' = 0):
    """

    :param symbol:
    :param wait: 是否计算预计价格
    :param wait_price: 手动传入价格 不传或者为0，自动按照当前价格计算
    :return:
    """

    result = base_api.get_myTrades(symbol=symbol)
    current_price = wait_price
    if wait and wait_price == 0:
        current_price = get_symbol_price(symbol=symbol)

    profit = Decimal(0)
    commission_all = Decimal(0)
    qty_count_all = Decimal(0)
    avg_price = Decimal(0)
    if len(result) == 0:
        print('没数据')
        return
    for data in result:
        price = data['price']
        buyer = data['isBuyer']
        # 成交数量
        qty = Decimal(data['qty'])
        # 成交金额
        quoteQty = Decimal(data['quoteQty'])

        # 手续费
        commission = Decimal(data['commission'])
        commission_all += commission
        if buyer:
            qty_count_all += qty
            current = -quoteQty - commission
            print('买', symbol, '价格', price, '数量', qty, '成交金额', current)
        else:
            qty_count_all -= qty
            current = quoteQty - commission
            print('卖', symbol, '价格', price, '数量', qty, '成交金额', current)
        profit = profit + current
    # print(current_price)
    wait_ = qty_count_all * current_price + profit
    print('币种', symbol,
          '总盈利', profit,
          '总手续费', commission_all,
          '卖出预计盈利', wait_,
          '估值', wait_ * Decimal(6.8),
          '入手均价', profit / qty_count_all * -1,
          '现在价格', current_price,
          )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('SOLUSDT', wait=True, wait_price=Decimal(5))
    # print_hi('BANDUSDT')
    print_hi('KAVAUSDT', wait=True, wait_price=Decimal(5))
    # print_hi('QTUMUSDT', wait=True, wait_price=Decimal(0))
    # print_hi('SANDUSDT', wait=True, wait_price=Decimal(0))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
