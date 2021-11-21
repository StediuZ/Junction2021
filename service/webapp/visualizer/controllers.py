from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request, send_from_directory
from .models import TimeNow
from PIL import Image
from datetime import datetime
import base64, json, os, random, math
import pandas as pd
import numpy as np


visualizer_blueprint = Blueprint(
    'visualizer',
    __name__,
    template_folder='../templates/visualizer',
    url_prefix="/visualizer",
    static_url_path='',
    static_folder='../static',
)


@visualizer_blueprint.route('/')
def home():
    return render_template('home.html')

# Backend calendar form route (not uset but works on localhost:5000)
@visualizer_blueprint.route('/', methods=['GET', 'POST'])
def submitdate():
    dateSelected = request.form['date']
    return dateSelected

# Dummy vector data for vector testing in React
@visualizer_blueprint.route('/vectors')
def testvectors():
    X_max = 40
    Y_max = 20
    interval = 1
    vectorsTimes = {}
    hours = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    for hour in hours:
        vectors=[]
        for x in range(0,X_max,interval):
            for y in range(0,Y_max,interval):
                vectors.append([x,y,random.randrange(0,200,1),random.randrange(0,359,1)])
        vectorsTimes[hour] = vectors

    jsonString = json.dumps(vectorsTimes)
    return jsonString

# Fetching json format vector data from site_x.pkl
@visualizer_blueprint.route('/vector/<dateSelected>/<siteSelected>')
def vectordate(dateSelected, siteSelected):
    timestamp_min = "2021-08-05"
    timestamp_max = "2021-08-06"

    site = siteSelected
    #timestamp = dateSelected
    sitePath = 'webapp/static/site_' + site + '.pkl'
    devicePath = 'webapp/static/site_' + site + '.json'


    df_events = pd.read_pickle(sitePath, compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                     .dt.tz_convert('Europe/Helsinki')
                                     .dt.tz_localize(None))


    df_events_test_1 = df_events[df_events.timestamp.dt.date.astype(str) >= timestamp_min].copy()
    df_events_test_2 = df_events[df_events.timestamp.dt.date.astype(str) <= timestamp_max].copy()
    df_events_test = pd.merge(df_events_test_1,df_events_test_2)

    #We need device locations
    df_devices = pd.read_json(devicePath)


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


    cord = list(events_in_order['Coordinates'])
    time = list(events_in_order['timestamp'])
    index = 0

    print(create_vector(3,[1000,2000],20,20))

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
            vectors.append(create_vector(sec_diff, e1[1], x_delta, y_delta))
            context.append(e1)
            context.append(e2)
        else:
            context.append(e1)
            context.append(e2)

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
                else:
                    grid[gridpoint_index +2][2] = int(grid[gridpoint_index +2][2] + (max_dist - distance)*x)
                if y > 0:
                    grid[gridpoint_index +1][2] = int(grid[gridpoint_index +1][2] + (max_dist - distance)*y)
                else:
                    grid[gridpoint_index +3][2] = int(grid[gridpoint_index +3][2] + (max_dist - distance)*y)
    return json.dumps(grid)

# Fetching json format heatmap data from site_x.pkl
@visualizer_blueprint.route('/heat/<dateSelected>/<siteSelected>')
def heatdate(dateSelected, siteSelected):
    site = siteSelected
    timestamp = dateSelected
    sitePath = 'webapp/static/site_' + site + '.pkl'


    df_events = pd.read_pickle(sitePath, compression='gzip')
    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)
                                     .dt.tz_convert('Europe/Helsinki')
                                     .dt.tz_localize(None))

    df_events_test = df_events[df_events.timestamp.dt.date.astype(str) == timestamp].copy()

    hour = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    hours = list(df_events_test['timestamp'].dt.hour.astype(str))
    device = list(df_events_test['deviceid'])

    data = {}
    data = {timestamp:{}}
    for i in hour:
        data[timestamp][i]={}

    for i in hour:
        for x in range(0,len(df_events_test)):
            if(hours[x]==i):
                if(device[x] in data[timestamp][i]):
                    data[timestamp][i][device[x]]+=1
                else:
                    data[timestamp][i][device[x]]=1

    jsonString = json.dumps(data)
    return jsonString


@visualizer_blueprint.route('/site/<int:num>')
def sitepicture(num):
    siteName = 'site_' + str(num) + '.png'
    return send_from_directory('static', siteName)


@visualizer_blueprint.route('/sitemeta/<int:num>')
def sitemeta(num):
    sitePath = 'webapp/static/site_' + str(num) + '.png'
    with Image.open(sitePath) as img:
        width, height = img.size
    reso = str(round(100*height/width)) + '%'
    result = json.dumps({'reso':reso, 'width':width, 'height':height})
    return result

# Dummy feature for Python module structure
@visualizer_blueprint.route('/time')
def timenow():
    timeNow = TimeNow()
    return render_template('time.html', timeNow=timeNow)
