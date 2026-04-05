"""角色系統模組"""
import random

# 職業定義
CLASSES = {
    "戰士": {
        "description": "近戰高手，擁有強大的生命值與防禦力",
        "base_hp": 120,
        "base_mp": 30,
        "base_atk": 15,
        "base_def": 12,
        "base_spd": 8,
        "hp_growth": 18,
        "mp_growth": 4,
        "atk_growth": 3,
        "def_growth": 3,
        "spd_growth": 1,
        "skills": ["重擊", "防禦姿態", "戰吼"],
    },
    "法師": {
        "description": "魔法師，擁有強大的魔法攻擊力",
        "base_hp": 70,
        "base_mp": 100,
        "base_atk": 8,
        "base_def": 5,
        "base_spd": 9,
        "hp_growth": 8,
        "mp_growth": 15,
        "atk_growth": 1,
        "def_growth": 1,
        "spd_growth": 2,
        "skills": ["火球術", "冰封術", "魔力爆發"],
    },
    "盜賊": {
        "description": "敏捷的刺客，速度極快且擅長暴擊",
        "base_hp": 85,
        "base_mp": 50,
        "base_atk": 13,
        "base_def": 7,
        "base_spd": 15,
        "hp_growth": 10,
        "mp_growth": 6,
        "atk_growth": 2,
        "def_growth": 1,
        "spd_growth": 3,
        "skills": ["背刺", "煙霧彈", "連擊"],
    },
}

# 技能定義
SKILLS = {
    "重擊": {"mp_cost": 8, "damage_mult": 1.8, "type": "physical", "description": "強力的物理攻擊，造成1.8倍傷害"},
    "防禦姿態": {"mp_cost": 6, "effect": "defense_up", "value": 5, "turns": 3, "type": "buff", "description": "提升防禦力3回合"},
    "戰吼": {"mp_cost": 10, "effect": "atk_up", "value": 4, "turns": 3, "type": "buff", "description": "提升攻擊力3回合"},
    "火球術": {"mp_cost": 15, "damage_mult": 2.2, "type": "magic", "description": "發射火焰球，造成2.2倍魔法傷害"},
    "冰封術": {"mp_cost": 12, "damage_mult": 1.5, "effect": "freeze", "turns": 1, "type": "magic", "description": "冰凍敵人1回合"},
    "魔力爆發": {"mp_cost": 25, "damage_mult": 3.0, "type": "magic", "description": "強力魔法爆炸，造成3倍傷害"},
    "背刺": {"mp_cost": 10, "damage_mult": 2.5, "crit_rate": 0.5, "type": "physical", "description": "從背後偷襲，高暴擊率"},
    "煙霧彈": {"mp_cost": 8, "effect": "blind", "turns": 2, "type": "debuff", "description": "使敵人失明2回合，降低命中率"},
    "連擊": {"mp_cost": 12, "hits": 3, "damage_mult": 0.7, "type": "physical", "description": "連續攻擊3次，每次0.7倍傷害"},
}

# 等級所需經驗值
def exp_required(level):
    return int(100 * (level ** 1.5))


class Character:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        cls = CLASSES[job]

        self.level = 1
        self.exp = 0
        self.gold = 50

        self.base_hp = cls["base_hp"]
        self.base_mp = cls["base_mp"]
        self.base_atk = cls["base_atk"]
        self.base_def = cls["base_def"]
        self.base_spd = cls["base_spd"]

        self.max_hp = self.base_hp
        self.max_mp = self.base_mp
        self.hp = self.max_hp
        self.mp = self.max_mp

        self.skills = cls["skills"][:]
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None

        # 臨時加成 (戰鬥中)
        self.temp_atk = 0
        self.temp_def = 0
        self.status = None      # freeze, blind, poison
        self.status_turns = 0
        self.buffs = {}         # {effect: turns_remaining}

    @property
    def atk(self):
        bonus = 0
        if self.equipped_weapon:
            bonus += self.equipped_weapon.get("atk_bonus", 0)
        return self.base_atk + bonus + self.temp_atk

    @property
    def defense(self):
        bonus = 0
        if self.equipped_armor:
            bonus += self.equipped_armor.get("def_bonus", 0)
        return self.base_def + bonus + self.temp_def

    @property
    def spd(self):
        return self.base_spd

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        actual = max(1, dmg)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount):
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def restore_mp(self, amount):
        restored = min(amount, self.max_mp - self.mp)
        self.mp += restored
        return restored

    def gain_exp(self, amount):
        self.exp += amount
        leveled_up = []
        while self.exp >= exp_required(self.level):
            self.exp -= exp_required(self.level)
            self.level_up()
            leveled_up.append(self.level)
        return leveled_up

    def level_up(self):
        self.level += 1
        cls = CLASSES[self.job]
        self.base_hp += cls["hp_growth"]
        self.base_mp += cls["mp_growth"]
        self.base_atk += cls["atk_growth"]
        self.base_def += cls["def_growth"]
        self.base_spd += cls["spd_growth"]
        self.max_hp = self.base_hp
        self.max_mp = self.base_mp
        self.hp = self.max_hp
        self.mp = self.max_mp

        # 新技能解鎖
        all_skills = CLASSES[self.job]["skills"]
        if self.level == 3 and len(all_skills) > 1 and all_skills[1] not in self.skills:
            self.skills.append(all_skills[1])
        if self.level == 5 and len(all_skills) > 2 and all_skills[2] not in self.skills:
            self.skills.append(all_skills[2])

    def reset_battle_status(self):
        self.temp_atk = 0
        self.temp_def = 0
        self.status = None
        self.status_turns = 0
        self.buffs = {}

    def get_status_str(self):
        parts = [
            f"  等級: {self.level}  ({self.exp}/{exp_required(self.level)} EXP)",
            f"  職業: {self.job}",
            f"  HP: {self.hp}/{self.max_hp}  MP: {self.mp}/{self.max_mp}",
            f"  攻擊: {self.atk}  防禦: {self.defense}  速度: {self.spd}",
            f"  金幣: {self.gold}",
            f"  武器: {self.equipped_weapon['name'] if self.equipped_weapon else '無'}",
            f"  防具: {self.equipped_armor['name'] if self.equipped_armor else '無'}",
        ]
        return "\n".join(parts)

    def show_inventory(self):
        if not self.inventory:
            print("  背包是空的。")
            return
        print(f"  {'序號':<4} {'名稱':<12} {'類型':<8} {'說明'}")
        print("  " + "-" * 50)
        for i, item in enumerate(self.inventory, 1):
            print(f"  {i:<4} {item['name']:<12} {item['type']:<8} {item.get('description', '')}")
