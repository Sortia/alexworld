from bot.models import Item


class Message:

    @staticmethod
    def stats(user) -> str:
        text = ''

        for user_stat in user.stats.all():
            text += user_stat.stat.title + ': ' + str(user_stat.value) + '\n'

        text += '\nНераспределенных очков: ' + str(user.unallocated_stat_points)

        return text

    @staticmethod
    def inventory(user) -> str:
        text = ''

        for user_item in user.item.all():
            text += user_item.item.name + ' x' + str(user_item.count) + ' ' + str(user_item.item.sale_cost) + \
                    '♦ за шт.️ /sale_' + str(user_item.item.id)

            if user_item.item.type_id in range(1, 5):
                text += ' /equip_' + str(user_item.item.id)

            text += '\n\n'

        if text == '':
            text = 'Инвентарь пуст'

        return text

    @staticmethod
    def shop(user) -> str:
        text = 'В наличии ' + str(user.energy) + '♦\n\n'

        for item in Item.objects.all():
            if item.in_shop:
                text += item.name + ' - ' + str(item.buy_cost) + '♦️'

                text += Message.item_stats(item)

                text += ' /buy_' + str(item.id) + '\n\n'

        return text

    @staticmethod
    def item_stats(item):
        text = ''

        for stat in item.stats.all():
            text += ' ' + str(stat.value) + stat.stat.icon

        return text

    @staticmethod
    def equip(user):
        text = 'Экипировка: \n'

        for equip in user.equips.all():
            text += equip.item.name

            text += Message.item_stats(equip.item) + ' /unequip_' + str(equip.item.id)

        return text
