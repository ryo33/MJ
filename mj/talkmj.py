import mj as MJ
import tinysegmenter
# from parse_command import *

def main():
    mj = MJ.MJ()
    seg = tinysegmenter.TinySegmenter()
    while True:
        sentence = input("\t> ")
        if len(sentence) == 0:
            print("end")
            exit()
        else:
            mj.memory(seg.tokenize(sentence));
            print(repr(mj.talk()))

if __name__ == "__main__":
    main()

