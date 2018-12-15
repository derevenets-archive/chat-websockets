import base64
from pathlib import Path
from typing import Optional, List

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import cookie_storage, session_middleware
from cryptography import fernet

from chat_websockets.routes import init_routes
from chat_websockets.utils.common import init_config
from .middlewares import authorize

path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    """ Initialize jinja2 template for application """
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


def init_app(config: Optional[List[str]] = None) -> web.Application:
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)

    app = web.Application(
        middlewares=[
            session_middleware(
                cookie_storage.EncryptedCookieStorage(secret_key)
            ),
            authorize,
        ]
    )

    init_jinja2(app)
    init_config(app, config=config)
    init_routes(app)

    return app
