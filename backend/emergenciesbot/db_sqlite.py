import sqlite3

class DB_SQLite:

    def __init__(self, dbname="emergenciesbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        table_statement = "CREATE TABLE IF NOT EXISTS emergencies (description text NOT NULL, place text NOT NULL, time text NOT NULL, PRIMARY KEY(description))"
        # pure_url = "CREATE TABLE IF NOT EXISTS pure_url (data  real)"
        record_index = "CREATE INDEX IF NOT EXISTS recordIndex ON records (description ASC)"
        owner_index = "CREATE INDEX IF NOT EXISTS ownIndex ON records (user ASC)"
        self.conn.execute(table_statement)
        #self.conn.execute(record_index)
        #self.conn.execute(owner_index)
        self.conn.commit()

    def get_records(self, ):
        stmt = "SELECT * FROM emergencies"
        args = ()
        return [x for x in self.conn.execute(stmt, args)]

    def add_record(self, description, place, time):
        stmt = "INSERT INTO emergencies VALUES (?, ?, ?)"
        args = (description, place, time)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_record(self, description):
        stmt = "DELETE FROM emergencies WHERE description = (?)"
        args = (description)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_all(self):
        stmt = "DROP TABLE emergencies"
        self.conn.execute(stmt)
        self.conn.commit()
# Ignasi Oliver, Pau Nunez, Nil Quera, @HACKUPC Fall 2017

