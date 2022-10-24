import Exp2_Formula as lib1  # 为代码文件夹中的Exp2_Formula文件，用于处理命题公式的库
import InAndOut as IO

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

    # 打印真值表
    print("真值表为")
    IO.displayer(formula.truthTable, formula.varList, formula.inStr)
    state = IO.boolInput("是否要继续,1继续,0结束")
    del formula # 删除对象
print("程序结束")
