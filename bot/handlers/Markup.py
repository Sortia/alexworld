from telebot import types


class Markup:

    @staticmethod
    def default() -> types.ReplyKeyboardMarkup:
        keyboard = types.ReplyKeyboardMarkup()

        keyboard.row(
            types.KeyboardButton(text='Статистика'),
            types.KeyboardButton(text='Сражение')
        )

        keyboard.row(
            types.KeyboardButton(text='Инвентарь'),
        )

        keyboard.row(
            types.KeyboardButton(text='Блэкджек'),
            types.KeyboardButton(text='Шлюхи')
        )

        return keyboard

    @staticmethod
    def battle() -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(types.InlineKeyboardButton(text='Атака', callback_data='battle_attack'))
        keyboard.add(types.InlineKeyboardButton(text='Блок', callback_data='battle_block'))
        keyboard.add(types.InlineKeyboardButton(text='Уклонение', callback_data='battle_dodge'))

        return keyboard

    @staticmethod
    def new_world() -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(types.InlineKeyboardButton(text='Отправится в новый мир!', callback_data='new_world'))

        return keyboard

    @staticmethod
    def stats() -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton(text='👊🏻 Сила', callback_data='up_strength'),
            types.InlineKeyboardButton(text='❤ Выносливость', callback_data='up_stamina'),
        )

        keyboard.add(
            types.InlineKeyboardButton(text='️🤸🏻‍️ Ловкость', callback_data='up_agility'),
            types.InlineKeyboardButton(text='💙 Интеллект', callback_data='up_intelligence'),
        )

        return keyboard
