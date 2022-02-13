# if 语句:根据成绩评判等级
def CallLevel(score):
    if score >= 90 :
        print("优秀")
    elif score >= 60:
        print("及格")
    else:
        print("不及格")
CallLevel(score=60)


# for 语句:循环输出所有评分指标
def GetLevel(score):
    for lev in score:
        print(lev,end=" ") # 设置不换行
GetLevel(score=["优秀","及格","不及格"]) # 列表参数

print()
# while 语句:循环输出所有评分指标
def GetLevel2(score):
    countlen=len(score)
    while countlen > 0:
        print(score[countlen-1],end=" ") # 设置不换行
        countlen -= 1

GetLevel2(score=[90,30,100,98,60])

print()
# range() 函数:循环输出所有评分指标的下标
def GetValue(score):
    for lev in range(len(score)):
        print(lev,end=" ")
GetValue(score=["优秀","及格","不及格"])

print()
# break 语句:统计优秀成绩的个数
def GetHighLev(score):
    result=0
    for lev in score:
        if lev < 90:
            break
        else:
            result += 1
    print("成绩优秀的学生有："+str(result)+"位。")

GetHighLev(score=[90,30,100,98,60])
# continue 语句:统计优秀成绩的个数
def GetHighLev2(score):
    result=0
    for lev in score:
        if lev < 90:
            continue
        else:
            result += 1
    print("成绩优秀的学生有："+str(result)+"位。")

GetHighLev2(score=[90,30,100,98,60])
# pass 语句：什么也不做，占位符
def callPass():
    pass
print(callPass())
# 定义函数
#
