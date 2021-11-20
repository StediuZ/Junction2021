from flask import Blueprint, redirect, url_for, render_template

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main',
    static_url_path='',
    static_folder='../static'
)


@main_blueprint.route('/')
def index():
    return redirect(url_for('visualizer.home'))
