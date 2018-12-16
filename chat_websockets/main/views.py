import json
from time import time

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from bson.objectid import ObjectId

from .auth.models import User


def redirect(request, route_name):
    url = request.app.router[route_name].url_for()
    raise web.HTTPFound(url)


def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    print(session)
    redirect(request, 'main')


def convert_json(message):
    return json.dumps({'error': message})


class ChatList(web.View):
    pass


class LoginView(web.View):
    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please, enter login or email'}


class SingIn(web.View):
    @aiohttp_jinja2.template('auth/signin.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please enter your data'}

    async def post(self):
        data = await self.request.post()
        user = User(self.request.db, data)
        user_id = await user.create_user()
        print(user_id, type(user_id), "sign")
        if isinstance(user_id, ObjectId):
            session = await get_session(self.request)
            set_session(session, user_id, self.request)
        else:
            return web.Response(
                content_type='application/json',
                text=convert_json(user_id)
            )
