from bot.constants import stats
from bot.handlers.Markup import Markup
from bot.handlers.Message import Message
from bot.models import User


class UpStat:

    @staticmethod
    def handle(call, bot):
        user = User.objects.get(telegram_id=call.message.chat.id)

        if user.unallocated_stat_points > 0:
            stat = user.stats.get(stat_id=getattr(stats, call.data[3:]))
            stat.value = stat.value + 1
            stat.save()

            user.unallocated_stat_points = user.unallocated_stat_points - 1
            user.save()

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=Message.stats(user),
                reply_markup=Markup.stats(),
            )

