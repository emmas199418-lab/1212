"""戰鬥系統模組"""
import random
import time
from character import SKILLS
from items import use_item

# ── 敵人定義 ─────────────────────────────────────────────
ENEMIES = {
    # 新手村附近
    "哥布林": {
        "name": "哥布林", "hp": 40, "atk": 8, "defense": 3, "spd": 7,
        "exp": 20, "gold": (5, 12),
        "skills": ["普通攻擊"],
        "drops": [("小回復藥水", 0.3)],
        "description": "小型綠色怪物，常成群出現",
    },
    "野狼": {
        "name": "野狼", "hp": 55, "atk": 12, "defense": 4, "spd": 11,
        "exp": 30, "gold": (3, 8),
        "skills": ["普通攻擊", "撕咬"],
        "drops": [("小回復藥水", 0.2)],
        "description": "兇猛的野狼，速度很快",
    },
    # 黑森林
    "食人花": {
        "name": "食人花", "hp": 80, "atk": 14, "defense": 6, "spd": 4,
        "exp": 50, "gold": (10, 20),
        "skills": ["普通攻擊", "毒液噴射"],
        "drops": [("解毒藥", 0.4), ("小回復藥水", 0.25)],
        "description": "會噴毒的植物怪物",
    },
    "骷髏士兵": {
        "name": "骷髏士兵", "hp": 90, "atk": 16, "defense": 10, "spd": 6,
        "exp": 60, "gold": (15, 25),
        "skills": ["普通攻擊", "骨刺攻擊"],
        "drops": [("小回復藥水", 0.2)],
        "description": "由亡靈魔法操控的骨骼戰士",
    },
    # 廢棄礦坑
    "石頭巨人": {
        "name": "石頭巨人", "hp": 150, "atk": 22, "defense": 18, "spd": 3,
        "exp": 100, "gold": (25, 45),
        "skills": ["普通攻擊", "大地震"],
        "drops": [("中回復藥水", 0.3)],
        "description": "由岩石構成的巨大怪物",
    },
    "暗黑騎士": {
        "name": "暗黑騎士", "hp": 130, "atk": 25, "defense": 15, "spd": 9,
        "exp": 120, "gold": (30, 50),
        "skills": ["普通攻擊", "暗黑突刺", "防禦姿態"],
        "drops": [("中回復藥水", 0.25), ("小魔力藥水", 0.2)],
        "description": "被黑暗魔法腐蝕的騎士",
    },
    # BOSS
    "森林守護者": {
        "name": "森林守護者", "hp": 200, "atk": 20, "defense": 12, "spd": 8,
        "exp": 200, "gold": (60, 80),
        "skills": ["普通攻擊", "毒液噴射", "藤蔓束縛"],
        "drops": [("中回復藥水", 1.0), ("解毒藥", 0.8)],
        "description": "守護黑森林的古老樹靈",
        "is_boss": True,
    },
    "礦坑魔王": {
        "name": "礦坑魔王", "hp": 350, "atk": 35, "defense": 20, "spd": 10,
        "exp": 400, "gold": (100, 150),
        "skills": ["普通攻擊", "大地震", "暗黑爆炸", "狂暴"],
        "drops": [("大回復藥水", 1.0), ("中魔力藥水", 0.8)],
        "description": "統治廢棄礦坑的恐怖存在",
        "is_boss": True,
    },
    "魔王": {
        "name": "魔王", "hp": 600, "atk": 55, "defense": 30, "spd": 14,
        "exp": 1000, "gold": (300, 500),
        "skills": ["普通攻擊", "暗黑爆炸", "死亡凝視", "魔王憤怒", "黑暗復甦"],
        "drops": [("萬靈藥", 1.0)],
        "description": "籠罩大地的終極惡魔",
        "is_boss": True,
    },
}

# 區域敵人列表
AREA_ENEMIES = {
    "黑森林附近": ["哥布林", "野狼"],
    "黑森林": ["食人花", "骷髏士兵", "野狼"],
    "廢棄礦坑": ["石頭巨人", "暗黑騎士"],
    "魔王城堡": ["骷髏士兵", "暗黑騎士"],
}

AREA_BOSS = {
    "黑森林": "森林守護者",
    "廢棄礦坑": "礦坑魔王",
    "魔王城堡": "魔王",
}


def _pause(seconds=0.5):
    time.sleep(seconds)


def _calc_damage(atk, defense, is_magic=False, mult=1.0, crit=False):
    variance = random.uniform(0.85, 1.15)
    if is_magic:
        dmg = max(1, (atk * 1.5 - defense * 0.3) * variance * mult)
    else:
        dmg = max(1, (atk - defense * 0.6) * variance * mult)
    if crit:
        dmg *= 2.0
    return int(dmg)


class Enemy:
    def __init__(self, template):
        data = dict(template)
        self.name = data["name"]
        self.max_hp = data["hp"]
        self.hp = self.max_hp
        self.atk = data["atk"]
        self.defense = data["defense"]
        self.spd = data["spd"]
        self.exp = data["exp"]
        self.gold_range = data["gold"]
        self.skills = data["skills"][:]
        self.drops = data.get("drops", [])
        self.is_boss = data.get("is_boss", False)
        self.status = None
        self.status_turns = 0
        self.temp_def = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        actual = max(1, dmg)
        self.hp = max(0, self.hp - actual)
        return actual

    def choose_action(self):
        if len(self.skills) == 1:
            return self.skills[0]
        weights = [3] + [1] * (len(self.skills) - 1)
        return random.choices(self.skills, weights=weights, k=1)[0]

    def get_gold(self):
        return random.randint(*self.gold_range)

    def get_drops(self):
        from items import ALL_ITEMS
        result = []
        for item_name, rate in self.drops:
            if random.random() < rate and item_name in ALL_ITEMS:
                result.append(dict(ALL_ITEMS[item_name]))
        return result


def _enemy_action(enemy, character):
    """敵人行動，回傳描述"""
    if enemy.status == "freeze":
        enemy.status_turns -= 1
        if enemy.status_turns <= 0:
            enemy.status = None
        return f"  {enemy.name} 被冰凍，無法行動！"

    action = enemy.choose_action()
    messages = []

    if action == "普通攻擊":
        hit_rate = 0.7 if character.status == "blind" else 1.0
        if random.random() > hit_rate:
            return f"  {enemy.name} 攻擊了，但 {character.name} 閃避了！"
        dmg = _calc_damage(enemy.atk, character.defense)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 攻擊了 {character.name}，造成 {actual} 傷害！")

    elif action == "撕咬":
        dmg = _calc_damage(enemy.atk, character.defense, mult=1.4)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 發動撕咬，造成 {actual} 傷害！")

    elif action == "毒液噴射":
        dmg = _calc_damage(enemy.atk * 0.7, character.defense)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 噴出毒液，造成 {actual} 傷害！")
        if random.random() < 0.5 and character.status is None:
            character.status = "poison"
            character.status_turns = 3
            messages.append(f"  {character.name} 中毒了！")

    elif action == "骨刺攻擊":
        dmg = _calc_damage(enemy.atk, character.defense, mult=1.3)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 發射骨刺，造成 {actual} 傷害！")

    elif action == "大地震":
        dmg = _calc_damage(enemy.atk, character.defense * 0.5, mult=1.5)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 引發大地震，造成 {actual} 傷害！")

    elif action == "暗黑突刺":
        dmg = _calc_damage(enemy.atk, character.defense, mult=1.6)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 發動暗黑突刺，造成 {actual} 傷害！")

    elif action == "防禦姿態":
        enemy.temp_def += 5
        messages.append(f"  {enemy.name} 進入防禦姿態，防禦力提升！")

    elif action == "藤蔓束縛":
        dmg = _calc_damage(enemy.atk * 0.6, character.defense)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 用藤蔓束縛 {character.name}，造成 {actual} 傷害！")
        if character.status is None:
            character.status = "freeze"
            character.status_turns = 1
            messages.append(f"  {character.name} 被束縛，下回合無法行動！")

    elif action == "暗黑爆炸":
        dmg = _calc_damage(enemy.atk, character.defense, is_magic=True, mult=1.8)
        actual = character.take_damage(dmg)
        messages.append(f"  {enemy.name} 釋放暗黑爆炸，造成 {actual} 魔法傷害！")

    elif action == "死亡凝視":
        if random.random() < 0.15:
            character.hp = 0
            messages.append(f"  {enemy.name} 使用死亡凝視！{character.name} 直接倒下！")
        else:
            dmg = _calc_damage(enemy.atk, character.defense, mult=2.0)
            actual = character.take_damage(dmg)
            messages.append(f"  {enemy.name} 使用死亡凝視，造成 {actual} 傷害！")

    elif action == "魔王憤怒":
        for _ in range(2):
            dmg = _calc_damage(enemy.atk, character.defense, mult=0.9)
            actual = character.take_damage(dmg)
            messages.append(f"  {enemy.name} 狂怒打擊，造成 {actual} 傷害！")

    elif action == "黑暗復甦":
        heal = int(enemy.max_hp * 0.15)
        enemy.hp = min(enemy.max_hp, enemy.hp + heal)
        messages.append(f"  {enemy.name} 使用黑暗復甦，恢復了 {heal} HP！")

    elif action == "狂暴":
        enemy.atk = int(enemy.atk * 1.2)
        messages.append(f"  {enemy.name} 進入狂暴狀態，攻擊力大幅提升！")

    return "\n".join(messages)


def _player_action(character, enemy):
    """玩家行動，回傳 (是否繼續戰鬥, 描述)"""
    if character.status == "freeze":
        character.status_turns -= 1
        if character.status_turns <= 0:
            character.status = None
        return True, f"  {character.name} 被凍住，無法行動！"

    while True:
        print(f"\n  ┌── {character.name} HP:{character.hp}/{character.max_hp}  MP:{character.mp}/{character.max_mp}")
        if character.status:
            print(f"  │   狀態：{character.status} ({character.status_turns}回合)")
        print(f"  └── {enemy.name} HP:{enemy.hp}/{enemy.max_hp}")
        print("\n  【行動選擇】")
        print("   1. 普通攻擊")
        print("   2. 技能")
        print("   3. 使用道具")
        print("   4. 逃跑")

        choice = input("  選擇行動（1-4）：").strip()
        if choice == "1":
            crit = random.random() < 0.1
            dmg = _calc_damage(character.atk, enemy.defense + enemy.temp_def, crit=crit)
            actual = enemy.take_damage(dmg)
            msg = f"  {character.name} 攻擊了 {enemy.name}，造成 {actual} 傷害！"
            if crit:
                msg += "【暴擊！】"
            return True, msg

        elif choice == "2":
            if not character.skills:
                print("  你沒有任何技能！")
                continue
            print("\n  【技能列表】")
            for i, sk in enumerate(character.skills, 1):
                info = SKILLS.get(sk, {})
                print(f"   {i}. {sk}  MP消耗:{info.get('mp_cost',0)}  {info.get('description','')}")
            print("   0. 返回")
            sk_choice = input("  選擇技能：").strip()
            if sk_choice == "0":
                continue
            if not sk_choice.isdigit() or not (1 <= int(sk_choice) <= len(character.skills)):
                print("  無效選項。")
                continue
            skill_name = character.skills[int(sk_choice) - 1]
            skill = SKILLS.get(skill_name, {})
            cost = skill.get("mp_cost", 0)
            if character.mp < cost:
                print(f"  MP 不足！需要 {cost} MP，目前 {character.mp} MP。")
                continue
            character.mp -= cost
            return True, _use_skill(character, enemy, skill_name, skill)

        elif choice == "3":
            usable = [item for item in character.inventory if item["type"] == "消耗品"]
            if not usable:
                print("  背包中沒有消耗品！")
                continue
            print("\n  【消耗品列表】")
            for i, item in enumerate(usable, 1):
                print(f"   {i}. {item['name']}  {item.get('description','')}")
            print("   0. 返回")
            item_choice = input("  選擇道具：").strip()
            if item_choice == "0":
                continue
            if not item_choice.isdigit() or not (1 <= int(item_choice) <= len(usable)):
                print("  無效選項。")
                continue
            item = usable[int(item_choice) - 1]
            msg = use_item(character, item)
            character.inventory.remove(item)
            return True, f"  {msg}"

        elif choice == "4":
            # 逃跑成功率：速度比較
            escape_rate = min(0.8, max(0.1, character.spd / (character.spd + enemy.spd)))
            if random.random() < escape_rate:
                return False, "  成功逃跑了！"
            else:
                dmg = _calc_damage(enemy.atk, character.defense)
                actual = character.take_damage(dmg)
                return True, f"  逃跑失敗！{enemy.name} 趁機攻擊，造成 {actual} 傷害！"
        else:
            print("  請輸入有效的選項。")


def _use_skill(character, enemy, skill_name, skill):
    sk_type = skill.get("type", "physical")
    messages = [f"  {character.name} 使用了【{skill_name}】！"]

    if sk_type in ("physical", "magic"):
        is_magic = sk_type == "magic"
        mult = skill.get("damage_mult", 1.0)

        if "hits" in skill:
            total = 0
            for _ in range(skill["hits"]):
                crit = random.random() < skill.get("crit_rate", 0.1)
                dmg = _calc_damage(character.atk, enemy.defense + enemy.temp_def,
                                   is_magic=is_magic, mult=mult, crit=crit)
                actual = enemy.take_damage(dmg)
                total += actual
            messages.append(f"  連擊 {skill['hits']} 次，共造成 {total} 傷害！")
        else:
            crit = random.random() < skill.get("crit_rate", 0.1)
            dmg = _calc_damage(character.atk, enemy.defense + enemy.temp_def,
                               is_magic=is_magic, mult=mult, crit=crit)
            actual = enemy.take_damage(dmg)
            messages.append(f"  造成 {actual} {'魔法' if is_magic else ''}傷害！" + ("【暴擊！】" if crit else ""))

        # 附帶效果
        effect = skill.get("effect")
        if effect == "freeze" and random.random() < 0.7:
            enemy.status = "freeze"
            enemy.status_turns = skill.get("turns", 1)
            messages.append(f"  {enemy.name} 被冰封！")

    elif sk_type == "buff":
        effect = skill.get("effect")
        value = skill.get("value", 0)
        turns = skill.get("turns", 2)
        if effect == "defense_up":
            character.temp_def += value
            messages.append(f"  防禦力提升 {value} 點，持續 {turns} 回合！")
        elif effect == "atk_up":
            character.temp_atk += value
            messages.append(f"  攻擊力提升 {value} 點，持續 {turns} 回合！")

    elif sk_type == "debuff":
        effect = skill.get("effect")
        turns = skill.get("turns", 1)
        if effect == "blind":
            enemy.status = "blind"
            enemy.status_turns = turns
            messages.append(f"  {enemy.name} 失明了，命中率下降！")

    return "\n".join(messages)


def _process_poison(character):
    """處理中毒，回傳描述"""
    if character.status == "poison":
        dmg = max(1, int(character.max_hp * 0.05))
        character.take_damage(dmg)
        character.status_turns -= 1
        msg = f"  {character.name} 受到毒素傷害，損失 {dmg} HP！"
        if character.status_turns <= 0:
            character.status = None
            msg += "\n  毒素消退了。"
        return msg
    return ""


def run_battle(character, enemy_name, is_boss=False):
    """
    執行一場戰鬥。
    回傳 "win" / "lose" / "escape"
    """
    template = ENEMIES[enemy_name]
    enemy = Enemy(template)

    sep = "★" if is_boss else "─"
    print(f"\n{'═'*50}")
    if is_boss:
        print(f"  ！！BOSS 戰：{enemy.name}！！")
        print(f"  {enemy.description if hasattr(enemy, 'description') else ''}")
    else:
        print(f"  遭遇了 {enemy.name}！")
    print(f"{'═'*50}")
    _pause(0.5)

    turn = 1
    character.reset_battle_status()

    while True:
        print(f"\n  ──── 第 {turn} 回合 ────")

        # 玩家先攻還是敵人先攻
        player_first = character.spd >= enemy.spd or random.random() < 0.5

        actors = [(True, None), (False, None)] if player_first else [(False, None), (True, None)]

        result = None
        for (is_player, _) in actors:
            if is_player:
                cont, msg = _player_action(character, enemy)
                print(msg)
                _pause(0.3)
                if not cont:
                    result = "escape"
                    break
                if not enemy.is_alive():
                    result = "win"
                    break
            else:
                msg = _enemy_action(enemy, character)
                print(msg)
                _pause(0.3)
                if not character.is_alive():
                    result = "lose"
                    break

        # 毒素傷害
        poison_msg = _process_poison(character)
        if poison_msg:
            print(poison_msg)
            if not character.is_alive():
                result = "lose"

        if result:
            break
        turn += 1

    print(f"\n{'═'*50}")
    if result == "win":
        exp = enemy.exp
        gold = enemy.get_gold()
        drops = enemy.get_drops()

        lvl_ups = character.gain_exp(exp)
        character.gold += gold
        print(f"  打敗了 {enemy.name}！")
        print(f"  獲得 {exp} 經驗值  {gold} 金幣")
        for lvl in lvl_ups:
            print(f"\n  ✦ 等級提升！現在是 Lv.{lvl} ✦")
            print(f"  HP +{ENEMIES[enemy_name].get('hp', 0)}  ATK/DEF/SPD 提升！")
        for item in drops:
            character.inventory.append(item)
            print(f"  獲得了道具：{item['name']}")

    elif result == "lose":
        print(f"  {character.name} 倒下了……")

    elif result == "escape":
        print(f"  成功逃脫了！")

    print(f"{'═'*50}\n")
    character.reset_battle_status()
    return result
