from bot.handlers.Message import Message
from bot.models import User, Item, UserItem


class Shop:

    @staticmethod
    def handle(message, bot):
        user = User.objects.get(telegram_id=message.chat.id)

        bot.send_message(message.chat.id, Message.shop(user))

    @staticmethod
    def handle_buy(message, bot):
        try:
            item = Item.objects.get(id=message.text[5:])
            user = User.objects.get(telegram_id=message.chat.id)

            if user.energy >= item.buy_cost and item.in_shop:
                user.energy = user.energy - item.buy_cost

                try:
                    user_item = user.item.get(item=item)
                    user_item.count = user_item.count + 1
                    user_item.save()
                except UserItem.DoesNotExist:
                    user.item.create(
                        item=item,
                        count=1,
                    )

                user.save()

            bot.send_message(message.chat.id, "Куплено: " + item.name)

        except Item.DoesNotExist:
            pass

    @staticmethod
    def handle_sale(message, bot):
        try:
            user = User.objects.get(telegram_id=message.chat.id)
            user_item = user.item.get(item_id=message.text[6:])

            user.energy = user.energy + user_item.item.sale_cost
            user_item.count = user_item.count - 1
            user_item.save()
            user.save()

            if user_item.count == 0:
                user_item.delete()

            bot.send_message(message.chat.id, "Продано: " + user_item.item.name)

        except Item.DoesNotExist:
            bot.send_message(message.chat.id, "Что-то пошло не так")
