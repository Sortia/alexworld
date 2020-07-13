from telebot import types

from bot.models import User, Specialization


class ChooseSpecializationHandler:

    @staticmethod
    def handle(call, bot):
        user = User.objects.get(telegram_id=call.message.chat.id)

        if user.specialization_id:
            bot.send_message(call.message.chat.id, "Нельзя сменить класс!")
        else:
            specialization = Specialization.objects.get(name=call.data)

            user.specialization_id = specialization.id
            user.save()

            for specializationstat in specialization.specializationstat_set.all():
                user.stats.create(value=specializationstat.value, stat_id=specializationstat.stat_id)

            bot.send_message(
                call.message.chat.id,
                "Красавчик. Ты теперь " + specialization.title + '.',
                reply_markup=get_default_keyboard()
            )


def get_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    keyboard.row(
        types.KeyboardButton(text='Статистика'),
        types.KeyboardButton(text='Сражение')
    )

    keyboard.row(
        types.KeyboardButton(text='Блэкджек'),
        types.KeyboardButton(text='Шлюхи')
    )

    return keyboard
