from flask import Flask
from flask_graphql import GraphQLView

from data.schema import schema


def run_server(*args, **kwargs):
    app = Flask(__name__)
    app.debug = True
    
    graphql_view = GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    
    app.add_url_rule(rule='/graphql', view_func=graphql_view)
    
    app.run()
