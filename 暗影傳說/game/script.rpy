## =============================================
## 暗影傳說 - 主劇情腳本
## =============================================

# ---------- 圖片聲明 ----------
image bg_title       = "images/bg/bg_title.png"
image bg_forest      = "images/bg/bg_forest.png"
image bg_village     = "images/bg/bg_village.png"
image bg_inn         = "images/bg/bg_inn.png"
image bg_shop        = "images/bg/bg_shop.png"
image bg_dungeon     = "images/bg/bg_dungeon.png"
image bg_ruins       = "images/bg/bg_ruins.png"
image bg_boss_room   = "images/bg/bg_boss_room.png"
image bg_ending      = "images/bg/bg_ending.png"
image bg_gameover    = "images/bg/bg_gameover.png"

image char_elder    = "images/characters/char_elder.png"
image char_merchant = "images/characters/char_merchant.png"
image char_guard    = "images/characters/char_guard.png"
image char_demon    = "images/characters/char_demon.png"
image char_spirit   = "images/characters/char_spirit.png"
image char_ally     = "images/characters/char_ally.png"

# 佔位純色圖（若圖片不存在時顯示）
image bg_title      = Solid("#0d0d1e")
image bg_forest     = Solid("#0a1a0a")
image bg_village    = Solid("#1a1205")
image bg_inn        = Solid("#1a0f05")
image bg_shop       = Solid("#1a1a05")
image bg_dungeon    = Solid("#050505")
image bg_ruins      = Solid("#101008")
image bg_boss_room  = Solid("#1a0505")
image bg_ending     = Solid("#050d1a")
image bg_gameover   = Solid("#000000")

# ---------- 設定 ----------
define config.window_title = "暗影傳說"
define config.screen_width  = 1280
define config.screen_height = 720
define config.has_autosave   = True
define config.autosave_slots = 3
define config.save_directory = "暗影傳說"

# ---------- 自訂主選單 ----------
screen main_menu():
    tag menu
    add "bg_title"
    vbox:
        xalign 0.5 yalign 0.5
        spacing 0
        # 標題
        frame:
            background "#00000099"
            padding (40, 20)
            xalign 0.5
            vbox:
                spacing 4
                text "暗 影 傳 說" xalign 0.5 size 72 color "#d4a000" bold True
                text "Shadow Legend" xalign 0.5 size 28 color "#886600" italic True
        null height 48
        # 選單按鈕
        for label_, action_ in [
            ("開始新遊戲", Start()),
            ("繼續遊戲",  ShowMenu("load") if renpy.newest_slot() else NullAction()),
            ("設定",       ShowMenu("preferences")),
            ("結束遊戲",   Quit(confirm=True)),
        ]:
            textbutton label_:
                action action_
                xalign 0.5
                text_size 36
                text_color "#f0e0a0"
                text_hover_color "#ffffff"
                background "#00000066"
                hover_background "#55330088"
                padding (60, 14)
        null height 20
        text "Version 1.0  |  © 暗影傳說製作組" xalign 0.5 size 16 color "#666666"

# ---------- 遊戲開始 ----------
label splashscreen:
    scene black
    with Pause(0.5)
    show text "暗影傳說" at truecenter with dissolve
    with Pause(2.0)
    hide text with dissolve
    with Pause(0.5)
    return

label start:
    # 命名角色
    $ player_name = renpy.input("請輸入你的角色名稱：", default="無名", length=8).strip() or "無名"
    $ inventory = ["回復藥草", "回復藥草"]

    # 開場白
    scene bg_forest with fade
    show screen hud

    narrator "黑暗籠罩著大地。古老的預言說，當「暗影」降臨，世界將陷入永恆的黑夜。"
    narrator "然而在這混沌之世，有一名流浪劍士——[player_name]——正獨自穿越危險的迷霧森林。"

    mc "……又是個沒有星光的夜晚。"
    mc "（看了看破舊的地圖）聽說前方有個叫「晨曦村」的地方，說不定能找到線索。"

    # 前往村莊
    jump chapter1_village

# =============================================
# 第一章：晨曦村的危機
# =============================================
label chapter1_village:
    scene bg_village with dissolve

    narrator "──  第一章：晨曦村的危機  ──"
    narrator "進入村莊，村民們一臉恐慌，街道上幾乎空無一人。"

    show char_elder at left with moveinleft
    elder "陌生人！你來的正是時候！"
    mc "發生什麼事了？"
    elder "三天前，村子附近的廢墟開始傳出詭異的聲音，還有村民失蹤……"
    elder "昨晚，守衛發現廢墟中有暗影魔物出沒！我們的守衛長獨自前去查探，至今未回。"

    menu:
        "我可以去調查廢墟。":
            $ flag_village_saved = True
            mc "放心，我去看看。"
            elder "謝謝你！請先到村中的商店補充一些道具。"
            jump chapter1_shop_choice

        "這不關我的事。":
            mc "抱歉，我只是路過。"
            elder "……求求你了！我們已經無路可走！"
            narrator "看著老村長哀求的眼神，[player_name] 心中猶豫了。"
            menu:
                "（嘆氣）好吧，我去看看。":
                    $ flag_village_saved = True
                    mc "好吧，但我不保證什麼。"
                    jump chapter1_shop_choice
                "（轉身離去）":
                    jump chapter1_leave_village

label chapter1_leave_village:
    hide char_elder
    scene bg_forest with dissolve
    narrator "你離開了晨曦村，獨自踏入更深的森林。"
    narrator "但直覺告訴你，那個廢墟與你的目的地有所關聯……"
    mc "（停下腳步）……算了，我還是去看看。"
    jump chapter1_shop_choice

label chapter1_shop_choice:
    hide char_elder
    menu "你要先做什麼？":
        "前往商店購買道具":
            jump chapter1_shop
        "直接前往廢墟":
            jump chapter1_ruins_entrance

# ---------- 商店 ----------
label chapter1_shop:
    scene bg_shop with dissolve
    show char_merchant at center with moveinright

    merchant "歡迎！歡迎！我是艾德商店的老闆艾德。在這亂世，準備充足才能活下去！"

    jump shop_menu

label shop_menu:
    $ shop_items = ["回復藥草", "靈力水晶", "大回復藥水", "解毒草", "力量精華", "精鋼劍", "鎖子甲"]
    menu "【艾德的商店】  你有 [player_gold] 枚金幣":
        "回復藥草（20G）- 回復30HP" if player_gold >= 20:
            $ inventory.append("回復藥草")
            $ player_gold -= 20
            merchant "好的！這是最新鮮的藥草！"
            jump shop_menu
        "靈力水晶（25G）- 回復20MP" if player_gold >= 25:
            $ inventory.append("靈力水晶")
            $ player_gold -= 25
            merchant "小心保存，這可是純淨的魔力結晶！"
            jump shop_menu
        "大回復藥水（60G）- 回復80HP" if player_gold >= 60:
            $ inventory.append("大回復藥水")
            $ player_gold -= 60
            merchant "上等品！保你在危急時刻轉危為安！"
            jump shop_menu
        "解毒草（30G）- 解除中毒" if player_gold >= 30:
            $ inventory.append("解毒草")
            $ player_gold -= 30
            merchant "廢墟裡的毒蜘蛛可不好惹，帶著這個保險！"
            jump shop_menu
        "精鋼劍（200G）- 攻擊+8" if player_gold >= 200:
            $ inventory.append("精鋼劍")
            $ player_gold -= 200
            merchant "這把劍可是鍛造師的心血之作！"
            jump shop_menu
        "鎖子甲（180G）- 防禦+7" if player_gold >= 180:
            $ inventory.append("鎖子甲")
            $ player_gold -= 180
            merchant "穿上它，箭矢都難以刺穿！"
            jump shop_menu
        "離開商店":
            merchant "保重！江湖險惡，保命要緊！"
            hide char_merchant
            scene bg_village with dissolve
            jump chapter1_ruins_entrance

# ---------- 廢墟探索 ----------
label chapter1_ruins_entrance:
    scene bg_ruins with dissolve
    narrator "你抵達了村子東邊的古老廢墟。斷壁殘垣間，瀰漫著腐敗的黑霧。"
    mc "（警惕地握住劍柄）這股氣息……不尋常。"

    narrator "突然，一個身影從瓦礫後方衝出！"

    # 第一場戰鬥：骷髏士兵
    $ start_battle("廢墟骷髏", hp=40, atk=10, def_=3, reward_gold=25, reward_exp=30)
    call do_battle from _chapter1_battle1

    scene bg_ruins with dissolve
    show screen hud

    narrator "深入廢墟，你發現了被魔法符文束縛的守衛長。"
    show char_guard at center with moveinleft
    guard "（虛弱地）你……你是來救我的？"
    mc "先別說話，讓我解開這些符文。"
    guard "等等……廢墟深處有一個巨大的「暗影之門」，魔物就是從那裡湧出來的！"
    guard "門上刻著古代文字……好像需要什麼鑰匙才能關閉它。"

    menu:
        "我去找鑰匙，你先回村子。":
            mc "你撐得住嗎？"
            guard "有你破除符文，我能自己走回去。去吧，那扇門不能一直開著！"
            hide char_guard
            jump chapter1_deep_ruins

        "和我一起去找鑰匙。":
            guard "……好，我雖然受傷，但我熟悉這裡的地形。"
            hide char_guard
            narrator "守衛長雖然虛弱，但仍緊跟在你身後。"
            $ flag_met_ally = True
            jump chapter1_deep_ruins

label chapter1_deep_ruins:
    narrator "你深入廢墟核心，四周的黑霧愈發濃烈。"

    # 第二場戰鬥：暗影獸
    $ start_battle("暗影獸", hp=65, atk=14, def_=5, reward_gold=40, reward_exp=55)
    call do_battle from _chapter1_battle2

    scene bg_ruins with dissolve
    show screen hud

    narrator "在一塊古老的石板旁，你找到了一個發著藍光的碎片。"
    mc "（撿起碎片）這就是傳說中的「古代碎片」？"
    $ inventory.append("古代碎片")
    "獲得【古代碎片】！"

    jump chapter2_shadow_gate

# =============================================
# 第二章：暗影之門
# =============================================
label chapter2_shadow_gate:
    scene bg_dungeon with dissolve
    narrator "──  第二章：暗影之門  ──"
    narrator "你持著古代碎片走向廢墟最深處的巨門。"
    narrator "巨門高達十米，表面刻滿了黑色的符文，散發著令人不安的黑紫色光芒。"

    mc "（將碎片嵌入門上的凹槽）……"
    narrator "碎片猛地發出耀眼的白光，符文開始逐一熄滅。"
    narrator "但就在此時，一個高大的身影從門中衝出！"

    show char_demon at center with moveinright

    demon "哈哈哈！竟有人膽敢阻擋暗影的降臨！"
    mc "（怒目而視）你是誰？！"
    demon "我是「暗影傳說」中預言的使者——幽冥魔將！"
    demon "預言說，只有集齊三塊古代碎片，才能永久封印暗影之門。"
    demon "而你……只有一塊！"
    mc "……那另外兩塊在哪裡？"
    demon "哈哈，找到了又如何？你只不過是一個流浪的廢物！"

    menu:
        "（怒拔長劍）廢話少說，受死！":
            mc "比起說廢話，我更習慣用劍說話！"
            $ start_battle("幽冥魔將", hp=120, atk=20, def_=10, reward_gold=100, reward_exp=120)
            call do_battle from _chapter2_battle1
            jump chapter2_demon_defeated

        "（冷靜）先告訴我，其他兩塊碎片在哪裡。":
            mc "我需要知道另外兩塊碎片的位置。"
            demon "（冷笑）呵……你倒是沉得住氣。"
            demon "一塊在北方雪山的精靈遺跡，另一塊……在我手中！"
            demon "要想要？用命來換！"
            $ start_battle("幽冥魔將", hp=120, atk=20, def_=10, reward_gold=100, reward_exp=120)
            call do_battle from _chapter2_battle2
            jump chapter2_demon_defeated

label chapter2_demon_defeated:
    scene bg_dungeon with dissolve
    show screen hud
    narrator "幽冥魔將倒下了，一塊閃爍著黑色光芒的碎片從他身上掉落。"
    $ inventory.append("古代碎片")
    "獲得第二塊【古代碎片】！"
    mc "（望向遠方）還有一塊……在北方的精靈遺跡。"

    jump chapter3_elven_ruins

# =============================================
# 第三章：精靈的試煉
# =============================================
label chapter3_elven_ruins:
    scene bg_ruins with dissolve
    narrator "──  第三章：精靈的試煉  ──"
    narrator "你跋山涉水，來到了傳說中精靈族遺棄的北方遺跡。"
    narrator "此地瀰漫著古老的魔法氣息，與廢墟中的邪惡氣息截然不同。"

    show char_spirit at center with dissolve
    spirit "（輕柔的聲音）……有人類來到了這裡。"
    mc "（環顧四周）是誰？！"
    spirit "（從光芒中顯現）不必驚慌。我是這座遺跡的守護精靈，已在此沉睡了千年。"
    spirit "你身上的古代碎片……讓我感受到了。你是來尋找第三塊碎片的吧？"

    mc "是的。我需要封印暗影之門。"
    spirit "……那扇門，在我入睡前便已存在。我知道它的危險。"
    spirit "但第三塊碎片，不是你想拿就能拿的。你必須通過我的試煉。"

    menu:
        "我接受試煉":
            mc "說吧，試煉是什麼？"
            spirit "很簡單——擊敗遺跡的守護神獸。若你能做到，証明你有足夠的力量守護這個世界。"
            jump chapter3_trial_battle
        "有沒有其他辦法？":
            spirit "……有，但只有一個。"
            spirit "你必須放棄你現有的力量，讓我將精靈之力注入你體內。但這很危險，可能讓你失去意識。"
            menu:
                "接受精靈之力":
                    spirit "閉上眼睛……"
                    narrator "一股溫暖的光芒湧入你的身體。"
                    $ player_hp = player_max_hp
                    $ player_mp = player_max_mp
                    $ player_atk += 5
                    $ player_def += 3
                    "精靈之力注入！HP、MP完全回復，能力值永久提升！"
                    jump chapter3_trial_battle
                "還是選擇試煉":
                    mc "試煉更光明正大。我選試煉。"
                    jump chapter3_trial_battle

label chapter3_trial_battle:
    hide char_spirit
    narrator "遺跡深處，一頭散發著金色光芒的巨大神獸現身！"

    $ start_battle("遺跡守護神獸", hp=160, atk=25, def_=15, reward_gold=150, reward_exp=200)
    call do_battle from _chapter3_battle

    scene bg_ruins with dissolve
    show screen hud
    show char_spirit at center with dissolve

    spirit "（微微一笑）……你的劍，確實有守護的力量。"
    spirit "這是第三塊古代碎片，請善用它。"
    $ inventory.append("古代碎片")
    "獲得第三塊【古代碎片】！"
    spirit "等等……在你去封印之前，讓我告訴你一件事。"
    spirit "傳說中還有一把「暗影聖劍」，沉睡在遺跡最深處。那把劍才是真正能消滅暗影的力量。"

    menu:
        "去尋找暗影聖劍":
            mc "帶我去！"
            jump chapter3_ancient_sword
        "直接去封印暗影之門":
            mc "我已經有足夠的力量了，先去封印。"
            $ flag_ancient_sword = False
            hide char_spirit
            jump chapter4_final

label chapter3_ancient_sword:
    hide char_spirit
    narrator "在遺跡最深處，一把散發著銀白色光芒的長劍懸浮在石台中央。"
    mc "（伸手觸碰）……這把劍，好像在等著我。"
    narrator "劍身傳來一陣溫暖，彷彿有意識的存在在與你溝通。"
    $ equipped_weapon = "暗影聖劍"
    $ player_atk += 15
    $ flag_ancient_sword = True
    "裝備了【暗影聖劍】！攻擊力大幅提升！"
    jump chapter4_final

# =============================================
# 第四章：暗影的終結
# =============================================
label chapter4_final:
    scene bg_boss_room with fade
    narrator "──  第四章：暗影的終結  ──"
    narrator "你帶著三塊古代碎片，再度回到了那扇巨大的暗影之門。"
    narrator "黑紫色的光芒比之前更加濃烈，彷彿門後的存在感受到了威脅。"

    mc "（將三塊碎片依次嵌入門上）……就是現在！"
    narrator "三塊碎片同時發出刺眼的白光，暗影之門劇烈震動起來！"
    narrator "但就在此時，一股強大的黑暗力量從門中噴湧而出——"
    narrator "一個巨大的存在降臨了！"

    show char_demon at center with dissolve
    demon "哈哈哈哈！以為三塊碎片就能封印我？！"
    demon "我是暗影之主本體！那個「幽冥魔將」只不過是我的分身！"
    mc "（死死盯著黑暗巨影）……你果然還在。"
    demon "你一個流浪劍士，憑什麼對抗暗影的力量？！"

    if flag_ancient_sword:
        mc "（握緊暗影聖劍）因為我有一把為消滅你而生的劍！"
        demon "那把劍……！這不可能！"
    else:
        mc "憑我的意志！這片大地上的人們，不應該活在暗影之中！"
        demon "空口白話！受死吧！"

    # 最終決戰
    if flag_ancient_sword:
        $ start_battle("暗影之主", hp=280, atk=32, def_=18, reward_gold=500, reward_exp=600)
    else:
        $ start_battle("暗影之主", hp=320, atk=38, def_=22, reward_gold=500, reward_exp=600)

    call do_battle from _chapter4_final_battle

    $ flag_final_boss = True
    jump ending

# =============================================
# 結局
# =============================================
label ending:
    scene black with fade
    narrator "……黑暗消散了。"

    scene bg_ending with dissolve
    narrator "隨著暗影之主的隕落，三塊古代碎片迸發出強烈的白光，將暗影之門永久封印。"
    narrator "黑霧散去，久違的星光重新照耀大地。"

    mc "（仰望著滿天星斗）……終於結束了。"

    if flag_village_saved:
        narrator "晨曦村的村民們歡呼雀躍，老村長熱淚盈眶。"
        elder "感謝你，勇者！你拯救了我們，也拯救了整個世界！"

    if flag_met_ally:
        $ flag_true_ending = True
        show char_ally at right with moveinright
        ally "（微笑）……沒想到一開始覺得你只是個冷漠的劍客。"
        mc "（淡淡地）我只是做了該做的事。"
        ally "那就繼續做下去吧。這個世界，還需要像你這樣的人。"

    if flag_true_ending:
        narrator "── 真實結局：光明的守護者 ──"
        narrator "你不再是孤獨的流浪劍士。"
        narrator "一段新的旅程，在晨曦的光芒中展開……"
    else:
        narrator "── 普通結局：暗影的終結者 ──"
        narrator "你獨自封印了暗影，卻再次踏上了流浪的旅途。"
        narrator "或許，有一天，你會找到真正屬於自己的地方。"

    scene black with fade
    show text "感謝遊玩\n暗 影 傳 說" at truecenter with dissolve
    with Pause(3.0)
    hide text with dissolve
    with Pause(1.0)

    return
