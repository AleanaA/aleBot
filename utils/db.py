import sqlite3
from sqlite3 import Error

class Database:
    def connect(self):
        try:
            conn = sqlite3.connect("database.db")
            return conn
        except Error as e:
            print(e)

    def close(self, db):
        db.commit()
        db.close()

    def insert(self, table, values):
        db = self.connect()
        cur = db.cursor()
        cur.execute("INSERT INTO {0} VALUES {1}".format(table, values))
        cur.close()
        self.close(db)
    
    def getrows(self, table, row=None):
        db = self.connect()
        cur = db.cursor()
        if row:
            cur.execute("SELECT * FROM {0} WHERE rowid = {1}".format(table, row))
        else:
            cur.execute("SELECT * FROM {0}".format(table))
        r = cur.fetchall()
        cur.close()
        self.close(db)
        return r

    def delete(self, table, row):
        db = self.connect()
        cur = db.cursor()
        cur.execute("DELETE FROM {0} WHERE rowid = {1}".format(table, row))
        cur.close()
        self.close(db)

    def user_table(self, userid):
        db = self.connect()
        cur = db.cursor()
        cur.execute("CREATE table IF NOT EXISTS {} (titles)".format(userid))
        cur.close()
        self.close(db)

    def guild_table(self, guildid):
        db = self.connect()
        cur = db.cursor()
        cur.execute("CREATE table IF NOT EXISTS {} (role, permission_level)".format(guildid))
        cur.close()
        self.close(db)