from bot.handlers import choose_specialization


class GetMarkupHandler:

    @staticmethod
    def handle(message, bot):
        bot.send_message(
            message.chat.id,
            "Держи",
            reply_markup=choose_specialization.get_default_keyboard()
        )
