import mj
import tinysegmenter
import sys

if __name__ == "__main__":
    mj = mj.MJ()
    seg = tinysegmenter.TinySegmenter()
    with open(sys.argv[1], "r") as f:
        sentences = f.readlines()
        for sentence in sentences:
            mj.memory(seg.tokenize(sentence))
    for i in range(0, 20):
        print(mj.talk())
