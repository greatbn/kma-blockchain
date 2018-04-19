#!/usr/bin/python
import os

MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.getenv('MONGODB_PORT', 27017)
MONGODB_DBNAME = os.getenv('MONGODB_DBNAME', 'blockchain')
#REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
MONGODB_COLLECTIONS = {
    'pending_transactions': 'transactions',
    'list_nodes': 'nodes',
    'mining': 'mining'
}

ELASTIC_HOSTS = ["elastic"]
ELASTIC_INDEX = "blockchain"

API_NODE = os.getenv("API_NODE", "http://10.5.9.110:5000")
ENV = os.getenv('ENV', 'develop')

BLOCK_VAR_CONVERSIONS = {
    'txid': str,
    'index': int,
    'nonce': int,
    'hash': str,
    'prev_hash': str,
    'timestamp': str,
    'data': str
}
CHAINDATA_DIR = "./chaindata/"

NUM_ZEROS = 4
STANDARD_ROUNDS = 100000