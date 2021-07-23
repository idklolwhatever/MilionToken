#https://plotly.com/python/time-series/
from plotly.subplots import make_subplots
import plotly.express as px
import chart_studio.plotly as py
import plotly.graph_objects as go
import pandas as pd
import numpy as np

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
df = pd.read_csv('data.csv')
df['Date-Time'] = pd.to_datetime(df['Date-Time'])

def zoom(layout, x_range):
  print('yaxis updated')
  in_view = df.loc[figure.layout.xaxis.range[0]:figure.layout.xaxis.range[1]]
  figure.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

fig = make_subplots(          
            rows=1, cols=2, 
            subplot_titles=('MM Holders', 'MM Market Cap'),
            vertical_spacing=0.1,
            shared_xaxes=True   
)


def build_plot():
    fig.add_trace(go.Scatter(x=df['Date-Time'], y=df['Holders'], name="Holders",
                            line_color='deepskyblue'), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Date-Time'], y=df['Market Cap'], name="Market Cap",
                            line_color='dimgray'), row=1, col=2)

    #fig.add_trace(go.Bar(y=np.random.randint(3,9, 11)), row=2, col=1)
    fig.update_layout(title_text='Etherscan MM Webscrape Data',
        yaxis=dict(
            autorange = True,
            fixedrange= False
        ),
        xaxis=dict(
            autorange = True,
            fixedrange= False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1h",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3h",
                        step="hour",
                        stepmode="backward"),
                    dict(count=1,
                        label="1d",
                        step="day",
                        stepmode="backward"),
                    dict(count=2,
                        label="2d",
                        step="day",
                        stepmode="backward"),
                    dict(count=7,
                        label="1w",
                        step="day",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            # rangeslider=dict(
            #     visible=False,
            # ),
            type="date"
        ))


    #fig=go.FigureWidget(data=data, layout=layout)
    #fig.layout.on_change(zoom, 'xaxis.range')
    #fig.update_xaxes(rangeslider_thickness = 0.02)
    fig.show()

build_plot()