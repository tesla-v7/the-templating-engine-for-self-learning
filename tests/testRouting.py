import unittest
from Routing import Router

class RoutingTest(unittest.TestCase):
    def testRout(self):
        router = Router()
        router.addRoute(['GET', r'^/$', self.helloWorld])
        router.addRoute(['GET', r'^/xxx((/){1,1}[\w\d]*){0,2}$', self.helloWorld])
        self.command = 'GET'
        self.path = '/'
        self.test =  'Hello, world!'
        self.assertEqual(router.handle(self), 'Hello, world!')
        self.path = '/xxx'
        self.assertEqual(router.handle(self), 'Hello, world!')
        self.path = '/xxx/xxxx'
        self.assertEqual(router.handle(self), 'Hello, world!')
        self.path = '/xxx/xxxx/xxxxx'
        self.assertEqual(router.handle(self), 'Hello, world!')
        self.path = '/xxx/xxxx/xxxxx?id=qqq'
        self.assertEqual(router.handle(self), 'Hello, world!')
        self.path = '/xxx/xxxx/xxxxx?id=qqq&iid=jfjf'
        self.assertEqual(router.handle(self), 'Hello, world!')

    def helloWorld(self, request):
        return request.test