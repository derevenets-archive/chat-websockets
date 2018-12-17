import pathlib

from aiohttp import web

from chat_websockets.main.auth.views import LoginView, SingIn, SignOut
from chat_websockets.main.chat.views import ChatList

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route

    add_route('GET', '/',       ChatList,   name='main')

    add_route('*',   '/login',   LoginView, name='login')
    add_route('*',   '/signin',  SingIn,    name='signin')
    add_route('*',   '/signout', SignOut,   name='signout')

    # added static dir
    app.router.add_static(
        '/static/',
        path=(PROJECT_PATH / 'static'),
        name='static',
    )
