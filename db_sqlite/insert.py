#!/usr/bin/env python
import sqlite3


conn = sqlite3.connect('agenda.db')
cur = conn.cursor()

cur.execute("""
             CREATE TABLE agenda (
                 nome text,
                 telefone text)
            """)
cur.execute("""
             INSERT INTO agenda ( nome, telefone )
             VALUES ( ?, ? )
            """, ("Nilo", "7788-1432"))

conn.commit()
cur.close()
conn.close()
