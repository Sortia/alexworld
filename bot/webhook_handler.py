import json
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bot import config
from bot.handlers import BattleAction
from bot.handlers.BattleAction import BattleActionDodge, BattleActionAttack, BattleActionBlock
from bot.handlers.ChooseSpecialization import ChooseSpecializationHandler
from bot.handlers.GetMarkup import GetMarkupHandler
from bot.handlers.Start import Start
from bot.handlers.StartBattle import StartBattle
from bot.handlers.Stat import Stat

bot = telebot.TeleBot(config.bot_token)


@csrf_exempt
def handler(request):
    json_data = json.loads(request.body)
    update = telebot.types.Update.de_json(json_data)

    bot.process_new_updates([update])
    return HttpResponse("qwe")


# Handle '/start'
@bot.message_handler(commands=['start'])
def start_command(message): Start.handle(message, bot)


# Handle '/get_markup'
@bot.message_handler(commands=['get_markup'])
def get_markup_command(message): GetMarkupHandler.handle(message, bot)


# Handle 'Статистика' message
@bot.message_handler(func=lambda message: message.text == 'Статистика', content_types=['text'])
def print_stat(message): Stat.handle(message, bot)


# Handle specialization choose
@bot.callback_query_handler(func=lambda call: call.data in ['fighter', 'cleric', 'thief', 'mage'])
def choose_specialization(call): ChooseSpecializationHandler.handle(call, bot)


# Handle 'Сражение' message
@bot.message_handler(func=lambda message: message.text == 'Сражение', content_types=['text'])
def start_battle(message): StartBattle.handle(message, bot)


# Handle 'Блэкджек' message
@bot.message_handler(func=lambda message: message.text == 'Блэкджек', content_types=['text'])
def print_stat(message): bot.send_message(message.chat.id, "🍾")


# Handle 'Шлюхи' message
@bot.message_handler(func=lambda message: message.text == 'Шлюхи', content_types=['text'])
def print_stat(message): bot.send_message(message.chat.id, "👩🏼👩🏻👩🏻‍🦰")


# Handle attack button
@bot.callback_query_handler(func=lambda call: call.data == 'battle_attack')
def choose_specialization(call): BattleAction.execute(BattleActionAttack(), call, bot)


# Handle block button
@bot.callback_query_handler(func=lambda call: call.data == 'battle_block')
def choose_specialization(call): BattleAction.execute(BattleActionBlock(), call, bot)


# Handle dodge button
@bot.callback_query_handler(func=lambda call: call.data == 'battle_dodge')
def choose_specialization(call): BattleAction.execute(BattleActionDodge(), call, bot)
