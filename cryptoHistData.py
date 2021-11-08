###########################################################################
##
##
## Script to get the Historical data of coins listed in coin.txt
## sourcing from MESSARI API, output to myHistdata.xlsx
## Author: Bharath Kumar
## Date: 07/11/2021
##
##
## coin.txt content can be:
## btc
## ada
##
############################################################################

import os
import time
import requests
import pandas as pd
from pathlib import Path

def get_crypto_price(symbol, start, end):
    try:
        pd.set_option('display.max_rows', None)
        api_url = f'https://data.messari.io/api/v1/markets/binance-{symbol}-usdt/metrics/price/time-series?start={start}&end={end}&interval=1d'
        raw = requests.get(api_url).json()
        df = pd.DataFrame(raw['data']['values'])
        df = df.rename(columns = {0:'date',1:'open',2:'high',3:'low',4:'close',5:'volume'})
        df['date'] = pd.to_datetime(df['date'], unit = 'ms')
        df = df.set_index('date')
        #df.to_excel (r'~/myHistdata.xlsx', index = Ture, header=True)
        return df
    except:
        print(symbol+" data not found, skip")

def deleteContent(fName):
    with open(fName, "w"):
        pass

histData = []

with open(str(Path.home())+'/coin.txt') as f:
    coinList = [line.rstrip() for line in f]
for coin in coinList:
	histData.append(coin)
	histData.append(get_crypto_price(coin, '2020-11-06', '2021-11-06'))
	time.sleep(2)
#print(histData)
toExcelData = pd.DataFrame(histData)

deleteContent(str(Path.home())+'/myHistdata.xlsx')
toExcelData.to_excel(str(Path.home())+'/myHistdata.xlsx', index = False, header=True)
