from flask import Flask
from flask_graphql import GraphQLView

from data.schema import schema


def run_server(*args, **kwargs):
    options = {
        'host': '0.0.0.0',
        'port': '5000',
        'debug': True,
        'graphiql': True,
        'secret_key': 'SET-YOUR-SECRET-KEY',
    }
    options.update(kwargs)
    
    app = Flask(__name__)
    
    # set the SECRET_KEY before loading the config
    SECRET_KEY = options['secret_key']
    
    graphql_view = GraphQLView.as_view('graphql', schema=schema,
                                       graphiql=options['graphiql'])
    
    app.add_url_rule(rule='/graphql', view_func=graphql_view)
    
    app.run(host=options['host'], port=options['port'], debug=options['debug'])
