# render
import os


app_root = locals()["app_root"]

# main
CustomException = type("CustomException", (Exception,), {})


def custom_exception(string):
    class tmp(CustomException):
        def __init__(self, msg=string, *args, **kwargs):
            super().__init__(msg, *args, **kwargs)
    return tmp


def myfunc2(a):
    return os.path.join(app_root, a)


