from telebot import types

from bot.models import Specialization


class Markup:

    @staticmethod
    def default() -> types.ReplyKeyboardMarkup:
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

    @staticmethod
    def battle() -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(types.InlineKeyboardButton(text='Атака', callback_data='battle_attack'))
        keyboard.add(types.InlineKeyboardButton(text='Блок', callback_data='battle_block'))
        keyboard.add(types.InlineKeyboardButton(text='Уклонение', callback_data='battle_dodge'))

        return keyboard

    @staticmethod
    def specializations() -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        specializations = Specialization.objects.all()

        for specialization in specializations:
            btn = types.InlineKeyboardButton(text=specialization.title, callback_data=specialization.name)
            keyboard.add(btn)

        return keyboard
