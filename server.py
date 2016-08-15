from http.server import HTTPServer
from config import serverConf
from http_hendler import Handler
from loger import loger
from DataAccessLayer import InMemoryDataAccessLayer
from Routes import routes
from Routing import Router
from template1 import Template
from langRu import lang as ru
import time

def main():
    loger.file = './log/server.log'
    # Handler.favicon = '/static/image/favicon_2.gif'
    Handler.tableData = InMemoryDataAccessLayer()
    Handler.routing = Router()
    Handler.routing.addRoutes(routes)
    listTemplates = ['logon', 'blogRead', 'blogsRead', 'createPost', 'adminPosts', 'editPost', 'form',\
                     'index1', 'registration']
    Handler.templates = dict([(key, Template(key + '.html'))for key in listTemplates])
    Handler.templateLang = {
        'ru': ru,
        # 'en': en,
        # '__': no,
    }
    Handler.templateData = {
        'favicon': '/static/image/favicon_2.gif',
    }
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





