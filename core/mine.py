from config import *
import requests
import apscheduler
import utils
import block_utils
from block import Block
import sync
from apscheduler.events import EVENT_JOB_EXECUTED
import nodes
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

mongo_conn = utils.MongoDBWrapper()

def validate_possible_block(sche, mongo_conn, possible_block, txid):
    """
    validate new possible block 
    if True, save to local
    """
    possible_block = Block(possible_block)
    if possible_block.is_valid():
        possible_block.self_save()
        try:
            if mongo_conn.query_mining_tx(possible_block.txid):
                sche.remove_job('mining')
                print "Removed mining job"
        except apscheduler.jobstores.base.JobLookupError:
            print "No mining job exist"
        # remove in pending transactions
        mongo_conn.remove_pending_transaction(possible_block['txid'])
        return True
    return False

def broadcast_mined_block(new_block):
    new_block = new_block.__dict__
    NODES = nodes.get_list_node(mongo_conn)
    for peer in NODES:
        endpoint = peer + "/mined"
        try:
            r = requests.post(peer, json=new_block)
        except Exception:
            print "Peer %s is not online now" % peer
            continue
    return True

def mine_block_listener(event):
    if event.job_id == 'mining':
        
        new_block = event.retval

        if new_block:
            new_block.self_save()
            broadcast_mined_block(new_block)
            txid = new_block.txid
            mongo_conn.remove_pending_transaction(txid)
            mongo_conn.remove_mining_tx(txid)
        else:
            pass

def mine_for_block(sched, mongo_conn):
    print "Starting mining listener"
    if mongo_conn.check_free_job():
        print "Node is mining other transaction"
        return False
    try:
        pending_tx = mongo_conn.query_a_pending_transaction()
        if pending_tx:
            # add to pending 
            mongo_conn.add_mining_tx(pending_tx['txid'])
            print "Start minging transaction id %s " % pending_tx['txid']
            blockchain = sync.sync_local()
            sched.add_job(
                proof_of_work,
                args=[blockchain, pending_tx],
                id='mining'
            )
            sched.add_listener(
                mine_block_listener,
                EVENT_JOB_EXECUTED
            )
        else:
            print "No pending transaction"
    except Exception as e:
        ## query pending transaction fail or not have any pending transaction
        raise Exception(e)

def proof_of_work(blockchain, data=None):
    if data:
        print "Starting Proof of Work"
        prev_block = blockchain.most_recent_block()
        txid = data['txid']
        nonce = 0
        # build block
        del data['txid']
        del data['_id']
        timestamp = data['timestamp']
        del data['timestamp']
        new_block = block_utils.create_new_block_from_prev(
            prev_block=prev_block,
            txid=txid,
            timestamp=timestamp,
            data=data)
        
        new_block.update_self_hash()
        while str(new_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
            new_block.nonce += 1
            new_block.update_self_hash()
            # print new_block.to_dict()
            if new_block.is_valid():
        # print new_block
                print "New block was mined"
                print new_block.to_dict()
                return new_block
    print "No data input"

