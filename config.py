import os

class serverConf:
    # name = 'localhost'
    # name = '172.29.41.30'
    name = ''
    port = 8080

class templateConf:
    dir = os.path.join(os.getcwd(), 'templates')

class PageConst:
    postsToPage = 5
    numberByttonsPagination = 1

