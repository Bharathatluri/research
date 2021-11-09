###########################################################################
##
##
## Script to get the Historical data(from 2019 Jan 01) of coins listed in coin.txt
## sourcing from MESSARI API, output to myHistdata.xlsx
## Author: Bharath Kumar
## Date: 07/11/2021
##
##
## coin.txt content can be:
## btc
## ada
##
## Data Range - Defaul start date: 2019-01-01 Till Today
## * Today is considered when script is executed *
##
############################################################################

import os
import time
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from csv import reader
from openpyxl import load_workbook

''' All required variables and data '''

today = datetime.today().strftime('%Y-%m-%d')

allData = pd.DataFrame()

missingCoins = []

coinListFile = str(Path.home())+'/coin.txt'

outFile = str(Path.home())+'/myHistdata.xlsx'


''' Func to get the historical data from API for a specific sym '''

def get_crypto_price(symbol, start, end):
    try:

        pd.set_option('display.max_rows', None)
        api_url = f'https://data.messari.io/api/v1/markets/binance-{symbol}-usdt/metrics/price/time-series?start={start}&end={end}&interval=1d'
        raw = requests.get(api_url).json()
        df = pd.DataFrame(raw['data']['values'])
        df = df.rename(columns = {0:'date',1:'open',2:'high',3:'low',4:'close',5:'volume'})
        df['date'] = pd.to_datetime(df['date'], unit = 'ms')
        #df = df.set_index('date')
        return df

    except:

        print(symbol+" data not found, skip")

''' Func to Trucate the file content '''

def deleteContent(fName):
    with open(fName, "w"):
        pass

''' Func to write the data to Excel '''

def writeToExcel(outFile):
        writer = pd.ExcelWriter(outFile, engine = 'openpyxl')
        allData.to_excel(writer, sheet_name = 'Historical Data', index = False, header=True)
        missingCoinsData.to_excel(writer, sheet_name = 'Missing Data', index = False, header=True)
        writer.save()
        writer.close()

with open(coinListFile) as f:
    coinList = [line.rstrip() for line in f]

for coin in coinList:
	histData = get_crypto_price(coin, '2019-01-01', today)

	if histData is None:
		missingCoins.append(coin)
		pass
	else:
		histData['coin']=coin

	#print(histData)
	# Sleep is needed, otherwise api fail to gather data for many coins
	time.sleep(2)
	''' allData is Panda DataFrame, .append will add new to allData '''
	allData = allData.append(histData, ignore_index=True)
#print(missingCoins)

''' missCoinsData will hold list of coins which doesn't have any data in API '''
missingCoinsData = pd.DataFrame( list(reader(missingCoins)))
missingCoinsData = missingCoinsData.rename(columns = {0:'coins'})

''' Truncate existing data in excel for every run '''
deleteContent(outFile)
''' Write new data to excel '''
writeToExcel(outFile)




