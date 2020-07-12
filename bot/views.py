import json
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from bot.models import User, Specialization

token = '1298659316:AAGbzUTmBKfxwkOL5gTUvMSumGrc-dkLm9s'
bot = telebot.TeleBot(token)
webhook_url = 'https://46f09987cb9d.ngrok.io/bot/handler'


@csrf_exempt
def handler(request):
    json_data = json.loads(request.body)
    update = telebot.types.Update.de_json(json_data)

    bot.process_new_updates([update])
    return HttpResponse("qwe")


# Handle '/start'
@bot.message_handler(commands=['start'])
def start_command(message):
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


@bot.message_handler(func=lambda message: 'Статистика', content_types=['text'])
def print_stat(message):
    try:
        user = User.objects.get(telegram_id=message.chat.id)

        message_text = ''

        for user_stat in user.userstat_set.all():
            message_text += user_stat.stat.title + ': ' + str(user_stat.value) + '\n'

        bot.send_message(message.chat.id, message_text)

    except User.DoesNotExist:
        return


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text, reply_markup=get_default_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = User.objects.get(telegram_id=call.message.chat.id)

    if user.specialization_id:
        bot.send_message(call.message.chat.id, "Нельзя сменить класс!")
    else:
        specialization = Specialization.objects.get(name=call.data)

        user.specialization_id = specialization.id
        user.save()

        for specializationstat in specialization.specializationstat_set.all():
            user.userstat_set.create(value=specializationstat.value, stat_id=specializationstat.stat_id)

        bot.send_message(
            call.message.chat.id,
            "Красавчик. Ты теперь " + specialization.title + '.',
            reply_markup=get_default_keyboard()
        )

        # print_stat(message=call.message)


def webhook(request):
    bot.remove_webhook()

    bot.set_webhook(webhook_url)

    return ''


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


def get_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    keyboard.row(
        types.KeyboardButton(text='Статистика'),
        types.KeyboardButton(text='Задания')
    )

    keyboard.row(
        types.KeyboardButton(text='Блэкджек'),
        types.KeyboardButton(text='Шлюхи')
    )

    return keyboard
