import rpyc
import sys
import os

def send_to_minion(block_uuid,data,minions):
  print "sending: " + str(block_uuid) + str(minions)
  minion=minions[0]
  minions=minions[1:]
  host,port=minion.split(":")

  con=rpyc.connect(host,port=port)
  minion = con.root.Minion()
  minion.put(block_uuid,data,minions)


def read_from_minion(block_uuid,minion):
  host,port = minion.split(":")
  con=rpyc.connect(host,port=port)
  minion = con.root.Minion()
  return minion.get(block_uuid)

def get(master,fname):
  file_table = master.get_file_table_entry(fname)
  if not file_table:
    print "404: file not found"
    return

  for block in file_table:
    for m in [master.get_minions()[_] for _ in block[1]]:
      data = read_from_minion(block[0],m)
      if data:
        sys.stdout.write(data)
        break
    else:
        print "No blocks found. Possibly a corrupt file"

def put(master,source,dest):
  size = os.path.getsize(source)
  blocks = master.write(dest,size)
  with open(source) as f:
    for b in blocks:
      data = f.read(master.get_block_size())
      block_uuid=b[0]
      minions = [master.get_minions()[_] for _ in b[1]]
      send_to_minion(block_uuid,data,minions)


def main(args):
  con=rpyc.connect("localhost",port=2131)
  master=con.root.Master()
  
  if args[0] == "get":
    get(master,args[1])
  elif args[0] == "put":
    put(master,args[1],args[2])
  else:
    print "try 'put srcFile destFile OR get file'"


if __name__ == "__main__":
  main(sys.argv[1:])