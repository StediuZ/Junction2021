from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request
from .models import TimeNow

visualizer_blueprint = Blueprint(
    'visualizer',
    __name__,
    template_folder='../templates/visualizer',
    url_prefix="/visualizer"
)


@visualizer_blueprint.route('/')
def home():
    return render_template('home.html')

@visualizer_blueprint.route('/date', methods=['GET', 'POST'])
def querydate():
    dateSelected = request.form['date']
    return dateSelected


@visualizer_blueprint.route('/time')
def timenow():
    timeNow = TimeNow()
    return render_template('time.html', timeNow=timeNow)
