# PyDFS

# Componenets:
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

## Minion:
Minions are relatively simple in operations and implementation. Given a block address either they can read or write and forward same block to next minion.

## Client:
Client will interact with both minions and master. Given a get or put operation, it will first contact master to query metadata and then pertaining minions to perform data operation.
