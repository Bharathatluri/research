###########################################################################
##
##
## Script to get the Historical data of coins listed in coin.txt
## sourcing from MESSARI API, output to myHistdata.xlsx
## Author: Bharath Kumar
## Date: 07/11/2021
## 
## coin.txt content:
## btc
## ada
##
##
############################################################################

import os
import time
import requests
import pandas as pd
from pathlib import Path

''' Func to get the historical data from API for a specific sym '''
def get_crypto_price(symbol, start, end):
    try:
        pd.set_option('display.max_rows', None)
        api_url = f'https://data.messari.io/api/v1/markets/binance-{symbol}-usdt/metrics/price/time-series?start={start}&end={end}&interval=1d'
        raw = requests.get(api_url).json()
        df = pd.DataFrame(raw['data']['values'])
        df = df.rename(columns = {0:'date',1:'open',2:'high',3:'low',4:'close',5:'volume',6:'symbol'})
        df['date'] = pd.to_datetime(df['date'], unit = 'ms')
        df = df.set_index('date')
        return df
    except:
        print(symbol+" data not found, skip")

''' Func to truncate the file content '''
def deleteContent(fName):
    with open(fName, "w"):
        pass

#histData=[]
#allData=[]

deleteContent(str(Path.home())+'/myHistdata_1.xlsx')

with open(str(Path.home())+'/coin_test.txt') as f:
    coinList = [line.rstrip() for line in f]

for coin in coinList:
	#histData.append(coin)
	#histData.append(get_crypto_price(coin, '2021-11-01', '2021-11-06'))
	histData = get_crypto_price(coin, '2021-11-04', '2021-11-06')
	#histData type is: <class 'pandas.core.frame.DataFrame'>
	time.sleep(1)
	#if histData is None:
	#	pass
	#else:
	#	for data in histData:
	#		print(data)
	#		allData.append(data)
	#print(histData)
	#toExcelData = pd.DataFrame(histData)
	toExcelData = pd.DataFrame.append(histData, ignore_index=True)
	#print(toExcelData)	
	#writeToExcel(histData)
#print(allData)
#print(type(allData)	)
#toExcelData = pd.concat(allData, ignore_index=False)
toExcelData.to_excel(str(Path.home())+'/myHistdata_1.xlsx', index = False, header=True)

#deleteContent('/Users/bharath/myHistdata.xlsx')
#toExcelData.to_excel (r'/Users/bharath/myHistdata.xlsx', index = False, header=True)

#def writeToExcel(histData):
#	histData.to_excel(r'/Users/bharath/myHistdata.xlsx', index = False, header=True, truncate_sheet=False)
