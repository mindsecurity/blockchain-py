#!/usr/bin/env python
import sqlite3


conn = sqlite3.connect('agenda.db')
cur = conn.cursor()

cur.execute(""" DELETE FROM agenda
                WHERE nome = 'André' """)
print("Registros apagados: ",  cur.rowcount)

if cur.rowcount == 1:
    conn.commit()
    print("Alterações gravadas.")
else:
    conn.rollback()
    print("Alterações abortadas.")

cur.close()
conn.close()
