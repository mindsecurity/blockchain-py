create = cur.execute("""
                    CREATE TABLE agenda (
                    nome text,
                    telefone text)
                    """)

insert = cur.execute("""
                    INSERT INTO agenda ( nome, telefone )
                    VALUES ( ?, ? )
                    """, ("Nilo", "7788-1432"))

select = cur.execute("SELECT * FROM agenda")

delete = cur.execute(""" DELETE FROM agenda
                    WHERE nome = 'André' """)

dados = [("João", "98901-0109"),
         ("André", "98902-8900"),
         ("Maria", "97891-3321")]

cur.executemany("""
            INSERT INTO agenda ( nome, telefone )
            VALUES ( ?, ? )""", dados)

