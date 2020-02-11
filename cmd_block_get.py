import json
import logging

import click
import requests

logging.basicConfig()

@click.command()
@click.argument('index')
@click.option('-p', 'port', default=5000, help='Port of the local node to manage')
def cmd_block(index, port):

    r = requests.get(f'http://localhost:{port}/block/{index}')

    print(json.dumps(r.json(), sort_keys=True))


if __name__ == '__main__':
    cmd_block()

