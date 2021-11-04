from flask import Flask
from api.controller import dashboard_app


def create_app(*, mode='DEVELOPMENT') -> Flask:
    """Create a flask app instance."""

    flask_app = Flask('dashboard_app')
    flask_app.config['JSON_SORT_KEYS'] = False
    flask_app.config['APP_MODE'] = mode

    # import blueprints
    flask_app.register_blueprint(dashboard_app)

    return flask_app
