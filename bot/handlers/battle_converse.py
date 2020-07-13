from telebot import types


def send_action_message(call, bot, battle, block=None, dodge=None, adding_message=''):
    if block is not None:
        if block:
            adding_message = '\n Успешно блокировано'
        else:
            adding_message = '\n Блокирование не удалось'

    if dodge is not None:
        if dodge:
            adding_message = '\n Успешное уклонение'
        else:
            adding_message = '\n Уклонение не удалось'

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=get_message(battle) + adding_message,
        reply_markup=get_markup(),
    )


def send_victory_message(call, bot, battle):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Победа',
    )


def send_defeat_message(call, bot, battle):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Поражение',
    )


def get_message(battle):
    # battle_data = json.loads(battle.data)

    message = '👹Противник: ' + battle.monster.name + '\n' + \
              '❤ХП моба: ' + battle.data['monster']['current_hp'] + '/' + battle.data['monster']['max_hp'] + '\n' + \
              '❤Твое ХП: ' + battle.data['user']['current_hp'] + '/' + battle.data['user']['max_hp'] + '\n'

    return message


def get_markup():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(text='Атака', callback_data='battle_attack'))
    keyboard.add(types.InlineKeyboardButton(text='Блок', callback_data='battle_block'))
    keyboard.add(types.InlineKeyboardButton(text='Уклонение', callback_data='battle_dodge'))

    return keyboard


def get_victory_message(battle):
    return "Поздравляю!"
