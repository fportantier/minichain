#!/usr/bin/env python3

import hashlib
import json
import logging
from time import time

import click
import requests

logging.basicConfig()

# Based on https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

'''
Example Block

block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transaction': {
            somekey1: somevalue1,
            somekey2: somevalue2,
    },
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
'''


def valid_proof(last_block_proof, proof, last_block_hash):
    """Validates the Proof"""

    guess = f'{last_block_proof}{proof}{last_block_hash}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"


def block_hash(block):
    """Calculates the hash of a block"""

    block_string = json.dumps(block, sort_keys=True).encode()
    block_hash = hashlib.sha256(block_string).hexdigest()
    return block_hash


def proof_of_work(last_block):
    """Returns a valid proof"""

    last_block_proof = last_block['proof']

    last_block_hash = block_hash(last_block)

    proof = 0
    while valid_proof(last_block_proof, proof, last_block_hash) is False:
        proof += 1

    return proof



@click.command()
@click.option('-p', 'port', default=5000, help='Port of the local node to manage')
@click.option('--bad-proof', 'bad_proof', is_flag=True, default=False, help='Use a bad proof to test')
@click.option('--bad-timestamp', 'bad_timestamp', is_flag=True, default=False, help='Use a bad timestamp to test')
@click.argument('args', nargs=-1)
def cmd_block_new(port, bad_proof, bad_timestamp, args):

    data = dict(zip(args[::2], args[1::2]))

    if not data:
        print('not arguments')
        return False

    last_block = requests.get(f'http://localhost:{port}/block/last').json()

    #print(json.dumps(last_block, sort_keys=True))

    proof = proof_of_work(last_block)

    block = {
        'index': last_block['index'] + 1,
        'timestamp': time(),
        'data': data,
        'proof': proof,
        'previous_hash': block_hash(last_block), #previous_hash or self.hash(self.chain[-1]),
    }

    if bad_proof:
        block['proof'] = 4321

    if bad_timestamp:
        block['timestamp'] = time() + 5000

    #print(json.dumps(block, sort_keys=True))

    r = requests.post(f'http://localhost:{port}/block', json=block) #).json()
    print(r.json())


if __name__ == '__main__':
    cmd_block_new()
