import json
import logging

import click
import requests

logging.basicConfig()

@click.command()
@click.option('-p', 'port', default=5000, help='Port of the local node to manage')
def cmd_chain_get(port):

    try:
        r = requests.get(f'http://localhost:{port}/chain')
    except Exception as e:
        logging.error(e)
        return False

    print(json.dumps(r.json(), indent=4))


if __name__ == '__main__':
    cmd_chain_get()
