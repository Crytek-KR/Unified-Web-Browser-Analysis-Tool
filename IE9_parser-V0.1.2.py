# -*- coding: utf-8 -*-

import re
import binascii
import os
import sqlite3

filepath = "index.dat"

block_size = 128
signature = "55524c20"

count=0


def IE9parser():
    con = sqlite3.connect("IE9parser.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE URL(DataA text)")
    index=0
    gdata = {}
    with open(filepath, "rb") as f:
        for m in re.finditer( b'\x55\x52\x4c\x20', f.read()):
            #print "%X" % m.start()
            f.seek(m.start()+4)

            block_count = f.read(4).encode("hex")
            record_size = block_size * int("".join([block_count[i:i+2] for i in range(0, len(block_count), 2)][::-1]).lstrip('0'), 16)

            f.seek(m.start() + 104) #Move to URL STRING
            data = f.read(record_size - 104).split(b'\x00')
            
            #for i in range(1,200):
            #    f2 = open("IE9parser.txt",'w')
            #    f2.write(data[0])
            #    f2.close
            print data[0]
            #print index
            gdata[index] = data[0]
            #print gdata[index]
            #print data[1]
            #print data[2]

            
            cursor.execute("INSERT INTO URL VALUES(?)", [gdata[index]])
            index = index+1
            print index
            #index=index+1
        con.commit()
        con.close()
    
if __name__ == '__main__':
    IE9parser()
