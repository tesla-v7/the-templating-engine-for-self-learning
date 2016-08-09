class httpMetod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    REFRESH = 'REFRESH'
    HEAD = 'HEAD'

class mimeType:
    html = 'text/html'
    css = 'text/css'
    js = 'ext/javascript'
    xml = 'text/xml'
    jpg = 'image/jpeg'
    png = 'image/png'
    gif = 'image/gif'
    ico = 'image/vnd.microsoft.icon'

    @classmethod
    def getAttributes(cls):
        return dict([(attr, getattr(mimeType, attr)) for attr in dir(mimeType) if not hasattr(getattr(mimeType, attr), '__call__') and not attr.startswith("__")])

class httpVersion:
    ver11 = 'HTTP/1.1'
    ver09 = 'HTTP/0.9'

class httpCode:
    Ok = 200
    Redirect = 302
    NotFound = 404
    ServerErr = 500

if __name__ == '__main__':
    print(mimeType.getAttributes())
