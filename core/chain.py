from block import Block

class Chain(object):

    def __init__(self, blocks):
        self.blocks = blocks

    def is_valid(self):
        """
        Is a valid blockchain
        1, each block is indexed one after the other
        2, each block's prev_hash is the hash of the previous block
        3, The block's hash is valid for the number of zeros
        """
        for index, cur_block in enumerate(self.blocks[1:]):
            prev_block = self.blocks[index]
            if prev_block.index + 1 != cur_block.index:
                print('Index Error')
                return False
            if not cur_block.is_valid():
                print('Block invalid')
                return False
            if prev_block.hash != cur_block.prev_hash:
                print('Hash error')
                return False
        return True

    def self_save(self):
        """
        Save blockchain to file system
        """
        for block in self.blocks:
            b.self_save()
        return True

    def add_block(self, new_block):
        if new_block.index > len(self.blocks):
            pass
        self.blocks.append(new_block)
        return True

    def block_list_to_dict(self):
        return [b.to_dict() for b in self.blocks]

    def most_recent_block(self):
        return self.blocks[len(self.blocks)-1]

    def __len__(self):
        return len(self.blocks)