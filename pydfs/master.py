import rpyc
import uuid
import threading 

from rpyc.utils.server import ThreadedServer

def set_conf():
  MasterService.exposed_Master.block_size = 1024
  MasterService.exposed_Master.replication_factor = 2
  MasterService.exposed_Master.minions = {"1":"localhost:8888","2":"localhost:9999"}


class MasterService(rpyc.Service):
  class exposed_Master():
    file_table = {}
    block_mapping = {}
    minions = {}

    block_size = 0
    replication_factor = 0

    def exposed_read(self,fname):
      f=file_table[fname]
      pass
      # return {"num_blk":3,
      #         "blk_meta":[
      #                       [(minion_loc,uuid),(minion_loc,uuid)],
      #                       [(minion_loc,uuid),(minion_loc,uuid)]
      #                     ]
      #        }


    def exposed_write(self):
      pass
      # exits()
      # calc_num_blk()
      # # coroutines for each block.
      # for each block:
      #   algo_find_minions()
      #   put_entry     

    def exposed_put(self,val):
      self.__class__.replication_factor = val


if __name__ == "__main__":
  set_conf()
  t = ThreadedServer(MasterService, port = 2131)
  t.start()