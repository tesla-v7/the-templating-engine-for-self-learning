from datetime import datetime
from exeptions import DataError

class _DataAccessLayer:
    def __init__(self):
        self.__dict__ = []
    # def __getattr__(self, item):
    #     try:
    #         return self.__dict__[item]
    #     except KeyError:
    #         raise DataError('Data error value not found' + item)
    #
    # def __setattr__(self, key, value):
    #     try:
    #         tmp = self.__dict__[key]
    #         self.__dict__[key] = value
    #     except KeyError:
    #         raise DataError('Data error value not found' + key)

    def add(self, data):
        pass

    def save(self):
        pass

    def find(self, key, value):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

class InMemoryDataAccessLayer






