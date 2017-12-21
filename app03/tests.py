from django.test import TestCase

# Create your tests here.


# class Foo(object):
#     def __init__(self,name):
#         self.name = name
#
#     @classmethod
#     def instance(cls,*args,**kwargs):
#         if not hasattr(cls,"_instance"):
#             print(hasattr(cls,"_instance"))
#
# obj = Foo.instance("zhang")


# class Foo(object):
#     def __init__(self):
#         pass
#     def first(self):
#         print("哈哈哈哈")
#     def second(self):
#         print("呵呵呵")
#
#
# obj = Foo()
# ret = hasattr(obj,"first")
# res = getattr(obj,"second")
# print(res,end=" ")



li = [
    {"全部",["男","女"]},
    {"全部",["男","小动物"]}
]
class Foo(object):
    def __init__(self,name,data_list):
        self.name = name
        self.data_list = data_list
    def __iter__(self):
        yield "全部"
        for item in self.data_list:
            yield item

obj1 = Foo("全部",["男","女"])
obj2 = Foo("全部",["小动物","小植物"])

obj_list = [obj1,obj2]


for obj in obj_list:
    for item in obj:
        print(item)

