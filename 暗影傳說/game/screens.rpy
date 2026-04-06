## =============================================
## 暗影傳說 - 畫面定義（HUD、背包、狀態）
## =============================================

# ---------- 戰鬥/遊戲中 HUD ----------
screen hud():
    zorder 5
    # HP 列
    frame:
        xpos 20 ypos 20
        xsize 280 ysize 110
        background "#00000099"
        padding (12, 8)
        vbox:
            spacing 6
            text "[player_name]  Lv.[player_lv]" size 20 color "#f0e6d2"
            hbox:
                spacing 8
                text "HP" size 18 color "#ff7777"
                bar value player_hp range player_max_hp xsize 160 ysize 16
                text "[player_hp]/[player_max_hp]" size 16 color "#ffaaaa"
            hbox:
                spacing 8
                text "MP" size 18 color "#7799ff"
                bar value player_mp range player_max_mp xsize 160 ysize 16
                text "[player_mp]/[player_max_mp]" size 16 color "#aabbff"
            text "G:[player_gold]  ATK:[player_atk]  DEF:[player_def]" size 16 color "#d4c080"

# ---------- 背包畫面 ----------
screen inventory_screen():
    modal True
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 700 ysize 500
        background "#1a1a2e"
        padding (20, 20)
        vbox:
            spacing 12
            text "⚔  背  包  ⚔" xalign 0.5 size 32 color "#f0d060"
            text "裝備：[equipped_weapon]  |  [equipped_armor]" size 20 color "#aaccff" xalign 0.5
            null height 8
            if len(inventory) == 0:
                text "背包是空的" xalign 0.5 size 24 color "#888888"
            else:
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    ysize 320
                    vbox:
                        spacing 8
                        for idx, item in enumerate(inventory):
                            $ item_info = item_db.get(item, {})
                            $ desc = item_info.get("desc", "未知道具")
                            textbutton "[item]  —  [desc]":
                                action Function(use_item_from_bag, item)
                                text_size 22
                                text_color "#e8e8e8"
                                hover_background "#334466"
                                padding (10, 6)
            null height 8
            textbutton "關閉背包":
                xalign 0.5
                action Hide("inventory_screen")
                text_size 24 text_color "#ffdd88"
                background "#33224466"
                hover_background "#554433"
                padding (20, 10)

# ---------- 狀態畫面 ----------
screen status_screen():
    modal True
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 500 ysize 480
        background "#1a1a2e"
        padding (24, 24)
        vbox:
            spacing 14
            text "[ 冒險者狀態 ]" xalign 0.5 size 30 color "#f0d060"
            null height 4
            grid 2 8:
                xspacing 20 yspacing 8
                text "姓名" size 22 color "#aaaacc"
                text "[player_name]" size 22 color "#ffffff"
                text "等級" size 22 color "#aaaacc"
                text "[player_lv]" size 22 color "#ffff88"
                text "HP" size 22 color "#ff9999"
                text "[player_hp] / [player_max_hp]" size 22 color "#ffbbbb"
                text "MP" size 22 color "#9999ff"
                text "[player_mp] / [player_max_mp]" size 22 color "#bbbbff"
                text "攻擊" size 22 color "#ffcc66"
                text "[player_atk]" size 22 color "#ffdd88"
                text "防禦" size 22 color "#66ccff"
                text "[player_def]" size 22 color "#88ddff"
                text "速度" size 22 color "#88ff88"
                text "[player_spd]" size 22 color "#aaffaa"
                text "經驗" size 22 color "#cc88ff"
                text "[player_exp] / [player_exp_next]" size 22 color "#ddaaff"
            null height 8
            text "武器：[equipped_weapon]  防具：[equipped_armor]" size 20 color "#d4c080" xalign 0.5
            null height 8
            textbutton "關閉":
                xalign 0.5
                action Hide("status_screen")
                text_size 24 text_color "#ffdd88"
                background "#33224466"
                hover_background "#554433"
                padding (20, 10)

# ---------- 戰鬥畫面 ----------
screen battle_screen(enemy_n, enemy_h, enemy_mh, enemy_a, enemy_d, log):
    modal True
    add "#00000099"
    frame:
        xalign 0.5 yalign 0.5
        xsize 760 ysize 560
        background "#110a1e"
        padding (24, 20)
        vbox:
            spacing 10
            # 標題
            text "⚔  戰  鬥  ⚔" xalign 0.5 size 32 color "#ff4444"
            null height 4
            # 敵人狀態
            hbox:
                xalign 0.5
                spacing 12
                add "char_[enemy_n].png" zoom 0.3 if renpy.loadable("images/characters/char_[enemy_n].png") else NullDisplayable()
                vbox:
                    spacing 6
                    text "[enemy_n]" size 26 color "#ff8888"
                    hbox:
                        spacing 6
                        text "HP" size 20 color "#ff5555"
                        bar value enemy_h range enemy_mh xsize 220 ysize 18
                        text "[enemy_h]/[enemy_mh]" size 18 color "#ffaaaa"
                    text "ATK:[enemy_a]  DEF:[enemy_d]" size 18 color "#cc8888"
            # 分隔線
            null height 4
            text "─────────────────────────────────" xalign 0.5 color "#554444"
            # 玩家狀態
            hbox:
                xalign 0.5
                spacing 16
                vbox:
                    spacing 4
                    text "[player_name]  Lv.[player_lv]" size 22 color "#e8d5a3"
                    hbox:
                        spacing 6
                        text "HP" size 18 color "#ff7777"
                        bar value player_hp range player_max_hp xsize 180 ysize 16
                        text "[player_hp]/[player_max_hp]" size 16 color "#ffaaaa"
                    hbox:
                        spacing 6
                        text "MP" size 18 color "#7799ff"
                        bar value player_mp range player_max_mp xsize 180 ysize 16
                        text "[player_mp]/[player_max_mp]" size 16 color "#aabbff"
            null height 4
            # 戰鬥記錄
            frame:
                background "#0d0d1a"
                xsize 700 ysize 80
                padding (10, 6)
                vbox:
                    for line in log[-3:]:
                        text line size 18 color "#cccccc"
            null height 6
            # 行動選擇
            hbox:
                xalign 0.5
                spacing 16
                textbutton "⚔ 普通攻擊":
                    action Return("attack")
                    text_size 22 text_color "#ffdd88"
                    background "#2a1a00"
                    hover_background "#554400"
                    padding (16, 10)
                textbutton "✨ 技能（-10MP）":
                    action Return("skill") if player_mp >= 10 else NullAction()
                    text_size 22
                    text_color "#88aaff" if player_mp >= 10 else "#555577"
                    background "#001a2a"
                    hover_background "#003355"
                    padding (16, 10)
                textbutton "🎒 使用道具":
                    action Return("item")
                    text_size 22 text_color "#88ffaa"
                    background "#001a0d"
                    hover_background "#003322"
                    padding (16, 10)
                textbutton "💨 逃跑":
                    action Return("flee")
                    text_size 22 text_color "#aaaaaa"
                    background "#1a1a1a"
                    hover_background "#333333"
                    padding (16, 10)

# ---------- 戰鬥道具選擇 ----------
screen battle_item_screen(items):
    modal True
    add "#000000aa"
    frame:
        xalign 0.5 yalign 0.5
        xsize 500 ysize 380
        background "#1a1a2e"
        padding (20, 20)
        vbox:
            spacing 10
            text "選擇使用的道具" xalign 0.5 size 28 color "#f0d060"
            if len(items) == 0:
                text "沒有可用的道具" xalign 0.5 size 22 color "#888888"
            else:
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    ysize 240
                    vbox:
                        spacing 8
                        for item in items:
                            $ info = item_db.get(item, {})
                            $ desc = info.get("desc", "")
                            textbutton "[item] — [desc]":
                                action Return(item)
                                text_size 20 text_color "#e8e8e8"
                                hover_background "#334466"
                                padding (10, 6)
            textbutton "取消":
                xalign 0.5
                action Return(None)
                text_size 22 text_color "#ffdd88"
                background "#33224466"
                hover_background "#554433"
                padding (16, 8)

# ---------- 快捷選單（Escape 鍵） ----------
screen quick_menu():
    zorder 100
    if quick_menu:
        hbox:
            xalign 0.5 yalign 1.0
            yoffset -20
            spacing 10
            textbutton "背包":
                action Show("inventory_screen")
                text_size 20 text_color "#e8e8e8"
                background "#00000088"
                hover_background "#334455"
                padding (12, 6)
            textbutton "狀態":
                action Show("status_screen")
                text_size 20 text_color "#e8e8e8"
                background "#00000088"
                hover_background "#334455"
                padding (12, 6)
            textbutton "存檔":
                action ShowMenu("save")
                text_size 20 text_color "#e8e8e8"
                background "#00000088"
                hover_background "#334455"
                padding (12, 6)
            textbutton "讀檔":
                action ShowMenu("load")
                text_size 20 text_color "#e8e8e8"
                background "#00000088"
                hover_background "#334455"
                padding (12, 6)
            textbutton "主選單":
                action MainMenu()
                text_size 20 text_color "#e8e8e8"
                background "#00000088"
                hover_background "#554433"
                padding (12, 6)
