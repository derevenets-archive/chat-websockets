import aiohttp_jinja2
from aiohttp import web

from .models import Message


class ChatList(web.View):

    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        message = Message(self.request.db)
        messages = await message.get_messages()
        return {'messages': messages}


class WebSocket(web.View):
    pass
