from bot.handlers.Markup import Markup
from bot.models import User


class Start:

    @staticmethod
    def handle(message, bot) -> None:
        try:
            User.objects.get(telegram_id=message.chat.id)
            bot.send_message(message.chat.id, "Ты уже зарегестрирован.")
        except User.DoesNotExist:
            user = Start.create_user(message.from_user)
            specialization_buttons = Markup.specializations()

            bot.send_message(message.chat.id, "Йо! Ты успешно зареган.")

            bot.send_message(
                user.telegram_id,
                "Теперь выбери специализацию из предложенных.",
                reply_markup=specialization_buttons
            )

    @staticmethod
    def create_user(user_data) -> User:
        return User.objects.create(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            telegram_id=user_data.id,
            language_code=user_data.language_code,
            is_bot=user_data.is_bot,
        )
