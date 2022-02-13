def countNum(param):
    reslut = ""
    if(param[1]+param[2]) == 0:
        reslut ="除数不能为0"
    else:
        res = param[0]/(param[1]+param[2])
        reslut ="this count: "+str(res)
    print(reslut)

if __name__=="__main__":
    countNum([10,2,3])