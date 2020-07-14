import random
from abc import abstractmethod

from bot.constants import stats
from bot.handlers.BattleConverse import BattleConverse
from bot.handlers.MonsterAttack import MonsterAttack
from bot.models import User, Battle, MonsterLoot, Loot, UserLoot


class BattleAction:
    battle = Battle
    block = None
    dodge = None

    def handle(self, call, bot) -> None:
        self.init(call.message.chat.id)
        self.perform_action()
        self.perform_step()

        if self.check_user_victory():
            self.process_user_victory(call, bot)
            return

        self.maybe_monster_attack()

        if self.check_user_defeat():
            self.process_user_defeat(call, bot)
            return

        self.send_message(call, bot)

    def init(self, telegram_id) -> None:
        user = User.objects.get(telegram_id=telegram_id)
        self.battle = user.battle.filter(is_win=None).all()[0]

    @abstractmethod
    def perform_action(self) -> None:
        pass

    def perform_step(self) -> None:
        self.battle.data['meta']['steps_to_monster_damage'] = int(
            self.battle.data['meta']['steps_to_monster_damage']) - 1
        self.battle.data['meta']['step_number'] = int(self.battle.data['meta']['step_number']) + 1

    def check_user_victory(self) -> bool:
        return int(self.battle.data['monster']['current_hp']) <= 0

    def process_user_victory(self, call, bot) -> None:
        self.battle.win()
        self.give_loot()
        BattleConverse.send_victory_message(call, bot, self.battle)

    def maybe_monster_attack(self) -> None:
        if self.battle.data['meta']['steps_to_monster_damage'] == 0:
            MonsterAttack.attack(self.battle, self.block, self.dodge)

    def check_user_defeat(self) -> bool:
        return int(self.battle.data['user']['current_hp']) <= 0

    def process_user_defeat(self, call, bot) -> None:
        self.battle.defeat()
        BattleConverse.send_defeat_message(call, bot, self.battle)

    def send_message(self, call, bot) -> None:
        BattleConverse.send_action_message(call, bot, self.battle, self.block, self.dodge)

    def give_loot(self):
        self.battle.data['loot'] = list()

        for monster_loot in self.battle.monster.loot.all():
            count_loot = random.randint(monster_loot.min_count, monster_loot.max_count)

            if count_loot == 0:
                return

            self.battle.data['loot'].append({
                'name': monster_loot.loot.name,
                'count': count_loot,
            })

            try:
                loot = self.battle.user.loot.get(loot=monster_loot.loot)
                loot.count = loot.count + count_loot
                loot.save()
            except UserLoot.DoesNotExist:
                self.battle.user.loot.create(
                    loot=monster_loot.loot,
                    count=count_loot,
                )

    @staticmethod
    def get_result_by_chance(chance) -> bool:
        return True if random.random() < chance else False

    def __del__(self) -> None:
        self.battle.save()


class BattleActionAttack(BattleAction):
    def perform_action(self) -> None:
        user_damage = self.get_user_damage()
        self.battle.data['monster']['current_hp'] = int(self.battle.data['monster']['current_hp']) - user_damage

    def get_user_damage(self) -> int:
        return random.randint(self.battle.data['user']['min_damage'], self.battle.data['user']['max_damage'])


class BattleActionBlock(BattleAction):
    def perform_action(self) -> None:
        block_chance = self.calculate_block_chance()
        self.block = self.get_result_by_chance(block_chance)

    def calculate_block_chance(self) -> float:
        user_strength = self.battle.user.stats.get(stat_id=stats.strength).value
        monster_strength = self.battle.monster.stats.get(stat_id=stats.strength).value

        return user_strength / monster_strength / 2


class BattleActionDodge(BattleAction):
    def perform_action(self) -> None:
        dodge_chance = self.calculate_dodge_chance()
        self.dodge = self.get_result_by_chance(dodge_chance)

    def calculate_dodge_chance(self) -> float:
        user_agility = self.battle.user.stats.get(stat_id=stats.agility).value
        monster_agility = self.battle.monster.stats.get(stat_id=stats.agility).value

        return user_agility / monster_agility / 3


def execute(battle_action: BattleAction, call, bot) -> None:
    battle_action.handle(call, bot)
