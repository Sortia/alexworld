import json
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bot import config
from bot.handlers.choose_specialization import ChooseSpecializationHandler
from bot.handlers.start import StartHandler
from bot.handlers.stat import StatHandler

bot = telebot.TeleBot(config.bot_token)


@csrf_exempt
def handler(request):
    json_data = json.loads(request.body)
    update = telebot.types.Update.de_json(json_data)

    bot.process_new_updates([update])
    return HttpResponse("qwe")


# Handle '/start'
@bot.message_handler(commands=['start'])
def start_command(message): StartHandler.handle(message, bot)


# Handle 'Статистика' message
@bot.message_handler(func=lambda message: message.text == 'Статистика', content_types=['text'])
def print_stat(message): StatHandler.handle(message, bot)


# Handle specialization choose
@bot.callback_query_handler(func=lambda call: call.data in ['fighter', 'cleric', 'thief', 'mage'])
def choose_specialization(call): ChooseSpecializationHandler.handle(call, bot)
