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


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))


# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
 
# Options
options = "hmo:"
 
# Long options
long_options = ["Help", "My_file", "Output ="]
 
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--Help"):
            print ("Displaying Help\n")
            print ("Simply enter a start and stop date-time in quotations!")
            print("For examples in the terminal: python3.9 graph.py -h \'2021-07-21 00:00:00\' \'2022-07-21 00:00:00\' \n\n")
            quit() 
        elif currentArgument in ("-m", "--My_file"):
            print ("Displaying file_name:", sys.argv[0])
             
        elif currentArgument in ("-o", "--Output"):
            print (("Enabling special output mode (% s)") % (currentValue))
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
###############################################################################
plt.ion()
#Create Figure and axes here with shared x-axis
fig, (ax1, ax2) = plt.subplots(nrows=2,sharex=True,figsize=(20, 12))

while True:
    #Read in seperate files and change to a date format
    df = pd.read_csv('data.csv')
    df['Date-Time'] = pd.to_datetime(df['Date-Time'])

    df_bsc = pd.read_csv('data_bsc.csv')
    df_bsc['Date-Time'] = pd.to_datetime(df_bsc['Date-Time'])

    # Need to combine Dfs based on closest timestamps
    df_new = df.merge(df_bsc, how='inner', on=['Month','Day','Hour','Minute'], suffixes=("_ES","_BSC"))
    #Create a new column for the new total column for holders and market cap
    df_new['Holders Total']=df_new['Holders_ES']+df_new['Holders_BSC']
    df_new['Market Cap Total']=df_new['Market Cap_ES']+df_new['Market Cap_BSC']

    x_start = df[df['Date-Time'] >= sys.argv[1]]['Date-Time'].min() #'2021-07-16 09:49:37']
    x_stop  = df[df['Date-Time'] <= sys.argv[2]]['Date-Time'].max()
    time_delta = (x_stop - x_start)

    linewidth=1
    alpha=0.5

    #First is just BSC
    ax1.plot(df['Date-Time'], df['Holders'], linewidth=linewidth, color='black')#plt.fill_between(ages, total_population)
    ax1.fill_between(df['Date-Time'], df['Holders'],label="EtherScan", color='blue', alpha=alpha)

    #Second is just BSC
    ax1.plot(df_bsc['Date-Time'], df_bsc['Holders'], linewidth=linewidth, color='black')# Graph just the BSC Data
    ax1.fill_between(df_bsc['Date-Time'], df_bsc['Holders'],label="BSC", color='red', alpha=alpha)

    #Third is both EtherScan nd BSC
    ax1.plot(df_new['Date-Time_BSC'], df_new['Holders Total'], linewidth=linewidth, color='black')
    ax1.fill_between(df_new['Date-Time_BSC'], df_new['Holders Total'],label = "BSC and EtherScan", color='green', alpha=0.7)

    #Formating
    ax1.set(title=f'Etherscan and BSC Webscrape MM Holders \n Start: {x_start} Stop: {x_stop}', xlabel='Date-Time', ylabel='Number of Holders')
    ax1.grid(color='black', linestyle='-', linewidth=linewidth, which='major', alpha=0.5)
    ax1.grid(color='grey', linestyle='-', linewidth=linewidth, which='minor', alpha=0.5)

    #Annotations
    #
    max_hold = df[df['Holders'] == df['Holders'].max()].iloc[0]['Holders']
    max_hold_date = df[df['Holders'] == df['Holders'].max()].head(1)['Date-Time'].values #df[df['Holders'] == df['Holders'].max()].iloc[0]['Date-Time']
    ax1.annotate(f'EtherScan Holders ATH {max_hold}', xy=(max_hold_date,max_hold), xytext=(-50,-25),
                textcoords='offset pixels', arrowprops=dict(arrowstyle='-|>'))

    max_hold = df_new[df_new['Holders Total'] == df_new['Holders Total'].max()].iloc[0]['Holders Total']
    max_hold_date = df_new[df_new['Holders Total'] == df_new['Holders Total'].max()].head(1)['Date-Time_BSC'].values #df[df['Holders'] == df['Holders'].max()].iloc[0]['Date-Time']
    ax1.annotate(f'BSC & EtherScan Holders ATH {max_hold}', xy=(max_hold_date,max_hold), xytext=(-50,-25),
                textcoords='offset pixels', arrowprops=dict(arrowstyle='-|>'))

    #Set date axis ticks for major and minor
    #ax2.xaxis.set_minor_locator(mdates.AutoDateLocator())
    #WARNING since the axes are shared, this formatting should only need to be applied once
    # x_minor_lct = HourLocator(byhour = range(0,24+1,6))
    # ax1.xaxis.set_minor_locator(x_minor_lct)
    # ax1.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))

    # ax1.xaxis.set_major_locator(mdates.DayLocator())
    # ax1.xaxis.set_major_formatter(mdates.DateFormatter("\n%D"))

    ax1.set_ylim(bottom=14800, top=15100)    
    ax1.legend(loc='lower right')

    ###############################################################################
    ###############################################################################
    # First is just EtherScan
    ax2.plot(df['Date-Time'], df['Market Cap'], linewidth=linewidth, color='black')
    ax2.fill_between(df['Date-Time'], df['Market Cap'], label = "EtherScan",color='blue', alpha=alpha)

    #Second is just BSC
    ax2.plot(df_bsc['Date-Time'], df_bsc['Market Cap'], linewidth=linewidth, color='black')
    ax2.fill_between(df_bsc['Date-Time'], df_bsc['Market Cap'], label = "BSC",color='red', alpha=alpha)  

    #Third is both EtherScan and BSC
    ax2.plot(df_new['Date-Time_BSC'], df_new['Market Cap Total'], linewidth=linewidth, color='black')#Graph the BSC and EtherScape market cap dat
    ax2.fill_between(df_new['Date-Time_BSC'], df_new['Market Cap Total'], label = "BSC and EtherScan",color='green', alpha=alpha) 

    #Formating
    ax2.set(title=f'Etherscan and BSC Webscrape MM Market Cap \n Start: {x_start} Stop: {x_stop}', xlabel='Date-Time', ylabel='Market Cap in Millions of Dollars')
    ax2.grid(color='black', linestyle='-', linewidth=1, which='major')
    ax2.grid(color='grey', linestyle='-', linewidth=linewidth, which='minor', alpha=0.25)

    #Annotations
    max_mc = df[df['Market Cap'] == df['Market Cap'].max()].iloc[0]['Market Cap']
    max_mc_date = df[df['Market Cap'] == df['Market Cap'].max()].head(1)['Date-Time'].values #df[df['Holders'] == df['Holders'].max()].iloc[0]['Date-Time']
    ax2.annotate(f'Market Cap ATH {max_mc}', xy=(max_mc_date,max_mc), xytext=(10,-100),
                textcoords='offset pixels', arrowprops=dict(arrowstyle='-|>'))




    #Set date axis ticks for major and minor
    #ax2.xaxis.set_minor_locator(mdates.AutoDateLocator())
    #WARNING since the axes are shared, this formatting should only need to be applied once

    #pdb.set_trace()
    if time_delta.seconds < 1*60*60:
        print(f'The number of minutes are: {time_delta.seconds/60}')
        x_minor_lct = MinuteLocator(byminute = range(0,60+1,1))
        ax2.xaxis.set_minor_locator(x_minor_lct)
        ax2.xaxis.set_minor_formatter(mdates.DateFormatter("%M"))
        ax2.xaxis.set_major_locator(mdates.DayLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("\n%H")) 
    elif time_delta.days < 2:#This is done to better display ticks for the smaller date-time ranges
        x_minor_lct = HourLocator(byhour = range(0,24+1,1))
        ax2.xaxis.set_minor_locator(x_minor_lct)
        ax2.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))
        ax2.xaxis.set_major_locator(mdates.DayLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("\n%D"))
    else:
        x_minor_lct = HourLocator(byhour = range(0,24+1,4))
        ax2.xaxis.set_minor_locator(x_minor_lct)
        ax2.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))
        ax2.xaxis.set_major_locator(mdates.DayLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("\n%D"))

    scale_y = 1e6
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
    #ax2.set_xlim(left=df['Date-Time'].values[0], right=df['Date-Time'].values[-1]) 

    #pdb.set_trace()
    ax2.set_xlim(left=x_start, right=x_stop)
    ax2.set_ylim(bottom=35000000)    
    ax2.legend(loc='lower right')


    sns.set()

    fig.autofmt_xdate() # In this case, it just rotates the tick labels
    ax1.set_facecolor('white')
    ax2.set_facecolor('white')

    #plt.savefig(f'./graphs/MM_{time.ctime()}.png')
    
    print('Waiting to Update Graph')
    #https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7
    fig.canvas.draw_idle()
    fig.canvas.start_event_loop(2*60)
    ax1.clear()
    ax2.clear()
    plt.cla()
    #time.sleep(2*60)
    #plt.draw()
    #plt.show()
    #time.sleep(10)
    #plt.pause(5)
    
    #plt.clf()
