import random

from bot.handlers import battle_converse


class MonsterAttackHandler:

    @staticmethod
    def attack(battle, call, bot, is_block=False, is_dodge=False):
        if battle.data['meta']['steps_to_monster_damage'] == 0:
            battle = set_monster_attack(battle, is_block, is_dodge)

            if int(battle.data['user']['current_hp']) <= 0:
                set_defeat(battle, battle.data)
                battle_converse.send_defeat_message(call, bot, battle)

        return battle


def set_defeat(battle, battle_data):
    battle_data['user']['current_hp'] = '0'
    battle.save()


def set_monster_attack(battle, is_block, is_dodge):
    monster_damage = get_monster_damage(battle)

    if is_block:
        monster_damage = round(monster_damage / 2)

    if is_dodge:
        monster_damage = 0

    battle.data['user']['current_hp'] = str(int(battle.data['user']['current_hp']) - monster_damage)
    battle.data['meta']['steps_to_monster_damage'] = battle.data['monster']['attack_speed']
    battle.save()

    return battle


def get_monster_damage(battle):
    return round(random.randint(int(battle.data['monster']['min_damage']), int(battle.data['monster']['max_damage'])))
