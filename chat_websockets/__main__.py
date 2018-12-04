import base64

from aiohttp import web
from aiohttp_session import setup, cookie_storage
from cryptography import fernet

from .app import init_app


def create_app() -> web.Application:
    app = init_app()
    # import aiohttp_debugtoolbar
    # aiohttp_debugtoolbar.setup(app, check_host=False)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
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
