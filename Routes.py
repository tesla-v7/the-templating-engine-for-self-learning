from httpConstant import httpMetod
import server_handlers as handlers

routes = [
    [httpMetod.GET, r'^/$', handlers.home],
    [httpMetod.GET, r'^/admin((/){1,1}[\w\d]*){0,0}$', handlers.logon],
    [httpMetod.POST, r'^/admin((/){1,1}[\w\d]*){0,0}$', handlers.logon],
    [httpMetod.GET, r'^/admin/view((/){1,1}[\w\d]*){0,3}$', handlers.admin],
    [httpMetod.GET, r'^/blog((/){1,1}[\w\d]*){1,1}$', handlers.blog],
    [httpMetod.GET, r'^/blog((/){1,1}[\w\d]*){2,2}$', handlers.read],
    [httpMetod.GET, r'^/static((/){1,1}[\w\d\.]*){2,2}$', handlers.static],
    [httpMetod.GET, r'^/registration$', handlers.registration],
    [httpMetod.POST, r'^/registration$', handlers.registration],
    [httpMetod.GET, r'^/logout$', handlers.logout],
    [httpMetod.POST, r'^/create$', handlers.create],
    [httpMetod.GET, r'^/create$', handlers.create],
    [httpMetod.GET, r'^/delete((/){1,1}[\w\d]*){1,1}$', handlers.delete],
    [httpMetod.GET, r'^/edit((/){1,1}[\w\d]*){1,1}$', handlers.edit],
    [httpMetod.POST, r'^/edit((/){1,1}[\w\d]*){1,1}$', handlers.edit],
]