class ErrorPost(Exception):
    pass

class UserError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

class DataError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

class TemplateError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

class RoutesAddError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

class HandleError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)