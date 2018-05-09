from apistar import App

from .routes import routes
from .components import components


app = App(routes=routes, components=components)


def run_api_server(*args, **kwargs):
    options = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': True,
        'secret_key': 'SET-YOUR-SECRET-KEY',
    }
    options.update(kwargs)
    
    app.serve(host=options['host'], port=options['port'],
              debug=options['debug'])


if __name__ == '__main__':
    run_api_server()
