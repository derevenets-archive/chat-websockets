import json
from time import time

from aiohttp import web


def redirect(request, route_name):
    url = request.app.router[route_name].url_for()
    raise web.HTTPFound(url)


def set_session(session, user_id, request):
    session['user_id'] = str(user_id)
    session['last_visit'] = time()
    redirect(request, route_name='main')


def convert_json(message):
    return json.dumps({'error': message})
