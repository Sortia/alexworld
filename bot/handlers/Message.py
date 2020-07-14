class Message:

    @staticmethod
    def stats(user):
        text = ''

        for user_stat in user.stats.all():
            text += user_stat.stat.title + ': ' + str(user_stat.value) + '\n'

        text += '\nНераспределенных очков: ' + str(user.unallocated_stat_points)

        return text

    @staticmethod
    def inventory(user):
        text = ''

        for loot in user.loot.all():
            text += loot.loot.name + ' x' + str(loot.count) + '\n'

        return text
