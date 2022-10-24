def boolInput(chars):
    flag = 1
    P = -1
    while flag:
        P = input("请输入" + chars + ",用0或1输入,不要带任何其他字符如空格")
        if (P == '0') | (P == '1'):
            flag = 0
        else:
            print("输入错误，请重新输入")
    print("输入的", chars, "为", P)
    R = bool(int(P))
    return R


def displayer(truth_table, var_list, formula_in):
    for char in var_list:
        print(char, end="   ")
    print(formula_in)
    for line in truth_table:
        for elem in line:
            if elem:
                print("1", end="   ")
            else:
                print("0", end="   ")
        print("")  # 换行
