from telebot import types

from bot.models import User, Specialization


class StartHandler:

    @staticmethod
    def handle(message, bot):
        try:
            User.objects.get(telegram_id=message.chat.id)
            bot.send_message(message.chat.id, "Ты уже зарегестрирован.")
        except User.DoesNotExist:
            user = create_user(message.from_user)
            specialization_keyboard = get_choose_specialization_keyboard()

            bot.send_message(message.chat.id, "Йо! Ты успешно зареган.")

            bot.send_message(
                user.telegram_id,
                "Теперь выбери специализацию из предложенных.",
                reply_markup=specialization_keyboard
            )


def create_user(user_data):
    return User.objects.create(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        telegram_id=user_data.id,
        language_code=user_data.language_code,
        is_bot=user_data.is_bot,
    )


def get_choose_specialization_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    specializations = Specialization.objects.all()

    for specialization in specializations:
        btn = types.InlineKeyboardButton(text=specialization.title, callback_data=specialization.name)
        keyboard.add(btn)

    return keyboard
