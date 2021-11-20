def create_module(app, **kwargs):
    from .controllers import visualizer_blueprint
    app.register_blueprint(visualizer_blueprint)
