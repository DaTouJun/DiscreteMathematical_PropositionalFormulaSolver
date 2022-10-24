# GuanSheng 2022.10

"""
用!表示否定
用∧表示合取
用∨表示析取
用→表示条件
用↔表示双条件
原子命题请用大写字母表示
"""

"""
优先级：非>合取>析取>条件>双条件
"""


class Formula:
    # 这里是类的初始化函数，将重置一些变量并接受输入
    def __init__(self):
        self.operatorList = ["↔", "→", "∨", "∧", "!", "(", ")", "#"]  # 这是存储操作符的列表
        self.inStr = ''  # 输入的命题公式字符串
        self.suffixStr = ''  # 命题公式转后缀表达式的字符串
        self.numProposition = 0  # 这是命题变元的个数
        self.varList = []  #
        self.truthTable = []
        state1 = True
        while state1:  # 循环接受输入
            self.printHint()
            print("请输入命题公式")
            self.inStr = input()
            self.inStr = self.inStr.replace(" ", "")  # 去除空格
            state1 = not self._validationTest()  # 检查输入问题
        print("成功输入命题公式")
        self._countVariable()
        self._calculateSuffixString()  # 计算后缀表达式
        print("后缀表达式为" + self.suffixStr)
        assignTable = Formula._generateAssignTable(self.numProposition)  # 得到指派表
        for lp1 in assignTable:
            res = self._calculateTruthTable(lp1)  # 计算得到真值表
            lNew = lp1.copy()  # 复制一份指派的list
            lNew.append(res)  # 在最后加上结果
            self.truthTable.append(lNew)  # 把算完的压到真值表中

    # 输入检查
    def _validationTest(self):
        state = True
        for i in range(0, len(self.inStr) - 1):
            if self._isOperator2(self.inStr[i]) & self._isOperator2(self.inStr[i + 1]):
                print("输入错误，发现两联结词相连")
                state = False
                break
            if self.inStr[i].isupper() & self.inStr[i + 1].isupper():
                print("输入错误，发现两原子命题相连")
                state = False
                break
            if not (self._isOperator1(self.inStr[i]) | (self._isOperator2(self.inStr[i])) | (
                    self.inStr[i].isupper()) | (self.inStr[i] == "(") | (self.inStr[i] == ")")):
                print("输入错误，发现未知符号")
                state = False
                break
            if self._isOperator2(self.inStr[i]) & (self.inStr[i + 1] == ")"):
                print("输入错误，发现二元联结词前后无匹配")
                state = False
                break
            if self.inStr[i].isupper() & (self._isOperator1(self.inStr[i + 1])):
                print("输入错误，命题变元后应跟双目联结词")
                state = False
                break
            if self.inStr[i].isupper() & (self.inStr[i + 1] == "("):
                print("输入错误，命题变元后不能紧跟括号")
                state = False
                break
            if (self.inStr[i] == ")") & self.inStr[i + 1].isupper():
                print("输入错误，命题变元前不能紧跟括号")
                state = False
                break

        for i in range(0, len(self.inStr)):
            if self.inStr[i].islower():
                print("输入错误，发现小写字母")
                state = False
                break
            if self.inStr[i].isnumeric():
                print("输入错误，发现数字")
                state = False
                break

        countC = 0  # 记录括号匹配
        for c in self.inStr:
            if c == '(':
                countC += 1
            if c == ')':
                countC -= 1
            if countC < 0:
                state = False
        if countC != 0:
            print("输入错误，发现括号不匹配")
            state = False

        return state

    # 原子命题计数
    def _countVariable(self):
        for c in self.inStr:
            if c.isupper():
                if c not in self.varList:
                    self.varList.append(c)
        self.varList.sort()
        self.numProposition = self.varList.__len__()

    # 根据输入的，计算整个命题公式的真值
    def _calculateTruthTable(self, assign_list):
        assignDict = self._getAssignDictionary(assign_list)  # 得到对每一个原子命题的指派
        strToCalcu = self.suffixStr  # 复制一份后缀表达式
        stackToCalcu = []  # 准备后缀表达式的list，并在下一句完成转换
        for i in range(strToCalcu.__len__() - 1, -1, -1):
            stackToCalcu.append(strToCalcu[i])
        stackComputing = []  # 临时存储结果的栈
        while stackToCalcu.__len__():  # 如果后缀表达式没算完就继续
            nextElem = stackToCalcu.pop()  # 得到下一个元
            if not (Formula._isParenthesis(nextElem) | Formula._isOperator1(nextElem) | Formula._isOperator2(
                    nextElem)):  # 如果是一个变元
                stackComputing.append(assignDict[nextElem])  # 压到结果栈中，并完成向真值的转换
            elif Formula._isOperator1(nextElem):  # 如果是个单目运算符
                operand1 = stackComputing.pop()  # 从结果栈中抽一个
                res = Formula._operatorNot(operand1, assignDict)  # 计算下
                stackComputing.append(res)  # 算完压栈
            elif Formula._isOperator2(nextElem):  # 如果是个双目运算符
                operand2 = stackComputing.pop()  # 先抽第二个
                operand1 = stackComputing.pop()  # 再抽第一个
                if nextElem == "∧":  # 析取求与
                    res = Formula._operatorAnd(operand1, operand2, assignDict)
                elif nextElem == "∨":  # 合取求或
                    res = Formula._operatorOr(operand1, operand2, assignDict)
                elif nextElem == "→":  # 双条件求双条件
                    res = Formula._operatorCondition(operand1, operand2, assignDict)
                else:  # 必定是双条件了
                    res = Formula._operatorDoubleCondition(operand1, operand2, assignDict)
                stackComputing.append(res)  # 算完压回去
        res = stackComputing[0]  # 全部算完拿结果
        return res  # 返回结果

    # 由中缀表达式得到后缀表达式
    def _calculateSuffixString(self):
        priDictionary = Formula._getPriDict()  # 得到优先级字典
        OPND = []  # 结果操作数栈
        OPTR = ["#"]  # 临时运算符栈
        formula = self.inStr  # 复制命题公式
        formula = formula.__add__("#")  # 加一个#用来表示结尾
        formulaCharList = []  # 需要算的命题公式转换成list便于操作
        for i in range(formula.__len__() - 1, -1, -1):
            formulaCharList.append(formula[i])
        while OPTR.__len__() != 0:  # 运算符栈空了截止
            if formulaCharList.__len__():  # 需要算的不空则进行即使暖
                nextOp = formulaCharList[formulaCharList.__len__() - 1]  # 得到下一个操作标识
                # 若是操作数则直接压栈到结果OPND中
                if not (Formula._isOperator2(nextOp) | Formula._isOperator1(nextOp) | Formula._isParenthesis(nextOp) | (
                        nextOp == "#")):
                    OPND.append(formulaCharList.pop())
                else:  # 不是操作数可能是括号、操作符、#号
                    top = OPTR[OPTR.__len__() - 1]  # 拿操作符栈顶
                    key = nextOp + top  # 得到key查字典
                    pri = priDictionary[key]  # 查字典
                    if pri == 1:  # 如果为1则将下一个操作符压栈
                        OPTR.append(formulaCharList.pop())
                    elif pri == 0:  # 如果为0俩符相消
                        OPTR.pop()  # 弹出丢掉
                        formulaCharList.pop()  # 弹出丢掉
                    elif pri == -1:  # 如果为-1则将OPTR的压到结果OPND中
                        while pri == -1:  # 循环压入
                            OPND.append(OPTR.pop())  #
                            top = OPTR[OPTR.__len__() - 1]
                            key = nextOp + top
                            pri = priDictionary[key]
                    elif pri == -32:  # -32不匹配肯定错了
                        print("ERROR!!!!，表达式有误")
                        exit(0)
                        return
            else:  # 需要算的没了，剩余算符压栈
                OPND.append(OPTR.pop())
        self.suffixStr = "".join(OPND)  # 合成list为string

    # 得到指派的字典，用来给变元赋值
    def _getAssignDictionary(self, table_list_in):  # 得到指派表
        dictionary = {}  # 拿一个空的
        for var in self.varList:
            dictionary[var] = table_list_in[self.varList.index(var)]  # 用真值表对每一个命题变元指派
        dictionary[False] = False  # 避免算完的再算没有key
        dictionary[True] = True  # 避免算完的再算没有key
        return dictionary  # 返回

    # 输出提示信息,静态方法
    @staticmethod
    def printHint():
        print("输入的公式中请参考下列输入，可以有空格但是要匹配")
        print("""           用!表示否定
            用∧表示合取
            用∨表示析取
            用→表示条件
            用↔表示双条件
            原子命题请用单个大写字母表示
        不支持多个字母的命题变元""")

    # 判断是否是单目联结词
    @staticmethod
    def _isOperator1(chara):
        opList = ['!']
        if chara in opList:
            return True
        else:
            return False

    # 判断是否是联结词
    @staticmethod
    def _isOperator2(chara):
        opList = ['∧', '∨', '→', '↔']
        if chara in opList:
            return True
        else:
            return False

    # 判断是否是括号
    @staticmethod
    def _isParenthesis(chara):
        list = ["(", ")"]
        if chara in list:
            return True
        else:
            return False

    # 生成指派表
    @staticmethod
    def _generateAssignTable(nums):
        lists = []
        for i in range(0, 2 ** nums):  # 第i行
            tempLs = []
            for j in range(0, nums):
                s = bool(int(i % 2 ** (nums - j) / 2 ** (nums - j - 1)))
                tempLs.append(s)
            lists.append(tempLs)
        return lists

    # 计算合取
    @staticmethod
    def _operatorAnd(operand1, operand2, dictionary):
        return dictionary[operand1] & dictionary[operand2]

    # 计算析取
    @staticmethod
    def _operatorOr(operand1, operand2, dictionary):
        return dictionary[operand1] | dictionary[operand2]

    # 计算条件
    @staticmethod
    def _operatorCondition(operand1, operand2, dictionary):
        return (not dictionary[operand1]) | dictionary[operand2]

    # 计算双条件
    @staticmethod
    def _operatorDoubleCondition(operand1, operand2, dictionary):
        return (dictionary[operand1] & dictionary[operand2]) | ((not dictionary[operand1]) & (not dictionary[operand2]))

    # 计算否定
    @staticmethod
    def _operatorNot(operand, dictionary):
        return not dictionary[operand]

    # 生成优先级字典
    @staticmethod
    def _getPriDict():
        operatorList = ["↔", "→", "∨", "∧", "!", "(", ")", "#"]  # 这是存储操作符的列表
        # 这是一个二维权级表
        # 输入两个字符，前边的栈顶，可以入栈
        priForm = [
            [1, -1, -1, -1, -1, 1, -1, 1],  # ↔
            [1, 1, -1, -1, -1, 1, -1, 1],  # →
            [1, 1, 1, -1, -1, 1, -1, 1],  # ∨
            [1, 1, 1, 1, -1, 1, -1, 1],  # ∧
            [1, 1, 1, 1, 1, 1, -1, 1],  # !
            [1, 1, 1, 1, 1, 1, 1, 1, 1],  # (
            [-1, -1, -1, -1, -1, 0, -1, -32],  # )
            [-1, -1, -1, -1, -1, -1, -1, 0]  # #
        ]
        # 这是优先级的表格1代表前高，0代表相等，-1代表后高
        # 其中，1是压栈，0是出栈相消，-1要出栈并压入结果栈
        priDictionary = {}  # 这是用来存储优先级的字典
        # 压入字典
        for i in range(0, 8):
            for j in range(0, 8):
                key = operatorList[i] + operatorList[j]
                priDictionary[key] = priForm[i][j]
        return priDictionary  # 返回优先级字典
