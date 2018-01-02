from django.test import TestCase

# Create your tests here.

num = 3
def myfunc(n):
    print(n)
    if n>1:
        myfunc(n-1)  #myfunc(a=3)
                     #  print(n)
                     #     myfunc(b=2)
                     #        print(n)
    print(n)         #          myfunc(c= 1) a = 3        b = 2          c= 1
                     #              print(n)
                     #                   if n>1:
                     #              print(n)
                     #       print(n)
                     #  print(n)

# myfunc(num)


class A:
    def text(self):
        print("form A")

class B(A):
    def text(self):
        print("from B")

class C(A):
    def text(self):
        print("from C")


class D(B):
    def text(self):
        print("from D")

class E(C):
    def text(self):
        print("from E")

class F(D,E):
    def text(self):
        print("from F")

# print(F.__mro__)


# cmd = input("请输入指令：").strip()
# # func = __import__(cmd)
# # print(func.time())
# import importlib
# func = importlib.import_module(cmd)
# print(func.time())

class FOO:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.say = "hello"

    def say(self):
        pass
    def __setattr__(self, key, value):
        print("======key:%s====value:%s"%(key,value))


# f = FOO("egon",18)





#
#
#
# class Bar:
#     __slots__ = ["x","y"]
#
# qq = Bar()
# qq.x = 1
# print(qq.x)
#
# qq.y = 2
# print(qq.y)


# qq.z = 3
# print(qq.z)



# class Mymeta(type):
#     def __init__(self,a,b,c):
#         pass
#     def __call__(self, *args, **kwargs):
#         print("========>")
#         obj = self.__new__(self)
#         self.__init__(obj,())
#
#
#
# class Zhang(Mymeta):
#     def __init__(self):
#         print("-=====自动执行")
#
# obj = Zhang()
# print(obj())





