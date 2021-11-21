import pandas as pd
import numpy as np
import base64
import imageio as iio
from plotting import Plotting
import plotly.graph_objects as go
import json
from datetime import datetime
import math
def create_real_vectors(site,timestamp):
    #site = 'site_1'
    #timestamp = "2021-08-05"

    df_events = pd.read_pickle(f'./data/{site}/{site}.pkl', compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                    .dt.tz_convert('Europe/Helsinki')
                                    .dt.tz_localize(None))


    df_events_test = df_events[df_events.timestamp.dt.date.astype(str) == timestamp].copy()

    df_devices = pd.read_json(f'./data/{site}/{site}.json')



    events_in_order = df_events_test.sort_values(by='timestamp').copy()

    min_time = 0.4
    max_time = 4
    min_d = 2
    max_d = 200
    arrow_multiplier = 1
    context_length = 40

    event_deviceid = list(events_in_order['deviceid'])
    x_list = list(df_devices['x'])
    y_list = list(df_devices['y'])
    coo = [(x_list[i], y_list[i]) for i in range(0, len(x_list))]
    coordinates = []
    for dev_id in event_deviceid:
        coordinates.append(coo[dev_id]) 
    events_in_order['Coordinates'] = coordinates

    def create_vector(time_diff, e1_coordinate, x_delta, y_delta,hour):
        x = e1_coordinate[0]
        y = e1_coordinate[1]
        length = arrow_multiplier*time_diff/max_time
        degrees = math.degrees(math.atan2(x_delta, y_delta))
        return (hour,[x,y,length, degrees])
        
    context = []

    cord = list(events_in_order['Coordinates'])
    time = list(events_in_order['timestamp'])
    better_time = list(events_in_order['timestamp'].dt.hour.astype(str))
    index = 0

    vectors = []

    for index in range(0,len(cord)-1):
        diff = time[index + 1] - time[index]
        sec_diff = (diff).total_seconds()
        x_delta = abs(cord[index][0] - cord[index + 1][0])
        y_delta = abs(cord[index][1] - cord[index + 1][1])
        dist = math.sqrt(pow(x_delta,2) + pow(y_delta,2))
        e1 = [time[index], cord[index]]
        e2 = [time[index+1], cord[index+1]]
        
        if sec_diff > max_time or dist < min_d:
            context.append(e2)
            
        elif (dist < max_d and dist > min_d) and sec_diff < min_time:
            clock = time[index] + diff/2
            x_m = cord[index][0] + x_delta/2
            y_m = cord[index][1] + y_delta/2
            em = [clock, [x_m,y_m]]
        elif (dist <= max_d and dist >= min_d) and (sec_diff <= max_time and sec_diff >= min_time):
            vectors.append(create_vector(sec_diff, e1[1], x_delta, y_delta, better_time[index]))
            context.append(e1)
            context.append(e2)
        else: 
            context.append(e1)
            context.append(e2)
            
    vectors_time = {}
    hours = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    for hour in hours:
            vectors_time[hour]={}
    for hourr in hours:
        temp_vectors = []
        for vector in vectors:
            if(vector[0] == hourr):
                temp_vectors.append(vector[1])
        vectors_time[hourr] = temp_vectors
    return json.dump(vectors_time)