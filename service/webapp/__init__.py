from flask import Flask


def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)


    from .visualizer import create_module as visualizer_create_module
    from .main import create_module as main_create_module
    visualizer_create_module(app)
    main_create_module(app)

    return app
