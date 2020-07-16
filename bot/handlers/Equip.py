from bot.models import User, UserItem, UserEquipItem


class Equip:

    @staticmethod
    def handle(message, bot):
        try:
            user = User.objects.get(telegram_id=message.chat.id)
            user_item = user.item.filter(item_id=message.text[7:]).get()

            try:
                user_equip = user.equips.filter(type=user_item.item.type).get()
                user.item.create(count=1, item=user_equip.item)
                user_equip.delete()
            except UserEquipItem.DoesNotExist:
                pass

            user.equips.create(user=user, item=user_item.item, type=user_item.item.type)
            user_item.delete()

            bot.send_message(chat_id=message.chat.id, text='Экипировано: ' + user_item.item.name)

        except UserItem.DoesNotExist:
            bot.send_message(chat_id=message.chat.id, text='У вас нет этого предмета')
