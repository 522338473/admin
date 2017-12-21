from django.test import TestCase

# Create your tests here.





class Foo(object):
    def inner(self):
        print("你好啊，我是inner函数")

obj = Foo()
print(Foo.inner)
print(obj.inner)




# for i in range(1,2,3):
#     print(i)

i = 0
while i<3:
    print(i)
    i+=1
else:
    print("end")







