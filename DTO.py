from datetime import datetime
import uuid
import re
# from exeptions import DataError

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