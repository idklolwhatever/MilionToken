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

#API Github
#https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API#get-address-info

#esc_key = 'DH49RWSITZZQFH5F8KBY542GWEGQVPNBAK'
esc_key = 'freekey'

#https://api.ethplorer.io/getAddressTransactions/0x000000000000000000000000000000000000dead?apiKey=freekey&limit=10
mm_address = '0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611'


addresses = pd.read_csv('./data/Holders/8_1_2021_export-tokenholders-for-contract-0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611.csv')

for address in addresses['HolderAddress'].unique():
    pdb.set_trace()
    url = f"https://api.ethplorer.io/getAddressInfo/{mm_address}?apiKey={esc_key}&limit=10&?a=0x5922b0bbae5182f2b70609f5dfd08f7da561f5a4"

    
    req = Request(url=url, headers=headers)
    html = urlopen(req).read() 
    soup = BeautifulSoup(html,'html.parser')
    data = json.loads(soup.get_text())
    print(json.dumps(data,indent=4))
    pdb.set_trace()

million_data = data['tokenInfo']
print('\nMillion Token Data: \n'*1)
print(json.dumps(million_data,indent=4))