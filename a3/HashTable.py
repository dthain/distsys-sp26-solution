# This is the basic implementation of the HashTable
# It does nothing special, and may end up throwing
# exceptions that the server must catch.

import re
import os
import json

class HashTable:
    def __init__(self):
        self.table = {}
    
################################################
# Assignment 2: Basic Table Operations
################################################

    # may need further sanitation
    # if keys become unique we will have to return them from insert
    def makekey( self, key ):
        return key
    
    def insert( self, key, value ):
        self.table[self.makekey(key)] = value

    def remove( self, key ):
        return self.table.pop(self.makekey(key))

    def lookup( self, key ):
        return self.table[self.makekey(key)]

    def size( self ):
        return (len(self.keys()))
    
    def query( self, key ):
        result = []
        try:
            value = self.table[key]
            result = True
        except KeyError:
            pass
        return result
