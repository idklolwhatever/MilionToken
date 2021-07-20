import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pdb
#%matplotlib

df = pd.read_csv('data.csv')
df['Date-Time'] = pd.to_datetime(df['Date-Time'])
fig, (ax1, ax2) = plt.subplots(nrows=2,sharex=True,figsize=(10, 12))

ax1.plot(df['Date-Time'], df['Holders'])
ax2.plot(df['Date-Time'], df['Market Cap'])

ax1.set(title='Etherscan and BSC Webscrape (MM)',
    xlabel='Date-Time',
    ylabel='Number of Holders')

ax2.set(title='Etherscan and BSC Webscrape (MM)',
    xlabel='Date-Time',
    ylabel='Market Cap [$]')
    
ax1.grid(color='black', linestyle='-', linewidth=1, which='major')
ax2.grid(color='black', linestyle='-', linewidth=1, which='major')

ax1.xaxis.set_major_formatter(mdates.DateFormatter("%D %H:%M:%S"))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%D %H:%M:%S"))

###############################################################################
df_bsc = pd.read_csv('data_bsc.csv')

df_bsc['Date-Time'] = pd.to_datetime(df_bsc['Date-Time'])
# Graph just the BSC Data
ax1.plot(df_bsc['Date-Time'], df_bsc['Holders'], label = "BSC")
#Graph the BSC and EtherScan Data additatively

# Need to combine Dfs based on closest timestamps
df_new = df.merge(df_bsc, how='inner', on=['Month','Day','Hour','Minute'], suffixes=("_ES","_BSC"))

#Create a new column for the new total column for holders and market cap
df_new['Holders Total']=df_new['Holders_ES']+df_new['Holders_BSC']
df_new['Market Cap Total']=df_new['Market Cap_ES']+df_new['Market Cap_BSC']

ax1.plot(df_new['Date-Time_BSC'], df_new['Holders Total'], label = "BSC and Etherscan")

ax1.set_ylim(bottom=12300)    
ax1.legend(loc='lower right')

#Graph only the BSC market cap data

ax2.plot(df_bsc['Date-Time'], df_bsc['Market Cap'], label = "BSC")
#Graph the BSC and EtherScape market cap data   

ax2.plot(df_new['Date-Time_BSC'], df_new['Market Cap Total'], label = "BSC and Etherscan")

ax2.set_ylim(bottom=35000000)    
ax2.legend(loc='lower right')

fig.autofmt_xdate() # In this case, it just rotates the tick labels
plt.show()