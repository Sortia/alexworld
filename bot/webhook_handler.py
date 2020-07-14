import json
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bot import config
from bot.handlers import BattleAction
from bot.handlers.BattleAction import BattleActionDodge, BattleActionAttack, BattleActionBlock
from bot.handlers.GetMarkup import GetMarkupHandler
from bot.handlers.Inventory import Inventory
from bot.handlers.NewWorld import NewWorld
from bot.handlers.Start import Start
from bot.handlers.StartBattle import StartBattle
from bot.handlers.Stat import Stat
from bot.handlers.UpStat import UpStat

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


# Handle 'Сражение' message
@bot.message_handler(func=lambda message: message.text == 'Сражение', content_types=['text'])
def start_battle(message): StartBattle.handle(message, bot)


# Handle 'Сражение' message
@bot.message_handler(func=lambda message: message.text == 'Инвентарь', content_types=['text'])
def start_battle(message): Inventory.handle(message, bot)


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


# Handle dodge button
@bot.callback_query_handler(func=lambda call: call.data == 'new_world')
def choose_specialization(call): NewWorld.handle(call, bot)


# Handle dodge button
@bot.callback_query_handler(func=lambda call: call.data in ['up_strength', 'up_stamina', 'up_agility', 'up_intelligence'])
def choose_specialization(call): UpStat.handle(call, bot)
