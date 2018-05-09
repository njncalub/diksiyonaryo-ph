from api.app import run_api_server as run


def run_api_server(settings):
    run(host=settings.API_SERVER_HOST, port=settings.API_SERVER_PORT,
        debug=settings.API_SERVER_DEBUG)
