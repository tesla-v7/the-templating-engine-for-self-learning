from httpConstant import mimeType
from httpConstant import httpVersion
from httpConstant import httpCode
from template1 import Template
from exeptions import DataError, TemplateError
from httpConstant import httpMetod
import uuid
from DAL import User, Blog
from Pagination import Pagination
import datetime

def admin(request):
    request.protocol_version = httpVersion.ver11
    bdUser = authentication(request)
    if bdUser:
        request.user = bdUser
        print('---/loggon')
        print(request.cookie['ID'].output(header=''))
        request.send_response(httpCode.Redirect)
        request.send_header('content-type', mimeType.html)
        request.send_header('Set-Cookie', request.cookie['ID'].output(header=''))
        request.send_header('Location', '/admin/view')
        request.end_headers()
        return request
    try:
        tmp = Template('admin.html')
        data = {
            'lang': 'ru',
            'title': 'Админка',
            'head': 'Авторизация',
            'home': 'Главная',
            'favicon': request.favicon,
            'login': 'Пользователь',
            'password': 'Пароль',
            'logon': 'Вход',

        }
        text = tmp.render(data)
        # print(text)
    except (DataError, TemplateError):
        print('---------------/ex')
        page500('')
        return request
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    try:
        request.send_header('Set-Cookie', request.cookie['ID'].output(header=''))
    except KeyError:
        pass
    request.end_headers()
    request.wfile.write(text)
    return request

def view(request):
    bdUser = authentication(request)
    if bdUser:
        tmp = Template('edit.html')
        blogs = request.tableData.getBlogText(bdUser.userName, 5)
        pagination = Pagination('/admin/view', 5, 1)
        page = pagination.getInt(request.data)
        data = {
            'lang': 'ru',
            'title': 'Редактор постов',
            'head': 'Редактор постов',
            'hi': 'Добро пожаловать',
            'logout': 'Выход',
            'create': 'Создать',
            'page': str(page),
            'user': bdUser.getText(),
            'listBlogs': 'Посты:',
            'sandboxLabel': 'Песточница',
            'blogs': pagination.getData(page, blogs),
            'countText': 'Всего постов: ',
            'blogCount': str(len(blogs)),
            'btnDelete': 'Удалить',
            'btnEdit': 'Редактировать',
            'pagination': pagination.render(page, blogs),
            'favicon': request.favicon,
        }
        print(data)
        text = tmp.render(data)
        request.send_response(httpCode.Ok)
        request.send_header('content-type', mimeType.html)
        request.end_headers()
        request.wfile.write(text)
        return request
    redirectAuthentication(request, '/admin')
    return request

def blog(request):
    tmp = Template('blogsRead.html')
    user = request.path.split('?')
    user = user[0].split('/')[2]
    bdUser = request.tableData.findUser('userName', user)
    if not bdUser:
        page404(request)
        return request
    blogs = request.tableData.getBlogText(user, 30, sandbox=True)
    pagination = Pagination('/'.join(['', 'blog', bdUser.userName]), 5, 1)
    page = pagination.getInt(request.data)
    data = {
        'lang': 'ru',
        'favicon': request.favicon,
        'title': ' '.join(['Блог', bdUser.firstName, bdUser.lastName]),
        'head': ' '.join(['Блог', bdUser.firstName, bdUser.lastName]),
        'avatar': bdUser.avatar,
        'home': 'Главная',
        'page': str(page),
        'autor': bdUser.userName,
        # 'user': bdUser.getText(),
        'listBlogs': 'Посты:',
        'blogs': pagination.getData(page, blogs),
        'countText': 'Всего постов: ',
        'blogCount': str(len(blogs)),
        'btnRead': 'Читать',
        'pagination': pagination.render(page, blogs),
    }
    text = tmp.render(data)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(text)
    return request

def read(request):
    tmp = Template('blogRead.html')
    urlTmp = request.path.split('?')
    try:
        user = urlTmp[0].split('/')[2]
        id = urlTmp[0].split('/')[3]
    except IndexError:
        page404(request)
        return request
    bdUser = request.tableData.findUser('userName', user)
    pagination = Pagination('/'.join(['', 'blog', bdUser.userName]), 5, 1)
    page = pagination.getInt(request.data)
    blog = request.tableData.findOneBlog(user, 'id', id)
    data = {
        'lang': 'ru',
        'favicon': request.favicon,
        'title': ' '.join(['Блог', bdUser.firstName, bdUser.lastName]),
        'head': ' '.join(['Блог', bdUser.firstName, bdUser.lastName]),
        'home': 'Главная',
        'page': str(page),
        'autor': bdUser.userName,
        'avatar': bdUser.avatar,
        'listBlogs': 'Вернуться к списку постов',
        'blog': blog.getText(),
        'countText': 'Всего постов: ',
        'btnRead': 'Читать',
    }
    text = tmp.render(data)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(text)
    return request

def index(request):
    # request.protocol_version = httpVersion.ver11
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode('index'))
    return request

def create(request):
    bdUser = authentication(request)
    if bdUser:
        if request.command == httpMetod.GET:
            tmp = Template('createPost.html')
            # blogs = request.tableData.getBlogText(bdUser.userName)
            data = {
                'lang': 'ru',
                'title': 'Создать пост',
                'head': 'Создать пост',
                'post': 'Пост',
                'labelSandbox': 'Песочница',
                'send': 'Отправить',
                'favicon': request.favicon,
            }
            text = tmp.render(data)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(text)
            return request
        elif request.command == httpMetod.POST:
            blog = Blog(bdUser.userName)
            blog.load(request.data)
            request.tableData.addBlog(blog)
            blogBdAll = request.tableData.findAllBlog(bdUser.userName)
            pagination = Pagination('/admin/view', 5, 1)
            print('page= ', pagination.getPageNum(blog, blogBdAll))
            redirectAuthentication(request, '/admin/view?page=1')# + str(pagination.getPageNum(blog, blogBdAll)))
            return request
    redirectAuthentication(request, '/admin')
    return request

def static(request):
    param = request.path.split('/')
    path = './static/' + param[2] + '/' + param[3]
    mime = param[3].split('.')[1]
    try:
        file = open(path, 'rb')
        tmplRAW = file.read()
        file.close()
    except (FileNotFoundError, IsADirectoryError):
        page404(request)
        return request
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.getMime(mime))
    request.end_headers()
    request.wfile.write(tmplRAW)
    return request

def registration(request):
    bdUser = authentication(request)
    if not bdUser:
        if request.command == httpMetod.POST:
            user = User()
            user.load(request.data)
            request.tableData.addUser(user)
        elif request.command == httpMetod.GET:
            tmp = Template('registration.html')
            data = {
                'lang': 'ru',
                'title': 'Регистрация',
                'head': 'Форма регистрации',
                'firstName': 'Имя',
                'lastName': 'Фамилия',
                'login': 'Логин',
                'password': 'Пароль',
                'avatar': 'Аватар',
                'registration': 'Регистрироваться',
                'favicon': request.favicon,
            }
            text = tmp.render(data)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(text)
            return request
    request.tableData.print()
    redirectAuthentication(request, '/admin')
    return request

def edit(request):
    bdUser = authentication(request)
    if bdUser:
        if request.command == httpMetod.GET:
            tmp = Template('editPost.html')
            try:
                id = request.dataMas[1]
            except KeyError:
                redirectAuthentication(request, '/admin/view?page=1')
                return request
            blog = request.tableData.findOneBlog(bdUser.userName, 'id', id)
            data = {
                'lang': 'ru',
                'title': 'Редактировать пост',
                'head': 'Редактировать пост',
                'body': 'Пост',
                'send': 'Отправить',
                'labelSandbox': 'Песточница',
                'labelDateCreate': 'Дата создания:',
                'labelDateEdit': 'Дата редактирования:',
                'post': blog.getTextRaw(),
                'favicon': request.favicon,
            }
            #TODO read in google
            # invalid
            # boundary in multipart
            # form
            # b
            text = tmp.render(data)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(text)
            return request
        elif request.command == httpMetod.POST:
            blog = Blog('')
            try:
                id = request.dataMas[1]
            except KeyError:
                redirectAuthentication(request, '/admin/view?page=1')
                return request
            blog.load(request.data)
            blog.id = id
            blogBd = request.tableData.findOneBlog(bdUser.userName, 'id', blog.id)
            print(blogBd.getText())
            if bdUser.userName == blogBd.autor:
                blogBdAll = request.tableData.findAllBlog(bdUser.userName)
                blogBd.edit(blog)
                pagination = Pagination('/admin/view', 5, 1)
                print('page= ', pagination.getPageNum(blogBd, blogBdAll))
                redirectAuthentication(request, '/admin/view?page=' + str(pagination.getPageNum(blogBd, blogBdAll)))
            return request
    redirectAuthentication(request, '/admin')
    return request

def delete(request):
    bdUser = authentication(request)
    if bdUser:
        try:
            id = str(request.dataMas[1])
            request.tableData.deleteBlog(bdUser.userName, 'id', id)
        except KeyError:
            pass
        try:
            page = str(request.data['page'][0])
        except KeyError:
            page = '1'
        print('---/ page /---', page)
        redirectAuthentication(request, '/admin/view?page=' + page)
        return request
    redirectAuthentication(request, '/admin')
    return request


def logout(request):
    bdUser = authentication(request)
    if bdUser:
        bdUser.sid = ''
        expiration = datetime.datetime.now() + datetime.timedelta(days=-30)
        request.cookie['ID']["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    request.send_response(httpCode.Redirect)
    request.send_header('content-type', mimeType.html)
    request.send_header('Set-Cookie', (request.cookie['ID'].output(header='')).replace('expires=', 'expires= -'))
    request.send_header('Location', '/')
    request.end_headers()
    return request

def home(request):
    # bdUser = authentication(request)
    data = {
        'lang': 'ru',
        'title': 'Редактировать пост',
        'favicon': request.favicon,
        'count': str(request.tableData.countUsers()),
        'registration': 'Регистрация',
        'logon': 'Вход',
        'readblogs': 'Читать блоги',
        'autors': request.tableData.getAllUsers(),
    }
    # print(data['autors'])
    tmp = Template('index1.html')
    text = tmp.render(data)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(text)
    return request

def about(request):
    # request.protocol_version = httpVersion.ver11
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode('about'))
    return request

def page404(request):
    # request.protocol_version = httpVersion.ver11
    request.send_response(httpCode.NotFound)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode('404 not found'))
    return request

def page500(request):
    # request.protocol_version = httpVersion.ver11
    request.send_response(httpCode.ServerErr)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode('500 server error'))
    return request

def authentication(request):
    try:
        bdUser = request.tableData.findUser('sid', request.cookie['ID'].coded_value)
        if bdUser and bdUser.sid:
            return bdUser
        else:
            expiration = datetime.datetime.now() + datetime.timedelta(days=-30)
            request.cookie['ID']["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
            return None
    except KeyError:
        if request.command == httpMetod.POST:
            user = User()
            user.load(request.data)
            bdUser = request.tableData.findUser('userName', user.userName)
            if (bdUser and bdUser.password == user.password):
                expiration = datetime.datetime.now() + datetime.timedelta(days=30)
                bdUser.sid = str(uuid.uuid5(uuid.NAMESPACE_DNS, bdUser.userName).hex)
                request.cookie['ID'] = bdUser.sid
                request.cookie['ID']['Path'] = '/'
                # request.cookie['ID']['Domain'] = 'localhost'
                request.cookie['ID']["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
                return bdUser
    return None

def redirectAuthentication(request, path='/'):
    request.send_response(httpCode.Redirect)
    request.send_header('content-type', mimeType.html)
    request.send_header('Location', path)
    request.end_headers()
    return request
