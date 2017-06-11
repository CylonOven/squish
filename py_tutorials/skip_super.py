"""
An attempt to see if its possible to skip a method of  a child class when using super.
The way to do it is you call teh super of the child-class you want to skip.
"""

class A(object):
    text = None

    @classmethod
    def more_text(cls, more ):
        print(cls.text + more)


class B(A):

    @classmethod
    def important_stuff(cls,):
        print("important stuff")

    @classmethod
    def more_text(cls, more):
        print("unwanted code")
        super(B, cls).more_text(more)


class C(A):

    @classmethod
    def more_text(cls, more):
        print(cls.text + " Mother")
        super(C, cls).more_text(more)


class D(B,C):
    text = "hello"
    
    @classmethod
    def more_text(cls, more):
        
        super(B, cls).more_text(more)

D.important_stuff()
D.more_text(" world")


class E(D, B, C):
    text = "We must save"

    @classmethod
    def more_text(cls, more):
        print(cls.text + more)
        super(E, cls).more_text(more)

E.important_stuff()
E.more_text(" everyone")
