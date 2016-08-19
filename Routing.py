from exceptions import RoutesAddError
from exceptions import HandleError
import server_handlers as handlers
from loger import loger
import re

class Router:
    def __init__(self):
        self.__routes = []

    def addRoute(self, rout):
        try:
            tmp = Rout(rout)
            if tmp == None:
                raise RoutesAddError('Rout add error')
            self.__routes.append(tmp)
        except RoutesAddError as ex:
            loger.error('Internal error no matching type metod="{}" path="{}" func="{}"'.format(*rout))
            print('Error add Route ')

    def addRoutes(self, routes):
        for rout in routes:
            self.addRoute(rout)

    def handle(self, request):
        try:
            handle = self.getHandle(request)
            return handle(request)
        except HandleError as ex:
            loger.warning('No handler for url = "{}"'.format(request.path))
            handlers.page404(request)
            # print('error ---------------')
            print('Error url: {} metod: {}'.format(request.path, ex.value))

    def getHandle(self, request):
        for rout in self.__routes:
            handle = rout.getHendler(request.command, request.path)
            if handle:
                return handle

        raise HandleError('Url Err')

    def prn(self):
        allText = '---'
        for text in self.__routes:
            print(text.getPath)
            allText += ' ' + text.getPath()
        return allText

class Rout:
    def __new__(cls, *args, **kwargs):
        param = args[0]
        if type(param) != list or len(param) != 3 or type(param[0]) != str or type(param[1]) != str or not hasattr(param[2], '__call__'):
            return None
        return super(Rout, cls).__new__(cls)

    def __init__(self, rout):
        self.__metod = rout[0]
        self.__path = rout[1]
        self.__handler = rout[2]

    def getHendler(self, metod, path):
        if(self.__metod == metod and re.match(self.__path, path.split('?')[0])):
            return self.__handler
        return None

    def getPath(self):
        return self.__path

