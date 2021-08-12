import pdb, os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib.error
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
import time, re
from tqdm import tqdm
import json

headers = {'User-Agent': 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94 safari/537.36'}


esc_url = "https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611"
esc_url_api = f"https://api.ethplorer.io/getAddressInfo/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611?apiKey=freekey"

#API Documentation: https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
bsc_url = "https://bscscan.com/token/0xbf05279f9bf1ce69bbfed670813b7e431142afa4"
bsc_key = '33ZABD5NV1J7XJJGGZCX7M3H2XVG868BTM'
bsc_address = '0xbf05279f9bf1ce69bbfed670813b7e431142afa4'
bsc_url_api = f"https://bscscan.com/token/{bsc_address}?apikey={bsc_address}"


f'https://bscscan.com/getAddressTransactions/{bsc_address}?apiKey=freekey'


#https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0xbf05279f9bf1ce69bbfed670813b7e431142afa4&apikey=33ZABD5NV1J7XJJGGZCX7M3H2XVG868BTM



# 56 is for the code chain for Binance Smart Chain
#https://api.covalenthq.com/v1/56/tokens/0xBF05279F9Bf1CE69bBFEd670813b7e431142Afa4/token_holders/?key=ckey_9f1e4e6ae5b74be9be04c23d7b6%20&page-size=1
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    req = Request(url=esc_url_api, headers=headers)
    req_bsc = Request(url=bsc_url_api, headers=headers)
    try:
        if  urlopen(req).read():### Need to  have error pass here 
            html = urlopen(req).read() 
            soup = BeautifulSoup(html,'html.parser')
            data = json.loads(soup.get_text())
            print(json.dumps(data,indent=4))
            million_data = data['tokenInfo']
            print('\nMillion Token Data: \n'*1)
            print(json.dumps(million_data,indent=4))
            #pd.to_datetime(million_data['lastUpdated'], unit='s')
            df_es_api = pd.DataFrame({'address': [million_data['address']],
                                  'decimals': [million_data['decimals']],
                                  'name': [million_data['name']],
                                  'symbol': [million_data['symbol']],
                                  'totalSupply': [million_data['totalSupply']],
                                  'lastUpdated': [million_data['lastUpdated']],
                                  'slot': [million_data['slot']],
                                  'issuancesCount': [million_data['issuancesCount']],
                                  'holdersCount': [million_data['holdersCount']],
                                  'website': [million_data['website']],
                                  'telegram': [million_data['telegram']],
                                  'reddit': [million_data['reddit']],
                                  'image': [million_data['image']],
                                  'coingecko': [million_data['coingecko']],
                                  'ethTransfersCount': [million_data['ethTransfersCount']],
                                  'rate': [million_data['price']['rate']],
                                  'diff': [million_data['price']['diff']],
                                  'diff7d': [million_data['price']['diff7d']],
                                  'ts': [million_data['price']['ts']],
                                  'marketCapUsd': [million_data['price']['marketCapUsd']],
                                  'availableSupply': [million_data['price']['availableSupply']],
                                  'volume24h': [million_data['price']['volume24h']],
                                  'volDiff1': [million_data['price']['volDiff1']],
                                  'volDiff7': [million_data['price']['volDiff7']],
                                  'currency': [million_data['price']['currency']],
                                  })
            
            with open('./data/data_esc_api.csv', 'a') as f: # 'a' is for append mode
                df_es_api.to_csv(f, header=False)
            pdb.set_trace()
            
            df_es = pd.DataFrame({'Date-Time': [time.ctime()],
                        'Date': [pd.to_datetime(million_data['price']['ts'],unit='s')],
                        'Year': [pd.to_datetime(million_data['price']['ts'],unit='s').year],
                        'Month': [pd.to_datetime(million_data['price']['ts'],unit='s').month],
                        'Day': [pd.to_datetime(million_data['price']['ts'],unit='s').day],
                        'Hour': [pd.to_datetime(million_data['price']['ts'],unit='s').hour],
                        'Minute': [pd.to_datetime(million_data['price']['ts'],unit='s').minute],
                        'Second': [pd.to_datetime(million_data['price']['ts'],unit='s').second],
                        'Time': [pd.to_datetime(million_data['price']['ts'],unit='s').time()],
                        'Price': [million_data['price']['rate']],
                        'Holders': [million_data['holdersCount']],
                        'Market Cap [$USD]': [million_data['price']['marketCapUsd']],
                        'Max Supply': [float(million_data['totalSupply'])*1E-18]
                        })
            print(df_es)
            
            
            # with open('./data/data_esc.csv', 'a') as f: # 'a' is for append mode
            #     df_es.to_csv(f, header=False)

        if  urlopen(req_bsc).read():### Need to  have error pass here 
            html = urlopen(req_bsc).read() 
            soup = BeautifulSoup(html,'html.parser')

            price = float(soup.body.find_all('span', attrs={'class': 'd-block'})[11].text.split(' ')[0].split('$')[1])
            x = soup.body.find('div', attrs={'class': 'mr-3'}).getText()
            holders = float(re.findall(r'[0-9]+',x.replace(',',''))[0])

            #holders = float(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' ')[0].split('\n')[1].replace(',',''))
            market_cap = float(soup.body.find_all('span', attrs={'class':'d-block'})[-1].getText().split('$')[1].split('\n')[0].replace(',',''))

            # For BSC, supply is ETH supply locked
            # when you bridge you lock the tokens in aspecial bridge contract on ETH
            # Active tokens = (999,999-24,2554.072249
            max_supply = float(soup.body.find_all('span', attrs={'class':'hash-tag text-truncate'})[0].getText().replace(',',''))

            df_bsc = pd.DataFrame({'Date-Time': [time.ctime()],
                        'Date': [now.date()],
                        'Year': [now.year],
                        'Month': [now.month],
                        'Day': [now.day],
                        'Hour': [now.hour],
                        'Minute': [now.minute],
                        'Second': [now.second],
                        'Time': [now.ctime().split(' ')[3]],
                        'Price': [price],
                        'Holders': [holders],
                        'Market Cap [$USD]': [market_cap],
                        'Max Supply': [max_supply]
                        })
            print(df_bsc)
            # with open('./data/data_bsc_api.csv', 'a') as f: # 'a' is for append mode
            #     df_bsc.to_csv(f, header=False)
        
        total_holders = df_bsc['Holders'].values+df_es['Holders'].values
        print(f'The current total number of holders is: {total_holders}')    
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: {}'.format(e.reason))
    
    for i in tqdm (range (30*1), desc="Waiting for new data", ascii=False, ncols=100):
        time.sleep(1)
    #time.sleep(60*2)# This will pause it every 5 minutes so as not to get kicked off server.