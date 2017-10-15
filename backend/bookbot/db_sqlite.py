import sqlite3

class DB_SQLite:

    def __init__(self, dbname="bookbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        table_statement = "CREATE TABLE IF NOT EXISTS person (nom text NOT NULL, telf text NOT NULL, mail text, barri text, llibre_buscat text, llibre_donat text, PRIMARY KEY (nom, telf))"
        # pure_url = "CREATE TABLE IF NOT EXISTS pure_url (data  real)"
        decoded_url = "CREATE TABLE IF NOT EXISTS decoded_url (data text)"
        #json_url = "CREATE TABLE IF NOT EXISTS json_url (data text)"
        # WHATCHOUT! Added two indeces to make both get_records() and get_items() faster,
        # but chan take up too much space when dealing with a lot of data
        record_index = "CREATE INDEX IF NOT EXISTS recordIndex ON records (description ASC)"
        owner_index = "CREATE INDEX IF NOT EXISTS ownIndex ON records (user ASC)"
        self.conn.execute(table_statement)
        self.conn.execute(decoded_url)
        self.conn.execute(record_index)
        self.conn.execute(owner_index)
        self.conn.commit()

    def get_records(self, llibre_donat_ins, llibre_buscat_ins):
        stmt = "SELECT nom, telf, mail, barri FROM person WHERE (llibre_buscat = (?) AND llibre_donat = (?))"
        args = (llibre_donat_ins, llibre_buscat_ins)
        return [x for x in self.conn.execute(stmt, args)]

    def add_record(self, nom, telf, mail, barri, llibre_buscat, llibre_donat):
        stmt = "INSERT INTO person (nom, telf, mail, barri, llibre_buscat, llibre_donat) VALUES (?, ?, ?, ?, ?, ?)"
        args = (nom, telf, mail, barri, llibre_buscat, llibre_donat)
        self.conn.execute(stmt, args)
        self.conn.commit()

    
    def add_decoded_url(self, received_data):
        stmt = "INSERT INTO decoded_url (data) VALUES (?)"
        args = (received_data, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_record(self, nom, telf):
        stmt = "DELETE FROM person WHERE nom = (?) AND telf = (?)"
        args = (nom, telf)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_all(self):
        stmt = "DROP TABLE person"
        self.conn.execute(stmt)
        self.conn.commit()
# Ignasi Oliver, Pau Nunez, Nil Quera, @HACKUPC Fall 2017
