import rpyc
import uuid

from rpyc.utils.server import ThreadedServer

def set_conf():
  MasterService.exposed_Master.block_size = 1024
  MasterService.exposed_Master.replication_factor = 2
  MasterService.exposed_Master.minions = {"1":"localhost:8888","2":"localhost:9999"}


class MinionService(rpyc.Service):
  class exposed_Minion():
    blocks = {}

    def exposed_put(self):
      pass

    def exposed_get(self):
      pass   
 
    def pass_on():
      pass

if __name__ == "__main__":
  set_conf()
  t = ThreadedServer(MasterService, port = 8888)
  t.start()