# 字典: 理解字典的最佳方式是把它看做无序的键：值对（key:value 对）集合，键必须是互不相同的（在同一个字典之内）。一对大括号创建一个空的字典： {} 。初始化列表时，在大括号内放置一组逗号分隔的键：值对，这也是字典输出的方式。

def calldict(dicts):
    print("原始字典",end=' ')
    print(dicts)   # 原始字典
    dicts['欧阳修'] = '宋朝' # 追加字典
    print("追加后的字典",end=' ')
    print(dicts)    # 追加后的字典
    print("字典键的集合",end=' ')
    print(list(dicts.keys())) # 字典键的集合
    print("字典键的排序",end=' ')
    print(sorted(dicts.keys())) # 字典键的排序
    print("字典值的集合",end=' ')
    print(list(dicts.values())) # 字典值的集合

calldict(dicts = {'李白': '唐朝', '杜甫': '唐朝'})