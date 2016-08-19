from httpConstant import mimeType
import mimetypes
from httpConstant import httpVersion
from httpConstant import httpCode
from exeptions import DataError, TemplateError, UserError
from httpConstant import httpMetod
import uuid
from DataAccessLayer import User, Post
from Pagination import Pagination
import datetime
from config import PageConst
from loger import loger

cookie_time_format = '%a, %d-%b-%Y %H:%M:%S PST'
class urlList:
    root = '/'
    blog = '/blog'
    create = '/create'
    logon = '/logon'
    logout = '/logout'
    admin = '/admin/view'



def logonUser(request):
    request.protocol_version = httpVersion.ver11
    bdUser = authentication(request)
    if not bdUser:
        pageLogonUser(request)
        return request
    request.user = bdUser
    request.send_response(httpCode.Redirect)
    request.send_header('content-type', mimeType.html)
    request.send_header('Set-Cookie', request.cookie['ID'].output(header=''))
    request.send_header('Location', '/admin/view')
    request.end_headers()
    return request

def pageLogonUser(request):
    request.protocol_version = httpVersion.ver11
    bdUser = authentication(request)
    if bdUser:
        logonUser(request)
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

def pageEditPosts(request):
    bdUser = authentication(request)
    if not bdUser:
        redirectToPage(request, urlList.logon)
        return request
    posts = request.tableData.getBlogText(bdUser.userName, words=5)
    pagination = Pagination(urlList.admin, PageConst.postsToPage, PageConst.numberByttonsPagination)
    pageNumber = pagination.getPageNumberInRequest(request.dataGet)
    pageData = request.templateData
    pageData['lang'] = request.templateLang['ru']['adminPosts']
    pageData['metod'] = {
        'user': bdUser.getPropertysInDict(),
        'blogs': pagination.getPageElementsSortZA(pageNumber, posts),
        'blogCount': str(len(posts)),
        'pagination': pagination.render(pageNumber, posts),
    }
    htmlPage = request.templates['adminPosts'].render(pageData)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def pageReadBlog(request):
    bdUser = request.tableData.findUser('userName', request.urlList[1])
    if not bdUser:
        page404(request)
        return request
    posts = request.tableData.getBlogText(bdUser.userName, 30, sandbox=True)
    pagination = Pagination('/'.join(['', 'blog', bdUser.userName]), PageConst.postsToPage, PageConst.numberByttonsPagination)
    pageNumber = pagination.getPageNumberInRequest(request.dataGet)
    pageData = request.templateData
    pageData['lang'] = request.templateLang['ru']['pageReadBlog']
    pageData['metod'] = {
        'fullName': bdUser.fullName,
        'avatar': bdUser.avatar,
        'page': str(pageNumber),
        'autor': bdUser.userName,
        'blogs': pagination.getPageElementsSortZA(pageNumber, posts),
        'blogCount': str(len(posts)),
        'pagination': pagination.render(pageNumber, posts),
    }
    htmlPage = request.templates['blogsRead'].render(pageData)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def pageReadPost(request):
    try:
        userName = request.urlList[1]
        idPost = request.urlList[2]
    except IndexError:
        page404(request)
        return request
    bdUser = request.tableData.findUser('userName', userName)
    if not bdUser:
        redirectToPage(request, '/')
        return request
    pagination = Pagination('/'.join([urlList.blog, bdUser.userName]), PageConst.postsToPage, PageConst.numberByttonsPagination)
    post = request.tableData.findOneBlog(bdUser.userName, 'id', idPost)
    blogPageNum = pagination.getPageNumberOfBlogsSortZA(post, request.tableData.findAllBlog(bdUser.userName))
    if not post:
        redirectToPage(request, '/'.join([urlList.blog, bdUser.userName]))
        return request
    pageData = request.templateData
    pageData['lang'] = request.templateLang['ru']['pageReadPost']
    pageData['metod'] = {
        'fullName': bdUser.fullName,
        'page': str(blogPageNum),
        'autor': bdUser.userName,
        'avatar': bdUser.avatar,
        'blog': post.getPropertysInDict(),
    }
    htmlPage = request.templates['blogRead'].render(pageData)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def pageCreatePost(request):
    bdUser = authentication(request)
    if not bdUser:
        redirectToPage(request, '/logon')
        return request
    pageData = request.templateData
    pageData['lang'] = request.templateLang['ru']['createPost']
    htmlPage = request.templates['createPost'].render(pageData)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def createPost(request):
    bdUser = authentication(request)
    if not bdUser:
        redirectToPage(request, urlList.logon)
        return request
    blog = Post(bdUser.userName)
    blog.load(request.dataPost)
    request.tableData.addBlog(blog)
    redirectToPage(request, '?'.join([urlList.admin, 'page=1']))
    return request

def staticContentReturn(request):
    path = './static/%s/%s' % (request.urlList[1], request.urlList[2])
    try:
        file = open(path, 'rb')
        contentRaw = file.read()
        file.close()
    except (FileNotFoundError, IsADirectoryError):
        page404(request)
        return request
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimetypes.guess_type(request.path)[0])
    request.end_headers()
    request.wfile.write(contentRaw)
    return request

def pageRegistrationUser(request):
    bdUser = authentication(request)
    if bdUser:
        request.tableData.print()
        redirectToPage(request, urlList.logon)
        return request
    pageData = request.templateData
    pageData['lang'] = request.templateLang['ru']['registration']
    htmlPage = request.templates['registration'].render(pageData)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def registrationUser(request):
    bdUser = authentication(request)
    if bdUser:
        request.tableData.print()
        redirectToPage(request, '/'.join([urlList.admin, bdUser.userName]))
        return request
    user = User()
    try:
        user.load(request.dataPost)
    except UserError:

        pageRegistrationUser(request)
        return request
    request.tableData.addUser(user)
    redirectToPage(request, urlList.logon)
    return request

def pageEditPost(request):
    bdUser = authentication(request)
    if not bdUser:
        redirectToPage(request, urlList.logon)
        return request
    try:
        idPost = request.urlList[1]
    except KeyError:
        redirectToPage(request, '?'.join([urlList.admin, 'page=1']))
        return request
    post = request.tableData.findOneBlog(bdUser.userName, 'id', idPost)
    pageData = request.templateData
    pageData['lang'] = request.templateLang['ru']['editPost']
    try:
        pageData['metod'] = {
            'post': post.getPropertysInDict(),
        }
    except AttributeError:
        loger.warning('page edit post id"%s" not found' % idPost)
        redirectToPage(request, urlList.admin)
        return request
    htmlPage = request.templates['editPost'].render(pageData)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def editPost(request):
    bdUser = authentication(request)
    if not bdUser:
        redirectToPage(request, urlList.logon)
        return request
    post = Post('')
    post.load(request.dataPost)
    try:
        post.id = request.urlList[1]
    except KeyError:
        redirectToPage(request, '?'.join([urlList.admin, 'page=1']))
        return request
    postBd = request.tableData.findOneBlog(bdUser.userName, 'id', post.id)
    postsBd = request.tableData.findAllBlog(bdUser.userName)
    try:
        postBd.edit(post)
    except AttributeError:
        loger.warning('edit post id "%s" not found' % post.id)
        redirectToPage(request, urlList.admin)
        return request
    pagination = Pagination(urlList.admin, PageConst.postsToPage, PageConst.numberByttonsPagination)
    redirectToPage(request, '?'.join([urlList.admin, 'page=%d' % pagination.getPageNumberOfBlogsSortZA(postBd, postsBd)]))
    return request

def deletePostId(request):
    bdUser = authentication(request)
    if not bdUser:
        redirectToPage(request, urlList.logon)
        return request
    try:
        idPost = request.urlList[1]
        pagination = Pagination('', PageConst.postsToPage, PageConst.numberByttonsPagination)
        postDelete = request.tableData.findOneBlog(bdUser.userName, 'id', idPost)
        pageNubmer = pagination.getPageNumberOfBlogsSortZA(postDelete, request.tableData.findAllBlog(bdUser.userName))
        request.tableData.deleteBlog(bdUser.userName, 'id', postDelete.id)
    except (KeyError, AttributeError):
        loger.warning('delete post id="%s" not found' % idPost)
        redirectToPage(request, urlList.logon)
        return request
    redirectToPage(request, '?'.join([urlList.admin, 'page=%d' % pageNubmer]))
    return request

def logoutUser(request):
    bdUser = authentication(request)
    if bdUser:
        bdUser.sid = ''
        expiration = datetime.datetime.now() + datetime.timedelta(days=-30)
        request.cookie['ID']['expires'] = expiration.strftime(cookie_time_format)
    request.send_response(httpCode.Redirect)
    request.send_header('content-type', mimeType.html)
    request.send_header('Set-Cookie', (request.cookie['ID'].output(header='')).replace('expires=', 'expires= -'))
    request.send_header('Location', '/')
    request.end_headers()
    return request

def pageHome(request):
    data = request.templateData
    data['lang'] = request.templateLang['ru']['index1']
    data['metod'] = {
        'count': str(request.tableData.getCountUsers()),
        'autors': request.tableData.getAllUsers(),
    }
    htmlPage = request.templates['index1'].render(data)
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(htmlPage)
    return request

def about(request):
    request.send_response(httpCode.Ok)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode('about'))
    return request

def page404(request):
    request.send_response(httpCode.NotFound)
    request.send_header('content-type', mimeType.html)
    request.end_headers()
    request.wfile.write(str.encode(request.templateLang['ru']['serverErr'][404]))
    return request

def page500(request):
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
            request.cookie['ID']["expires"] = expiration.strftime(cookie_time_format)
            return None
    except KeyError:
        if request.command == httpMetod.POST:
            user = User()
            try:
                user.load(request.dataPost)
            except UserError:
                return None
            bdUser = request.tableData.findUser('userName', user.userName)
            if (bdUser and bdUser.password == user.password):
                expiration = datetime.datetime.now() + datetime.timedelta(days=30)
                bdUser.sid = str(uuid.uuid5(uuid.NAMESPACE_DNS, bdUser.userName).hex)
                request.cookie['ID'] = bdUser.sid
                request.cookie['ID']['Path'] = '/'
                request.cookie['ID']["expires"] = expiration.strftime(cookie_time_format)
                return bdUser
            loger.warning('invalid credentials user: %s' % user.userName)
    return None

def redirectToPage(request, path='/'):
    request.send_response(httpCode.Redirect)
    request.send_header('content-type', mimeType.html)
    request.send_header('Location', path)
    request.end_headers()
    return request
