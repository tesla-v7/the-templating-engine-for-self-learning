class HttpMetod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    REFRESH = 'REFRESH'
    HEAD = 'HEAD'

class MimeType:
    html = 'text/html'
    css = 'text/css'
    js = 'ext/javascript'
    xml = 'text/xml'
    jpg = 'image/jpeg'
    png = 'image/png'
    gif = 'image/gif'
    ico = 'image/vnd.microsoft.icon'
    zip = 'application/zip'

    @classmethod
    def getMime(cls, filExtension):
        # tmp = dict([(attr, getattr(mimeType, attr)) for attr in dir(mimeType) if not hasattr(getattr(mimeType, attr), '__call__') and not attr.startswith("__")])
        tmp = dict([(attr, getattr(cls, attr)) for attr in dir(cls) if not hasattr(getattr(cls, attr), '__call__') and not attr.startswith("__")])
        try:
            mime = tmp[filExtension]
        except KeyError:
            mime = tmp['zip']
        return mime

class HttpVersion:
    ver11 = 'HTTP/1.1'
    ver09 = 'HTTP/0.9'

class HttpCode:
    Ok = 200
    Redirect = 302
    NotFound = 404
    ServerErr = 500

if __name__ == '__main__':
    print(MimeType.getMime('zip'))
