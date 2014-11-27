import sqlite3
import sqliter

class Dictionary(sqliter.Sqliter):
    ID_LENGTH = 16

    def check_db(self):
        if not self.exist_table("word"):
            self.execute("CREATE TABLE `word` (`id` TEXT PRIMARY KEY, `word` TEXT UNIQUE, `count` INT DEFAULT 0, `created` DATETIME DEFAULT CURRENT_TIMESTAMP)")
        if not self.exist_table("chain"):
            self.execute("""CREATE TABLE `chain` (`id` TEXT PRIMARY KEY, `first` TEXT, `second` TEXT, `third` TEXT, `count` INT DEFAULT 0, `created` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(`first`) REFERENCES `word`(`id`), FOREIGN KEY(`second`) REFERENCES `word`(`id`), FOREIGN KEY(`third`) REFERENCES `word`(`id`))""")
        if not self.exist_table("relevance"):
            self.execute("""CREATE TABLE `relevance` (`id` TEXT PRIMARY KEY, `first` TEXT, `second` TEXT, `count` INT DEFAULT 0, `created` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(`first`) REFERENCES `word`(`id`), FOREIGN KEY(`second`) REFERENCES `word`(`id`))""")
        if not self.exist_table("log"):
            self.execute("CREATE TABLE `log` (`id` TEXT PRIMARY KEY, `created` DATETIME DEFAULT CURRENT_TIMESTAMP)")
        if not self.exist_table("log_token"):
            self.execute("""CREATE TABLE `log_token` (`id` TEXT PRIMARY KEY, `log_id` TEXT, `token` TEXT, `created` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(`log_id`) REFERENCES `log`(`id`))""")

    def memory_word(self, word):
        result = self.exist_word(word)
        if result == False:
            return self.insert_word(word)
        else:
            self.add("word", result, "count")
            return result

    def memory_chain(self, chain):
        result = self.exist_chain(chain)
        if result == False:
            return self.insert_chain(chain)
        else:
            self.add("chain", result, "count")
            return result

    def exist_word(self, word):
        result = self.fetchone("SELECT `id` FROM `word` WHERE `word` = ?", [word])
        if result and result[0]:
            return result[0]
        return False

    def exist_chain(self, chain):
        result = self.fetchone("SELECT `id` FROM `chain` WHERE `first` = ? AND `second` = ? AND `third` = ?", chain)
        if result and result[0]:
            return result[0]
        return False

    def insert_chain(self, chain):
        return self.insert("chain", ("first", "second", "third"), chain)

    def insert_word(self, word):
        return self.insert("word", "word", word)

    def get_words_id(self, words):
        return [self.get_word_id(word) for word in words]

    def get_word_id(self, word):
        item_id = self.exist_word(word)
        if item_id:
            return item_id
        else:
            return self.insert_word(word)
