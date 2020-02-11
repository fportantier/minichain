import hashlib
import json
import logging
from pathlib import Path
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import click
import requests
from flask import Flask, jsonify, request

# Based on https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

'''
Example Block

block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            somekey1: somevalue1,
            somekey2: somevalue2,
        },
        {
            otherkey1: othervalue1,
            otherkey2: othervalue2,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
'''


logging.basicConfig()

class Blockchain:


    def save_chain(self):
        with self.chain_file.open('w') as outfile:
            outfile.write(json.dumps(self.chain, indent=4))

    def load_chain(self):
        if self.chain_file.is_file():
            self.chain = json.load(self.chain_file.open())
        else:
            self.chain = []
            # Create the genesis block
            self.new_block(previous_hash='1', proof=100)
            self.save_chain()


    def __configure(self):

        self.home.mkdir(exist_ok=True)

        self.chain_file = self.home / 'chain.json'.format(self.instance_name)

        self.current_transactions = []

        self.load_chain()


    def __init__(self, instance_name):

        self.home = Path.home() / '.minichain'
        self.instance_name = instance_name
        self.__configure()


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True


    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        self.save_chain()

        return block


    def get_block(self, index):
        """
        Get a block by index

        :index: Index (position) of the block on the chain
        :return: The block or None if the a block does not exists
        """

        if index < 1:
            return None

        try:
            return self.chain[index-1]
        except IndexError:
            return None


    def new_transaction(self, transaction):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append(transaction)

        return self.last_block['index'] + 1


    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"




    def new_block(self):
        # We run the proof of work algorithm to get the next proof...
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        app.blockchain.new_transaction(
            sender="0",
            recipient=app.blockchain.node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = app.blockchain.hash(last_block)
        block = app.blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transaction'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }











logging.basicConfig()

@click.command()
@click.argument('index')
@click.option('-p', 'port', default=5000, help='Port of the local node to manage')
def cmd_block(index, port):

    r = requests.get(f'http://localhost:{port}/block/{index}')

    print(json.dumps(r.json(), sort_keys=True))


if __name__ == '__main__':
    cmd_block()

