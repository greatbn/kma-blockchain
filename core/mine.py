from config import *
import requests
import apscheduler
import utils
from block import Block

def validate_possible_block(sche, mongo_conn, possible_block, txid):
    """
    validate new possible block 
    if True, save to local
    """
    possible_block = Block(possible_block)
    if possible_block.is_valid():
        possible_block.self_save()
        try:
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
    for peer in SEED_NODES:
        endpoint = peer + "/mined"
        try:
            r = requests.post(peer, json=new_block)
        except Exception:
            print "Peer %s is not online now" % peer
            continue
    return True

def mine_for_block(sched, mongo_conn):
    print "Starting mining listener"
    print sched.get_jobs()
    # import ipdb;ipdb.set_trace()
    if sched.get_job('mining'):
        print "Node is mining other transaction"
        return False
    print "No mining job exist"
    print "query pending transaction"
    pending_tx = mongo_conn.query_a_pending_transaction()
    print pending_tx
    if len(pending_tx) == 0:
        print "No pending transaction"
    print "Start minging"
    print pending_tx
    

