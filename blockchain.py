
# Based on https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

'''
Example Block

block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'data': {
            somekey1: somevalue1,
            somekey2: somevalue2,
    },
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
'''

import hashlib
import json
import logging
from pathlib import Path
from time import time


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
            self.chain.append(dict(index=0, previous_hash='1', proof=100, data={"msg" : "Genesis Block"}))
            self.save_chain()


    def __init__(self, instance_name):

        self.home = Path.home() / '.minichain'
        self.instance_name = instance_name
        self.home.mkdir(exist_ok=True)
        self.chain_file = self.home / 'chain.json'.format(self.instance_name)
        self.load_chain()


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


    def insert_block(self, block):

        if not self.valid_proof(self.last_block['proof'], block['proof'], self.hash(self.last_block)):
            print('invalid block proof')
            return False

        if block['index'] != (self.last_block['index'] + 1):
            print('invalid block index')
            return False

        if block['timestamp'] < self.last_block['timestamp']:
            print('timestamp older than last block')
            return False

        if block['timestamp'] > time():
            print('timestamp in the future')
            return False

        self.chain.append(block)
        self.save_chain()

        return True
