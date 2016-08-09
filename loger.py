import os.path
import datetime

class loger:
    # path = ''
    file = ''

    # @staticmethod
    @classmethod
    def log(cls, msg):
        if(os.path.isfile(cls.file)):
            fileHandl = open(cls.file, 'a')
            fileHandl.write(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ' INFO '+  msg + '\n')
            fileHandl.close
    @classmethod
    def warning(cls, msg):
        if (os.path.isfile(cls.file)):
            fileHandl = open(cls.file, 'a')
            fileHandl.write(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ' WARNING ' + msg + '\n')
            fileHandl.close()

    @classmethod
    def error(cls, msg):
        if (os.path.isfile(cls.file)):
            fileHandl = open(cls.file, 'a')
            fileHandl.write(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ' ERROR ' + msg + '\n')
            fileHandl.close()
        pass
