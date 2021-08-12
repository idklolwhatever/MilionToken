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

headers = {'User-Agent': 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94 safari/537.36'}
reg_url = "https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611"
bsc_url = "https://bscscan.com/token/0xbf05279f9bf1ce69bbfed670813b7e431142afa4"
while True:
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
    req = Request(url=reg_url, headers=headers)
    req_bsc = Request(url=bsc_url, headers=headers)
    try:
        if  urlopen(req).read():### Need to  have error pass here 
            html = urlopen(req).read() 
            soup = BeautifulSoup(html,'html.parser')
            #print(soup.prettify())
            #pdb.set_trace()
            price = float(soup.body.find_all('span', attrs={'class': 'd-block'})[12].text.split(' ')[0].split('$')[1])
            #print(price)
            #print('TEST1 '*10)
            #print(soup.body.find('div', attrs={'class': 'mr-3'}).prettify()    )
            #print('NEXT \n')
            #print(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' '))
            #print('\n')
            #print(float(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' ')[0].split('\n')[1].replace(',','')))
            ###############################################################################
            # WARNING: There was a weird issue where occasionally when trying to find holders, the returned text
            # would for some reason randomly not have  space, thus causing a crash and needing another way
            # to ignore spliting by spaces and only look at numbers
            ###########################################################################
            x = soup.body.find('div', attrs={'class': 'mr-3'}).getText()
            holders = float(re.findall(r'[0-9]+',x.replace(',',''))[0])
            #holders = float(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' ')[0].split('\n')[1].replace(',',''))
            #print(holders)
            market_cap = float(soup.body.find_all('span', attrs={'class':'d-block'})[-1].getText().split('$')[1].split('\n')[0].replace(',',''))
            #print(market_cap)
            max_supply = float(soup.body.find_all('span', attrs={'class':'hash-tag text-truncate'})[0].getText().replace(',',''))
            
            df_es = pd.DataFrame({'Date-Time': [time.ctime()],
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
            print(df_es)

            with open('./data/data_esc.csv', 'a') as f: # 'a' is for append mode
                df_es.to_csv(f, header=False)

        if  urlopen(req_bsc).read():### Need to  have error pass here 
            html = urlopen(req_bsc).read() 
            soup = BeautifulSoup(html,'html.parser')
            #
            #price = float(soup.body.find_all('span', attrs={'class': 'd-block'})[11].text.split(' ')[0].split('$')[1].replace('\n','').replace(',',''))
            #print('TEST2 '*10)
            #print(soup.body.find('div', attrs={'class': 'mr-3'}).prettify()    )
            #print('NEXT2\n')
            #print(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' '))
            #print('\n')
            #print(float(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' ')[0].split('\n')[1].replace(',','')))
            x = soup.body.find('div', attrs={'class': 'mr-3'}).getText()
            holders = float(re.findall(r'[0-9]+',x.replace(',',''))[0])

            #holders = float(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' ')[0].split('\n')[1].replace(',',''))
            #pdb.set_trace()
            #print(float(soup.body.find_all('span', attrs={'class':'d-block'})[-1].getText()))
            #market_cap = float(soup.body.find_all('span', attrs={'class':'d-block'})[-1].getText().split('$')[1].split('\n')[0].replace(',',''))
            market_cap = float(soup.body.find_all('span', attrs={'class':'d-block'})[-1].getText().replace('\n','').replace(',','').replace('$',''))
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
            with open('./data/data_bsc.csv', 'a') as f: # 'a' is for append mode
                df_bsc.to_csv(f, header=False)
        
        total_holders = df_bsc['Holders'].values+df_es['Holders'].values
        print(f'The current total number of holders is: {total_holders}')    
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: {}'.format(e.reason))
    
    for i in tqdm (range (30*1), desc="Waiting for new data", ascii=False, ncols=100):
        time.sleep(1)
    #time.sleep(60*2)# This will pause it every 5 minutes so as not to get kicked off server.