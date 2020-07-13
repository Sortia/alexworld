from bot.handlers.Markup import Markup
from bot.models import User, Specialization


class ChooseSpecializationHandler:

    @staticmethod
    def handle(call, bot) -> None:
        user = User.objects.get(telegram_id=call.message.chat.id)

        if user.specialization_id:
            bot.send_message(call.message.chat.id, "Нельзя сменить класс!")
            return

        user.specialization = Specialization.objects.get(name=call.data)
        user.save()

        for specializationstat in user.specialization.stats.all():
            user.stats.create(value=specializationstat.value, stat_id=specializationstat.stat_id)

        bot.send_message(
            call.message.chat.id,
            "Красавчик. Ты теперь " + user.specialization.title + '.',
            reply_markup=Markup.default()
        )
