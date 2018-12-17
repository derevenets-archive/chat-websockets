import base64

import aiohttp_debugtoolbar
from aiohttp import web
from aiohttp_session import setup, cookie_storage

from .app import init_app, SECRET_KEY


def create_app() -> web.Application:
    app = init_app()
    aiohttp_debugtoolbar.setup(app, check_host=False)

    secret_key = base64.urlsafe_b64decode(SECRET_KEY)
    setup(app, cookie_storage.EncryptedCookieStorage(secret_key))

    return app


def main() -> None:
    app = init_app()
    app_settings = app['config']['app']

    web.run_app(
        app,
        host=app_settings['host'],
        port=app_settings['port'],
    )


if __name__ == '__main__':
    main()
