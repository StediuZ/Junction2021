
import pandas as pd
import numpy as np
import base64
import imageio as iio
from plotting import Plotting
import plotly.graph_objects as go
import json

def fetch_data(site, timestamp)
    #site = 'site_1'
    #timestamp = "2021-08-05"

    df_events = pd.read_pickle(f'./data/{site}/{site}.pkl', compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                     .dt.tz_convert('Europe/Helsinki')
                                     .dt.tz_localize(None))

    df_events_test = df_events[df_events.timestamp.dt.date.astype(str) == timestamp].copy()

    hour = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']#list(df_events_test['timestamp'].dt.hour.astype(str))
    hours = list(df_events_test['timestamp'].dt.hour.astype(str))
    device = list(df_events_test['deviceid'])

    data = {}
    data = {timestamp_min:{}}                              
    for i in hour:
        data[timestamp_min][i]={}

    for i in hour:
        for x in range(0,len(df_events_test)):
            if(hours[x]==i):
                if(device[x] in data[timestamp_min][i]):
                    data[timestamp_min][i][device[x]]+=1
                else:
                    data[timestamp_min][i][device[x]]=1

    jsonString = json.dumps(data)
    return jsonString

