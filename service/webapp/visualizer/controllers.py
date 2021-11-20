from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request, send_from_directory
from .models import TimeNow

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


@visualizer_blueprint.route('/date/<dateSelected>')
def urldate(dateSelected):
    return dateSelected


@visualizer_blueprint.route('/site/<int:num>')
def sitepicture(num):
    siteName = 'site_' + str(num) + '.png'
    return send_from_directory('static', siteName)


@visualizer_blueprint.route('/time')
def timenow():
    timeNow = TimeNow()
    return render_template('time.html', timeNow=timeNow)
