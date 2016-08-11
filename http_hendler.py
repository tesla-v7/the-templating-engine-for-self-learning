from http.server import BaseHTTPRequestHandler
from loger import loger
import urllib
from cgi import parse_header, parse_multipart
from http.cookies import SimpleCookie as cookie


class Handler(BaseHTTPRequestHandler):
    tableData = None
    routing = None

    def __init__(self, request, client_address, server):
        print('Handler.__init__')
        super(Handler, self).__init__(request, client_address, server)

    def do_GET(self):
        self.sessionCookie()
        data = self.path.split('?')
        self.dataMas = data[0].split('/')
        self.dataMas.pop(0)
        self.data = {} if len(data) < 2 else urllib.parse.parse_qs(data[1])
        loger.log('url = "{}"'.format(self.path))
        self.routing.handle(request=self)

    def do_POST(self):
        self.sessionCookie()
        data = self.path.split('?')
        self.dataMas = data[0].split('/')
        self.dataMas.pop(0)
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            self.data = parse_multipart(self.rfile, pdict)
            self.data = dict([(key, self.data[key][0].decode('utf-8') if key != 'avatar' else self.data[key][0]) for key in self.data ])
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            self.data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            self.data = dict([(key, self.data[key][0]) for key in self.data])
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



