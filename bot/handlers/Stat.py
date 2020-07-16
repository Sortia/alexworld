from bot.handlers.Markup import Markup
from bot.handlers.Message import Message
from bot.models import User


class Stat:

    @staticmethod
    def handle(message, bot):
        try:
            user = User.objects.get(telegram_id=message.chat.id)

            text = Message.stats(user) + '\n\n' + Message.equip(user)

            bot.send_message(message.chat.id, text, reply_markup=Markup.stats())

        except User.DoesNotExist:
            return
