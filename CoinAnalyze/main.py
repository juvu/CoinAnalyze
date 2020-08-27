# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from decimal import Decimal

from binance_f import RequestClient
from configparser import ConfigParser

config = ConfigParser()
# 传入读取文件的地址，encoding文件编码格式，中文必须
config.read('config.ini', encoding='UTF-8')

base_api = RequestClient(url='https://api.binance.com',
                         api_key=config['binance']['api_key'],
                         secret_key=config['binance']['secret_key'])
f_api = RequestClient(url='https://fapi.binance.com',
                      api_key=config['binance']['api_key'],
                      secret_key=config['binance']['secret_key'])


def print_hi(symbol, wait: 'bool' = False, wait_price: 'Decimal' = 0):
    """

    :param symbol:
    :param wait: 是否计算预计价格
    :return:
    """
    result = base_api.get_myTrades(symbol=symbol)
    current_price = wait_price
    if wait:
        if wait_price == 0:
            recentTrade = f_api.get_symbol_price_ticker(symbol=symbol)
            current_price = Decimal(recentTrade[0].price)

    profit = Decimal(0)
    commission_all = Decimal(0)
    qty_count_all = Decimal(0)
    avg_price = Decimal(0)
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
        else:
            qty_count_all -= qty
            current = quoteQty - commission
        profit = profit + current

    wait_ = qty_count_all * current_price + profit
    print('币种', symbol,
          '总盈利', profit,
          '总手续费', commission_all,
          '卖出预计盈利', wait_,
          '入手均价', profit / qty_count_all * -1,
          '现在价格', current_price,
          )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('SOLUSDT')
    # print_hi('BANDUSDT')
    print_hi('KAVAUSDT', wait=True, wait_price=Decimal(0))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
