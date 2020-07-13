import random

from bot.constants import stats
from bot.handlers import battle_converse
from bot.handlers.monster_attack import MonsterAttackHandler
from bot.models import User


class BattleBlockHandler:

    @staticmethod
    def handle(call, bot):
        user = User.objects.get(telegram_id=call.message.chat.id)
        battle = user.battle_set.filter(is_win=None).all()[0]

        block_chance = calculate_block_chance(battle)
        is_block = get_result_by_chance(block_chance)

        battle.data['meta']['steps_to_monster_damage'] = int(battle.data['meta']['steps_to_monster_damage']) - 1
        battle.data['meta']['step_number'] = str(int(battle.data['meta']['move_number']) + 1)
        battle.save()

        MonsterAttackHandler.attack(battle, call, bot, is_block=is_block)

        if int(battle.data['user']['current_hp']) <= 0:
            battle.defeat()
            battle_converse.send_defeat_message(call, bot, battle)
        else:
            battle_converse.send_action_message(call, bot, battle, block=is_block)


def calculate_block_chance(battle):
    user_strength = battle.user.stats.get(stat_id=stats.strength).value
    monster_strength = battle.monster.stats.get(stat_id=stats.strength).value

    return user_strength / monster_strength / 2


def get_result_by_chance(chance):
    return True if random.random() < chance else False
