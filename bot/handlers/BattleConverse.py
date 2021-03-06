from telebot import types

from bot.handlers.Markup import Markup


class BattleConverse:

    @staticmethod
    def send_action_message(call, bot, battle, block=None, dodge=None, adding_message='\n'):
        if block is not None:
            if block:
                adding_message += 'Успешно блокировано'
            else:
                adding_message += 'Блокирование не удалось'

        if dodge is not None:
            if dodge:
                adding_message += 'Успешное уклонение'
            else:
                adding_message += 'Уклонение не удалось'

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_message(battle) + adding_message + '\n Ход: ' + str(battle.data['meta']['step_number']),
            reply_markup=Markup.battle(),
        )

    @staticmethod
    def send_victory_message(call, bot, battle):
        item_message = ''

        for item in battle.data['item']:

            if not item['count'] == 0:
                item_message += item['name'] + ' x' + str(item['count']) + '\n'

        if not item_message == '':
            item_message = 'Получено: \n' + item_message

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Победа\n\n' + item_message,
        )

    @staticmethod
    def send_defeat_message(call, bot, battle):
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Поражение \n\n' + battle.monster.win_speech,
        )


def get_message(battle) -> str:
    message = '👹Противник: ' + battle.monster.name + '\n' + \
              '❤ХП моба: ' + str(battle.data['monster']['current_hp']) + '/' + str(battle.data['monster']['max_hp']) + '\n' + \
              '❤Твое ХП: ' + str(battle.data['user']['current_hp']) + '/' + str(battle.data['user']['max_hp']) + '\n'

    return message


