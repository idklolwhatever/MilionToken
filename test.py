import pandas as pd
import matplotlib
#Need this backend to annoying have the updated figure windows not pop to the foreground constantly
matplotlib.use("Qt5Agg")#https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7
#matplotlib.use('MACOSX')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DayLocator,DayLocator, HourLocator,MinuteLocator,SecondLocator, DateFormatter, drange, date2num
import seaborn as sns
import pdb
import matplotlib.ticker as ticker
import time, sys, getopt
from datetime import timedelta
from tqdm import tqdm


#Read in seperate files and change to a date format
df = pd.read_csv('data.csv')
df['Date-Time'] = pd.to_datetime(df['Date-Time'])

df_bsc = pd.read_csv('data_bsc.csv')
df_bsc['Date-Time'] = pd.to_datetime(df_bsc['Date-Time'])

# Need to combine Dfs based on closest timestamps down to the closest reasonable time (minutes)
idk = df.merge(df_bsc, how='inner', on=['Month','Day','Hour','Minute'], suffixes=("","_BSC"))
#Now need to create another dataframe that only contains data up until BSC starts recording
lol = df[df['Date-Time'] <= df_bsc['Date-Time'].min()]
#Now need to concat one on top of the other and then sort by Date-Time and make sure to fill in NAN and NAT's with zeros for later mathmatics
df_new = pd.concat([idk,lol]).sort_values(by=['Date-Time']).fillna(0)


df_new['Holders Total']=df_new['Holders']+df_new['Holders_BSC']
df_new['Market Cap Total']=df_new['Market Cap']+df_new['Market Cap_BSC']
df_new['Price Total']=df_new['Price']+df_new['Price_BSC']

###############################################################################################
# AXIS 4: Holder Rates
###############################################################################################
# #pdb.set_trace()
# date = pd.to_datetime('2021-07-16 09:44:36')
# df_x_bound['Date-Time'].sub(date).abs().idxmin()#Returns index of timestamp closest to date
#The following will create a new column where 
def holder_rate(row):
    time_crt = row['Date-Time']
    time_old = time_crt - timedelta(hours=1)
    time_old_index = df_new['Date-Time'].sub(time_old).idxmin()
    time_old_nearest = df_new.iloc[time_old_index]['Date-Time']
    time_delta = time_crt - time_old_nearest
    
    holder_crt = row['Holders Total']
    holders_old = df_new.iloc[time_old_index]['Holders Total']
    
    holder_rate = (holder_crt - holders_old)/(time_delta.seconds/(60*60))
    #pdb.set_trace()
    print(f'time_crt: {time_crt}')
    print(f'time_old: {time_old}')
    print(f'time_old_index: {time_old_index}')
    print(f'time_old_nearest: {time_old_nearest}')
    print(f'time_delta: {time_delta}')
    print(f'holder_crt: {holder_crt}')
    print(f'holders_old: {holders_old}')
    print(f'holder_rate: {holder_rate}')
    print(f'\n')
    return(holder_rate)

df_new['Holder/Hour'] = df_new.apply(lambda row: holder_rate(row), axis=1)
# df_x_bound['Holder Rate'] = df_x_bound.apply(lambda row: holder_rate(row['Date-Time'], row['Holders']))
# #df_x_bound['Holder Rate'] =  df_x_bound['Holders Total'].apply(lambda row: holder_rate(row))
# pdb.set_trace()
# df_x_bound['Holder Rate'] = df_x_bound['Holders Total'].apply(lambda x: (x - df_x_bound['Holders Total'].iloc[df_x_bound['Date-Time'].sub(date).abs().idxmin()])/((x['Date-Time']-date).seconds) )     ; df_x_bound
# ##df_x_bound['Holders'].apply(lambda x: df_x_bound['Date-Time'].sub(date).abs().idxmin())

