from bot.handlers.Markup import Markup
from bot.models import User, Stat
from bot.texts.Text import Text


class Start:

    @staticmethod
    def handle(message, bot) -> None:
        try:
            User.objects.get(telegram_id=message.chat.id)
        except User.DoesNotExist:
            Start.create_user(message.from_user)

            bot.send_message(message.chat.id, Text.foreword(), reply_markup=Markup.new_world())
            # bot.send_message(message.chat.id, Text.welcome(), reply_markup=Markup.new_world())

    @staticmethod
    def create_user(user_data):
        user = User.objects.create(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            telegram_id=user_data.id,
            language_code=user_data.language_code,
            is_bot=user_data.is_bot,
        )

        for stat in Stat.objects.all():
            user.stats.create(stat=stat)
