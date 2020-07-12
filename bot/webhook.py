import telebot
from django.http import HttpResponse

from bot import config

bot = telebot.TeleBot(config.bot_token)


def set_webhook(request):
    bot.remove_webhook()
    bot.set_webhook(config.webhook_url)

    return HttpResponse("qwe")
