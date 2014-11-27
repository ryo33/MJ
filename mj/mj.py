import dictionary
import random

class MJ:
    def __init__(self):
        self.dic = dictionary.Dictionary("MJ.db");

    def memory(self, tokens):
        if len(tokens) == 0:
            return True
        words = []
        for token in tokens:
            words.append(self.dic.memory_word(token))
        for i in range (0, len(words)):
            if i == 0:
                first = None
            else:
                first = words[i - 1]
            if i == len(words) - 1:
                third = None
            else:
                third = words[i + 1]
            self.dic.memory_chain([first, words[i], third])
        self.dic.commit()
        return False

    def talk(self):
        count = self.dic.fetchone("SELECT COUNT(`id`) FROM `word`")[0];
        word = self.dic.fetchone("SELECT `id` FROM `word` LIMIT " + str(self.rand(count)) + ", 1")
        count = self.dic.fetchone("SELECT COUNT(`id`) FROM `chain` WHERE `second` = ?", word)[0];
        chain = self.dic.fetchone("SELECT `first`, `second`, `third` FROM `chain` WHERE `second` = ? LIMIT " + str(self.rand(count)) + ", 1", word)
        return self.search_back(chain) + "".join([self.dic.fetchone("SELECT `word` FROM `word` WHERE `id` = ?", i)[0] for i in chain if i]) + self.search_forward(chain)

    def search_back(self, chain):
        if chain and chain[0]:
            count = self.dic.fetchone("SELECT COUNT(`id`) FROM `chain` WHERE `second` = ? AND `third` = ?", (chain[0], chain[1]))[0];
            chain = self.dic.fetchone("SELECT `first`, `second`, `third` FROM `chain` WHERE `second` = ? AND `third` = ? LIMIT " + str(self.rand(count)) + ", 1", (chain[0], chain[1]))
            if chain[0]:
                return self.search_back(chain) + self.dic.fetchone("SELECT `word` FROM `word` WHERE `id` = ?", chain[0])[0]
        return ""

    def search_forward(self, chain):
        if chain and chain[2]:
            count = self.dic.fetchone("SELECT COUNT(`id`) FROM `chain` WHERE `first` = ? AND `second` = ?", (chain[1], chain[2]))[0];
            chain = self.dic.fetchone("SELECT `first`, `second`, `third` FROM `chain` WHERE `first` = ? AND `second` = ? LIMIT " + str(self.rand(count)) + ", 1", (chain[1], chain[2]))
            if chain[2]:
                return self.dic.fetchone("SELECT `word` FROM `word` WHERE `id` = ?", chain[2])[0] + self.search_forward(chain)
        return ""

    def rand(self, rand_width):
        if rand_width > 1:
            return random.randint(0, rand_width - 1)
        else:
            return 0
