import hashlib
import os
import json
from config import *

class Block(object):
    def __init__(self, data):
        """
        Find field: index, timestamp, data, prev_hash, nonce
        """
        for key, value in data.items():
            if key in BLOCK_VAR_CONVERSIONS:
                setattr(self, key, BLOCK_VAR_CONVERSIONS[key](value))
            else:
                setattr(self, key, value)
    
    def header_string(self):
        """
        convert block to string
        """
        return str(self.index) + self.prev_hash + self.data + str(self.timestamp) + str(self.nonce) + str(self.txid)
    
    def update_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string())
        new_hash = sha.hexdigest()
        self.hash = new_hash
        return new_hash

    def self_save(self):
        """
        Save to local file
        """
        index = str(self.index).zfill(6)
        filename = '%s%s.json' % (CHAINDATA_DIR, index)
        with open(filename, 'w') as block_file:
            json.dump(self.to_dict(), block_file)

    def to_dict(self):
        """
        Convert block to a dict
        """
        info = {}
        info['index'] = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash'] = str(self.hash)
        info['data'] = str(self.data)
        info['nonce'] = str(self.nonce)
        info['txid'] = str(self.txid)
        return info

    def is_valid(self):
        """
        check is block valid
        """
        self.update_self_hash()
        if str(self.hash[0:NUM_ZEROS]) == '0'*NUM_ZEROS:
            return True
        else:
            return False