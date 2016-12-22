import rpyc
import sys


def get(master,fname):
  pass


def put(master,source,dest):
  pass


def main(args):
  con=rpyc.connect("localhost",port=2131)
  master=con.root.Master()

  if args[0] == "get":
    get(master,args[1])
  elif args[0] == "put"
    put(master,args[1],args[2])


if __name__ == "__main__":
  main(sys.argv[1:])