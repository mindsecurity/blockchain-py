#!/usr/bin/env python
import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError


DB_name = 'test_blockchain.db'

def connect(func):
    """Decorator to (re)open a sqlite database connection when needed.

    A database connection must be open when we want to perform a database query
    but we are in one of the following situations:
    1) there is no connection
    2) the connection is closed

    Parameters
    ----------
    func : function
        function which performs the database query

    Returns
    -------
    inner func : function
    """
    def inner_func(conn, *args, **kwargs):
        try:
            # I don't know if this is the simplest and fastest query to try
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)
    return inner_func

@connect
def create_table(conn, table_name):
    table_name = scrub(table_name)
    sql = 'CREATE TABLE {} (id_index INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'previous_hash TEXT UNIQUE, proof INTEGER, timestamp REAL, transactions TEXT)'.format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)


@connect
def insert_one(conn, previous_hash, proof, timestamp, transactions, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('previous_hash', 'proof', 'timestamp', 'transactions') VALUES (?, ?, ?, ?)"\
        .format(table_name)
    try:
        conn.execute(sql, (previous_hash, proof, timestamp, transactions))
        conn.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            '{}: "{}" already stored in table "{}"'.format(e, previous_hash, table_name))


@connect
def insert_many(conn, items, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('previous_hash', 'proof', 'timestamp', 'transactions') VALUES (?, ?, ?, ?)"\
        .format(table_name)
    entries = list()
    for x in items:
        entries.append((x['previous_hash'], x['proof'], x['timestamp'], x['transactions']))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
              .format(e, [x['previous_hash'] for x in items], table_name))


@connect
def select_one(conn, item_name, table_name):
    table_name = scrub(table_name)
    item_name = scrub(item_name)
    sql = 'SELECT * FROM {} WHERE previous_hash="{}"'.format(table_name, item_name)
    c = conn.execute(sql)
    result = c.fetchone()
    if result is not None:
        return tuple_to_dict(result)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'
            .format(item_name, table_name))


@connect
def select_all(conn, table_name):
    table_name = scrub(table_name)
    sql = 'SELECT * FROM {}'.format(table_name)
    c = conn.execute(sql)
    results = c.fetchall()
    return list(map(lambda x: tuple_to_dict(x), results))


@connect
def update_one(conn, previous_hash, proof, timestamp, transactions, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE previous_hash=? LIMIT 1)'\
        .format(table_name)
    sql_update = 'UPDATE {} SET proof=?, timestamp=?, transactions=? WHERE previous_hash=?'\
        .format(table_name)
    c = conn.execute(sql_check, (previous_hash,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_update, (proof, timestamp, transactions, previous_hash))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table "{}"'
            .format(previous_hash, table_name))


@connect
def delete_one(conn, previous_hash, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE previous_hash=? LIMIT 1)'\
        .format(table_name)
    table_name = scrub(table_name)
    sql_delete = 'DELETE FROM {} WHERE previous_hash=?'.format(table_name)
    c = conn.execute(sql_check, (previous_hash,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_delete, (previous_hash,))  # we need the comma
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored in table "{}"'
            .format(previous_hash, table_name))


def connect_to_db(db=None):
    """Connect to a sqlite DB. Create the database if there isn't one yet.

    Open a connection to a SQLite DB (either a DB file or an in-memory DB).
    When a database is accessed by multiple connections, and one of the
    processes modifies the database, the SQLite database is locked until that
    transaction is committed.

    Parameters
    ----------
    db : str
        database name (without .db extension). If None, create an In-Memory DB.

    Returns
    -------
    connection : sqlite3.Connection
        connection object
    """
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection


def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum())


def tuple_to_dict(mytuple):
    mydict = dict()
    mydict['id_index'] = mytuple[0]
    mydict['previous_hash'] = mytuple[1]
    mydict['timestamp'] = mytuple[2]
    mydict['transactions'] = mytuple[3]
    return mydict

def main():

    table_name = 'blocks'
    conn = connect_to_db()  # in-memory database
    # conn = connect_to_db(DB_name)  # physical database (i.e. a .db file)

    create_table(conn, table_name)

    my_items = [
    {'previous_hash': 'bread', 'proof': 0.35, 'timestamp': 20, 'transactions': 'bla bla bla'},
    {'previous_hash': 'daf09', 'proof': 05.11, 'timestamp': 440, 'transactions': 'f 8safu fasd8f'},
    {'previous_hash': 'l1k2j', 'proof': 431.95, 'timestamp': 6780, 'transactions': '9dsaf09sd '},
    ]

    # CREATE
    insert_many(conn, my_items, table_name='blocks')
    insert_one(conn, 'bread2', proof=2.0, timestamp=552345, transactions='bbla123adfda s2343asdf 242asda', table_name='blocks')
    # if we try to insert an object already stored we get an ItemAlreadyStored
    # exception
    # insert_one(conn, 'milk', price=1.0, quantity=3, table_name='items')

    # READ
    print('SELECT bread')
    print(select_one(conn, 'bread', table_name='blocks'))
    print('SELECT all')
    print(select_all(conn, table_name='blocks'))
    # if we try to select an object not stored we get an ItemNotStored exception
    # print(select_one(conn, 'pizza', table_name='items'))

    # conn.close()  # the decorator @connect will reopen the connection

    # UPDATE
    print('UPDATE bread, SELECT bread')
    update_one(conn, 'bread', proof=1324.5, timestamp=52633566, transactions='adoijfa 9asdf f09fa sd', table_name='blocks')
    print(select_one(conn, 'bread', table_name='blocks'))
    # if we try to update an object not stored we get an ItemNotStored exception
    # print('UPDATE pizza')
    # update_one(conn, 'pizza', price=1.5, quantity=5, table_name='items')

    # DELETE
    print('DELETE bread2, SELECT all')
    delete_one(conn, 'bread2', table_name='blocks')
    print(select_all(conn, table_name='blocks'))
    # if we try to delete an object not stored we get an ItemNotStored exception
    # print('DELETE fish')
    # delete_one(conn, 'fish', table_name='items')

    # save (commit) the changes
    # conn.commit()

    # close connection
    conn.close()

if __name__ == '__main__':
    main()
