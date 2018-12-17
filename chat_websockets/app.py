import base64
from pathlib import Path
from typing import Optional, List

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import cookie_storage, session_middleware
from motor import motor_asyncio as ma

from chat_websockets.routes import init_routes
from chat_websockets.utils.common import init_config
from .middlewares import authorize, db_handler

path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    """ Initialize jinja2 template for application """
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


# TODO: move to settings and make it more safe
SECRET_KEY = b'dmnWwD9-Up3q8MoEVsC1LhhnTQ_snTmLKJ-A9s8OivI='


# TODO: should be refactored or moved to better place
async def on_shutdown(server, app, handler):
    server.close()
    await server.wait_closed()
    app.client.close()  # database connection close
    await app.shutdown()
    await handler.finish_connections(10.0)
    await app.cleanup()


def init_app(config: Optional[List[str]] = None) -> web.Application:
    secret_key = base64.urlsafe_b64decode(SECRET_KEY)

    app = web.Application(
        middlewares=[
            session_middleware(
                cookie_storage.EncryptedCookieStorage(secret_key)
            ),
            authorize,
            db_handler
        ]
    )

    init_jinja2(app)
    init_config(app, config=config)
    init_routes(app)

    # MONGO_HOST    - mongodb://mongo:27017
    # MONGO_DB_NAME - chat_test_db
    app.client = ma.AsyncIOMotorClient('mongodb://mongo_db:27017')
    app.db = app.client['chat_test_db']

    # app.on_shutdown.append(on_shutdown)

    return app
