#!/usr/bin/env python
import sqlite3


conn = sqlite3.connect('agenda.db')
cur = conn.cursor()

cur.execute("SELECT * FROM agenda")
resultado = cur.fetchall()

for row in resultado:
    print("Nome: %s\nTelefone: %s" % (row))

cur.close()
conn.close()
