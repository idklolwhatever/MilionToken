import requests, pdb
import pandas as pd
import matplotlib
#Need this backend to annoying have the updated figure windows not pop to the foreground constantly
matplotlib.use("Qt5Agg")#https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

base_id = "appzg6zehJO2LASwA"
table_name = "data_bsc"
url = "https://api.airtable.com/v0/" + base_id + "/" + table_name

params=()#Use this to select all records

api_key = "keyZj1YTbjmij4snl"
headers = {"Authorization": "Bearer " + api_key}

params = ()
airtable_records = []
run = True
while run is True:
  response = requests.get(url, params=params, headers=headers)
  airtable_response = response.json()
  airtable_records += (airtable_response['records'])
  if 'offset' in airtable_response:
     run = True
     params = (('offset', airtable_response['offset']),)
  else:
     run = False


#Now reform the JSON like structure to Pandas DataFrame
airtable_records
airtable_rows = [] 
airtable_index = []
for record in airtable_records:
    airtable_rows.append(record['fields'])
    airtable_index.append(record['id'])#uses each rows unique index
#df = pd.DataFrame(airtable_rows, index=airtable_index
df = pd.DataFrame(airtable_rows)
df['Date-Time']=pd.to_datetime(df['Date-Time'])
df = df.sort_values(by=['Date-Time'])
#pdb.set_trace()



###############################################################################
plt.ion()#Enable interactive mode!
###############################################################################
# #Create Figure and axes here with shared x-axis
fig, ((ax1, ax2) , (ax3, ax4)) = plt.subplots(2,2,sharex=True,figsize=(20, 12))
linewidth=1
alpha=0.5
    #Order matters when plotting these as the older figures go ontop the new ones
    #First is both EtherScan nd BSC
ax1.plot(df['Date-Time'], df['Holders'], linewidth=linewidth, color='black')
ax1.fill_between(df['Date-Time'], df['Holders'],label = "BSC and EtherScan", color='red', alpha=alpha)



fig.autofmt_xdate() # In this case, it just rotates the tick labels
ax1.set_facecolor('white')
plt.tight_layout()


fig.canvas.draw_idle()#draw only if idle; defaults to draw but backends can overrride
fig.canvas.start_event_loop(timeout=10)#Start an event loop. This is used to start a blocking event loop so that interactive functions, such as ginput and waitforbuttonpress, can wait for events. This should not be confused with the main GUI event loop, which is always running and has nothing to do with this.
fig.canvas.stop_event_loop()
ax1.clear()
ax2.clear()
ax3.clear()
ax4.clear()
plt.cla()