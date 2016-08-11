from http.server import BaseHTTPRequestHandler
from loger import loger
import urllib
from cgi import parse_header, parse_multipart
from http.cookies import SimpleCookie as cookie


class Handler(BaseHTTPRequestHandler):
    tableData = None
    routing = None
    templates = None
    templateData = None
    urlMas = None
    dataGet = None
    dataPost = None


    def __init__(self, request, client_address, server):
        print('Handler.__init__')
        super(Handler, self).__init__(request, client_address, server)

    def do_GET(self):
        self.sessionCookie()
        data = self.path.split('?')
        request = {}
        # self.dataMas = data[0].split('/')
        self.urlMas = data[0].split('/')
        # self.dataMas.pop(0)
        self.urlMas.pop(0)

        # self.data = {} if len(data) < 2 else urllib.parse.parse_qs(data[1])
        self.dataGet = {} if len(data) < 2 else urllib.parse.parse_qs(data[1])
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def do_POST(self):
        self.sessionCookie()
        data = self.path.split('?')
        self.urlMas = data[0].split('/')
        self.urlMas.pop(0)
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            self.dataPost = parse_multipart(self.rfile, pdict)
            self.dataPost = dict([(key, self.dataPost[key][0].decode('utf-8') if key != 'avatar' else self.dataPost[key][0]) for key in self.dataPost ])
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            self.dataPost = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            self.dataPost = dict([(key, self.dataPost[key][0]) for key in self.dataPost])
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def do_PUT(self):
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def do_DELETE(self):
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def sessionCookie(self):
        cookiestring = "\n".join(self.headers.get_all('Cookie', failobj=[]))
        c = cookie()
        c.load(cookiestring)
        self.cookie = c



