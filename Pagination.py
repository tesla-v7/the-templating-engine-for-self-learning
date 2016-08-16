class Pagination():
    def __init__(self, urlAction, elementsOnPage=3, pageMax=1):
        self._urlAction = urlAction
        self._elementsOnPage = elementsOnPage
        self._pageMax = min(10, max(1, pageMax))
        self._templatePages = '<div class="pagination">{page}</div>'

    def getPageNumberInRequest(self, data):
        try:
            pageNum = int(data['page'][0])
        except (KeyError, ValueError, TypeError):
            pageNum = 1
        return pageNum

    def getPageNumberOfBlog(self, blog, listElementsAZ):
        index = len(listElementsAZ) - listElementsAZ.index(blog)
        page = index // self._elementsOnPage
        if index % self._elementsOnPage:
            page += 1
        return page

    def getPageElements(self, pageNum, listElementsAZ):
        listElemtnsZA = listElementsAZ[::-1]
        try:
            pageNum = int(pageNum)
        except ValueError:
            pageNum = 1
        allElements = len(listElemtnsZA)
        pageAll = allElements // self._elementsOnPage
        pageNum = max(1, min(pageAll, pageNum))
        if allElements % self._elementsOnPage:
            pageAll += 1
        startElement = self._elementsOnPage * (pageNum - 1)
        endElement = startElement + self._elementsOnPage
        if startElement > allElements:
            return []
        if endElement > allElements:
            return listElemtnsZA[startElement:]
        return listElemtnsZA[startElement: endElement]


    def render(self, pageCurrentNumber, listElements):
        try:
            pageCurrentNumber = int(pageCurrentNumber)
        except ValueError:
            pageCurrentNumber = 1
        htmlPagination = ''
        page = _Page(self._urlAction + '?page=')
        pageAll = len(listElements) // self._elementsOnPage
        if len(listElements) % self._elementsOnPage:
            pageAll += 1

        pageCurrentNumber = max(1, min(pageAll, pageCurrentNumber))
        pageStar = max(1, pageCurrentNumber - self._pageMax)
        pageEnd = min(pageAll, pageCurrentNumber + self._pageMax)

        if pageStar > 1:
            htmlPagination += page.render(1,'<<')
        if pageStar > 2:
            htmlPagination += page.render(pageCurrentNumber - 1, '<')
        if pageStar > 1:
            htmlPagination += '...'
        i = pageStar
        while i <= pageEnd:
            if i != pageCurrentNumber:
                htmlPagination += page.render(i)
            else:
                htmlPagination += page.render(i, i, False)
            i += 1
        if pageEnd < pageAll:
            htmlPagination += '...'
        if pageEnd < pageAll - 1:
            htmlPagination += page.render(pageCurrentNumber + 1, '>')
        if pageEnd < pageAll:
            htmlPagination += page.render(pageAll,'>>')
        return self._templatePages.format(page=htmlPagination)

class _Page():
    def __init__(self, urlAction):
        self._urlAction = urlAction
        self._templateUrl = '<a href="{urlAction}">{page}</a>'
        self._templatePage = '<div class="page{select}">{num}</div>'

    def render(self, numPage, label=None, href=True):
        if not label:
            label = str(numPage)
        htmlPage = self._templatePage.format(num=label, select='' if href else ' select')
        if href:
            return self._templateUrl.format(urlAction=self._urlAction + str(numPage), page=htmlPage)
        return htmlPage

if __name__ == '__main__':
    page = Pagination('/admin/view', 3, 2)
    print(page.render(5, [1,2,3,4,5,6,7,8,9,1,1,1,1,1,1,1,1,1,1]))