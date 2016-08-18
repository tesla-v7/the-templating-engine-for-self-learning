class UserError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

    pass

class DataError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

    pass

class TemplateError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

    pass

class RoutesAddError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

    pass

class HandleError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

    pass

