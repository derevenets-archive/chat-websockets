from datetime import datetime

MESSAGE_COLLECTION = 'messages'


class Message:

    def __init__(self, db):
        self.collection = db[MESSAGE_COLLECTION]

    async def save(self, user, text):
        return await self.collection.insert_one({
            'user': user,
            'message': text,
            'time': datetime.now()
        })

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)

