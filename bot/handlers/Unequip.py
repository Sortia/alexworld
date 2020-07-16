from bot.models import User, UserEquipItem


class Unequip:

    @staticmethod
    def handle(message, bot):
        user = User.objects.get(telegram_id=message.chat.id)

        try:
            equip = user.equips.get(item_id=message.text[9:])

            user_item = user.item.create(count=1, item=equip.item)
            equip.delete()

            bot.send_message(chat_id=message.chat.id, text='Перенесено в инвентарь: ' + user_item.item.name)

        except UserEquipItem.DoesNotExist:
            pass
