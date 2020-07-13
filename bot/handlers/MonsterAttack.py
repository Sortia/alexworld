import random


class MonsterAttack:

    @staticmethod
    def attack(battle, is_block=False, is_dodge=False) -> None:
        monster_damage = MonsterAttack.get_monster_damage(battle)

        if is_block:
            monster_damage = round(monster_damage / 2)

        if is_dodge:
            monster_damage = 0

        battle.data['user']['current_hp'] = str(int(battle.data['user']['current_hp']) - monster_damage)
        battle.data['meta']['steps_to_monster_damage'] = battle.data['monster']['attack_speed']

    @staticmethod
    def get_monster_damage(battle) -> int:
        return random.randint(battle.data['monster']['min_damage'], battle.data['monster']['max_damage'])
