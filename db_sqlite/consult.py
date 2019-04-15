#!/usr/bin/env python
import sqlite3


conn = sqlite3.connect('agenda.db')
cur = conn.cursor()

cur.execute("SELECT * FROM agenda")
resultado = cur.fetchone()
print("Nome: %s\nTelefone: %s" % (resultado))
cur.close()
conn.close()
