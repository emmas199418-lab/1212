## =============================================
## 暗影傳說 - GUI 設定（最小化版本）
## 覆蓋 Ren'Py 預設 GUI 以符合暗色調主題
## =============================================

init python:
    gui.init(1280, 720)

define gui.text_font = gui.preference("font", "fonts/NotoSansCJK-Regular.ttc")
define gui.name_text_font = "fonts/NotoSansCJK-Regular.ttc"
define gui.interface_text_font = "fonts/NotoSansCJK-Regular.ttc"

define gui.text_size = 26
define gui.name_text_size = 30
define gui.interface_text_size = 22
define gui.label_text_size = 28
define gui.notify_text_size = 22
define gui.title_text_size = 72

define gui.text_color = '#ddd0b8'
define gui.accent_color = '#d4a000'
define gui.idle_color = '#888888'
define gui.idle_small_color = '#aaaaaa'
define gui.hover_color = '#f0d060'
define gui.selected_color = '#ffffff'
define gui.insensitive_color = '#555555'
define gui.muted_color = '#4a4032'
define gui.hover_muted_color = '#7a6852'
define gui.interface_text_color = '#cccccc'
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.choice_button_text_idle_color = '#ddd0b8'
define gui.choice_button_text_hover_color = '#ffffff'

define gui.textbox_height = 200
define gui.textbox_yalign = 1.0
define gui.dialogue_text_xpos = 268
define gui.dialogue_text_ypos = 65
define gui.dialogue_width = 1116
define gui.dialogue_xalign = 0.5
define gui.namebox_width = None
define gui.namebox_xalign = 0.0
define gui.name_xalign = 0.0
define gui.slot_time_format = "%Y-%m-%d %H:%M"

define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

define gui.navigation_xpos = 60
define gui.skip_transition = dissolve
define gui.game_menu_background = "#0d0d1e"

style default:
    font "fonts/NotoSansCJK-Regular.ttc"
    size 26

style say_dialogue:
    color "#ddd0b8"
    size 26
    line_spacing 4

style say_label:
    color "#d4a000"
    size 30
    bold True

style choice_button:
    background "#1a1a2e"
    hover_background "#332244"
    padding (20, 12)

style choice_button_text:
    idle_color "#ddd0b8"
    hover_color "#ffffff"
    size 24
