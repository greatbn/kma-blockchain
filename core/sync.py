from config import *
import os
import requests
import utils
import json
import glob
from chain import Chain
from block import Block

mongo_conn = utils.MongoDBWrapper()

def sync_transactions():
    # print "Start syncing"
    # get local pending transactions
    pending_transactions = mongo_conn.query_pending_transactions()
    pending_txid = []
    for tx in pending_transactions:
        pending_txid.append(tx['txid'])
    # check other seed node pending transaction if not exist write to local
    for node in SEED_NODES:
        endpoint = "%s%s" % (node, "/pending-transactions")
        try:
            r = requests.get(endpoint)
            data = r.json()['pending']
            for tx in data:
                if tx['txid'] not in pending_txid:
                    # print "New pending transaction"
                    del tx['_id']
                    mongo_conn.new_pending_transaction(tx)
                    pending_txid.append(tx['txid'])
        except requests.exceptions.ConnectionError:
            # print "Seed node %s not connected" % node
            continue
    return True
            

def sync_node():
    # get local node
    nodes = mongo_conn.query_confirm_node()
    node_id = []
    for node in nodes:
        node_id.append(node['uuid'])
    # check seed nodes if not exist append to list and write to local
    for node in SEED_NODES:
        endpoint = "%s%s" % (node, "/confirm-nodes")
        try:
            r = requests.get(endpoint)
            data = r.json()['nodes']
            for n in data:
                if n['uuid'] not in node_id:
                    del n['_id']
                    mongo_conn.register_node(n)
                    node_id.append(n['uuid'])
        except requests.exceptions.ConnectionError:
            print "Node %s is not connected" % node
    return True

def sync_local():
    local_chain = Chain([])
    if os.path.exists(CHAINDATA_DIR):
        for filepath in glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
            with open(filepath, 'r') as block_file:
                try:
                    block_info = json.load(block_file)
                except:
                    raise Exception("block error")
                local_block = Block(block_info)
                local_chain.add_block(local_block)
    return local_chain

def sync_overall(save=False):
    local_chain = sync_local()
    for peer in SEED_NODES:
        endpoint = peer + '/blockchain'
        try:
            r = requests.get(endpoint)
            chain_data = r.json()
            peer_blocks = [Block(block_dict) for block_dict in chain_data]
            peer_chain = Chain(peer_blocks)
            # check valid , if valid and longer, sync local
            if peer_chain.is_valid() and len(peer_chain) > len(local_chain):
                local_chain = peer_chain
        except Exception as e:
            raise Exception(e)
    if save:
        local_chain.self_save()
    return local_chain


def sync():
    sync_overall(save=True)

