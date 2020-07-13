import json
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bot import config
from bot.handlers.battle_attack import BattleAttackHandler
from bot.handlers.battle_block import BattleBlockHandler
from bot.handlers.battle_dodge import BattleDodgeHandler
from bot.handlers.black_jack import BlackJackHandler
from bot.handlers.choose_specialization import ChooseSpecializationHandler
from bot.handlers.get_markup import GetMarkupHandler
from bot.handlers.start import StartHandler
from bot.handlers.start_battle import StartBattleHandler
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


# Handle '/get_markup'
@bot.message_handler(commands=['get_markup'])
def get_markup_command(message): GetMarkupHandler.handle(message, bot)


# Handle 'Статистика' message
@bot.message_handler(func=lambda message: message.text == 'Статистика', content_types=['text'])
def print_stat(message): StatHandler.handle(message, bot)


# Handle specialization choose
@bot.callback_query_handler(func=lambda call: call.data in ['fighter', 'cleric', 'thief', 'mage'])
def choose_specialization(call): ChooseSpecializationHandler.handle(call, bot)


# Handle 'Сражение' message
@bot.message_handler(func=lambda message: message.text == 'Сражение', content_types=['text'])
def start_battle(message): StartBattleHandler.handle(message, bot)


# Handle 'Блэкджек' message
@bot.message_handler(func=lambda message: message.text == 'Блэкджек', content_types=['text'])
def print_stat(message): bot.send_message(message.chat.id, "🍾")


# Handle 'Шлюхи' message
@bot.message_handler(func=lambda message: message.text == 'Шлюхи', content_types=['text'])
def print_stat(message): bot.send_message(message.chat.id, "👩🏼👩🏻👩🏻‍🦰")


# Handle specialization choose
@bot.callback_query_handler(func=lambda call: call.data == 'battle_attack')
def choose_specialization(call): BattleAttackHandler.handle(call, bot)


# Handle specialization choose
@bot.callback_query_handler(func=lambda call: call.data == 'battle_block')
def choose_specialization(call): BattleBlockHandler.handle(call, bot)


# Handle specialization choose
@bot.callback_query_handler(func=lambda call: call.data == 'battle_dodge')
def choose_specialization(call): BattleDodgeHandler.handle(call, bot)
