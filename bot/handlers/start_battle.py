from bot import user_state
from bot.constants import stats
from bot.handlers import battle_converse
from bot.models import User, Monster, Battle


class StartBattleHandler:

    @staticmethod
    def handle(message, bot):
        user = User.objects.get(telegram_id=message.chat.id)
        user.state = user_state.fight
        user.save()

        monster = Monster.objects.get(id=1)
        battle = create_battle(user, monster)

        response = send_start_message(battle, bot)

        battle.data['meta']['message_id'] = response.message_id
        battle.save()


def create_battle(user, monster):
    return Battle.objects.create(
        user=user,
        monster=monster,
        data={
            "monster": {
                "attack_speed": calculate_monster_damage_speed(user, monster),
                "max_hp": calculate_hp(monster),
                "current_hp": calculate_hp(monster),
                "min_damage": calculate_min_damage(monster),
                "max_damage": calculate_max_damage(monster),
            },
            "user": {
                "max_hp": calculate_hp(user),
                "current_hp": calculate_hp(user),
                "min_damage": calculate_min_damage(user),
                "max_damage": calculate_max_damage(user),
            },
            "meta": {
                "steps_to_monster_damage": calculate_monster_damage_speed(user, monster),
                "step_number": "0"
            },
            "actions": {}
        }
    )


def calculate_monster_damage_speed(user, monster):
    user_agility = user.stats.get(stat_id=stats.agility).value
    monster_agility = monster.stats.get(stat_id=stats.agility).value

    attack_speed = round(user_agility * 2.5 / monster_agility)

    return str(1 if attack_speed == 0 else attack_speed)


def calculate_hp(monster):
    monster_stamina = monster.stats.get(stat_id=stats.stamina).value

    return str(round(monster_stamina * 10))


def calculate_min_damage(monster):
    monster_strength = monster.stats.get(stat_id=stats.strength).value

    return str(round(monster_strength - (monster_strength * 0.2)))


def calculate_max_damage(monster):
    monster_strength = monster.stats.get(stat_id=stats.strength).value

    return str(round(monster_strength + (monster_strength * 0.2)))


def send_start_message(battle, bot):
    return bot.send_message(
        chat_id=battle.user.telegram_id,
        text=battle_converse.get_message(battle),
        reply_markup=battle_converse.get_markup(),
    )
