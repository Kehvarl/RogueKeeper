class Creature:
    def __init__(self, hp=0, power=0, defense=0, xp=0):
        """
        Give a Creature stats
        :param hp: Current (and Max) Hit Points
        :param power: Attack Damage
        :param defense: Defense Rating
        :param xp: Experience Points Value
        """
        self.label = 'Creature'
        self.base_max_hp = hp
        self.hp = hp
        self.base_power = power
        self.base_defense = defense
        self.xp = xp
        self.owner = None

    @property
    def max_hp(self):
        """
        Get the current maximum HP with all bonuses
        :return int: Max HP
        """
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0
        return self.base_max_hp + bonus

    @property
    def defense(self):
        """
        Get the current Defense rating with all bonuses
        :return int: Defense
        """
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0
        return self.base_defense + bonus

    @property
    def power(self):
        """
        Get the current Attack rating with all bonuses
        :return int : AttackPower
        """
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0
        return self.base_power + bonus

    def take_damage(self, amount):
        """
        Deal damage to this creature
        :param int amount: Quantity of Damage dealt
        :return list: Description of outcome
        """
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        """
        Heal this creature
        :param int amount: Quantity of HP restored
        """
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        """
        Attack and deal damage to another creature
        :param Entity target: The creature being damaged
        :return list: The outcome of the attack
        """
        results = []

        if target.fighter is None:
            results.append({'message': 'Cannot attack {0}'.format(
                target.name)})
        else:
            damage = self.power - target.fighter.defense

            if damage > 0:
                results.append({'message': '{0} attacks {1} for {2} hit points'.format(
                    self.owner.name.capitalize(), target.name, str(damage))})
                results.extend(target.fighter.take_damage(damage))
            else:
                results.append({'message': '{0 attacks {1} but does no damage'.format(
                    self.owner.name.capitalize(), target.name)})
        return results
