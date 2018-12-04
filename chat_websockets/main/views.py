import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session


def redirect(request, route_name):
    url = request.app.router[route_name].url()
    raise web.HTTPFound(url)


class LoginView(web.View):
    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please, enter login or email'}
