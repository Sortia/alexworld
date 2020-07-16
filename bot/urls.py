from django.urls import path

from . import webhook, webhook_handler

app_name = 'bot'
urlpatterns = [
    path('webhook', webhook.set_webhook, name='webhook'),
    path('handler', webhook_handler.handler, name='handler'),
]
