from bson.objectid import ObjectId

USER_COLLECTION = 'users'


class User:
    def __init__(self, db, data) -> None:
        self.db = db
        self.collection = self.db[USER_COLLECTION]
        self.email = data.get('email')
        self.login = data.get('login')
        self.password = data.get('password')
        self.id = data.get('id')

    async def check_user_exists(self):
        """Check if user with provided login exists"""
        return await self.collection.find_one({'login': self.login})

    async def get_login(self):
        user = await self.collection.find_one({'_id': ObjectId(self.id)})
        print('get_login user', user)
        return user.get('login')

    async def create_user(self):
        user_exists = await self.check_user_exists()
        result = 'User exists'
        if not user_exists:
            result = await self.collection.insert_one({
                'email': self.email,
                'login': self.login,
                'password': self.password
            })
        return result
