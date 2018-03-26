from config import *
import requests
import utils

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