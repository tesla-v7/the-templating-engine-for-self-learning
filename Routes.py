from httpConstant import httpMetod
import server_handlers as handlers

routes = [
    [httpMetod.GET, r'^/$', handlers.homePage],
    [httpMetod.GET, r'^/admin((/){1,1}[\w\d]*){0,0}$', handlers.logonUser],
    [httpMetod.POST, r'^/admin((/){1,1}[\w\d]*){0,0}$', handlers.logonUser],
    [httpMetod.GET, r'^/admin/view((/){1,1}[\w\d]*){0,3}$', handlers.postsEdit],
    [httpMetod.GET, r'^/blog((/){1,1}[\w\d]*){1,1}$', handlers.blogsRead],
    [httpMetod.GET, r'^/blog((/){1,1}[\w\d]*){2,2}$', handlers.blogRead],
    [httpMetod.GET, r'^/static((/){1,1}[\w\d\.]*){2,2}$', handlers.staticContentReturn],
    [httpMetod.GET, r'^/registration$', handlers.registrationUser],
    [httpMetod.POST, r'^/registration$', handlers.registrationUser],
    [httpMetod.GET, r'^/logout$', handlers.logoutUser],
    [httpMetod.POST, r'^/create$', handlers.createPost],
    [httpMetod.GET, r'^/create$', handlers.createPost],
    [httpMetod.GET, r'^/delete((/){1,1}[\w\d]*){1,1}$', handlers.deletePostId],
    [httpMetod.GET, r'^/edit((/){1,1}[\w\d]*){1,1}$', handlers.editPost],
    [httpMetod.POST, r'^/edit((/){1,1}[\w\d]*){1,1}$', handlers.editPost],
]