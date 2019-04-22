import rpyc
import uuid
import math
import random
import configparser
import signal
import pickle
import sys
import os

from rpyc.utils.server import ThreadedServer

BLOCK_SIZE = 100
REPLICATION_FACTOR = 2
MINIONS = {"1": ("127.0.0.1", 8000),
           "2": ("127.0.0.1", 9000),}

class MasterService(rpyc.Service):
    """
    file_block = {'file.txt': ["block1", "block2"]}
    block_minion = {"block1": [1,3]}
    minions = {"1": (127.0.0.1,8000), "3": (127.0.0.1,9000)}
    """

    file_block = {}
    block_minion = {}
    minions = MINIONS

    block_size = BLOCK_SIZE
    replication_factor = REPLICATION_FACTOR

    def exposed_read(self, file):
        """
        returns [{"block1": [(127.0.0.1,8000)]}, "block2": ...]
        """

        mapping = []
        # iterate over all of file's blocks
        for blk in self.file_block[file]:
            minion_addr = []
            # get all minions that contain that block
            for m_id in self.block_minion[blk]:
                minion_addr.append(self.minions[m_id])

            mapping.append({"block_id": blk, "block_addr": minion_addr})
        return mapping

    def exposed_write(self, file, size):

        self.file_block[file] = []

        num_blocks = int(math.ceil(float(size) / self.block_size))
        return self.alloc_blocks(file, num_blocks)

    def alloc_blocks(self, file, num_blocks):
        return_blocks = []
        for i in range(0, num_blocks):
            block_id = str(uuid.uuid1()) # generate a block
            minion_ids = random.sample(     # allocate REPLICATION_FACTOR number of minions
                list(self.minions.keys()), self.replication_factor)
            minion_addr = [self.minions[m] for m in minion_ids]
            self.block_minion[block_id] = minion_ids
            self.file_block[file].append(block_id)

            return_blocks.append(
                {"block_id": block_id, "block_addr": minion_addr})

        return return_blocks


if __name__ == "__main__":
    t = ThreadedServer(MasterService(), port=2131, protocol_config={
    'allow_public_attrs': True,
})
    t.start()
