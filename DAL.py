from datetime import datetime
import uuid
import re
from exeptions import DataError

# class _DataTable():
#     def __init__(self):
#         self.__dict__ = []
#
#     def __getattr__(self, item):
#         try:
#             return self.__dict__[item]
#         except KeyError:
#             raise DataError('Data error value not found' + item)
#
#     def __setattr__(self, key, value):
#         try:
#             tmp = self.__dict__[key]
#             self.__dict__[key] = value
#         except KeyError:
#             raise DataError('Data error value not found' + key)

class _DataAccessLayer:
    def addUser(self, data):
        pass

    def countUsers(self):
        pass

    def addBlog(self, data):
        pass

    def save(self):
        pass

    def findUser(self, key, value):
        pass

    def getAllUsers(self):
        pass

    def findOneBlog(self, autor, id, value):
        pass

    def findAllBlog(self, autor, sandbox=False):
        pass

    def getBlogText(self, autor, words=-1, sandbox=False):
        pass

    def findBlog(self, key, value):
        pass

    def deleteUser(self, key):
        pass

    def deleteBlog(self, key):
        pass


class InMemoryDataAccessLayer(_DataAccessLayer):
    def __init__(self, id=None):
        self._users = []
        self._blogs = {}

    def addUser(self, obj):
        self._users.append(obj)

    def countUsers(self):
        return len(self._users)

    def addBlog(self, blog):
        try:
            tmp = self._blogs[blog.autor]
        except KeyError:
            self._blogs[blog.autor] = []
        self._blogs[blog.autor].append(blog)

    def save(self):
        pass

    def findUser(self, key, value):
        for item in self._users:
            try:
                if item.find(key, value):
                    return item
            except AttributeError:
                return None
        return None

    def getAllUsers(self):
        users = []
        for user in self._users:
            users.append(user.getText())
        return users

    def findOneBlog(self, autor, id, value):
        try:
            for item in self._blogs[autor]:
                if item.find(id, value):
                    return item
        except (AttributeError, KeyError):
            return None
        return None

    def findAllBlog(self, autor, sandbox=False):
        if sandbox:
            allPost = []
            try:
                for blog in self._blogs[autor]:
                    if not blog.sandbox:
                        allPost.append(blog)
                return allPost
            except KeyError:
                return []
        try:
            allPost = self._blogs[autor]
            return allPost
        except KeyError:
            return []

    def getBlogText(self, autor, words=-1, sandbox=False):
        result = []
        for blog in self.findAllBlog(autor, sandbox=sandbox):
            result.append(blog.getText(words))
        return result

    def deleteUser(self, key, value):
        for item in self._users:
            try:
                if item.find(key, value):
                    self._users.remove(item)
                    return True
            except AttributeError:
                return False
        return False

    def deleteBlog(self, autor, key, value):
        try:
            for item in self._blogs[autor]:
                if item.find(key, value):
                    self._blogs[autor].remove(item)
                    return True
        except (AttributeError, KeyError):
            return False
        return False


    def print(self):
        for item in self._users:
            print(item)

    def printBlogs(self):
        for item in self._blogs:
            print(item)

class Item():
    def find(self, key, value):
        return getattr(self, key) == value

class User(Item):
    def __init__(self, userName='', password='', firstName='', lastName=''):
        self.userName = userName
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.avatar = '/static/image/2.jpg'
        self.sid = None

    def __str__(self):
        return self.userName + ' ' + self.password

    def load(self, postRequest):
        # print(postRequest)
        avatarRaw = None
        for key in postRequest:
            try:
                # tmpKey = getattr(self, key)
                if key != 'avatar':
                    setattr(self, key, postRequest[key])
                else:
                    avatarRaw = postRequest[key]
                # tmpKey = postRequest[key][0]
            except AttributeError:
                continue
        if avatarRaw:
            self.avatar = '/static/image/' + self.userName + '.jpg'
            f = open('.' + self.avatar, 'w+b')
            f.write(avatarRaw)
            f.close()

    def getText(self):
        return {
            'userName': self.userName,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'avatar': self.avatar,
        }

class Blog(Item):
    def __init__(self, autor, title='', text='', sandbox=False):
        self.autor = autor
        self.title = title
        self.text = text
        self.sandbox = sandbox
        self.datetime = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.datetimeEdit = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.id = str(uuid.uuid4().hex)
        # self.id = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.autor + datetime.now().strftime('%Y.%m.%d %H:%M:%S')).hex)

    def setDatetimtNow(self):
        self.datetime = datetime.now().strftime('%Y.%m.%d %H:%M:%S')

    def setDatetimt(self, value):
        try:
            self.datetime = datetime.strftime(value, '%Y.%m.%d %H:%M:%S')
            return True
        except ValueError:
            self.setDatetimtNow()
            return False

    def load(self, postRequest):
        print(postRequest)
        for key in postRequest:
            try:
                # if key == 'text':
                #     setattr(self, key, postRequest[key][0].replace('\n','<br>'))
                #     continue
                setattr(self, key, postRequest[key])
            except AttributeError:
                continue
        self.sandbox = bool(self.sandbox)

    def getText(self, words=-1):
        text = self.text.replace('\n', '<br>')
        if words > 0:
            text = re.search(r'(\b.+?\b(\s+|$)){0,' + str(words) + '}', text).group(0) + '...'
        return {
            'autor': self.autor,
            'text': text,
            'datatime': self.datetime,
            'id': self.id,
            'title': self.title,
            'sandbox': str(self.sandbox),
        }

    def getTextRaw(self):
        return {
            'autor': self.autor,
            'text': self.text.replace('\r\n', '&#13;&#10;'),
            'datatime': self.datetime,
            'datatimeEdit': self.datetimeEdit,
            'id': self.id,
            'title': self.title,
            'sandbox': str(self.sandbox),
        }

    def edit(self, blog):
        self.text = blog.text
        self.title = blog.title
        self.sandbox = blog.sandbox
        self.datetimeEdit = datetime.now().strftime('%Y.%m.%d %H:%M:%S')





