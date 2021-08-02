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
pd.set_option('display.expand_frame_repr',False)
pd.set_option('display.max_columns',7,'max_rows',40,'display.max.colwidth',15)

from selenium import webdriver
driver = webdriver.Chrome(executable_path='./chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("headless")# does not seem to be working currently for whatever reasons

headers = {'User-Agent': 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94 safari/537.36'}
esc_url = "https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611#balances"
bsc_url = "https://bscscan.com/token/0xbf05279f9bf1ce69bbfed670813b7e431142afa4"


while True:
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    req_esc = Request(url=esc_url, headers=headers)
    req_bsc = Request(url=bsc_url, headers=headers)
    try:
        if  urlopen(req_esc).read():### Need to  have error pass here 
            driver.get(esc_url)
            html = urlopen(req_esc).read() 
            soup = BeautifulSoup(html,'html.parser')
            pdb.set_trace()

            price = float(soup.body.find_all('span', attrs={'class': 'd-block'})[12].text.split(' ')[0].split('$')[1])
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


    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: {}'.format(e.reason))
    
    for i in tqdm (range (30*1), desc="Waiting for new data", ascii=False, ncols=100):
        time.sleep(1)