from config import *

from pymongo import MongoClient
from bson import json_util
import json
import uuid
import datetime

class MongoDBWrapper(object):

    def __init__(self):
        conn = MongoClient(host=MONGODB_HOST,
                           port=MONGODB_PORT)
        db = conn[MONGODB_DBNAME]
        self.tx = db[MONGODB_COLLECTIONS['pending_transactions']]
        self.node = db[MONGODB_COLLECTIONS['list_nodes']]
        self.mining = db[MONGODB_COLLECTIONS['mining']]
    

    def new_pending_transaction(self, data):
        # push new transaction to mongodb
        # return transaction id
        try:
            if 'txid' not in data:
                txid = uuid.uuid4()
                data['txid'] = str(txid)
            timestamp = datetime.datetime.utcnow().strftime("%Y/%m/%d-%H:%M:%S:%f")
            data['timestamp'] = timestamp
            self.tx.save(data)
            return txid
        except Exception as e:
            raise Exception("Cannot add new transaction %s " % e)

    def remove_pending_transaction(self, txid):
        # remove pending transaction
        # the transaction which is mined
        try:
            self.tx.delete_one({'txid': txid})
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
            self.node.delete_one({'uuid': node_uuid})
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
    
    def query_a_pending_transaction(self):
        # query one pending transaction
        try:
            data = self.tx.find_one()
            if data:
                return json.loads(json_util.dumps(dict(data)))
            else:
                return False
        except Exception as e:
            raise Exception("Cannot get a pending transaction %s" % e)

    def add_mining_tx(self, txid):
        # add mining txid
        try:
            data = {'txid': txid}
            self.mining.save(data)
            return True
        except Exception as e:
            raise Exception("Cannot add mining job %s" % e)
    
    def remove_mining_tx(self, txid):
        try:
            self.mining.delete_one({'txid': txid})
            return True
        except Exception as e:
            raise Exception("Cannot remove mining job %s" % e)

    def query_mining_tx(self, txid):
        try:
            data = self.mining.find_one({'txid': txid})
            if data:
                return True
            else:
                return False
        except Exception as e:
            raise Exception("Cannot query mining job %s" % e)
    
    def check_free_job(self):
        # neu dang co job thi tra ve True
        # khi do se khong thuc hien mining nua
        try:
            data = self.mining.find({})
            # print dict(data)
            if dict(data):
                return True
            else:
                return False
        except Exception as e:
            raise Exception("Cannot check free job %s " % e)
