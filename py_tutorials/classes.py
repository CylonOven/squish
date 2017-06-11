class Foo():
    class_value = "class Value that is the same across all instances"
    def __init__(self, name, y = "default value, this is a kwarg", *args, **kws):
        """ init method, called when creating the instance of the class"""
        self.instance_value = "self is the isntance of the class"
        y = y # you need the self since there is a namespace inside each function and method, as you might now, so unless values are assigend to self they will be 'lost'
        self.name = name # Params passed into the __init__ method can be assigend to the instance inorder to 'save them'
        if args:
            print(args)
        if kws:
            print(kws)

    def hello(self):
        """ ususal way of defining 'methods' methods are bascially the same as functions but they are assigned to a class, or 'object' """
        print("hello {}".format(self.name))
        #print "hello" + name # will fail since name is undefined, inorder to access it it needs to be assigned to self

    @staticmethod
    def static():
        """ Methods with this decorator are static, meaning they can be called from the base class without having an instance
            Note that this method can only reach the class object by calling it's own name, in this case Foo"""
        print("lel")
        print(Foo.classmethod)

    @classmethod
    def classmethod(cls, foo):
        """ Classs methods take the class object as teh first arg, however just like self, you don't need to pass it in directly, it's done when you call the method 'from' the class object"""
        print(cls.class_value)
        cls.static()
        f = Foo("Indrek")
        f.hello()
        #cls.hello() #Fail
        print(cls.hello == Foo.hello)

    def __str__(self):
        """this method is called when python trys to convert this object into a string"""
        return self.hello()

    def __repr__(self):
        """this method is called when python is trying to repersent the object in a way that if inputted will be evaulutated into the same object
        It's a little confusing but think about the way dicts can be made with {} or dict()
        >>> f = Foo("lel")
        >>> f
        Foo("lel")
        >>> print(f)
        hello lel
        """
        return "Foo('{}')".format(self.name)

f = Foo("Indrek")
f.hello()
#hello Indrek
g = Foo("Ginger")
g.hello()
#hello Ginger

g.class_value == f.class_value
print(g.name)
#ginger
print(f.name)
#Indrek

#True
Foo("lel","Y",#is assigned to the kword parameter y in the __init__
    1,2,3,4,5,6,7,"lel", #These are assigned to args, args is a tuple or list or something of args that don't fit in, so you can pass any number of arguments
    kw1 = "kw1", kw2 = "xxx")

#Classes are objects just like everything in python are objects, ints, functions, etc
#They are a way to link the functions/method (Method is the same as a function except it's an attrebute of an object)
#to the data that is works with
