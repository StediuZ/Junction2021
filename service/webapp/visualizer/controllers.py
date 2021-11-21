from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request, send_from_directory
from .models import TimeNow
from PIL import Image
import base64, json, os, random
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


@visualizer_blueprint.route('/', methods=['GET', 'POST'])
def submitdate():
    dateSelected = request.form['date']
    return dateSelected


@visualizer_blueprint.route('/vectors')
def testvectors():
    X_max = 40
    Y_max = 20
    interval = 1
    vectors=[]
    hour = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    for x in range(0,X_max,interval):
        for y in range(0,Y_max,interval):
            vectors.append([x,y,random.randrange(0,200,1),random.randrange(0,359,1)])
    jsonString = json.dumps(vectors)
    return jsonString


@visualizer_blueprint.route('/vector/<dateSelected>/<siteSelected>')
def vectordate(dateSelected, siteSelected):
    return dateSelected + siteSelected


@visualizer_blueprint.route('/heat/<dateSelected>/<siteSelected>')
def heatdate(dateSelected, siteSelected):
    #site = 'site_1'
    #timestamp = "2021-08-05"
    site = siteSelected
    timestamp = dateSelected
    sitePath = 'webapp/static/site_' + site + '.pkl'
    #sitePath = os.getcwd()
    #return str(sitePath)

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


@visualizer_blueprint.route('/time')
def timenow():
    timeNow = TimeNow()
    return render_template('time.html', timeNow=timeNow)
