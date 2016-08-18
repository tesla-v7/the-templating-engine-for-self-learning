from exeptions import UserError
from datetime import datetime
import uuid
import re

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
        return self.firstName + ' ' + self.lastName

    @property
    def fullName(self):
        return self.firstName + ' ' + self.lastName

    def load(self, postRequest):
        try:
            if len(postRequest['userName']) < 3:
                raise UserError('short userName')
                return False
        except KeyError:
            raise UserError('Not found userName in data POST request')
            return False
        avatarRaw = None
        for key in postRequest:
            try:
                if key != 'avatar':
                    setattr(self, key, postRequest[key])
                else:
                    avatarRaw = postRequest[key]
            except AttributeError:
                continue
        if avatarRaw:
            self.avatar = '/static/image/' + self.userName + '.jpg'
            f = open('.' + self.avatar, 'w+b')
            f.write(avatarRaw)
            f.close()
        return True

    def getPropertysInDict(self):
        return {
            'userName': self.userName,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'fullName': self.fullName,
            'avatar': self.avatar,
        }


class Post(Item):
    def __init__(self, autor, title='', text='', sandbox=False):
        self.autor = autor
        self.title = title
        self.text = text
        self.sandbox = sandbox
        self.datetime = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.datetimeEdit = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.id = str(uuid.uuid4().hex)

    def setDatetimtNow(self):
        self.datetime = datetime.now().strftime('%Y.%m.%d %H:%M:%S')

    def setDatetime(self, value):
        try:
            self.datetime = datetime.strftime(value, '%Y.%m.%d %H:%M:%S')
            return True
        except ValueError:
            self.setDatetimtNow()
            return False

    def load(self, postRequest):
        for key in postRequest:
            try:
                setattr(self, key, postRequest[key])
            except AttributeError:
                continue
        self.sandbox = bool(self.sandbox)

    def getPropertyInDictWithLiminWords(self, words=-1):
        text = self.text.replace('\n', '<br>')
        if words > 0:
            text = re.search(r'(\b.+?\b(\s+|$)){0,' + str(words) + '}', text).group(0) + '...'
        property = ['autor', 'datetime', 'id', 'title']
        result = dict([(key, getattr(self, key)) for key in property])
        result['text'] = text
        result['sandbox'] = str(self.sandbox)
        return result

    def getPropertysInDict(self):
        property = ['autor', 'text', 'datetime', 'datetimeEdit', 'id', 'title']
        result = dict([(key, getattr(self, key)) for key in property])
        result['sandbox'] = str(self.sandbox)
        return result

    def edit(self, blog):
        if self.__class__ != blog.__class__:
            return False
        self.text = blog.text
        self.title = blog.title
        self.sandbox = blog.sandbox
        self.datetimeEdit = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        return True