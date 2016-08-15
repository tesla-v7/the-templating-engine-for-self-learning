# coding: utf-8
import re
#import exeptions
from exeptions import TemplateError
import operator

BLOCK_ROOT = 'root'
BLOCK_CODE = 'code'
BLOCK_VAR = 'var'
BLOCK_TEXT = 'txt'

logical = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# class TemplateError(Exception):
#     pass

class _Node(object):
    def __init__(self, text):
        self._fork = None
        self._next = None
        self._type = BLOCK_ROOT
        self._code = text

    def setFork(self, fork):
        self._fork = fork

    def setNext(self, next):
        self._next = next

    def getFork(self):
        return self._fork

    def getNext(self):
        return self._next

    def getCode(self):
        return self._code

    def getType(self):
        return self._type

    def render(self, rawData):
        text = ''
        data = []
        data.append(rawData)
        if (self._next):
            text += self._next.render(data)
        return text

    def compil(self, data):
        pass

    def getVal(self, key, data):
        keys = key.split('.')
        numberKey = len(keys)
        if numberKey == 0:
            return None
        for newScopeData in data:
            try:
                if newScopeData.get(keys[0]):
                    if numberKey == 1:
                        return newScopeData[keys[0]]
                    else:
                        return self.getVal('.'.join(keys[1:]), [newScopeData[keys[0]]])
            except AttributeError as ex:
                raise TemplateError('Parce data error: ' + str(ex))
        return None

    def prn(self):
        print(self._code)
        if (self._fork):
            self._fork.prn()
        if (self._next):
            self._next.prn()

class _NodeText(_Node):
    def __init__(self, text):
        super(_NodeText, self).__init__(text)
        self._type = BLOCK_TEXT

    def render(self, data):
        tmp = self.compil(data)
        if (self._next):
            tmp += self._next.render(data)
        return tmp

    def compil(self, data):
        return self._code

class _NodeVar(_Node):
    def __init__(self, text):
        super(_NodeVar, self).__init__(text)
        self._type = BLOCK_VAR
        self._code = self._code[2:-2]

    def render(self, data):
        text = self.compil(data)
        if (self._next):
            text += self._next.render(data)
        return text

    def compil(self, data):
        tmp = self.getVal(self._code, data)
        if tmp == None:
            # return ' DEADBEAF '
            raise TemplateError('Key {{' + self._code + '}} not found in data')
        if(type(tmp) != 'str'):
            tmp = str(tmp)
        return tmp

class _NodeCode(_Node):
    def __init__(self, text):
        super(_NodeCode, self).__init__(text)
        self._type = BLOCK_CODE
        self._code = self._code[2:-2]

class _NodeFor(_NodeCode):
    def render(self, data):
        text = self.compil(data)
        if(self._next):
            text += self._next.render(data)
        return text

    def compil(self, data):
        text = ''
        vars = self._code.split(' ')
        if len(vars) != 4:
            return ''
        try:
            vars[3] = vars[3].replace(':', '')
            localVar = self.getVal(vars[3], data)
            if localVar == None:
                return ''
        except KeyError:
            return ''
        i = 0
        for step in localVar:
            i += 1
            data.append(dict([(vars[1], step)]))
            text += self._fork.render(data)
            _ = data.pop()
        return text

class _NodeIf(_NodeCode):
    def render(self, data):
        tmp = ''
        if self._compil(data):
            if (self._fork):
                tmp += self._fork.render(data)
        else:
            point = self._fork
            while point != None and point._code.find('else') == -1:
                point = point._next
            tmp +=  point.render(data, True) if point != None else ''
        if (self._next):
            tmp += self._next.render(data)
        return tmp

    def _compil(self, data):
        vars = self._code.split(' ')
        if len(vars) != 4:
            return False
        vars[3] = vars[3].replace(':', '')
        return self._compare(self.getVal(vars[1], data), self.getVal(vars[3], data), vars[2])

    def _compare(self, var1, var2, oprtr):
        try:
            result = logical[oprtr](var1, var2)
            print('if/--', self._code, var1, var2, oprtr, result)
        except KeyError as ex:
            raise TemplateError('Parce logical operations error: ' + str(ex) + ' ' + self._code)
        return result

    def getVal(self, key, data):
        keys = key.split('.')
        if (len(keys) == 0):
            return None
        for dd in data:
            try:
                if dd.get(keys[0]):
                    if (len(keys) == 1):
                        return dd[keys[0]]
                    else:
                        return self.getVal('.'.join(keys[1:]), [dd[keys[0]]])
            except AttributeError as ex:
                raise TemplateError('Parce data error: ' + str(ex))
        return key

class _NodeElse(_NodeCode):
    def render(self, data, condition = False):
        tmp = ''#self.compil(data)
        if (condition):
            tmp += self._fork.render(data)
        if (self._next):
            tmp += self._next.render(data)
        return tmp

class _NodeEnd(_Node):
    def __init__(self, text):
        super(_NodeEnd, self).__init__(text)
        self._type = BLOCK_CODE
    def render(self, data):
        return ''

class _Parse():
    def __init__(self, templateText = None):
        self.__pars = []
        if (templateText):
            self.__parsRaw(templateText)

    def __parsRaw(self, templateText):  #парс в массив по типу лексем
        self.__pars = re.split(r'({{.*?}}|{%.*?%})', self.__trim(templateText))
        self.__pars = self.__trimPars(self.__pars)
        pass

    def __trim(self, templateText):  # удаление не значемых литералов
        tmpTxt = re.sub('[\r\n]', '', templateText)
        tmpTxt = re.sub('[\ \t]{2,}', ' ', tmpTxt)
        tmpTxt = re.sub('<!--.*?-->', '', tmpTxt)
        tmpTxt = re.sub('\{\%[\s]{1,}', '{%', tmpTxt)
        tmpTxt = re.sub('[\s]{1,}\%\}', '%}', tmpTxt)
        return tmpTxt

    def __trimPars(self, tmpl):  # удаление пустых блоков
        tmpPars = []
        for txt in tmpl:
            buf = txt.strip()
            if (buf != ''):
                tmpPars.append(buf)
        return tmpPars

    def getParse(self):
        return self.__pars

class _Tree():
    def __init__(self, tmplParse):
        self._root = None
        if tmplParse:
            self._root = self.createTree(tmplParse)

    def createTree(self, tmplParse):
        if not len(tmplParse):
            return None
        stack = []
        root = _Node('root')
        point = root
        for sheet in tmplParse:
            node = self.createNode(sheet)
            if (point.getType() == BLOCK_TEXT or point.getType() == BLOCK_VAR or point.getType() == BLOCK_ROOT):
                point.setNext(node)
                point = point.getNext()
            elif (point.getType() == BLOCK_CODE):
                if (point.getCode().find('end') == -1):
                    if point.getCode().find('else') == -1:
                        stack.append(point)
                    else:
                        point.setNext(_NodeEnd('end'))
                    point.setFork(node)
                    point = point.getFork()
                else:
                    if len(stack) == 0:
                        raise TemplateError('Parce error: excess block {% end %}')
                    point = stack.pop()
                    point.setNext(node)
                    point = point.getNext()
        # root.prn()
        return root

    def createNode(self, sheet):
        node = None
        if (sheet[0:2] == '{{'):
            node = _NodeVar
        elif (sheet[0:2] == '{%'):
            if (sheet.find('end') != -1):
                node = _NodeEnd
                # pass
            elif (sheet.find('for') != -1):
                node = _NodeFor
                # pass
            elif (sheet.find('if') != -1):
                node = _NodeIf
                # pass
            elif (sheet.find('else') != -1):
                node = _NodeElse
            else:
                raise TemplateError('Parce error: unknown block operator ' + sheet)
        else:
            node = _NodeText
        return node(sheet)

    def getCompil(self):
        return self._root

class Template():
    def __init__(self, fileName = None, text=None):
        self.__path = './template/'
        self.fileName = fileName
        if fileName:
            self._tmplParse = _Parse(self.__readTemplate(fileName)).getParse()
            self._root = _Tree(self._tmplParse).getCompil()
            del self._tmplParse
        if text:
            self._tmplParse = _Parse(text).getParse()
            self._root = _Tree(self._tmplParse).getCompil()
            del self._tmplParse

    def __readTemplate(self, fileName):
        try:
            file = open(self.__path + fileName, 'r')
            tmplRAW = file.read()
            file.close()
            return tmplRAW
        except (FileNotFoundError, PermissionError) as ex:
            # print('-----/ ', ex)
            raise TemplateError('File template error: ' + str(ex))

    def render(self, data):
        try:
            tmp = str.encode(re.sub('[\s]{2,}', ' ', self._root.render(data)))
            return tmp
        except TemplateError as ex:
            print(' '.join(['ERR', self.fileName, str(ex)]))

    def prn(self):
        self._root.prn()

if(__name__ == '__main__'):
    data = {
        'lang': 'ru',
        'title': 'title_test',
        'createPostLink': '#link',
        'createPostLabel': 'link_label',
        'posts': [
            {'id': 1.1, 'post': 'p1', 'autor': 'a1', 'datatime': 'd1'},
            {'id': 2, 'post': 'p2', 'autor': 'a2', 'datatime': 'd2'},
            {'id': 3.55, 'post': 'p3', 'autor': 'a3', 'datatime': 'd3'},
            {'id': 4, 'post': 'p4', 'autor': 'a4', 'datatime': 'd4'},
        ],
        'tests': [
            {'id': 1, 'mas': [{'t1': '_11'}, {'t1': '_12'}, {'t1': '_13'}, {'t1': '_14'}]},
            {'id': '2', 'mas': [{'t1': '_21'}, {'t1': '_22'}, {'t1': '_23'}, {'t1': '_24'}]},
            {'id': 3, 'mas': [{'t1': '_31'}, {'t1': '_32'}, {'t1': '_33'}, {'t1': '_34'}]},
        ],
        # '': '',
        # '': '',
        # '': '',
        # '': '',
    }
    tmpl = Template('index.html')
    print(tmpl.render(data))
    # tmpl.prn()