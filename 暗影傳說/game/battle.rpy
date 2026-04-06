## =============================================
## 暗影傳說 - 戰鬥系統
## =============================================
init python:
    import random

    # ── 初始化一場戰鬥 ──
    def start_battle(name, hp, atk, def_, reward_gold, reward_exp):
        store.enemy_name      = name
        store.enemy_hp        = hp
        store.enemy_max_hp    = hp
        store.enemy_atk       = atk
        store.enemy_def       = def_
        store.enemy_reward_gold = reward_gold
        store.enemy_reward_exp  = reward_exp
        store.battle_log      = ["戰鬥開始！與 {} 交戰！".format(name)]
        store.battle_turn     = 0
        store.player_poisoned = False
        store.player_buff_atk = 0
        store.in_battle       = True

    # ── 玩家普通攻擊 ──
    def battle_attack():
        base = store.player_atk + store.player_buff_atk
        dmg = max(1, base - store.enemy_def + random.randint(-3, 5))
        store.enemy_hp = max(0, store.enemy_hp - dmg)
        store.battle_log.append("你揮劍攻擊，造成 {} 點傷害！".format(dmg))

    # ── 玩家技能攻擊（消耗MP） ──
    def battle_skill():
        if store.player_mp < 10:
            store.battle_log.append("MP 不足，無法使用技能！")
            return
        store.player_mp -= 10
        base = int((store.player_atk + store.player_buff_atk) * 1.8)
        dmg = max(1, base - store.enemy_def + random.randint(0, 8))
        store.enemy_hp = max(0, store.enemy_hp - dmg)
        store.battle_log.append("⚡ 你施展【暗影斬】，造成 {} 點大傷害！".format(dmg))

    # ── 敵人攻擊 ──
    def enemy_attack():
        if store.enemy_hp <= 0:
            return
        dmg = max(1, store.enemy_atk - store.player_def + random.randint(-2, 4))
        store.player_hp = max(0, store.player_hp - dmg)
        store.battle_log.append("{} 攻擊你，造成 {} 點傷害！".format(store.enemy_name, dmg))

    # ── 使用道具（戰鬥中） ──
    def use_item_in_battle(item_name):
        if item_name not in store.inventory:
            return
        info = store.item_db.get(item_name, {})
        t = info.get("type", "")
        v = info.get("val", 0)
        if t == "heal_hp":
            store.player_hp = min(store.player_max_hp, store.player_hp + v)
            store.battle_log.append("你使用了【{}】，回復 {} 點 HP！".format(item_name, v))
            store.inventory.remove(item_name)
        elif t == "heal_mp":
            store.player_mp = min(store.player_max_mp, store.player_mp + v)
            store.battle_log.append("你使用了【{}】，回復 {} 點 MP！".format(item_name, v))
            store.inventory.remove(item_name)
        elif t == "buff_atk":
            store.player_buff_atk += v
            store.battle_log.append("你使用了【{}】，攻擊力暫時提升 {}！".format(item_name, v))
            store.inventory.remove(item_name)
        elif t == "cure":
            store.player_poisoned = False
            store.battle_log.append("你使用了【{}】，解除了中毒！".format(item_name))
            store.inventory.remove(item_name)
        else:
            store.battle_log.append("這個道具在戰鬥中無法使用。")

    # ── 嘗試逃跑 ──
    def try_flee():
        chance = 0.5 + (store.player_spd - 10) * 0.03
        chance = max(0.1, min(0.9, chance))
        return random.random() < chance

    # ── 戰鬥勝利結算 ──
    def battle_victory():
        store.player_gold += store.enemy_reward_gold
        gain_exp(store.enemy_reward_exp)
        store.in_battle = False
        store.player_buff_atk = 0

    # ── 獲得經驗值並處理升級 ──
    def gain_exp(exp):
        store.player_exp += exp
        while store.player_exp >= store.player_exp_next:
            store.player_exp -= store.player_exp_next
            store.player_lv += 1
            store.player_max_hp += 20
            store.player_hp = store.player_max_hp
            store.player_max_mp += 10
            store.player_mp = store.player_max_mp
            store.player_atk += 3
            store.player_def += 2
            store.player_spd += 1
            store.player_exp_next = int(store.player_exp_next * 1.5)

    # ── 從背包外使用道具 ──
    def use_item_from_bag(item_name):
        if item_name not in store.inventory:
            return
        info = store.item_db.get(item_name, {})
        t = info.get("type", "")
        v = info.get("val", 0)
        if t == "heal_hp":
            store.player_hp = min(store.player_max_hp, store.player_hp + v)
            store.inventory.remove(item_name)
            renpy.notify("回復了 {} 點 HP！".format(v))
        elif t == "heal_mp":
            store.player_mp = min(store.player_max_mp, store.player_mp + v)
            store.inventory.remove(item_name)
            renpy.notify("回復了 {} 點 MP！".format(v))
        elif t == "cure":
            store.player_poisoned = False
            store.inventory.remove(item_name)
            renpy.notify("解毒成功！")
        elif t in ("weapon", "armor"):
            if t == "weapon":
                store.equipped_weapon = item_name
                store.player_atk = info.get("val", store.player_atk)
            else:
                store.equipped_armor = item_name
                store.player_def = info.get("val", store.player_def)
            store.inventory.remove(item_name)
            renpy.notify("裝備了【{}】！".format(item_name))
        else:
            renpy.notify("現在無法使用這個道具。")

# ── 戰鬥 Label（呼叫後根據結果跳轉） ──
label do_battle:
    python:
        battle_result = None
        fled = False

    show screen hud

    while enemy_hp > 0 and player_hp > 0:
        $ action = renpy.call_screen(
            "battle_screen",
            enemy_n  = enemy_name,
            enemy_h  = enemy_hp,
            enemy_mh = enemy_max_hp,
            enemy_a  = enemy_atk,
            enemy_d  = enemy_def,
            log      = battle_log
        )

        if action == "attack":
            $ battle_attack()
            if enemy_hp > 0:
                $ enemy_attack()

        elif action == "skill":
            $ battle_skill()
            if enemy_hp > 0:
                $ enemy_attack()

        elif action == "item":
            $ usable = [i for i in inventory if item_db.get(i,{}).get("type","") in ("heal_hp","heal_mp","buff_atk","cure")]
            $ chosen = renpy.call_screen("battle_item_screen", items=usable)
            if chosen:
                $ use_item_in_battle(chosen)
            if enemy_hp > 0:
                $ enemy_attack()

        elif action == "flee":
            if try_flee():
                $ battle_log.append("你成功逃離了戰鬥！")
                $ fled = True
                $ in_battle = False
                jump battle_fled
            else:
                $ battle_log.append("逃跑失敗！")
                $ enemy_attack()

        $ battle_turn += 1

        if player_poisoned:
            $ player_hp = max(0, player_hp - 5)
            $ battle_log.append("中毒傷害！損失 5 點 HP。")

    if player_hp <= 0:
        $ in_battle = False
        hide screen hud
        jump battle_lost
    else:
        $ battle_victory()
        hide screen hud
        jump battle_won

label battle_won:
    "[enemy_name] 被擊倒了！"
    "獲得 [enemy_reward_exp] 點經驗值，[enemy_reward_gold] 枚金幣！"
    if player_lv > 1 and player_exp == 0:
        "✨ 等級提升！現在是 Lv.[player_lv]！"
        "HP 和 MP 已完全回復，能力值提升！"
    return

label battle_lost:
    scene bg_gameover with dissolve
    "你的力量耗盡，倒在了黑暗之中……"
    "……但命運似乎還未對你絕望。"
    menu:
        "從最後存檔讀取":
            $ renpy.load(renpy.newest_slot())
        "回到主選單":
            $ renpy.full_restart()

label battle_fled:
    "你拼命逃跑，終於甩脫了追擊！"
    return
