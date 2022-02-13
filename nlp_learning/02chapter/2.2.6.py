# set集合：集合是一个无序不重复元素的集。基本功能包括关系测试和消除重复元素。集合对象还支持 union（联合），intersection（交），difference（差）和 sysmmetric difference（对称差集）等数学运算。

def callset(basket):
    result= set(basket)
    print(result)

callset(basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'})

