from bot.handlers.Message import Message
from bot.models import User


class Inventory:

    @staticmethod
    def handle(message, bot):
        user = User.objects.get(telegram_id=message.chat.id)

        bot.send_message(message.chat.id, Message.inventory(user))
