import rpyc
import uuid
import threading 
import math
import random
import ConfigParser
import signal
import pickle
import sys
import os

from rpyc.utils.server import ThreadedServer

def int_handler(signal, frame):
  pickle.dump((MasterService.exposed_Master.file_table,MasterService.exposed_Master.block_mapping),open('fs.img','wb'))
  sys.exit(0)

def set_conf():
  conf=ConfigParser.ConfigParser()
  conf.readfp(open('dfs.conf'))
  MasterService.exposed_Master.block_size = int(conf.get('master','block_size'))
  MasterService.exposed_Master.replication_factor = int(conf.get('master','replication_factor'))
  minions = conf.get('master','minions').split(',')
  for m in minions:
    id,host,port=m.split(":")
    MasterService.exposed_Master.minions[id]=(host,port)

  if os.path.isfile('fs.img'):
    MasterService.exposed_Master.file_table,MasterService.exposed_Master.block_mapping = pickle.load(open('fs.img','rb'))

  print MasterService.exposed_Master.block_size, MasterService.exposed_Master.replication_factor, MasterService.exposed_Master.minions
class MasterService(rpyc.Service):
  class exposed_Master():
    file_table = {}
    block_mapping = {}
    minions = {}

    block_size = 0
    replication_factor = 0

    def exposed_read(self,fname):
      mapping = self.__class__.file_table[fname]
      return mapping

    def exposed_write(self,dest,size):
      if self.exists(dest):
        pass # ignoring for now, will delete it later

      self.__class__.file_table[dest]=[]

      num_blocks = self.calc_num_blocks(size)
      blocks = self.alloc_blocks(dest,num_blocks)
      return blocks

    def exposed_get_file_table_entry(self,fname):
      if fname in self.__class__.file_table:
        return self.__class__.file_table[fname]
      else:
        return None

    def exposed_get_block_size(self):
      return self.__class__.block_size

    def exposed_get_minions(self):
      return self.__class__.minions

    def calc_num_blocks(self,size):
      return int(math.ceil(float(size)/self.__class__.block_size))

    def exists(self,file):
      return file in self.__class__.file_table

    def alloc_blocks(self,dest,num):
      blocks = []
      for i in range(0,num):
        block_uuid = uuid.uuid1()
        nodes_ids = random.sample(self.__class__.minions.keys(),self.__class__.replication_factor)
        blocks.append((block_uuid,nodes_ids))

        self.__class__.file_table[dest].append((block_uuid,nodes_ids))

      return blocks


if __name__ == "__main__":
  set_conf()
  signal.signal(signal.SIGINT,int_handler)
  t = ThreadedServer(MasterService, port = 2131)
  t.start()