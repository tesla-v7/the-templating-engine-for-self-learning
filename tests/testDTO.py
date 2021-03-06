import unittest
from DTO import User, Blog

class DTOTest(unittest.TestCase):
    def testUser(self):
        userStandard = User('userName', 'password', 'firstName', 'lastName')
        user1 = User('', '', '', '')
        user1.load({
            'userName': 'userName',
            'password': 'password',
            'firstName': 'firstName',
            'lastName': 'lastName',
        })
        self.assertEqual(userStandard.getPropertysInDict(), user1.getPropertysInDict())

    def testBlog(self):
        blogStahdart = Blog('autor', 'title', 'text')
        blog1 = Blog('---')
        blog1.load({
            'autor': 'autor',
            'title': 'title',
            'text': 'text',
        })
        blogStahdartDict = blogStahdart.getPropertyInDict()
        blog1Dict = blog1.getPropertyInDict()
        self.assertNotEqual(blogStahdartDict, blog1Dict)
        del blogStahdartDict['id']
        del blog1Dict['id']
        self.assertEqual(blogStahdartDict, blog1Dict)