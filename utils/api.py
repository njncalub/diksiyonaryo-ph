from api.app import run_api_server as run


def run_api_server(host, port, debug=False):
    run(host=host, port=port, debug=debug)
