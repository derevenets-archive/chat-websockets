from aiohttp import web
from aiohttp_session import get_session


async def authorize(app, handler):

    async def middleware(request):
        def check_path(path):
            result = True
            for r in ['/login', '/static/', '/signin',
                      '/signout', '/_debugtoolbar/']:
                if path.startswith(r):
                    result = False
            return result

        session = await get_session(request)
        if session.get('user'):
            return await handler(request)
        elif check_path(request.path):
            url = request.app.router['login'].url_for()
            raise web.HTTPFound(url)

        return await handler(request)

    return middleware


async def db_handler(app, handler):
    async def middleware(request):
        if (request.path.startswith('/static/')
                or request.path.startswith('/_debugtoolbar')):
            return await handler(request)

        request.db = app.db
        return handler(request)

    return middleware
