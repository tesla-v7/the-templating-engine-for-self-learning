from httpConstant import mimeType
from httpConstant import httpVersion
from httpConstant import httpCode
from exeptions import DataError, TemplateError
from httpConstant import httpMetod
import uuid
from DataAccessLayer import User, Blog
from Pagination import Pagination
import datetime
from config import PageConst

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
        pageData = request.templateData
        pageData['lang'] = request.templateLang['ru']['logon']
        htmlPage = request.templates['logon'].render(pageData)
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
    request.wfile.write(htmlPage)
    return request

def admin(request):
    bdUser = authentication(request)
    if bdUser:
        blogs = request.tableData.getBlogText(bdUser.userName, words=5)
        pagination = Pagination('/admin/view', PageConst.postsToPage, PageConst.numberByttonsPagination)
        page = pagination.getPageNumberInRequest(request.dataGet)
        print('admin.page ', page)
        pageData = request.templateData
        pageData['lang'] = request.templateLang['ru']['adminPosts']
        pageData['metod'] = {
            # 'page': str(page),
            'user': bdUser.getText(),
            'blogs': pagination.getPageElementsSortZA(page, blogs),
            'blogCount': str(len(blogs)),
            'pagination': pagination.render(page, blogs),
        }
        htmlPage = request.templates['adminPosts'].render(pageData)
        request.send_response(httpCode.Ok)
        request.send_header('content-type', mimeType.html)
        request.end_headers()
        request.wfile.write(htmlPage)
        return request
    redirectAuthentication(request, '/admin')
    return request

def blog(request):
    bdUser = request.tableData.findUser('userName', request.urlMas[1])
    if not bdUser:
        page404(request)
        return request
    blogs = request.tableData.getBlogText(bdUser.userName, 30, sandbox=True)
    pagination = Pagination('/'.join(['', 'blog', bdUser.userName]), PageConst.postsToPage, PageConst.numberByttonsPagination)
    page = pagination.getPageNumberInRequest(request.dataGet)
    pageData = request.templateData
    pageData['lang'] = request.templateLang['ru']['blogsRead']
    pageData['metod'] = {
        'fullName': ' '.join([bdUser.firstName, bdUser.lastName]),
        'avatar': bdUser.avatar,
        'page': str(page),
        'autor': bdUser.userName,
        'blogs': pagination.getPageElementsSortZA(page, blogs),
        'blogCount': str(len(blogs)),
        'pagination': pagination.render(page, blogs),
    }
    htmlPage = request.templates['blogsRead'].render(pageData)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def read(request):
    urlTmp = request.path.split('?')
    try:
        userName = urlTmp[0].split('/')[2]
        idPostInBlog = urlTmp[0].split('/')[3]
    except IndexError:
        page404(request)
        return request
    bdUser = request.tableData.findUser('userName', userName)
    if bdUser:
        pagination = Pagination('/'.join(['', 'blog', bdUser.userName]), PageConst.postsToPage, PageConst.numberByttonsPagination)
        postRead = request.tableData.findOneBlog(bdUser.userName, 'id', idPostInBlog)
        blogPageNum = pagination.getPageNumberOfBlogsSortZA(postRead, request.tableData.findAllBlog(bdUser.userName))
        # page = pagination.getPageNumberInRequest(request.dataGet)
        # blog = request.tableData.findOneBlog(userName, 'id', id)
        if postRead:
            pageData = request.templateData
            pageData['lang'] = request.templateLang['ru']['blogRead']
            pageData['metod'] = {
                'fullName': ' '.join([bdUser.firstName, bdUser.lastName]),
                'page': str(blogPageNum),
                'autor': bdUser.userName,
                'avatar': bdUser.avatar,
                'blog': postRead.getText(),
            }
            htmlPage = request.templates['blogRead'].render(pageData)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(htmlPage)
            return request
    redirectAuthentication(request, '/')
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
            pageData = request.templateData
            pageData['lang'] = request.templateLang['ru']['createPost']
            htmlPage = request.templates['createPost'].render(pageData)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(htmlPage)
            return request
        elif request.command == httpMetod.POST:
            blog = Blog(bdUser.userName)
            blog.load(request.dataPost)
            request.tableData.addBlog(blog)
            blogBdAll = request.tableData.findAllBlog(bdUser.userName)
            pagination = Pagination('/admin/view', PageConst.postsToPage, PageConst.numberByttonsPagination)
            print('page= ', pagination.getPageNumberOfBlogsSortZA(blog, blogBdAll))
            redirectAuthentication(request, '/admin/view?page=1')# + str(pagination.getPageNumberOfBlogsSortZA(blog, blogBdAll)))
            return request
    redirectAuthentication(request, '/admin')
    return request

def static(request):
    param = request.path.split('/')
    path = './static/' + param[2] + '/' + param[3]
    requestMimeType = param[3].split('.')[1]
    try:
        file = open(path, 'rb')
        contentRaw = file.read()
        file.close()
    except (FileNotFoundError, IsADirectoryError):
        page404(request)
        return request
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.getMime(requestMimeType))
    request.end_headers()
    request.wfile.write(contentRaw)
    return request

def registration(request):
    bdUser = authentication(request)
    if not bdUser:
        if request.command == httpMetod.POST:
            user = User()
            user.load(request.dataPost)
            request.tableData.addUser(user)
        elif request.command == httpMetod.GET:
            pageData = request.templateData
            pageData['lang'] = request.templateLang['ru']['registration']
            htmlPage = request.templates['registration'].render(pageData)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(htmlPage)
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
            pageData = request.templateData
            pageData['lang'] = request.templateLang['ru']['editPost']
            pageData['metod'] = {
                'post': blog.getTextRaw(),
            }
            htmlPage = request.templates['editPost'].render(pageData)
            request.send_response(httpCode.Ok)
            request.send_header('content-type', mimeType.html)
            request.end_headers()
            request.wfile.write(htmlPage)
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
            pagination = Pagination('/admin/view', PageConst.postsToPage, PageConst.numberByttonsPagination)
            redirectAuthentication(request, '/admin/view?page=' + str(pagination.getPageNumberOfBlogsSortZA(blogBd, blogBdAll)))
            return request
    redirectAuthentication(request, '/admin')
    return request

def delete(request):#TODO избавится от номера страницы по средством вычисления страницы удаляемого поста
    bdUser = authentication(request)
    page = '1'
    if bdUser:
        try:
            idPostInBlog = str(request.urlMas[1])
            pagination = Pagination('', PageConst.postsToPage, PageConst.numberByttonsPagination)
            # page = pagination.getPageNumberInRequest(request.dataGet)
            # print(bdUser.userName, 'id', idPostInBlog)
            # print(request.tableData.findOneBlog(bdUser.userName, 'id', idPostInBlog))
            postDelete = request.tableData.findOneBlog(bdUser.userName, 'id', idPostInBlog)
            page = pagination.getPageNumberOfBlogsSortZA(postDelete, request.tableData.findAllBlog(bdUser.userName))
            request.tableData.deleteBlog(bdUser.userName, 'id', idPostInBlog)
        except KeyError:
            pass
        # try:
        #     page = str(request.dataGet['page'][0])
        # except KeyError:
        #     page = '1'
        redirectAuthentication(request, '/admin/view?page=' + str(page))
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
        'count': str(request.tableData.getCountUsers()),
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
