# PyDFS

# Components:
 1. **Master :** Will contain metadata
 2. **Minion :** Will contain actual file data
 3. **Client :** Interacts with 1 and 2 to do stuff
   
## Master:
Master will contain metadata. Which is: file name, blocks associated with it and address of those blocks. Data structures wise, it would look something like this.
```
example file: /etc/passwd

    file_block = {"/etc/passwd": ["block0", "block1"]}
    block_minion = {"block0": [minion1 ,minion2],
                    "block1": [minion2, minion3]}
    minions = {
      "minion1": (host1, portX),
      "minion2": (host2, portY),
      "minion3": (host3, portZ)
    }
```

Also master will have following properties:
1. `replication_factor`: how many copies to make of a block
2. `block_size`: what should be size of each block
3. block placement strategy: random here

methods that master will expose will look like:
```
  def read(file)
  returns: [
              {"block_id": "block1", "block_addr": [(host1,portX),...]}, 
              {"block_id": "block2", "block_addr: [(host2,portY),...]"}
           ]


  def write(file, size)
  returns: [
              {"block_id": "block1", "block_addr": [(host1,portX),...]}, 
              {"block_id": "block2", "block_addr: [(host2,portY),...]"}
           ]
```
## Minion:
Minions are relatively simple in operations and implementation. Given a block address either they can read or write and forward same block to next minion.

methods:
```
  def put(block_id, data, minions) => writes the block on local disk and forward to minions

  def get(block_id) => reads the block and returns the contents

  def forward(block_id, data, minions) => calls put() on next minion with remaining minions as forward list
```

## Client:
Client will interact with both minions and master. Given a get or put operation, it will first contact master to query metadata and then pertaining minions to perform data operation.

```
  def get(file):
  contacts master to get metadata first and then calls appropriate minions to read blocks

  def put(input_file, file):
  contacts master to allocate blocks for `file` and then reads input file in blocks and calls minions to write the blocks
```

-----

## Misc:
 1. Minions will be anticipating PORT and DATA_DIR as arguments. Blocks will be stored under DATA_DIR.
 2. Block size, replication factors, list of minions are hard coded in master.
 3. We are not storing metadata on disk.