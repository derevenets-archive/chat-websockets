import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session


def redirect(request, route_name):
    url = request.app.router[route_name].url_for()
    raise web.HTTPFound(url)


class ChatList(web.View):
    pass


class LoginView(web.View):
    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please, enter login or email'}
