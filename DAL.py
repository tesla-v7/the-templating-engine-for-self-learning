from DTO import User, Blog

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









