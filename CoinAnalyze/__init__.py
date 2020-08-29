from configparser import ConfigParser
from binance_f import RequestClient

config = ConfigParser()
# 传入读取文件的地址，encoding文件编码格式，中文必须
config.read('config.ini', encoding='UTF-8')

base_api = RequestClient(url='https://api.binance.com',
                         api_key=config['binance']['api_key'],
                         secret_key=config['binance']['secret_key'])

f_api = RequestClient(url='https://fapi.binance.com',
                      api_key=config['binance']['api_key'],
                      secret_key=config['binance']['secret_key'])