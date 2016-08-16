class Pagination():
    def __init__(self, urlAction, elementsOnPage=3, pageMax=1):
        self._urlAction = urlAction
        self._elementsOnPage = elementsOnPage
        self._pageMax = min(10, max(1, pageMax)) #if pageMax > 0 else 1
        self._templatePages = '<div class="pagination">{page}</div>'

    def convertPageStrToInt(self, data):
        try:
            pageNum = int(data['page'][0])
        except (KeyError, ValueError, TypeError):
            pageNum = 1
        return pageNum

    def getPageNum(self, blog, mas):
        page =1
        index = len(mas) - mas.index(blog)
        page = index // self._elementsOnPage
        if index % self._elementsOnPage:
            page += 1
        return page

    def getPageData(self, pageNum, masAZ):
        masZA = masAZ[::-1]
        try:
            pageNum = int(pageNum)
        except ValueError:
            pageNum = 1
        pageAll = len(masZA) // self._elementsOnPage
        if len(masZA) % self._elementsOnPage:
            pageAll += 1
        pageNum = max(1, min(pageAll, pageNum))
        startEl = self._elementsOnPage * (pageNum - 1)
        endEl = startEl + self._elementsOnPage
        contEl = len(masZA)

        if startEl > contEl:
            return []
        if endEl > contEl:
            return masZA[startEl:]
        return masZA[startEl: endEl]


    def render(self, pageCurrentNum, mas):
        try:
            pageCurrentNum = int(pageCurrentNum)
        except ValueError:
            pageCurrentNum = 1
        htmlPagination = ''
        page = _Page(self._urlAction + '?page=')
        pageAll = len(mas) // self._elementsOnPage
        if len(mas) % self._elementsOnPage:
            pageAll += 1
        pageCurrentNum = max(1, min(pageAll, pageCurrentNum))
        pageStar = max(1, pageCurrentNum - self._pageMax)
        pageEnd = min(pageAll, pageCurrentNum + self._pageMax)

        if pageCurrentNum > 1:
            htmlPagination += page.render(1,'<<')
            htmlPagination += page.render(pageCurrentNum - 1, '<')
        if pageStar > 1:
            htmlPagination += '...'
        i = pageStar
        while i <= pageEnd:
            if i != pageCurrentNum:
                htmlPagination += page.render(i)
            else:
                htmlPagination += page.render(i, i, False)
            i += 1
        if pageEnd < pageAll:
            htmlPagination += '...'
        if pageCurrentNum < pageAll:
            htmlPagination += page.render(pageCurrentNum + 1, '>')
            htmlPagination += page.render(pageAll,'>>')
        return self._templatePages.format(page=htmlPagination)

class _Page():
    def __init__(self, urlAction):
        self._urlAction = urlAction
        self._templateUrl = '<a href="{urlAction}">{page}</a>'
        self._templatePage = '<div class="page{select}">{num}</div>'

    def render(self, numPage, label=None, href=True):
        if label:
            tmp = self._templatePage.format(num=label, select='' if href else ' select')
        else:
            tmp = self._templatePage.format(num=str(numPage), select='')
        if href:
            if not numPage:
                return self._templateUrl.format(urlAction=self._urlAction + label, page=tmp)
            else:
                return self._templateUrl.format(urlAction=self._urlAction + str(numPage), page=tmp)
        return tmp

if __name__ == '__main__':
    page = Pagination('/admin/view', 3, 2)
    print(page.render(5, [1,2,3,4,5,6,7,8,9,1,1,1,1,1,1,1,1,1,1]))