#load_ext autoreload
#autoreload 2
import pandas as pd
import numpy as np
import base64
import imageio as iio
from plotting import Plotting
import plotly.graph_objects as go
import json
from datetime import datetime
import math

site = 'site_1'
timestamp_min = "2021-08-05"
timestamp_max = "2021-08-06"
time_interval = "2h"#"5min"#"1D" 

df_events = pd.read_pickle(f'./data/{site}/{site}.pkl', compression='gzip')
df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                 .dt.tz_convert('Europe/Helsinki')
                                 .dt.tz_localize(None))
#idx  = df_events.loc[(df_events['deviceid'] == 1)].index 
#df_events.loc[idx][['10']]
#idx = [22, 32, 33, 188, 189, 456, 457, 482, 483, 576, 577]
#df_events.loc[idx]

df_events_test_1 = df_events[df_events.timestamp.dt.date.astype(str) >= timestamp_min].copy()
df_events_test_2 = df_events[df_events.timestamp.dt.date.astype(str) <= timestamp_max].copy()
df_events_test = pd.merge(df_events_test_1,df_events_test_2)

#We need device locations
df_devices = pd.read_json(f'./data/{site}/{site}.json')

#df_events_test.timestamp = df_events_test.timestamp.dt.floor(time_interval)

#Printing all events sorted by timestamp
print(df_events_test.sort_values(by='timestamp'))

#df_events_day.loc[:, 'timestamp'] = df_events_day['timestamp'].dt.floor('1D')

#df_events_test = df_events_test.groupby(['timestamp','deviceid']).sum()
#triggered = []
#for i in range (0,len(df_events_test['timestamp'])):
#    triggered.append(1)

#df_events_magic = pd.DataFrame({'timestamp':df_events_test['timestamp'],'deviceid':df_events_test['deviceid'],'triggered':triggered})
#df_events_magic

#df_events_magic.timestamp = df_events_magic.timestamp.dt.floor(time_interval)
#df_events_magic = df_events_magic.groupby(['timestamp','deviceid']).sum()
#df_events_magic.to_json('data.json')

#df_events_test['triggered'] = triggered
#df_events_test.timestamp = df_events_test.timestamp.dt.floor(time_interval)
#df_events_test = df_events_test.groupby(['timestamp','deviceid']).sum()
#df_events_test.to_json('data.json')

#day = []#list(df_events_test['timestamp'].dt.date.astype(str))
#hour = []#list(df_events_test['timestamp'].dt.hour.astype(str))
#device = []#list(df_events_test['deviceid'])
#triggered = []#list(df_events_test['triggered'])
#data = ["day":"" ,"time":[{"time":"","devices": [{"device_id": ,"num_of_events":""}]}]]
#for pv in range(0,len(df_events_test)):
#    new = df_events_test['timestamp'][pv]
#    if(df_events_test['timestamp'].dt.date.astype(str)[pv] not in day):
#        day.append(df_events_test['timestamp'].dt.date.astype(str)[pv])
        
#print(day)
    
    
    
    
#    data.append( {
#        "day":day[i],
 #       "time":[
  #              {
   #                 "hour":date[i],
    #                "devices": [
     #                   {
      #                      "device_id":device[i],
       #                     "num_of_events":triggered[i]
        #                }
         #           ]
          #      }
        #]
    #})
#jsonString = json.dumps(data)
#jsonFile = open("data.json", "w")
#jsonFile.write(jsonString)
#jsonFile.close()
#jsonString
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
#We have panda dataframe with Coordinates

#Create function for vector creaton
def create_vector(time_diff, e1_coordinate, x_delta, y_delta):
    x = e1_coordinate[0]
    y = e1_coordinate[1]
    length = arrow_multiplier
    degrees = math.degrees(math.atan2(x_delta, y_delta))
    return [x,y,length, degrees]
    
context = []

#some_events = events_in_order.head(10)

cord = list(events_in_order['Coordinates'])
time = list(events_in_order['timestamp'])
index = 0

print(create_vector(3,[1000,2000],20,20))

vectors = []
for index in range(0,len(cord)-1):
#while index < len(cord) - 1:
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
        vectors.append(create_vector(sec_diff, e1[1], x_delta, y_delta))
        context.append(e1)
        context.append(e2)
    else: 
        context.append(e1)
        context.append(e2)
        
    #print(context)
    #index+=1
max_dist = 4000
height = 2600
width = 5450
scale = 100

grid = []

for x in range(0, int(width/scale), 1):
    width_mult = width/int(width/scale)
    
    for y in range(0, int(height/scale), 1):
        height_mult = height/int(height/scale)
        
        grid.append([int(width_mult*x), int(height_mult*y),0,0])
        grid.append([int(width_mult*x), int(height_mult*y),0,90])
        grid.append([int(width_mult*x), int(height_mult*y),0,180])
        grid.append([int(width_mult*x), int(height_mult*y),0,270])

def vector_to_xy(vector):
    rad = math.radians(vector[3])
    x = math.sin(rad)
    y = math.cos(rad)
    return (x, y)
  
def dist(vector, gridpoint):
    x_delta= abs(vector[0] - gridpoint[0])
    y_delta= abs(vector[1] - gridpoint[1])
    distance = math.sqrt(pow(x_delta,2) + pow(y_delta,2))
    return distance
count = 0
for gridpoint_index in range(0, len(grid), 4):
    for vector in vectors:
        distance = dist(vector, grid[gridpoint_index])
        if distance < max_dist:
            (x, y) = vector_to_xy(vector)
            count += x+y
            if x > 0:
                grid[gridpoint_index][2] = int(grid[gridpoint_index][2]+ (max_dist - distance)*x)
                #print(grid[gridpoint_index][2]+ (max_dist - distance)*x)
                #print(grid[gridpoint_index])
            else:
                grid[gridpoint_index +2][2] = int(grid[gridpoint_index +2][2] + (max_dist - distance)*x)
            if y > 0:
                grid[gridpoint_index +1][2] = int(grid[gridpoint_index +1][2] + (max_dist - distance)*y)
            else:
                grid[gridpoint_index +3][2] = int(grid[gridpoint_index +3][2] + (max_dist - distance)*y)
grid
