#!/usr/bin/env python
import sqlite3


conn = sqlite3.connect('blockchain.db')
cur = conn.cursor()

cur.execute("SELECT * FROM chain2")
resultado = cur.fetchall()

for row in resultado:
    print("01: %s, 02: %s, 03: %s, 04: %s, 05: %s" % (row))

cur.close()
conn.close()
