## =============================================
## 暗影傳說 - 遊戲選項設定
## =============================================

define config.name = "暗影傳說"
define config.version = "1.0"
define gui.show_name = True

define config.window_title = "暗影傳說"
define config.screen_width  = 1280
define config.screen_height = 720

# 存檔資料夾名稱
define config.save_directory = "ShadowLegend-1"

# 文字框設定
define config.has_say_vbox = False

# 語言設定（繁體中文）
define config.language = None

# 自動存檔
define config.has_autosave = True
define config.autosave_slots = 3

# 字型設定（使用系統字體，或放自己的字體到 game/fonts/ 後修改路徑）
define gui.default_font = "fonts/NotoSansCJK-Regular.ttc"
define gui.name_text_font = "fonts/NotoSansCJK-Regular.ttc"

# 若沒有字體檔案，Ren'Py 會退回系統預設
init -1 python:
    import os
    font_path = os.path.join(config.gamedir, "fonts", "NotoSansCJK-Regular.ttc")
    if not os.path.exists(font_path):
        config.font_replacement_map = {}

define gui.text_size = 26
define gui.name_text_size = 30
define gui.interface_text_size = 22

# 對話框外觀
define gui.textbox_height = 185
define gui.textbox_yalign = 1.0
define gui.dialogue_text_xpos = 268
define gui.dialogue_text_ypos = 75
define gui.dialogue_width = 1116
define gui.dialogue_xalign = 0.5
define gui.namebox_width = None
define gui.namebox_xalign = 0.0
define gui.name_xalign = 0.0

# 顏色主題（暗色調）
define gui.accent_color = "#d4a000"
define gui.idle_color = "#888888"
define gui.idle_small_color = "#aaaaaa"
define gui.hover_color = "#f0d060"
define gui.selected_color = "#ffffff"
define gui.insensitive_color = "#555555"
define gui.muted_color = "#4a4032"
define gui.hover_muted_color = "#7a6852"
define gui.text_color = "#ddd0b8"
define gui.interface_text_color = "#cccccc"

# 對話框背景顏色
define gui.textbox_color = "#0d0d1e"
