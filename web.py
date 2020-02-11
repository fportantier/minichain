
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

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import logging
import requests
from flask import Flask, jsonify, request
from blockchain import Blockchain

logging.basicConfig()


# Instantiate the Node
app = Flask(__name__)



@app.route('/', methods=['GET'])
def get_status():

    response = {
        'chain_length': len(app.blockchain.chain),
        'last_block': app.blockchain.last_block,
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': app.blockchain.chain,
        'length': len(app.blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/block', methods=['POST'])
def new_block():

    block = request.get_json()

    result = app.blockchain.insert_block(block)

    if result is True:
        response = {'message': 'Block added to the chain'}
        return jsonify(response), 201
    else:
        response = {'message': result}
        return jsonify(response), 401


@app.route('/block/last', methods=['GET'])
def last_block():

    block = app.blockchain.last_block
    return jsonify(block), 200


@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):

    block = app.blockchain.get_block(index)
    if block:
        return jsonify(block), 200
    else:
        return jsonify({'error' : 'not found'}), 404


@app.route('/validate', methods=['GET'])
def validate():

    if app.blockchain.valid_chain(app.blockchain.chain):
        return jsonify({'result' : 'valid chain'}), 200
    else:
        return jsonify({'result' : 'invalid chain'}), 200


def make_app(port=5000):

    # Instantiate the Blockchain
    app.blockchain = Blockchain(instance_name=port)

    return app


