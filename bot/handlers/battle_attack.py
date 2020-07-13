import random

from bot.handlers import battle_converse
from bot.handlers.monster_attack import MonsterAttackHandler
from bot.models import User


class BattleAttackHandler:

    @staticmethod
    def handle(call, bot):
        user = User.objects.get(telegram_id=call.message.chat.id)
        battle = user.battle_set.filter(is_win=None).all()[0]
        user_damage = get_user_damage(battle.data)

        battle.data['monster']['current_hp'] = str(int(battle.data['monster']['current_hp']) - user_damage)
        battle.data['meta']['steps_to_monster_damage'] = int(battle.data['meta']['steps_to_monster_damage']) - 1
        battle.data['meta']['step_number'] = str(int(battle.data['meta']['step_number']) + 1)
        battle.save()

        if int(battle.data['monster']['current_hp']) <= 0:
            set_victory(battle, battle.data)
            battle.win()
            battle_converse.send_victory_message(call, bot, battle)

        else:
            MonsterAttackHandler.attack(battle, call, bot)

            if int(battle.data['user']['current_hp']) <= 0:
                battle_converse.send_defeat_message(call, bot, battle)
                battle.defeat()
            else:
                battle_converse.send_action_message(call, bot, battle)


def get_user_damage(battle_data):
    return random.randint(int(battle_data['user']['min_damage']), int(battle_data['user']['max_damage']))


def set_victory(battle, battle_data):
    battle_data['monster']['current_hp'] = 0
    battle.save()
