#https://towardsdatascience.com/airtable-python-made-possible-ii-uploading-data-into-airtable-from-python-using-airtables-api-3075009abf98
import requests, pdb
import pandas as pd
import matplotlib
#Need this backend to annoying have the updated figure windows not pop to the foreground constantly
matplotlib.use("Qt5Agg")#https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json





import os
from pprint import pprint
from airtable import Airtable

#https://pythonhowtoprogram.com/how-to-update-the-airtable-using-python3/
base_key = 'appzg6zehJO2LASwA' # Insert the Base ID of your working base
table_name = 'data_bsc' #Insert the name of the table in your working base
api_key = 'key5wRuTwYsRNvUyZ' #Insert your API Key
airtable = Airtable(base_key, table_name, api_key)
airtable_new = Airtable(base_key, 'idklol', api_key)
print(airtable)

pages = airtable.get_iter(maxRecords=1)
for page in pages:
    for record in page:
        pprint(record) #pprints short for pretty print, prints the data in a structured format

#Sorting the records
records = airtable.get_all(maxRecords=3000000, sort=[("Date-Time", 'desc')])
#pprint(records)

#Now reform the JSON like structure to Pandas DataFrame
airtable_rows = [] 
airtable_index = []
for record in records:
    airtable_rows.append(record['fields'])
    airtable_index.append(record['id'])#uses each rows unique index
#df = pd.DataFrame(airtable_rows, index=airtable_index
df = pd.DataFrame(airtable_rows)
#df['Date-Time']=pd.to_datetime(df['Date-Time'])
df = df.sort_values(by=['Date-Time'])


#airtable_new.insert(records[0]['fields'])
#Finally, this will upload all of the selected airtable rows to the proposed new table on airtable

df2 = pd.read_csv('Test.csv')
#df2['Date-Time']=pd.to_datetime(df2['Date-Time'])
df2 = df2.sort_values(by=['Date-Time'])
df2 = df2.fillna(0)
#df2 = df2.head(1)
pdb.set_trace()
#airtable_new.batch_insert(airtable_rows)
#Or just insert the who damn dataframe of interst
airtable_new.batch_insert(df2.to_dict('records'))