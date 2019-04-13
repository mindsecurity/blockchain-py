#!/usr/bin/env python3
import psycopg2
import config, sys
from configparser import ConfigParser



db_id, db_cnpj, db_name, db_email = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

def config(filename='db.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect(db_id, db_cnpj, db_name, db_email):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

 # execute a statement
        print('Inserting data on PostgreSQL...')
        sql = """ INSERT INTO companies ( id, cnpj, name, email )
                  VALUES ( %s, %s, '%s', '%s' )
            """ % (db_id, db_cnpj, db_name, db_email)

        cur.execute(sql)
        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into mobile table")

     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect(db_id,db_cnpj,db_name,db_email)
