from config import *

from pymongo import MongoClient
from bson import json_util
import json
import uuid

class MongoDBWrapper(object):

    def __init__(self):
        conn = MongoClient(host=MONGODB_HOST,
                           port=MONGODB_PORT)
        db = conn[MONGODB_DBNAME]
        self.tx = db[MONGODB_COLLECTIONS['pending_transactions']]
        self.node = db[MONGODB_COLLECTIONS['list_nodes']]
    

    def new_pending_transaction(self, data):
        # push new transaction to mongodb
        # return transaction id
        try:
            if 'txid' not in data:
                txid = uuid.uuid4()
                data['txid'] = str(txid)
            self.tx.save(data)
            return txid
        except Exception as e:
            raise Exception("Cannot add new transaction %s " % e)

    def remove_pending_transaction(self, txid):
        # remove pending transaction
        # the transaction which is mined
        try:
            rm_tx = self.tx.find({'txid': txid})
            self.tx.remove(rm_tx)
            return True
        except Exception as e:
            raise Exception("Cannot remove pending transactions %s " % e)

    def register_node(self, node):
        # adding node to database 
        # return node uuid
        try:
            if 'uuid' not in node:
                node_uuid = uuid.uuid4()
                node['is_confirm'] = bool(node['is_confirm'])
                node['uuid'] = str(node_uuid)
            self.node.save(node)
            return node_uuid
        except Exception as e:
            raise Exception("Can't add node to database %s " % e)
    
    def remove_node(self, node_uuid):
        # remove node from database
        try:
            rm_node = self.node.find({'uuid': node_uuid})
            self.node.remove(rm_node)
            return True
        except Exception as e:
            raise Exception("Can't remove node %s " % e)
    
    def query_confirm_node(self):
        # query all confirm node

        try:
            data = self.node.find({'is_confirm': True})
            return json.loads(json_util.dumps(list(data)))
        except Exception as e:
            raise Exception("Cannot get confirm nodes in "\
                            "blockchain network %s" % e)

    def query_pending_transactions(self):
        # query all transaction in database
        try:
            data = self.tx.find({})
            return json.loads(json_util.dumps(list(data)))
        except Exception as e:
            raise Exception("Cannot get pending transactions")