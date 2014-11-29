import mj

if __name__ == "__main__":
    m = mj.MJ()
    while True:
        i = input()
        if i:
            break
        for i in range(0, 10):
            print(m.talk())
