import numpy as np
from game.individuals.trait import Trait

class Ability(Trait):
    def __init__(self, ability_base, config, dna=None, default=False):
        self.max_dmg_reduce_by_armor = ability_base['armor_dmg_reduce']
        self.max_speed_increase = ability_base['max_speed_increase']
        self.max_poison_reduce = ability_base['max_poison_reduce']
        self.toxicity_max_dmg = ability_base['toxicity_max_dmg']
        if dna is None:
            if default:
                # increased armor controls how much dmg is taken if attacked
                # 0 means full dmg is taken
                # 1 means full armor_dmg_reduce is applied
                self.armor_ability = config['increased_armor']
                # speed controls additional speed
                # 0 means standard speed is applied
                # 1 means full max_speed_increase is applied
                # (e.g double speed with max_speed_increase = 1)
                self.speed = config['speed']
                # strength controls additional dmg dealt
                # 0 means base dmg is dealt
                # 1 means double dmg is dealt
                self.strength = config['strength']
                # poison resistance controls how much the current poison value affects the regular health decrease
                # 0 means full poison is applied each frame
                # 1 means max poison reduce is applied each frame
                self.poison_resistance = config['poison_resistance']
                # toxicity controls how much opponents receive dmg when they attack
                # 0 means that no dmg is dealt
                # 1 means toxicity_max_dmg is dealt
                self.toxicity = config['toxicity']
            else:
                init_values = np.random.dirichlet(np.ones(5), size=1)[0]
                self.armor_ability = init_values[0]
                self.speed = init_values[1]
                self.strength = init_values[2]
                self.poison_resistance = init_values[3]
                self.toxicity = init_values[4]
        else:
            # check if dna is valid
            self.check_dna(dna)
            self.armor_ability = dna[0]
            self.speed = dna[1]
            self.strength = dna[2]
            self.poison_resistance = dna[3]
            self.toxicity = dna[4]

    def calc_dmg_dealt_by_toxicity(self):
        """
        calculates the dmg dealt to attacker based on own toxicity
        """
        return self.toxicity * self.toxicity_max_dmg


    def calc_poison_reduce(self, poison):
        """
        applies poison resistance to the current poison value
        """
        # real poison = current_poison * (1 - (poison_resistance_ability * max_poison_resistance))
        return poison * (1 - self.poison_resistance * self.max_poison_reduce)


    def calc_dmg_with_strength(self, base_dmg, dmg):
        """
        applies dmg multiplier to dmg dealt
        """
        return (base_dmg + self.strength) * dmg


    def calc_dmg_on_armor(self, dmg):
        """
        applies armor stats to received damage
        """
        # real_dmg = inc_dmg * (1 - (armor_ability * armor_base))
        return dmg * (1 - self.armor_ability * self.max_dmg_reduce_by_armor)

    def calc_max_speed(self, max_speed):
        """
        applies speed stats to own max speed
        """
        return max_speed + self.speed * self.max_speed_increase

    def print(self):
        print("increased armor ability", self.armor_ability)
        print("speed ability", self.speed)
        print("strength ability", self.strength)
        print("poison resistance ability", self.poison_resistance)
        print("toxicity ability", self.toxicity)

    def get_dna(self):
        """
        wrap abilities into dna array
        """
        return [self.armor_ability, self.speed, self.strength, self.poison_resistance, self.toxicity]
