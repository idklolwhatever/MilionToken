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
    holder_crt = row['Holders Total']
    time_crt = row['Date-Time']

    time_old_week = time_crt - timedelta(days=7)
    time_old_week_index = df_new['Date-Time'].sub(time_old_week).abs().idxmin()
    time_old_week_nearest = df_new.iloc[time_old_week_index]['Date-Time']
    time_delta_nearest_week = time_crt - time_old_week_nearest
    holders_old_week = df_new.iloc[time_old_week_index]['Holders Total']

    time_old_day = time_crt - timedelta(days=1)
    time_old_day_index = df_new['Date-Time'].sub(time_old_day).abs().idxmin()
    time_old_day_nearest = df_new.iloc[time_old_day_index]['Date-Time']
    time_delta_nearest_day = time_crt - time_old_day_nearest
    holders_old_day = df_new.iloc[time_old_day_index]['Holders Total']
    
    time_old_hour = time_crt - timedelta(hours=1)
    time_old_hour_index = df_new['Date-Time'].sub(time_old_hour).abs().idxmin()
    time_old_hour_nearest = df_new.iloc[time_old_hour_index]['Date-Time']
    time_delta_nearest_hour = time_crt - time_old_hour_nearest
    holders_old_hour = df_new.iloc[time_old_hour_index]['Holders Total']

    time_old_minute = time_crt - timedelta(minutes=5)#Needs to be greater than 2 minutes (or whatever webscrapping interval is) otherwise it just keeps using same data and getting a zero on numerator
    time_old_minute_index = df_new['Date-Time'].sub(time_old_minute).abs().idxmin()
    time_old_minute_nearest = df_new.iloc[time_old_minute_index]['Date-Time']
    time_delta_nearest_minute = time_crt - time_old_minute_nearest
    holders_old_minute = df_new.iloc[time_old_minute_index]['Holders Total']
    
    
    holder_week_rate = (holder_crt - holders_old_week)/(time_delta_nearest_week.seconds/(60*60*24*7))
    holder_day_rate = (holder_crt - holders_old_day)/(time_delta_nearest_day.seconds/(60*60*24))
    holder_hour_rate = (holder_crt - holders_old_hour)/(time_delta_nearest_hour.seconds/(60*60))
    holder_minute_rate = (holder_crt - holders_old_minute)/(time_delta_nearest_minute.seconds/(60))
    pdb.set_trace()
    
    print(f'time_crt: {time_crt}')
    print(f'time_old: {time_old_hour}')
    print(f'time_old_hour_index: {time_old_hour_index}')
    print(f'time_old_hour_nearest: {time_old_hour_nearest}')
    print(f'time_delta_nearest_hour: {time_delta_nearest_hour}')
    print(f'holder_crt: {holder_crt}')
    print(f'holders_old_hour: {holders_old_hour}')
    print(f'holder_week_rate: {holder_week_rate}')
    print(f'holder_day_rate: {holder_day_rate}')
    print(f'holder_hour_rate: {holder_hour_rate}')
    print(f'holder_minute_rate: {holder_minute_rate}')
    print(f'\n')
    # pdb.set_trace()
    #return(holder_hour_rate,holder_minute_rate)
    #return a series instead of just the values (like in comment above) or else you will get one column with a tuple of all the values!
    return pd.Series([holder_week_rate,holder_day_rate,holder_hour_rate,holder_minute_rate],
        index=['Holders/Day','Holders/Hour', 'Holders/5-Minutes'])

df_holder_rates = df_new.apply(lambda row: holder_rate(row), axis=1).fillna(0)
df_new = pd.concat([df_new,df_holder_rates], axis=1, ignore_index=False)
#df_new['Holder/Hour'],df_new['Holder/Minute'] = df_new.apply(lambda row: holder_rate(row), axis=1)

# df_x_bound['Holder Rate'] = df_x_bound.apply(lambda row: holder_rate(row['Date-Time'], row['Holders']))
# #df_x_bound['Holder Rate'] =  df_x_bound['Holders Total'].apply(lambda row: holder_rate(row))
# pdb.set_trace()
# df_x_bound['Holder Rate'] = df_x_bound['Holders Total'].apply(lambda x: (x - df_x_bound['Holders Total'].iloc[df_x_bound['Date-Time'].sub(date).abs().idxmin()])/((x['Date-Time']-date).seconds) )     ; df_x_bound
# ##df_x_bound['Holders'].apply(lambda x: df_x_bound['Date-Time'].sub(date).abs().idxmin())

