import concurrent.futures


# ********************
# I copied isIter function from:
# https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
def isIter(obj):
    try:
        return iter(obj)
    except TypeError as te:
        return False
# ********************


def hasInstancecheck(__instance):
    try:
        isinstance(object, __instance)
        return True
    except Exception as e:
        return False


def getAttrs(objects, attrName):
    for obj in objects:
        yield getattr(obj, attrName)


def setAttrs(objects, attrName, attrValue):
    for obj in objects:
        setattr(obj, attrName, attrValue)


def retThread(func, *args, **kwargs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return executor.submit(func, *args, **kwargs).result()


def exceptLoop(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return exceptLoop(func, *args, **kwargs)


class SingletonMeta(type):

    def __init__(cls, name,
                 bases, attrs):

        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Singleton(metaclass=SingletonMeta):
    pass
