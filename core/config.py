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

SEED_NODES = [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002"
]

BLOCK_VAR_CONVERSIONS = {
    'txid': str,
    'index': int,
    'nonce': int,
    'hash': str,
    'prev_hash': str,
    'timestamp': str
}
CHAINDATA_DIR = "./chaindata/"

NUM_ZEROS = 6
STANDARD_ROUNDS = 100000