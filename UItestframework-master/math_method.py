__author__ = 'zz'
from  math_method import add

class MathMethod(Add):

    def sub(self):
        c=self.a+self.sub()
        return c

    def add_2(self):
        a=self.sub()
        b=self.add()
        c=a+b
        return c

t=MathMethod(4,5).sub()