import pdb, os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib.error
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
import time

headers = {'User-Agent': 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94 safari/537.36'}
reg_url = "https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611"

while True:
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
    req = Request(url=reg_url, headers=headers)
    try:
        if  urlopen(req).read():### Need to  have error pass here 
            html = urlopen(req).read() 
            soup = BeautifulSoup(html,'html.parser')
            #print(soup.prettify())

            price = float(soup.body.find_all('span', attrs={'class': 'd-block'})[12].text.split(' ')[0].split('$')[1])
            holders = float(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' ')[0].split('\n')[1].replace(',',''))
            market_cap = float(soup.body.find_all('span', attrs={'class':'d-block'})[-1].getText().split('$')[1].split('\n')[0].replace(',',''))
            # print(f"Date: {now.date()}")
            # print(f"Time: {now.time()}")
            # print(f"Year: {now.year}")
            # print(f"Month: {now.month}")
            # print(f"Day: {now.day}")
            # print(f"Hour: {now.hour}")
            # print(f"Minute: {now.minute}")
            # print(f"Second: {now.second}")
            # print(f"The price is: {price}$")
            # print(f"The number of holders is: {holders}")
        



            # writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
            # writer.save()

            # new dataframe with same columns
            df = pd.DataFrame({'Name': ['E','F','G','H'],
                            'Age': [100,70,40,60]})
            #writer = pd.ExcelWriter('data.xlsx', engine='openpyxl')
            #writer = pd.ExcelWriter('data.xlsx')
            # try to open an existing workbook
            #writer.book = load_workbook('data.xlsx')
            # copy existing sheets
            #writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
            # read existing file
            #reader = pd.read_excel(r'data.xlsx')
            # write out the new sheet
            #df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)

            #writer.close()
            df = pd.DataFrame({'Date-Time': [time.ctime()],
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
                        'Market Cap [$USD]': [market_cap]
                        })
            print(df)
            #pdb.set_trace()
            #df.to_excel('data.xlsx', index=False)
            with open('data.csv', 'a') as f: # 'a' is for append mode
                df.to_csv(f, header=False)

        
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: {}'.format(e.reason))

    time.sleep(60*5)