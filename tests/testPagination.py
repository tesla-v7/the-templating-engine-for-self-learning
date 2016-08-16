import unittest
from Pagination import Pagination

class PaginationTest(unittest.TestCase):
    def testPageNum(self):
        data = range(100)
        page = Pagination('/test', elementsOnPage=5, pageMax=2)
        self.assertEqual(page.getPageNumberOfBlog(data[0], data), 20)
        self.assertEqual(page.getPageNumberOfBlog(data[2], data), 20)
        self.assertEqual(page.getPageNumberOfBlog(data[4], data), 20)
        self.assertEqual(page.getPageNumberOfBlog(data[5], data), 2)
        self.assertEqual(page.getPageNumberOfBlog(data[99], data), 20)
        self.assertEqual(page.getPageNumberOfBlog(data[97], data), 20)
        self.assertEqual(page.getPageNumberOfBlog(data[95], data), 20)
        self.assertEqual(page.getPageNumberOfBlog(data[94], data), 19)
        self.assertEqual(page.getPageNumberOfBlog(data[92], data), 19)
        self.assertEqual(page.getPageNumberOfBlog(data[90], data), 19)
        self.assertEqual(page.getPageNumberOfBlog(data[50], data), 11)
        self.assertEqual(page.getPageNumberOfBlog(data[52], data), 11)
        self.assertEqual(page.getPageNumberOfBlog(data[54], data), 11)
        self.assertEqual(page.getPageNumberOfBlog(data[13], data), 3)

    def testDataPage(self):
        data = range(100)
        page = Pagination('/test', elementsOnPage=5, pageMax=2)
        self.assertEqual(page.getPageElements(1, data), data[:5])
        self.assertEqual(page.getPageElements(20, data), data[95:])
        self.assertEqual(page.getPageElements(2, data), data[5:10])
        self.assertEqual(page.getPageElements(19, data), data[90:95])
        self.assertEqual(page.getPageElements(13, data), data[60:65])
