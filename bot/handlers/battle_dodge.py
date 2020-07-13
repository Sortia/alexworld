import random

from bot.constants import stats
from bot.handlers import battle_converse
from bot.handlers.monster_attack import MonsterAttackHandler
from bot.models import User


class BattleDodgeHandler:

    @staticmethod
    def handle(call, bot):
        user = User.objects.get(telegram_id=call.message.chat.id)
        battle = user.battle_set.filter(is_win=None).all()[0]

        dodge_chance = calculate_dodge_chance(battle)
        is_dodge = get_result_by_chance(dodge_chance)

        battle.data['meta']['steps_to_monster_damage'] = int(battle.data['meta']['steps_to_monster_damage']) - 1
        battle.save()

        MonsterAttackHandler.attack(battle, call, bot, is_dodge=is_dodge)

        if int(battle.data['user']['current_hp']) <= 0:
            battle.defeat()
            battle_converse.send_defeat_message(call, bot, battle)
        else:
            battle_converse.send_action_message(call, bot, battle, dodge=is_dodge)


def calculate_dodge_chance(battle):
    user_agility = battle.user.stats.get(stat_id=stats.agility).value
    monster_agility = battle.monster.stats.get(stat_id=stats.agility).value

    return user_agility / monster_agility / 3


def get_result_by_chance(chance):
    return True if random.random() < chance else False
