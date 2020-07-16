import jsonfield
from django.db import models

from bot import user_state


class Stat(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    icon = models.CharField(max_length=20, default='')


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, default=True)
    telegram_id = models.IntegerField()
    language_code = models.CharField(max_length=10, null=True)
    is_bot = models.BooleanField()
    state = models.IntegerField(null=True, default=0)
    unallocated_stat_points = models.IntegerField(default=5)
    energy = models.IntegerField(default=1000)

    def get_equip_stat_value(self, stat_id):
        count_stat = 0

        for equip in self.equips.all():
            for item_stat in equip.item.stats.all():
                if item_stat.stat_id == stat_id:
                    count_stat += item_stat.value

        return count_stat


class UserStat(models.Model):
    value = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='stats')
    stat = models.ForeignKey(Stat, on_delete=models.DO_NOTHING)


class Monster(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, null=True)
    win_speech = models.CharField(max_length=255)

    def get_equip_stat_value(self, stat_id):
        return 0


class MonsterStat(models.Model):
    value = models.IntegerField()
    monster = models.ForeignKey(Monster, on_delete=models.DO_NOTHING, related_name='stats')
    stat = models.ForeignKey(Stat, on_delete=models.DO_NOTHING)


class Battle(models.Model):
    monster = models.ForeignKey(Monster, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='battle')
    is_win = models.BooleanField(null=True)
    data = jsonfield.JSONField()

    def win(self):
        self.is_win = True
        self.user.state = user_state.default
        self.user.save()
        self.save()

    def defeat(self):
        self.is_win = False
        self.user.state = user_state.default
        self.user.save()
        self.save()


class ItemType(models.Model):
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=20, null=True)


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    sale_cost = models.IntegerField(null=True)
    buy_cost = models.IntegerField(null=True)
    type = models.ForeignKey(ItemType, on_delete=models.DO_NOTHING)
    in_shop = models.BooleanField(default=False)


class MonsterItem(models.Model):
    min_count = models.IntegerField()
    max_count = models.IntegerField()
    monster = models.ForeignKey(Monster, on_delete=models.DO_NOTHING, related_name='item')
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name='monsters')


class UserItem(models.Model):
    count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='item')
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)


class ItemStat(models.Model):
    value = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name='stats')
    stat = models.ForeignKey(Stat, on_delete=models.DO_NOTHING)


class UserEquipItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='equips')
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(ItemType, on_delete=models.DO_NOTHING)

