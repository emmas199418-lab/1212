"""遊戲主世界模組"""
import random
from character import Character, CLASSES, exp_required
from items import show_shop, equip_item, ALL_ITEMS
from combat import run_battle, AREA_ENEMIES, AREA_BOSS

# ── 地圖定義 ─────────────────────────────────────────────
WORLD_MAP = {
    "新手村": {
        "description": "一個寧靜的小村莊，是冒險者的起點。",
        "connections": ["黑森林附近"],
        "has_shop": True,
        "has_inn": True,
        "has_boss": False,
        "enemies": [],
    },
    "黑森林附近": {
        "description": "黑森林的邊緣，可以感受到危險的氣息。",
        "connections": ["新手村", "黑森林"],
        "has_shop": False,
        "has_inn": False,
        "has_boss": False,
        "enemies": AREA_ENEMIES.get("黑森林附近", []),
    },
    "黑森林": {
        "description": "陰暗的森林，怪物橫行。傳說有一個強大的守護者…",
        "connections": ["黑森林附近", "廢棄礦坑入口"],
        "has_shop": True,
        "has_inn": True,
        "has_boss": True,
        "boss": "森林守護者",
        "boss_defeated": False,
        "enemies": AREA_ENEMIES.get("黑森林", []),
        "required_level": 3,
    },
    "廢棄礦坑入口": {
        "description": "通往廢棄礦坑的入口，石牆上刻著警告的符文。",
        "connections": ["黑森林", "廢棄礦坑"],
        "has_shop": False,
        "has_inn": False,
        "has_boss": False,
        "enemies": AREA_ENEMIES.get("黑森林", []),
    },
    "廢棄礦坑": {
        "description": "深邃的礦坑，充滿了礦物的氣息。傳說礦坑深處藏著巨大的邪惡…",
        "connections": ["廢棄礦坑入口", "魔王城堡"],
        "has_shop": True,
        "has_inn": True,
        "has_boss": True,
        "boss": "礦坑魔王",
        "boss_defeated": False,
        "enemies": AREA_ENEMIES.get("廢棄礦坑", []),
        "required_level": 6,
    },
    "魔王城堡": {
        "description": "魔王的居所，黑暗能量充斥著每個角落。",
        "connections": ["廢棄礦坑"],
        "has_shop": True,
        "has_inn": False,
        "has_boss": True,
        "boss": "魔王",
        "boss_defeated": False,
        "enemies": AREA_ENEMIES.get("魔王城堡", []),
        "required_level": 10,
    },
}


def print_title():
    print("""
╔══════════════════════════════════════════╗
║      ★ 暗 影 傳 說 ★                     ║
║      繁體中文文字 RPG 冒險遊戲           ║
╚══════════════════════════════════════════╝
""")


def create_character():
    """角色建立流程"""
    print("═" * 50)
    print("  【角色建立】")
    print("═" * 50)

    # 輸入名字
    while True:
        name = input("\n  請輸入你的角色名稱：").strip()
        if name:
            break
        print("  名稱不能為空！")

    # 選擇職業
    print("\n  請選擇職業：\n")
    jobs = list(CLASSES.keys())
    for i, job in enumerate(jobs, 1):
        cls = CLASSES[job]
        print(f"  {i}. 【{job}】")
        print(f"     {cls['description']}")
        print(f"     HP:{cls['base_hp']}  MP:{cls['base_mp']}  "
              f"攻擊:{cls['base_atk']}  防禦:{cls['base_def']}  速度:{cls['base_spd']}")
        print()

    while True:
        choice = input("  輸入職業編號（1-3）：").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(jobs):
            job = jobs[int(choice) - 1]
            break
        print("  請輸入有效的編號！")

    character = Character(name, job)
    # 給予初始裝備
    starter_weapon = {"戰士": "木劍", "法師": "木法杖", "盜賊": "短匕"}[job]
    character.equipped_weapon = dict(ALL_ITEMS[starter_weapon])
    character.inventory.append(dict(ALL_ITEMS["小回復藥水"]))
    character.inventory.append(dict(ALL_ITEMS["小回復藥水"]))

    print(f"\n  ══════════════════════════════")
    print(f"  歡迎，{job}【{name}】！")
    print(f"  你的冒險從新手村開始。")
    print(f"  起始武器：{starter_weapon}")
    print(f"  起始道具：小回復藥水 x2")
    print(f"  ══════════════════════════════")
    input("\n  按 Enter 繼續…")
    return character


def show_area(area_name, area_data):
    print(f"\n╔══ 【{area_name}】")
    print(f"║  {area_data['description']}")
    print(f"╚{'═'*40}")


def area_menu(character, area_name, world):
    """區域主選單，回傳下一個區域名稱或特殊指令"""
    area_data = world[area_name]
    show_area(area_name, area_data)

    options = []
    # 探索（有敵人才顯示）
    if area_data.get("enemies"):
        options.append(("探索", "在此區域探索，可能遭遇怪物"))
    # BOSS
    if area_data.get("has_boss") and not area_data.get("boss_defeated"):
        options.append(("BOSS 戰", f"挑戰 {area_data.get('boss', 'BOSS')}"))
    # 商店
    if area_data.get("has_shop"):
        options.append(("商店", "購買道具或裝備"))
    # 旅館
    if area_data.get("has_inn"):
        options.append(("旅館", "休息恢復 HP 和 MP（花費 20 金幣）"))
    # 移動
    for conn in area_data.get("connections", []):
        options.append((f"前往 {conn}", f"移動到 {conn}"))
    # 通用
    options.append(("查看角色", "查看角色狀態"))
    options.append(("背包", "管理背包道具"))
    options.append(("存檔提示", "顯示存檔提示"))

    while True:
        print("\n  【行動選單】")
        for i, (action, desc) in enumerate(options, 1):
            print(f"   {i}. {action}  — {desc}")

        choice = input("\n  請輸入選項編號：").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            print("  請輸入有效的編號。")
            continue

        action, _ = options[int(choice) - 1]

        # ── 探索 ──
        if action == "探索":
            if area_data["enemies"]:
                enemy_name = random.choice(area_data["enemies"])
                print(f"\n  你在探索中遭遇了 {enemy_name}！")
                result = run_battle(character, enemy_name)
                if result == "lose":
                    return "__lose__"
                show_area(area_name, area_data)

        # ── BOSS ──
        elif action.startswith("BOSS"):
            req_lv = area_data.get("required_level", 1)
            if character.level < req_lv:
                print(f"  你的等級太低！建議 Lv.{req_lv} 以上再挑戰。")
                confirm = input("  仍要強行挑戰？(y/N) ").strip().lower()
                if confirm != "y":
                    continue
            boss_name = area_data["boss"]
            result = run_battle(character, boss_name, is_boss=True)
            if result == "lose":
                return "__lose__"
            elif result == "win":
                area_data["boss_defeated"] = True
                print(f"  ✦ {boss_name} 已被擊敗！{area_name}的封印解除了。")
                if area_name == "魔王城堡":
                    return "__win__"

        # ── 商店 ──
        elif action == "商店":
            show_shop(area_name, character)

        # ── 旅館 ──
        elif action == "旅館":
            cost = 20
            if character.gold < cost:
                print(f"  金幣不足！住旅館需要 {cost} 金幣。")
            else:
                character.gold -= cost
                character.hp = character.max_hp
                character.mp = character.max_mp
                character.status = None
                character.status_turns = 0
                print(f"  安穩地休息了一晚，HP 和 MP 完全恢復！（消耗 {cost} 金幣）")

        # ── 前往 ──
        elif action.startswith("前往 "):
            dest = action[3:]
            dest_data = world.get(dest, {})
            req_lv = dest_data.get("required_level", 0)
            if req_lv and character.level < req_lv:
                print(f"  {dest} 危機四伏，建議等級 {req_lv} 以上再前往。")
                confirm = input("  仍要前進？(y/N) ").strip().lower()
                if confirm != "y":
                    continue
            return dest

        # ── 查看角色 ──
        elif action == "查看角色":
            print(f"\n  ══ 角色資訊 ══")
            print(character.get_status_str())
            print(f"\n  技能：{', '.join(character.skills)}")
            next_exp = exp_required(character.level)
            print(f"  下一等級：{next_exp - character.exp} EXP 後升級")

        # ── 背包 ──
        elif action == "背包":
            inventory_menu(character)

        # ── 存檔提示 ──
        elif action == "存檔提示":
            print("\n  本遊戲不支援存檔。結束遊戲請直接關閉視窗，或回到主選單。")

    return area_name


def inventory_menu(character):
    """背包管理介面"""
    while True:
        print("\n  ══ 背包 ══")
        character.show_inventory()
        print("\n   1. 使用道具")
        print("   2. 裝備武器/防具")
        print("   3. 查看裝備")
        print("   0. 返回")

        choice = input("  選擇：").strip()

        if choice == "0":
            break

        elif choice == "1":
            usable = [item for item in character.inventory if item["type"] == "消耗品"]
            if not usable:
                print("  沒有可用的消耗品。")
                continue
            print("\n  消耗品列表：")
            for i, item in enumerate(usable, 1):
                print(f"   {i}. {item['name']}  {item.get('description','')}")
            print("   0. 取消")
            sel = input("  選擇要使用的道具：").strip()
            if sel == "0":
                continue
            if sel.isdigit() and 1 <= int(sel) <= len(usable):
                from items import use_item
                item = usable[int(sel) - 1]
                msg = use_item(character, item)
                character.inventory.remove(item)
                print(f"  {msg}")
            else:
                print("  無效選項。")

        elif choice == "2":
            equippable = [item for item in character.inventory if item["type"] in ("武器", "防具")]
            if not equippable:
                print("  背包中沒有可裝備的物品。")
                continue
            print("\n  可裝備物品：")
            for i, item in enumerate(equippable, 1):
                print(f"   {i}. [{item['type']}] {item['name']}  {item.get('description','')}")
            print("   0. 取消")
            sel = input("  選擇要裝備的物品：").strip()
            if sel == "0":
                continue
            if sel.isdigit() and 1 <= int(sel) <= len(equippable):
                item = equippable[int(sel) - 1]
                character.inventory.remove(item)
                msg = equip_item(character, item)
                print(f"  {msg}")
            else:
                print("  無效選項。")

        elif choice == "3":
            print(f"\n  武器：{character.equipped_weapon['name'] if character.equipped_weapon else '未裝備'}")
            if character.equipped_weapon:
                print(f"         {character.equipped_weapon.get('description','')}")
            print(f"  防具：{character.equipped_armor['name'] if character.equipped_armor else '未裝備'}")
            if character.equipped_armor:
                print(f"         {character.equipped_armor.get('description','')}")
        else:
            print("  無效選項。")


def run_game():
    """主遊戲流程"""
    print_title()

    print("  1. 開始新遊戲")
    print("  2. 退出遊戲")
    choice = input("\n  請選擇：").strip()
    if choice != "1":
        print("  感謝遊玩！再見！")
        return

    character = create_character()

    current_area = "新手村"
    world = {k: dict(v) for k, v in WORLD_MAP.items()}

    print(f"\n  【故事開始】")
    print("  黑暗正在侵蝕大地，怪物們紛紛出沒，")
    print("  傳說只有打倒魔王才能拯救世界。")
    print("  你，是否願意踏上這段旅程？\n")
    input("  按 Enter 開始冒險…")

    while True:
        result = area_menu(character, current_area, world)

        if result == "__lose__":
            print("\n  ╔══════════════════════╗")
            print("  ║   G A M E   O V E R  ║")
            print("  ╚══════════════════════╝")
            print(f"\n  {character.name} 倒在了冒險途中……")
            print("  黑暗繼續籠罩著大地。\n")
            input("  按 Enter 返回主選單…")
            run_game()
            return

        elif result == "__win__":
            print("\n  ╔═══════════════════════════════╗")
            print("  ║   C O N G R A T U L A T I O N S  ║")
            print("  ╚═══════════════════════════════╝")
            print(f"\n  {character.name} 打敗了魔王！")
            print("  黑暗消散，大地重現光明。")
            print(f"  最終等級：Lv.{character.level}")
            print(f"  餘下金幣：{character.gold} 金")
            print("\n  感謝你的遊玩，英雄！\n")
            input("  按 Enter 返回主選單…")
            run_game()
            return

        elif result not in world:
            print(f"  無法前往 {result}。")
        else:
            current_area = result
