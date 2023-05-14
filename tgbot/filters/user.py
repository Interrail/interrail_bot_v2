import aiohttp
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

USERS = [5331201165, 2484640, 730469318, 47866924, 810931806, 59912687]


class UserAccess(BoundFilter):
    ACCESS = False

    async def check(self, message: Message):

        data = {'telegram_id': message.from_user.id}

        async with aiohttp.ClientSession() as session:
            async with session.post('https://order.interrail.uz/user/access_bot/', data=data) as resp:
                if resp.status == 200:
                    self.ACCESS = True
                else:
                    self.ACCESS = False
        return self.ACCESS


class IsGroup(BoundFilter):

    async def check(self, message: Message):
        return str(message.chat.type) == 'supergroup'
