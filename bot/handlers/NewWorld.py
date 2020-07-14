from bot.handlers.Markup import Markup
from bot.models import User
from bot.texts.Text import Text


class NewWorld:

    @staticmethod
    def handle(call, bot):
        user = User.objects.get(telegram_id=call.message.chat.id)

        if user.energy >= 1000:
            user.energy -= 1000
            user.save()
            bot.send_message(call.message.chat.id, 'Да здравствует новый мир!', reply_markup=Markup.default())
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=Text.foreword(),
            )
        else:
            bot.send_message(call.message.chat.id, "Недостаточно энергии")

