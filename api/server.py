from apistar import App

from .routes import routes
from .components import components


def create_app():
    return App(routes=routes,
               components=components,
               docs_url='/')


def run_api_server(*args, **kwargs):
    options = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': True,
    }
    options.update(kwargs)
    
    app = create_app()
    app.serve(host=options['host'],
              port=options['port'],
              debug=options['debug'])


if __name__ == '__main__':
    run_api_server()
