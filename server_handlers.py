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

def logon(request):
    request.protocol_version = httpVersion.ver11
    bdUser = authentication(request)
    if bdUser:
        request.user = bdUser
        request.send_response(httpCode.Redirect)
        request.send_header('content-type', mimeType.html)
        request.send_header('Set-Cookie', request.cookie['ID'].output(header=''))
        request.send_header('Location', '/admin/view')
        request.end_headers()
        return request
    try:
        data = request.templateData
        data['lang'] = request.templateLang['ru']['logon']
        text = request.templates['logon'].render(data)
    except (DataError, TemplateError):
        page500(request)
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

def admin(request):
    bdUser = authentication(request)
    if bdUser:
        blogs = request.tableData.getBlogText(bdUser.userName, 5)
        pagination = Pagination('/admin/view', 5, 1)
        page = pagination.getInt(request.dataGet)
        data = request.templateData
        data['lang'] = request.templateLang['ru']['adminPosts']
        data['metod'] = {
            'page': str(page),
            'user': bdUser.getText(),
            'blogs': pagination.getData(page, blogs),
            'blogCount': str(len(blogs)),
            'pagination': pagination.render(page, blogs),
        }
        text = request.templates['adminPosts'].render(data)
        request.send_response(httpCode.Ok)
        request.send_header('content-type', mimeType.html)
        request.end_headers()
        request.wfile.write(text)
        return request
    redirectAuthentication(request, '/admin')
    return request

def blog(request):
    user = request.urlMas[1]
    bdUser = request.tableData.findUser('userName', user)
    if not bdUser:
        page404(request)
        return request
    blogs = request.tableData.getBlogText(user, 30, sandbox=True)
    pagination = Pagination('/'.join(['', 'blog', bdUser.userName]), 5, 1)
    page = pagination.getInt(request.dataGet)
    data = request.templateData
    data['lang'] = request.templateLang['ru']['blogsRead']
    data['metod'] = {
        'fullName': ' '.join([bdUser.firstName, bdUser.lastName]),
        'avatar': bdUser.avatar,
        'page': str(page),
        'autor': bdUser.userName,
        'blogs': pagination.getData(page, blogs),
        'blogCount': str(len(blogs)),
        'pagination': pagination.render(page, blogs),
    }
    text = request.templates['blogsRead'].render(data)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(text)
    return request

def read(request):
    urlTmp = request.path.split('?')
    try:
        user = urlTmp[0].split('/')[2]
        id = urlTmp[0].split('/')[3]
    except IndexError:
        page404(request)
        return request
    bdUser = request.tableData.findUser('userName', user)
    pagination = Pagination('/'.join(['', 'blog', bdUser.userName]), 5, 1)
    page = pagination.getInt(request.dataGet)
    blog = request.tableData.findOneBlog(user, 'id', id)
    data = request.templateData
    data['lang'] = request.templateLang['ru']['blogRead']
    data['metod'] = {
        'fullName': ' '.join([bdUser.firstName, bdUser.lastName]),
        'page': str(page),
        'autor': bdUser.userName,
        'avatar': bdUser.avatar,
        'blog': blog.getText(),
    }
    text = request.templates['blogRead'].render(data)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(text)
    return request

def index(request):
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode('index'))
    return request

def create(request):
    bdUser = authentication(request)
    if bdUser:
        if request.command == httpMetod.GET:
            data = request.templateData
            data['lang'] = request.templateLang['ru']['createPost']
            text = request.templates['createPost'].render(data)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(text)
            return request
        elif request.command == httpMetod.POST:
            blog = Blog(bdUser.userName)
            blog.load(request.dataPost)
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
            user.load(request.dataPost)
            request.tableData.addUser(user)
        elif request.command == httpMetod.GET:
            data = request.templateData
            data['lang'] = request.templateLang['ru']['registration']
            text = request.templates['registration'].render(data)
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
            try:
                id = request.urlMas[1]
            except KeyError:
                redirectAuthentication(request, '/admin/view?page=1')
                return request
            blog = request.tableData.findOneBlog(bdUser.userName, 'id', id)
            data = request.templateData
            data['lang'] = request.templateLang['ru']['editPost']
            data['metod'] = {
                'post': blog.getTextRaw(),
            }
            text = request.templates['editPost'].render(data)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(text)
            return request
        elif request.command == httpMetod.POST:
            blog = Blog('')
            try:
                id = request.urlMas[1]
            except KeyError:
                redirectAuthentication(request, '/admin/view?page=1')
                return request
            blog.load(request.dataPost)
            blog.id = id
            blogBd = request.tableData.findOneBlog(bdUser.userName, 'id', blog.id)
            blogBdAll = request.tableData.findAllBlog(bdUser.userName)
            blogBd.edit(blog)
            pagination = Pagination('/admin/view', 5, 1)
            redirectAuthentication(request, '/admin/view?page=' + str(pagination.getPageNum(blogBd, blogBdAll)))
            return request
    redirectAuthentication(request, '/admin')
    return request

def delete(request):
    bdUser = authentication(request)
    if bdUser:
        try:
            id = str(request.urlMas[1])
            request.tableData.deleteBlog(bdUser.userName, 'id', id)
        except KeyError:
            pass
        try:
            page = str(request.dataGet['page'][0])
        except KeyError:
            page = '1'
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
    data = request.templateData
    data['lang'] = request.templateLang['ru']['index1']
    data['metod'] = {
        'count': str(request.tableData.countUsers()),
        'autors': request.tableData.getAllUsers(),
    }
    text = request.templates['index1'].render(data)
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
    request.wfile.write(str.encode(request.templateLang['ru']['serverErr'][404]))
    return request

def page500(request):
    # request.protocol_version = httpVersion.ver11
    request.send_response(httpCode.ServerErr)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode(request.templateLang['ru']['serverErr'][500]))
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
            user.load(request.dataPost)
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
