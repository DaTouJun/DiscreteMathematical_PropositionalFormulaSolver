import InAndOut as IO

state = True
while state:
    P = IO.boolInput("P")
    Q = IO.boolInput("Q")
    print("%5s%5s%5s%5s%5s%5s%5s" % ("P", "Q", "非P", "P∧Q", "P∨Q", "P→Q", "P↔Q"))
    print("%5d%5d%5d%5d%5d%5d%5d" % (P, Q, not P, P & Q, P | Q, (not P) | Q, not (P ^ Q)))
    print("是否要继续？是输入1，否输入0")
    state = IO.boolInput("是否要继续")
print("程序结束")
