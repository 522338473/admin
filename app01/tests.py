from django.test import TestCase

# Create your tests here.

a = ()
b = set()
c = {}
d = {1,2}
e = {"1":2}


# s = "1+2"
# # ss = int(s)
# sss = eval(s)
# print(s)
# # print(ss)
# print(sss)
#
# ss = "print(123)"
# eval(ss)






# list1 = [1,2,3]
# list2 = [4,5,6]
# list3 = zip(list1,list2)
# print(list(list3))                    #[(1, 4), (2, 5), (3, 6)]
# print(list(zip(*list3)))            #[(1, 2, 3), (4, 5, 6)]

# s = "zhang"
# zip()

# a = 0
# b = 2
# c = 2
# d = "1111111"
# e = "1111111"
# print(a and b)      #前边为假返回a，前边wi真返回啊、b
# print(a or b)     #前边为真返回a，前边为jia返回b    逻辑运算符
# print(a is not b)    #返回真假
# print(a & b)   #位运算符
# print(a | b)
#
# print(id(d),id(e))



# g = []
# h = []
# print(id(g),id(h))
#
# j = [1,2,3]
# k = j
# print(j,k,id(k),id(j))
# k[0] = 100
# print(j,k,id(k),id(j))


a = 10
b = a
print(id(a),id(b))
b = 20
print(a,b,"====",id(a),id(b))

c = [1,2]
d = c
d[1] = 100
e = c
e = [3,4]
print(c,d,"====",id(c),id(d))
print(c,e,"====",id(c),id(e))


print(round(12.5))
print(round(13.5))











# def age(n):
#     if n == 1:
#         return 10
#     else:
#         return age(n-1) + 2
#
# print(age(5))
# import sys


# def func(n):
#     if n == 10:
#         return
#     print("from func")
#     func(n-1)
#
# func(7)

# a = "zhang"
# b = a
# a = "ping"
# print(a,b)

c = [1,2]
d = c
d[1] = 100
print(c,d)


