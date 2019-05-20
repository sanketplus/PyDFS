import rpyc
import os
import sys
import logging

from rpyc.utils.server import ThreadedServer

DATA_DIR = "/tmp/minion/"
PORT = 8888
logging.basicConfig(level=logging.DEBUG)


class Minion(rpyc.Service):

    def exposed_put(self, block_id, data, minions):
        logging.debug("put block: " + block_id)
        out_path = os.path.join(DATA_DIR, block_id)
        with open(out_path, 'w') as f:
            f.write(data)
        if len(minions) > 0:
            self.forward(block_id, data, minions)

    def exposed_get(self, block_id):
        logging.debug("get block: " + block_id)
        block_addr = os.path.join(DATA_DIR, block_id)
        if not os.path.isfile(block_addr):
            logging.debug("block not found")
            return None
        with open(block_addr) as f:
            return f.read()

    def forward(self, block_id, data, minions):
        logging.debug("forwarding block: " + block_id + str(minions))
        next_minion = minions[0]
        minions = minions[1:]
        host, port = next_minion

        rpyc.connect(host, port=port).root.put(block_id, data, minions)


if __name__ == "__main__":
    PORT = int(sys.argv[1])
    DATA_DIR = sys.argv[2]

    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    logging.debug("starting minion")
    rpyc_logger = logging.getLogger('rpyc')
    rpyc_logger.setLevel(logging.WARN)
    t = ThreadedServer(Minion(), port=PORT,  logger=rpyc_logger, protocol_config={
    'allow_public_attrs': True,
})
    t.start()
