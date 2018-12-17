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
    session['user_id'] = str(user_id)
    session['last_visit'] = time()
    redirect(request, route_name='main')


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

    async def post(self):
        data = await self.request.post()
        user = User(self.request.db, data)
        result = await user.check_user_exists()

        # user object was returned, so, user exists
        if isinstance(result, dict):
            session = await get_session(self.request)
            set_session(session, result['_id'], self.request)
        else:
            return web.Response(
                content_type='application/json',
                text=convert_json(result)
            )


class SingIn(web.View):
    @aiohttp_jinja2.template('auth/signin.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please enter your data'}

    async def post(self):
        """Get data from POST request, create new User model and set session"""
        data = await self.request.post()
        print('data', data)
        user = User(self.request.db, data)
        result = await user.create_user()

        # user was created successfully
        if isinstance(result.inserted_id, ObjectId):
            session = await get_session(self.request)
            set_session(session, result.inserted_id, self.request)
        else:
            return web.Response(
                content_type='application/json',
                text=convert_json(result)
            )


class SignOut(web.View):
    pass
