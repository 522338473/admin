from django.test import TestCase

# Create your tests here.
# from django.http import QueryDict
#
#
# dc = QueryDict(mutable=True)
# dc["hobby"] = [1,2,3]
# print(dc.urlencode())

class Foo():
    _instance = None
    def __init__(self,name):
        self.name = [name,]
    def ass(self,na):
        self.name.append(na)
    @classmethod
    def instance(cls,*args,**kwargs):
        if not Foo._instance:
            obj = Foo(*args,**kwargs)
            Foo._instance = obj
        return Foo._instance



# obj1 = Foo.instance("alex")
# obj1.ass(111)
# print(obj1.name)      #['alex', 111]
#
# obj2 = Foo.instance("egon")
# obj2.ass(222)
# print(obj2.name)     #['alex', 111, 222]      第二次instance中直接走return函数



# a = 10
# b = a
# del a
# print(a)













