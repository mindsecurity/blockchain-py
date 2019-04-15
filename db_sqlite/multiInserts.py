#!/usr/bin/env python
import sqlite3


dados = [("João", "98901-0109"),
         ("André", "98902-8900"),
         ("Maria", "97891-3321")]

conn = sqlite3.connect('agenda.db')
cur = conn.cursor()

cur.executemany("""
            INSERT INTO agenda ( nome, telefone )
            VALUES ( ?, ? )""", dados)

conn.commit()
cur.close()
conn.close()
