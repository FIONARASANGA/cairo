"""
Production Start Script
"""
from gunicorn.app.base import BaseApplication
from factory import create_app
#from api.utils import 


class GunicornApp(BaseApplication):
    '''
    Bundle Gunicorn and Flask together, so that we can call it as a
    flask-script command.

    http://docs.gunicorn.org/en/stable/custom.html
    '''

    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


app = create_app(mode="DEVELOPMENT")
with app.app_context():
    app.config['APP_MODE'] = 'DEVELOPMENT'

if __name__ == '__main__':
    GunicornApp(app)
