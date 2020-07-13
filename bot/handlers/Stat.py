from bot.models import User


class Stat:

    @staticmethod
    def handle(message, bot):
        try:
            user = User.objects.get(telegram_id=message.chat.id)
            message_text = ''

            for user_stat in user.stats.all():
                message_text += user_stat.stat.title + ': ' + str(user_stat.value) + '\n'

            bot.send_message(message.chat.id, message_text)

        except User.DoesNotExist:
            return
