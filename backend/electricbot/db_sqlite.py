import sqlite3

class DB_SQLite:

    def __init__(self, dbname="electricbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        table_statement = "CREATE TABLE IF NOT EXISTS records (description text, user text)"
        # WHATCHOUT! Added two indeces to make both get_records() and get_items() faster,
        # but chan take up too much space when dealing with a lot of data
        record_index = "CREATE INDEX IF NOT EXISTS recordIndex ON records (description ASC)"
        owner_index = "CREATE INDEX IF NOT EXISTS ownIndex ON records (user ASC)"
        self.conn.execute(table_statement)
        self.conn.execute(record_index)
        self.conn.execute(owner_index)
        self.conn.commit()

    def get_records(self, user):
        stmt = "SELECT description FROM records WHERE user = (?)"
        args = (user, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def add_record(self, record_text, user):
        stmt = "INSERT INTO records (description, user) VALUES (?, ?)"
        args = (record_text, user)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_record(self, record_text, user):
        stmt = "DELETE FROM records WHERE description = (?) AND user = (?)"
        args = (record_text, user )
        self.conn.execute(stmt, args)
        self.conn.commit()
# Ignasi Oliver, Pau Nunez, Nil Quera, @HACKUPC Fall 2017
