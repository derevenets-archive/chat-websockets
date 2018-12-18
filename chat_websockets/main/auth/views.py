import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from bson.objectid import ObjectId

from .models import User
from .utils import redirect, convert_json, set_session


class LoginView(web.View):

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user_id'):
            redirect(self.request, 'main')
        return {'content': 'Please, enter login or email'}

    async def post(self):
        """Get data from POST request, check user existence and set session"""
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
        if session.get('user_id'):
            redirect(self.request, 'main')
        return {'content': 'Please enter your data'}

    async def post(self):
        """Get data from POST request, create new User model and set session"""
        data = await self.request.post()
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
    async def get(self):
        session = await get_session(self.request)
        if session.get('user_id'):
            del session['user_id']
            redirect(self.request, 'login')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')
