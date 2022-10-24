#  Copyright (c)  GuanSheng 2022.

import Exp2_Formula as lib1  # 为代码文件夹中的Exp2_Formula文件，用于处理命题公式的库
import InAndOut as IO       # 调用IO库，实现布尔输入和转换等

# 主入口点

state = True
while state:
    # 获得命题公式对象
    formula = lib1.Formula()

    # 打印命题变元
    print("共有%d个命题变元,分别是" % formula.numProposition)
    for c in formula.varList:
        print(c, "  ", end="")
    print("")

    # 主范式
    # l 记录小项
    # b 记录大项
    l = []
    b = []
    for i in range(0, 2 ** formula.numProposition):
        res = formula.truthTable[i][formula.truthTable[i].__len__() - 1]
        if res:
            l.append(i)
        else:
            b.append(i)

    if l.__len__() == 0:
        print("主析取范式为空")
    else:
        print("计算出主析取范式为")
        print(formula.inStr)
        print("⇔", end='  ')
        for elem in l:
            print("(", end="")
            for var in range(0, formula.numProposition):
                if formula.truthTable[elem][var]:
                    print("!" + formula.varList[var] + "∧", end="")
                else:
                    print(formula.varList[var] + "∧", end="")
            print("\b", end="")
            print(")∨", end="")
        print("\b")

        print("⇔", end='  ')
        for elem in l:
            print("m" + elem.__str__() + "∨", end="")
        print("\b")

    if b.__len__() == 0:
        print("主合取范式为空")
    else:
        print("计算出主合取范式为")
        print(formula.inStr)

        print("⇔", end='  ')
        for elem in b:
            print("(", end="")
            for var in range(0, formula.numProposition):
                if formula.truthTable[elem][var]:
                    print("!" + formula.varList[var] + "∨", end="")
                else:
                    print(formula.varList[var] + "∨", end="")
            print("\b", end="")
            print(")∧", end="")
        print("\b")

        print("⇔", end='  ')
        for elem in b:
            print("M" + elem.__str__() + "∧", end="")
        print("\b")

    state = IO.boolInput("是否要继续,1继续,0结束")
    del formula  # 删除对象
print("程序结束")
