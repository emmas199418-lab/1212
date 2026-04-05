"""道具系統模組"""

# ── 所有道具定義 ──────────────────────────────────────────
ALL_ITEMS = {
    # 消耗品
    "小回復藥水": {
        "name": "小回復藥水", "type": "消耗品",
        "description": "恢復 50 HP", "price": 20,
        "effect": "heal", "value": 50,
    },
    "中回復藥水": {
        "name": "中回復藥水", "type": "消耗品",
        "description": "恢復 120 HP", "price": 50,
        "effect": "heal", "value": 120,
    },
    "大回復藥水": {
        "name": "大回復藥水", "type": "消耗品",
        "description": "恢復 300 HP", "price": 120,
        "effect": "heal", "value": 300,
    },
    "小魔力藥水": {
        "name": "小魔力藥水", "type": "消耗品",
        "description": "恢復 30 MP", "price": 25,
        "effect": "mp_restore", "value": 30,
    },
    "中魔力藥水": {
        "name": "中魔力藥水", "type": "消耗品",
        "description": "恢復 70 MP", "price": 60,
        "effect": "mp_restore", "value": 70,
    },
    "解毒藥": {
        "name": "解毒藥", "type": "消耗品",
        "description": "解除中毒狀態", "price": 30,
        "effect": "cure_poison",
    },
    "萬靈藥": {
        "name": "萬靈藥", "type": "消耗品",
        "description": "完全恢復 HP 與 MP", "price": 300,
        "effect": "full_restore",
    },

    # 武器
    "木劍": {
        "name": "木劍", "type": "武器",
        "description": "攻擊 +3", "price": 30,
        "atk_bonus": 3,
    },
    "鐵劍": {
        "name": "鐵劍", "type": "武器",
        "description": "攻擊 +8", "price": 80,
        "atk_bonus": 8,
    },
    "精鋼劍": {
        "name": "精鋼劍", "type": "武器",
        "description": "攻擊 +15", "price": 200,
        "atk_bonus": 15,
    },
    "聖劍": {
        "name": "聖劍", "type": "武器",
        "description": "攻擊 +30", "price": 600,
        "atk_bonus": 30,
    },
    "木法杖": {
        "name": "木法杖", "type": "武器",
        "description": "攻擊 +2，魔法增幅", "price": 35,
        "atk_bonus": 2,
    },
    "水晶法杖": {
        "name": "水晶法杖", "type": "武器",
        "description": "攻擊 +10，魔法增幅", "price": 150,
        "atk_bonus": 10,
    },
    "短匕": {
        "name": "短匕", "type": "武器",
        "description": "攻擊 +5，速度 +2", "price": 50,
        "atk_bonus": 5,
    },
    "暗影利刃": {
        "name": "暗影利刃", "type": "武器",
        "description": "攻擊 +18，速度 +4", "price": 400,
        "atk_bonus": 18,
    },

    # 防具
    "布衣": {
        "name": "布衣", "type": "防具",
        "description": "防禦 +2", "price": 25,
        "def_bonus": 2,
    },
    "皮甲": {
        "name": "皮甲", "type": "防具",
        "description": "防禦 +6", "price": 70,
        "def_bonus": 6,
    },
    "鐵甲": {
        "name": "鐵甲", "type": "防具",
        "description": "防禦 +13", "price": 180,
        "def_bonus": 13,
    },
    "龍鱗甲": {
        "name": "龍鱗甲", "type": "防具",
        "description": "防禦 +25", "price": 500,
        "def_bonus": 25,
    },
    "法師長袍": {
        "name": "法師長袍", "type": "防具",
        "description": "防禦 +3，MP +20", "price": 60,
        "def_bonus": 3,
    },
    "輕便皮甲": {
        "name": "輕便皮甲", "type": "防具",
        "description": "防禦 +5，速度 +1", "price": 65,
        "def_bonus": 5,
    },
}

# ── 商店庫存 (區域對應) ──────────────────────────────────
SHOP_STOCK = {
    "新手村": ["小回復藥水", "小魔力藥水", "木劍", "布衣", "皮甲", "木法杖", "短匕"],
    "黑森林": ["小回復藥水", "中回復藥水", "小魔力藥水", "解毒藥", "鐵劍", "皮甲", "水晶法杖", "法師長袍", "輕便皮甲"],
    "廢棄礦坑": ["中回復藥水", "中魔力藥水", "解毒藥", "精鋼劍", "鐵甲", "水晶法杖"],
    "魔王城堡": ["大回復藥水", "中魔力藥水", "萬靈藥", "聖劍", "龍鱗甲", "暗影利刃"],
}


def get_item(name):
    return ALL_ITEMS.get(name)


def use_item(character, item):
    """使用消耗品，回傳描述字串"""
    if item["type"] != "消耗品":
        return f"{item['name']} 不是消耗品！"

    effect = item.get("effect")
    if effect == "heal":
        amount = character.heal(item["value"])
        return f"使用 {item['name']}，恢復了 {amount} HP！"
    elif effect == "mp_restore":
        amount = character.restore_mp(item["value"])
        return f"使用 {item['name']}，恢復了 {amount} MP！"
    elif effect == "cure_poison":
        if character.status == "poison":
            character.status = None
            character.status_turns = 0
            return f"使用 {item['name']}，解除了中毒狀態！"
        return f"使用 {item['name']}，但目前沒有中毒..."
    elif effect == "full_restore":
        character.hp = character.max_hp
        character.mp = character.max_mp
        return f"使用 {item['name']}，HP 與 MP 完全恢復！"
    return f"使用了 {item['name']}。"


def equip_item(character, item):
    """裝備武器或防具，回傳描述字串"""
    if item["type"] == "武器":
        old = character.equipped_weapon
        character.equipped_weapon = item
        if old:
            character.inventory.append(old)
        return f"裝備了 {item['name']}！" + (f"（卸下了 {old['name']}）" if old else "")
    elif item["type"] == "防具":
        old = character.equipped_armor
        character.equipped_armor = item
        if old:
            character.inventory.append(old)
        return f"裝備了 {item['name']}！" + (f"（卸下了 {old['name']}）" if old else "")
    return f"{item['name']} 無法裝備。"


def show_shop(area, character):
    """顯示商店並讓玩家購買"""
    stock_names = SHOP_STOCK.get(area, [])
    if not stock_names:
        print("這裡沒有商店。")
        return

    while True:
        print(f"\n══ {area} 商店 ══  （你的金幣：{character.gold}）")
        items = [ALL_ITEMS[n] for n in stock_names if n in ALL_ITEMS]
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item['name']:<12} {item['price']:>4} 金  {item.get('description','')}")
        print("  0. 離開商店")

        choice = input("\n請選擇要購買的商品編號：").strip()
        if choice == "0":
            print("離開了商店。")
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
            print("無效的選項。")
            continue

        item = items[int(choice) - 1]
        if character.gold < item["price"]:
            print(f"金幣不足！需要 {item['price']} 金，你只有 {character.gold} 金。")
        else:
            character.gold -= item["price"]
            character.inventory.append(dict(item))
            print(f"購買了 {item['name']}！剩餘金幣：{character.gold}")
