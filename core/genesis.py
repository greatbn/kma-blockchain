import os
from config import *
import block_utils
import sync

def mine_first_block():
    first_block = block_utils.create_new_block_from_prev(prev_block=None, data='First block.')
    first_block.update_self_hash() #calculate_hash(index, prev_hash, data, timestamp, nonce)
    while str(first_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
        first_block.nonce += 1
        first_block.update_self_hash()
    assert first_block.is_valid()
    return first_block


if __name__ == '__main__':
    #check if dir is empty from just creation, or empty before
    if not os.path.exists(CHAINDATA_DIR):
        os.mkdir(CHAINDATA_DIR)

    if os.listdir(CHAINDATA_DIR) == []:
        #create the first block
        first_block = mine_first_block()
        print first_block.to_dict()
        first_block.self_save()
        #need a data.txt to tell which port we're running on
        filename = "%s/data.txt" % CHAINDATA_DIR
        with open(filename, 'w') as data_file:
            data_file.write('Genesis block was created')
    else:
        print "Chaindata directory already has files. If you want to generate a first block, delete files and rerun"

