from bot.handlers.Markup import Markup


class GetMarkupHandler:

    @staticmethod
    def handle(message, bot):
        bot.send_message(
            message.chat.id,
            "Держи",
            reply_markup=Markup.default()
        )
