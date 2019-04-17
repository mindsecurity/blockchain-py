#!/usr/bin/env python
import sqlite3, sys

value1, value2, value3, value4, value5 = sys.argv[1], str(sys.argv[2]), sys.argv[3], sys.argv[4], str(sys.argv[5])

conn = sqlite3.connect('blockchain.db')
cur = conn.cursor()

#cur.execute('CREATE TABLE chain2(id_index INTEGER, previous_hash TEXT, proof INTEGER, timestamp NUMERIC, transactions TEXT)')
cur.execute('INSERT INTO chain2(id_index, previous_hash, proof, timestamp, transactions) VALUES ( "{nt}", "{ny}", "{nu}", "{ni}", "{no}" )'.format(nt=value1, ny=value2, nu=value3, ni=value4, no=value5))

conn.commit()
cur.close()
conn.close()
