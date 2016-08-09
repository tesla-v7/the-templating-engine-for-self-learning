from http.server import BaseHTTPRequestHandler
from Routes import routes
from Routing import Router
from loger import loger
import urllib
from cgi import parse_header, parse_multipart
# import mimetypes
from http.cookies import SimpleCookie as cookie
# from exeptions import RoutesAddError


class Handler(BaseHTTPRequestHandler):
    sessionData = None

    def __init__(self, request, client_address, server):
        print('Handler.__init__')
        if self.sessionData:
            self.tableData = self.sessionData

            # self.tableData.addUser(User('root', 'pass'))
            # i = 0
            # while i < 10:
            #     self.tableData.addUser(User('user_' + str(i), 'pass_' + str(i)))
            #     i += 1
            sessionData = self.tableData

        # if not self.tableData:
        #     self.tableData = InMemoryDataAccessLayer()


        self.routing = Router()
        self.routing.addRoutes(routes)
        super(Handler, self).__init__(request, client_address, server)

    def do_GET(self):
        # print(self.headers._headers)
        self.sessionCookie()
        data = self.path.split('?')
        print(data)
        self.dataMas = data[0].split('/')
        self.dataMas.pop(0)
        self.data = {} if len(data) < 2 else urllib.parse.parse_qs(data[1])
        print('---/', self.data)
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def do_POST(self):
        self.sessionCookie()
        data = self.path.split('?')
        print(data)
        self.dataMas = data[0].split('/')
        self.dataMas.pop(0)
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            # length = int(self.headers['content-length'])
            self.data = parse_multipart(self.rfile, pdict)
            self.data = dict([(key, self.data[key][0].decode('utf-8') if key != 'avatar' else self.data[key][0]) for key in self.data ])
            print(self.data)
            # self.data = urllib.urlencode(self.rfile.read(length))
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            self.data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            self.data = dict([(key, self.data[key][0]) for key in self.data])
            print(self.data)

        # length = int(self.headers['Content-Length'])
        # test = self.rfile.read(length)
        # print(str(length), test)
        # self.data = urllib.parse.parse_qsl(test)#.decode('utf-8'))
        # self.data = urllib.parse.parse_qsl(self.rfile.read(length))#.decode('utf-8'))
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def do_PUT(self):
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def do_DELETE(self):
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def sessionCookie(self):
        print('sessionCookie--/ ', self.headers.get_all('Cookie', failobj=[]))
        cookiestring = "\n".join(self.headers.get_all('Cookie', failobj=[]))
        c = cookie()
        c.load(cookiestring)
        self.cookie = c
        # print('---/', c['ID'])
        # print('---/', c['ID_'])
        # pass



