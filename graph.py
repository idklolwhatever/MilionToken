import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#%matplotlib

df = pd.read_csv('data.csv')
df['Date-Time'] = pd.to_datetime(df['Date-Time'])
fig, ax = plt.subplots(figsize=(8, 6))

#df.plot(x='Date-Time',y=['Holders'])
ax.plot(df['Date-Time'], df['Holders'])
#plt.ylim(0,1000000)
ax.set(title='Ethercan Webscrape (MM)',
    xlabel='Date-Time',
    ylabel='Number of Holders')
    
#plt.title('Ethercan Webscrape (MM)')
#plt.xlabel('Date-Time')
#plt.ylabel('Number of Holders')
ax.grid(color='black', linestyle='-', linewidth=1, which='major')
#plt.grid(color='black', linestyle='--', linewidth=1, which='minor')

ax.xaxis.set_major_formatter(mdates.DateFormatter("%D %H:%M:%S"))
fig.autofmt_xdate() # In this case, it just rotates the tick labels
plt.show()