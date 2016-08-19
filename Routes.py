from httpConstant import HttpMetod
import server_handlers as handlers

routes = [
    [HttpMetod.GET, r'^/$', handlers.pageHome],
    [HttpMetod.GET, r'^/logon((/){1,1}[\w\d]*){0,0}$', handlers.pageLogonUser],
    [HttpMetod.POST, r'^/logon((/){1,1}[\w\d]*){0,0}$', handlers.logonUser],
    [HttpMetod.GET, r'^/admin/view((/){1,1}[\w\d]*){0,3}$', handlers.pageEditPosts],
    [HttpMetod.GET, r'^/blog((/){1,1}[\w\d]*){1,1}$', handlers.pageReadBlog],
    [HttpMetod.GET, r'^/blog((/){1,1}[\w\d]*){2,2}$', handlers.pageReadPost],
    [HttpMetod.GET, r'^/static((/){1,1}[\w\d\.]*){2,2}$', handlers.staticContentReturn],
    [HttpMetod.GET, r'^/registration$', handlers.pageRegistrationUser],
    [HttpMetod.POST, r'^/registration$', handlers.registrationUser],
    [HttpMetod.GET, r'^/logout$', handlers.logoutUser],
    [HttpMetod.POST, r'^/create$', handlers.createPost],
    [HttpMetod.GET, r'^/create$', handlers.pageCreatePost],
    [HttpMetod.GET, r'^/delete((/){1,1}[\w\d]*){1,1}$', handlers.deletePostId],
    [HttpMetod.GET, r'^/edit((/){1,1}[\w\d]*){1,1}$', handlers.pageEditPost],
    [HttpMetod.POST, r'^/edit((/){1,1}[\w\d]*){1,1}$', handlers.editPost],
]