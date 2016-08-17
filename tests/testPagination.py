import unittest
from Pagination import Pagination

class PaginationTest(unittest.TestCase):
    def testPageNum(self):
        data = range(100)
        page = Pagination('/test', elementsOnPage=5, pageMax=2)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[0], data), 20)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[2], data), 20)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[4], data), 20)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[5], data), 2)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[99], data), 20)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[97], data), 20)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[95], data), 20)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[94], data), 19)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[92], data), 19)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[90], data), 19)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[50], data), 11)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[52], data), 11)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[54], data), 11)
        self.assertEqual(page.getPageNumberOfBlogsSortZA(data[13], data), 3)

    def testDataPage(self):
        data = range(100)
        page = Pagination('/test', elementsOnPage=5, pageMax=2)
        self.assertEqual(page.getPageElementsSortZA(1, data), data[:5])
        self.assertEqual(page.getPageElementsSortZA(20, data), data[95:])
        self.assertEqual(page.getPageElementsSortZA(2, data), data[5:10])
        self.assertEqual(page.getPageElementsSortZA(19, data), data[90:95])
        self.assertEqual(page.getPageElementsSortZA(13, data), data[60:65])
