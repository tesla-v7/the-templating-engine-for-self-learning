from http.server import HTTPServer
from config import serverConf
from http_hendler import Handler
from loger import loger
from DAL import User, InMemoryDataAccessLayer, Blog
import time

def main():
    loger.file = './log/server.log'
    Handler.favicon = '/static/image/favicon_2.gif'
    Handler.sessionData = InMemoryDataAccessLayer()
    loger.log('Start')
    try:
        print('Server start name: {0} port: {1}'.format(serverConf.name, serverConf.port))
        server = HTTPServer((serverConf.name, serverConf.port), Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print('')
        print('Server stop')

if(__name__ == '__main__'):
    main()
    pass





