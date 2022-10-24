#  Copyright (c)  GuanSheng 2022.
#
def generateAssignTable(nums):  # 生成一个表，包含所有情况
    lists = []
    for i in range(0, 2 ** nums):  # 第i行
        tempLs = []
        for j in range(0, nums):
            s = bool(int(i % 2 ** (nums - j) / 2 ** (nums - j - 1)))
            tempLs.append(s)
        lists.append(tempLs)
    return lists


def judge(member_list):
    # A B C D E F
    # 0 1 2 3 4 5
    C1 = member_list[0] | member_list[1]
    C2 = ((int(member_list[0]) + int(member_list[4]) + int(member_list[5])) == 2)
    C3 = not (member_list[1] ^ member_list[2])
    C4 = ((not member_list[0]) & member_list[3]) | (member_list[0] & (not member_list[3]))
    C5 = ((not member_list[2]) & member_list[3]) | (member_list[2] & (not member_list[3]))
    C6 = (not member_list[4]) | member_list[3]
    if C1 & C2 & C3 & C4 & C5 & C6:
        return True
    else:
        return False


# main
listChar = ["A", "B", "C", "D", "E", "F"]
table = generateAssignTable(6)
for l in table:
    if judge(l):
        for i in range(0, 6):
            if l[i]:
                print(listChar[i]+ "去了", end="  ")
            else:
                print(listChar[i] + "没去", end="  ")
        print("")   # 换行