from config import *
import datetime
import block
import uuid

def is_valid_chain(blockchain):
    """
    Check entire chain is valid
    """
    for block in blockchain:
        if not block.is_valid():
            return False
    return True


def dict_from_block_attributes(**kwargs):
    info = {}
    for key in kwargs:
        if key in BLOCK_VAR_CONVERSIONS:
            info[key] = BLOCK_VAR_CONVERSIONS[key](kwargs[key])
        else:
            info[key] = kwargs[key]
    
    return info


def create_new_block_from_prev(prev_block=None, data=None, timestamp=None, txid=None):
    if not txid:
        txid = str(uuid.uuid4())
    if not prev_block:
        index = 0
        prev_hash = ''
    else:
        index = int(prev_block.index) + 1
        prev_hash = prev_block.hash

    if not timestamp:
        timestamp = datetime.datetime.utcnow().strftime("%Y/%m/%d-%H:%M:%S:%f")
    
    nonce = 0
    block_info_dict = dict_from_block_attributes(
        index=index,
        timestamp=timestamp,
        data=data,
        prev_hash=prev_hash,
        nonce=nonce,
        txid=txid)
    new_block = block.Block(block_info_dict)
    return new_block
