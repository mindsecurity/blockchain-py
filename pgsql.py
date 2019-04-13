#!/usr/bin/env python3
import psycopg2
import config, sys
from configparser import ConfigParser



db_id, db_cnpj, db_name, db_email = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

sql = """ INSERT INTO companies ( id, cnpj, name, email )
          VALUES ( %s, %s, '%s', '%s' )
      """ % (db_id, db_cnpj, db_name, db_email)

def config(filename='db.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect(db_id, db_cnpj, db_name, db_email):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into mobile table")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect(db_id,db_cnpj,db_name,db_email)
