#!/usr/bin/env python
import sqlite3, json, sys

tr_name01 = 'sender'
tr_name02 = 'receiver'
tr_name03 = 'amount'

ID = sys.argv[1]
TABLE = sys.argv[2]

value1 = 'SELECT {ny} FROM chain2 WHERE id_index == "{nn}"'.format(ny=TABLE, nn=ID)
value2 = 'SELECT {ny} FROM chain2 WHERE id_index == "{nn}"'.format(nn=ID)
value3 = 'SELECT {ny} FROM chain2 WHERE id_index == "{nn}"'.format(nn=ID)
value4 = 'SELECT {ny} FROM chain2 WHERE id_index == "{nn}"'.format(nn=ID)
value5 = 'SELECT {ny} FROM chain2 WHERE id_index == "{nn}"'.format(nn=ID)

conn = sqlite3.connect('blockchain.db')
cur = conn.cursor()

RESPONSE = { 'message': "New Block Forged",
        'index': table_name1,
        'transactions': table_name5["{t1}", "{t2}", "{t3}".format(t1=tr_name01, t2=tr_name02, t3=tr_name03)],
        'proof': table_name4,
        'previous_hash': table_name2
    }
RESPONSE = json.dumps(RESPONSE)
RESPONSE =json.loads(json.dumps(RESPONSE))

CREATE = cur.execute('CREATE TABLE chain2(id_index INTEGER, previous_hash TEXT, proof INTEGER, timestamp NUMERIC, transactions TEXT)')
INSERT = cur.execute("INSERT INTO chain ( id_index, previous_hash, proof, timestamp, transactions ) VALUES ( {tn}, {nf}, {ny}, {un}, {ty} )".format(tn=ID, nf=RESPONSE, ny=value3, un=value4, ty=value5))

conn.commit()
cur.close()
conn.close()
