#!/usr/bin/env python
import sqlite_backend


class ModelSQLite(object):

    def __init__(self, application_items):
        self._item_type = 'product'
        self._connection = sqlite_backend.connect_to_db(sqlite_backend.DB_name)
        sqlite_backend.create_table(self.connection, self._item_type)
        self.create_items(application_items)

    @property
    def connection(self):
        return self._connection

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def create_item(self, previous_hash, proof, timestamp, transactions):
        sqlite_backend.insert_one(
            self.connection, previous_hash, proof, timestamp, transactions, table_name=self.item_type)

    def create_items(self, items):
        sqlite_backend.insert_many(
            self.connection, items, table_name=self.item_type)

    def read_item(self, previous_hash):
        return sqlite_backend.select_one(
            self.connection, previous_hash, table_name=self.item_type)

    def read_items(self):
        return sqlite_backend.select_all(
            self.connection, table_name=self.item_type)

    def update_item(self, previous_hash, proof, timestamp, transactions):
        sqlite_backend.update_one(
            self.connection, previous_hash, proof, timestamp, transactions, table_name=self.item_type)

    def delete_item(self, previous_hash):
        sqlite_backend.delete_one(
            self.connection, previous_hash, table_name=self.item_type)


if __name__ == '__main__':


    my_items = [
        {'previous_hash': 'bread', 'proof': 0.35, 'timestamp': 20, 'transactions': 'bla bla bla'},
        {'previous_hash': 'daf09', 'proof': 05.11, 'timestamp': 440, 'transactions': 'f 8safu fasd8f'},
        {'previous_hash': 'l1k2j', 'proof': 431.95, 'timestamp': 6780, 'transactions': '9dsaf09sd '},
    ]

    c = Controller(ModelSQLite(my_items), View())
    c.show_items()
    c.show_items(bullet_points=True)
    c.show_item('daf09')
    c.show_item('bread')

    c.insert_item('bread', proof=102432, timestamp=5873673, transactions='afjaf09 fsf09sdjf')
    c.insert_item('chocolate', proof=224340, timestamp=938427410, transactions='aasd09f a 0fa sf9d0')
    c.show_item('chocolate')

    c.update_item('bread', proof=1243232, timestamp=2330, transactions='bla bla')
    c.update_item('chocolate', proof=3455, timestamp=2440, transactions='buh buh')

    c.delete_item('daf09')
    c.delete_item('bread')

    c.show_items()

    # we close the current sqlite database connection explicitly
    if type(c.model) is ModelSQLite:
        sqlite_backend.disconnect_from_db(
            sqlite_backend.DB_name, c.model.connection)
        # the sqlite backend understands that it needs to open a new connection
        c.show_items()
