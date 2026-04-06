## =============================================
## 暗影傳說 - 角色定義與全域變數
## =============================================

# ---------- 角色定義 ----------
define narrator = Character(None, what_style="narrator_text")
define mc = Character("流浪劍士", color="#e8d5a3", what_color="#ffffff")
define elder = Character("村長", color="#a8d8a8", what_color="#ffffff")
define merchant = Character("商人艾德", color="#f4c97a", what_color="#ffffff")
define guard = Character("守衛長", color="#c0c0c0", what_color="#ffffff")
define demon = Character("暗影惡魔", color="#cc4444", what_color="#ffcccc")
define spirit = Character("古老精靈", color="#88ccff", what_color="#e8f4ff")
define ally = Character("冒險者莉娜", color="#ffaabb", what_color="#ffffff")

# ---------- 玩家屬性 ----------
default player_name = "無名"
default player_hp = 100
default player_max_hp = 100
default player_mp = 50
default player_max_mp = 50
default player_atk = 15
default player_def = 8
default player_spd = 10
default player_lv = 1
default player_exp = 0
default player_exp_next = 100
default player_gold = 50

# ---------- 背包系統 ----------
default inventory = []
default equipped_weapon = "鐵劍"
default equipped_armor = "舊皮甲"

# 道具資料庫（名稱: {描述, 效果類型, 效果值}）
define item_db = {
    "回復藥草":   {"desc": "回復 30 點 HP",        "type": "heal_hp",  "val": 30,  "price": 20},
    "靈力水晶":   {"desc": "回復 20 點 MP",        "type": "heal_mp",  "val": 20,  "price": 25},
    "大回復藥水": {"desc": "回復 80 點 HP",        "type": "heal_hp",  "val": 80,  "price": 60},
    "解毒草":     {"desc": "解除中毒狀態",         "type": "cure",     "val": 0,   "price": 30},
    "力量精華":   {"desc": "戰鬥中攻擊力+10",      "type": "buff_atk", "val": 10,  "price": 50},
    "鐵劍":       {"desc": "普通的鐵製長劍",       "type": "weapon",   "val": 15,  "price": 80},
    "精鋼劍":     {"desc": "鋒利的精鋼劍，攻擊+8","type": "weapon",   "val": 23,  "price": 200},
    "舊皮甲":     {"desc": "破舊的皮製盔甲",       "type": "armor",    "val": 8,   "price": 40},
    "鎖子甲":     {"desc": "堅固的鎖子甲，防禦+7","type": "armor",    "val": 15,  "price": 180},
    "古代碎片":   {"desc": "散發著神秘光芒的碎片", "type": "key",      "val": 0,   "price": 0},
}

# ---------- 戰鬥變數 ----------
default in_battle = False
default enemy_name = ""
default enemy_hp = 0
default enemy_max_hp = 0
default enemy_atk = 0
default enemy_def = 0
default enemy_reward_gold = 0
default enemy_reward_exp = 0
default battle_log = []
default player_poisoned = False
default player_buff_atk = 0
default battle_turn = 0

# ---------- 旗標 ----------
default flag_village_saved = False
default flag_met_ally = False
default flag_ancient_sword = False
default flag_final_boss = False
default flag_true_ending = False
default chapter = 1

# ---------- 樣式 ----------
style narrator_text:
    color "#d4c5a9"
    italic True
    size 28
