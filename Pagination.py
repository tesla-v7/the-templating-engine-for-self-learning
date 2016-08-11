class Pagination():
    def __init__(self, action, itemMax=3, pageMax=1):
        self._action = action
        self._itemMax = itemMax
        self._pageMax = pageMax if pageMax > 0 else 1
        self._tmpAll = '<div class="pagination">{page}</div>'

    def getInt(self, data):
        try:
            pageNum = int(data['page'][0])
        except (KeyError, ValueError, TypeError):
            pageNum = 1
        return pageNum

    def getPageNum(self, blog, mas):
        page =1
        index = len(mas) - mas.index(blog)
        page = index // self._itemMax
        if index % self._itemMax:
            page += 1
        return page

    def getData(self, pageNum, masAZ):
        masZA = masAZ[::-1]
        try:
            pageNum = int(pageNum)
        except ValueError:
            pageNum = 1
        pageAll = len(masZA) // self._itemMax
        if len(masZA) % self._itemMax:
            pageAll += 1
        pageNum = max(1, min(pageAll, pageNum))
        startEl = self._itemMax * (pageNum - 1)
        endEl = startEl + self._itemMax
        contEl = len(masZA)

        if startEl > contEl:
            return []
        if endEl > contEl:
            return masZA[startEl:]
        return masZA[startEl: endEl]


    def render(self, pageNum, mas):
        try:
            pageNum = int(pageNum)
        except ValueError:
            pageNum = 1
        text = ''
        tmplPage = _Page(self._action + '?page=')
        pageAll = len(mas) // self._itemMax
        if len(mas) % self._itemMax:
            pageAll += 1
        pageNum = max(1, min(pageAll, pageNum))

        pageStar = pageNum - self._pageMax
        if pageStar <= 0:
            pageStar = 1

        pageEnd = pageNum + self._pageMax
        if pageEnd > pageAll:
            pageEnd = pageAll

        if pageNum > 1:
            text += tmplPage.render(1,'<<')
            text += tmplPage.render(pageNum - 1,'<')
        if pageStar > 1:
            text += '...'
        i = pageStar
        while i <= pageEnd:
            if i != pageNum:
                text += tmplPage.render(i)
            else:
                text += tmplPage.render(i, i, False)
            i += 1
        if pageEnd < pageAll:
            text += '...'
        if pageNum < pageAll:
            text += tmplPage.render(pageNum + 1,'>')
            text += tmplPage.render(pageAll,'>>')
        return self._tmpAll.format(page=text)

class _Page():
    def __init__(self, action):
        self._actin = action
        self._tmpHref = '<a href="{action}">{page}</a>'
        self._tmpPage = '<div class="page{select}">{num}</div>'

    def render(self, num, text=None, href=True):
        if text:
            tmp = self._tmpPage.format(num=text, select='' if href else ' select')
        else:
            tmp = self._tmpPage.format(num=str(num), select='')
        if href:
            if not num:
                return self._tmpHref.format(action=self._actin + text, page=tmp)
            else:
                return self._tmpHref.format(action=self._actin + str(num), page=tmp)
        return tmp

if __name__ == '__main__':
    page = Pagination('/admin/view', 3, 2)
    print(page.render(5, [1,2,3,4,5,6,7,8,9,1,1,1,1,1,1,1,1,1,1]))