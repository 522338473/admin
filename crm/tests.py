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

myfunc(num)



