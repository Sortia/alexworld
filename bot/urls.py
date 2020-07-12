from django.urls import path

from . import views

app_name = 'bot'
urlpatterns = [
    path('webhook', views.webhook, name='webhook'),
    path('handler', views.handler, name='handler'),
]