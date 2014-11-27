import sqlite3
import string, random

class Sqliter:
    ID_LENGTH = 16

    def __init__(self, database="default.db"):
        self.con = sqlite3.connect(database)
        self.cursor = self.con.cursor()
        self.check_db()

    def check_db(self):
        pass

    def exist_table(self, table):
        if self.fetchone("SELECT `name` FROM `sqlite_master` WHERE `type` = \"table\" AND `name` = \"" + table + "\""):
            return True
        else:
            return False

    def update(self, table, item_id, columns, values=[]):
        columns_copy = self.get_list(columns)
        values_copy = self.get_list(values)
        values_copy.append(item_id)
        self.execute("UPDATE `" + table + "` SET " + ", ".join(["`" + column + "` = ?" for column in columns_copy]) + " WHERE `id` = ?", values_copy)

    def add(self, table, item_id, columns, values=[1]):
        columns_copy = self.get_list(columns)
        values_copy = self.get_list(values)
        values_copy.append(item_id)
        self.execute("UPDATE `" + table + "` SET " + ", ".join(["`" + column + "` = `" + column + "` + ?" for column in columns_copy]) + " WHERE `id` = ?", [values_copy[i % len(values_copy)] for i in range(0, len(columns_copy) + 1)])

    def insert(self, table, columns, values=[]):
        columns_copy = self.get_list(columns)
        columns_copy.append("id")
        values_copy = self.get_list(values)
        item_id = self.generate_unique_id(table)
        values_copy.append(item_id)
        self.execute("INSERT INTO `" + table + "`(" + ", ".join(["`" + column + "`" for column in columns_copy]) + ")VALUES(" + ", ".join(["?" for i in values_copy]) + ")", values_copy)
        return item_id

    def fetchone(self, sql, values=[]):
        self.execute(sql, values)
        return self.cursor.fetchone()

    def fetchall(self, sql, values=[]):
        self.execute(sql, values)
        return self.cursor.fetchall()

    def execute(self, sql, values=[]):
        self.cursor.execute(sql, self.get_list(values))

    def commit(self):
        self.con.commit()

    def generate_unique_id(self, table):
        while True:
            item_id = self.generate_id()
            result = self.fetchone("SELECT `id` FROM `" + table + "` WHERE `id` = ?", [item_id])
            if not (result and result[0]):
                return item_id

    def generate_id(self):
        return "".join([random.choice(string.ascii_letters + string.digits + "_") for i in range(0, self.ID_LENGTH)])

    def get_list(self, item):
        if isinstance(item, list):
            return item
        elif isinstance(item, tuple):
            return list(item)
        else:
            return [item]
