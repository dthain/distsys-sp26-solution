# This is the basic implementation of the HashTable
# It does nothing special, and may end up throwing
# exceptions that the server must catch.

import re
import os
import json
from HashTableUtil import HTFileMetadata

class HashTable:
    def __init__(self):
        self.table = {}
        self.ckpt_name = "hashtable.ckpt"
        self.log_name = "hashtable.log"
        self.log_recover()
        self.log_count = 0
        self.txn_file = open(self.log_name, "a+")
    
################################################
# Assignment 2: Basic Table Operations
################################################

    # may need further sanitation
    # if keys become unique we will have to return them from insert
    def makekey( self, key ):
        return key
    
    def insert( self, key, value ):
        # should not log insert until we know the file is written to disk
        self.table[self.makekey(key)] = value
        self.log_insert(key, value)

    def remove( self, key ):
        self.log_remove(key)
        return self.table.pop(self.makekey(key))

    def lookup( self, key ):
        return self.table[self.makekey(key)]

    def size( self ):
        return (len(self.keys()))
    
    def query( self, key ):
        result = False
        try:
            value = self.table[key]
            result = True
        except KeyError:
            pass
        return result

################################################
# Assignment 3: Checkpoint and Transaction Log #
################################################

    def log_insert( self, key, value ):
        record = { "method":"insert","key":key,"value":value.__dict__ }
        self.log_record(record)

    def log_remove( self, key ):
        record = { "method":"remove","key":key }
        self.log_record(record)

    # When adding a record to the transaction log, it is
    # essential to flush the output and force records to disk

    def log_record( self, record ):
        line = json.dumps(record)
        self.txn_file.write(line+"\n")
        self.txn_file.flush()
        os.fsync(self.txn_file)
        self.log_count += 1
        if self.log_count>100:
            self.log_compact()
            self.log_count = 0

    # To compact the log, save a new checkpoint file,
    # commit it atomically via rename, and then delete the
    # transaction log.

    def log_compact( self ):
        with open("table.ckpt.new","w") as f:
            data = json.dumps(self.table)
            f.write(data)
            f.flush()
            os.fsync(f)

        os.rename("table.ckpt.new","table.ckpt")
        self.txn_file.close()
        os.unlink("table.log")
        self.txn_file = open("table.log","a+")

    # To recover, simply load the entire checkpoint file,
    # then read in transactions one by one, and apply them.

    def log_recover( self ):
        # If the checkpoint and transaction files do
        # not yet exist, then create them in an empty state.

        if not os.path.exists(self.ckpt_name):
            with open(self.ckpt_name,"w") as f:
                f.write("{}\n")

        if not os.path.exists(self.log_name):
            with open(self.log_name,"w") as f:
                pass

        # Now recover the checkpoint file

        print("recovering " + self.ckpt_name)
        cfile = open(self.ckpt_name,"r")
        table = json.load(cfile)
        for key, value_dict in table.items():
            metadata = HTFileMetadata(filename=value_dict['filename'],
                                      size=value_dict['size'],
                                      file=None,
                                      path_on_disk=value_dict['path_on_disk'])
            self.table[key] = metadata
        cfile.close()

        # And play the transaction log
        print("recovering " + self.log_name)
        for line in open(self.log_name,"r"):
            record = json.loads(line)
            key = self.makekey(record["key"])
            if record['method']=="insert":
                metadata = HTFileMetadata(filename=record["value"]['filename'],
                                          size=record["value"]['size'],
                                          file=None,
                                          path_on_disk=record["value"]['path_on_disk'])
                self.table[key] = metadata
            elif record['method']=="remove":
                self.table.pop(key)
            else:
                raise Exception("Invalid transaction type!")
            
        # check the disk for the file data described in the table
        marked_for_deletion = []
        for filename, metadata in self.table.items():
            if os.path.exists(metadata.path_on_disk):
                # check if the size matches, later we can do a hash, checksum etc.
                actual_size = os.path.getsize(metadata.path_on_disk)
                if actual_size != metadata.size:
                    print(f"Failed to recover {filename}: size mismatch (expected {metadata.size}, got {actual_size})")
                    marked_for_deletion.append(filename)
                    continue
            else:
                print(f"Failed to recover {filename}: file not found on disk")
                marked_for_deletion.append(filename)
                continue

        for filename in marked_for_deletion:
            self.table.pop(filename)

        print("Recovered Files: " + ", ".join(self.table.keys()))

