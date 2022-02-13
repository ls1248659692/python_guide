# 通过案例理解python中的类：

#  父类是动物类，有初始化函数，且有动物讲话的方法
#  子类是一个狗类，继承父类所有属性，并扩展自己方法
#  调用子类讲话方法，并直接调用父类讲话方法

"""
# 欢迎进入我的主页：http://www.cnblogs.com/baiboy/.
"""
class BaseAnimal: # 父类：动物
    def __init__(self,name,age): # 初始化方法：括号里是形参
        self.name=name
        self.age=age
    def speak(self): # 父类的行为方法
        print("我的名字是[ %s ],今年[ %d ]岁" %(self.name,self.age))


class SubDog(BaseAnimal): # 子类：小狗
    def __init__(self,name,age,say): # 初始化方法：括号里是形参
        BaseAnimal.__init__(self,name,age)
        self.say=say
        print("这是子类[ %s ]."%(self.name))
        print('_'*20+'调用子函数方法'+'_'*20)
    def talk(self):      # 子类的行为方法
        # BaseAnimal.speak(self) # 调用父类的行为方法
        print("我的名字是[ %s ],今年[ %d ]岁,我想说： %s" %(self.name,self.age,self.say))


ani=SubDog('dog',12,'汪汪...')
print(ani.talk())
print('_'*20+'直接调用父函数方法'+'_'*20)
BaseAnimal('tom',13).speak()


