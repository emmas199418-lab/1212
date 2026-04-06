# 暗影傳說 Shadow Legend

> 奇幻風格繁體中文視覺小說 RPG，以 Ren'Py 引擎製作

---

## 安裝 Ren'Py

### 步驟 1：下載 Ren'Py SDK

前往官網下載最新版本（建議 8.x）：
https://www.renpy.org/latest.html

- **Windows**：下載 `renpy-X.X.X-sdk.zip`，解壓到任意位置
- **macOS**：下載 `.dmg` 安裝包
- **Linux**：下載 `.tar.bz2` 壓縮包

### 步驟 2：安裝字型（重要！）

繁體中文需要 CJK 字型，否則文字會顯示為方塊：

1. 下載 **Noto Sans CJK TC**：https://fonts.google.com/noto/specimen/Noto+Sans+TC
2. 下載後改名為 `NotoSansCJK-Regular.ttc`
3. 放到 `暗影傳說/game/fonts/` 資料夾

---

## 執行遊戲

### 方法一：透過 Ren'Py Launcher（建議）

1. 啟動 `renpy.exe`（Windows）或 `renpy.sh`（Linux/Mac）
2. 點擊「**+ 添加項目**」→ 選擇本專案資料夾（`暗影傳說/`）
3. 點擊「**啟動項目**」

### 方法二：直接執行（Windows）

```
renpy.exe 暗影傳說
```

### 方法三：命令列（Linux/Mac）

```bash
./renpy.sh 暗影傳說
```

---

## 遊戲資料夾結構

```
暗影傳說/
├── game/
│   ├── script.rpy          # 主劇情腳本（對話、劇情分支）
│   ├── battle.rpy          # 戰鬥系統
│   ├── screens.rpy         # UI 畫面（HUD、背包、狀態）
│   ├── define.rpy          # 角色定義、變數、道具資料庫
│   ├── options.rpy         # 遊戲設定
│   ├── gui.rpy             # 介面樣式
│   ├── fonts/
│   │   └── NotoSansCJK-Regular.ttc    ← 字型放這裡
│   └── images/
│       ├── bg/             ← 背景圖放這裡
│       ├── characters/     ← 角色立繪放這裡
│       └── ui/             ← UI 圖片放這裡
└── README.md
```

---

## 放入自製圖片

### 背景圖命名規則

| 檔名 | 場景 | 建議尺寸 |
|------|------|----------|
| `bg_title.png` | 標題畫面 | 1280×720 |
| `bg_forest.png` | 迷霧森林 | 1280×720 |
| `bg_village.png` | 晨曦村 | 1280×720 |
| `bg_inn.png` | 旅館 | 1280×720 |
| `bg_shop.png` | 商店 | 1280×720 |
| `bg_dungeon.png` | 地下城 | 1280×720 |
| `bg_ruins.png` | 古老廢墟 | 1280×720 |
| `bg_boss_room.png` | 暗影之門 | 1280×720 |
| `bg_ending.png` | 結局 | 1280×720 |
| `bg_gameover.png` | 遊戲結束 | 1280×720 |

### 角色立繪命名規則

| 檔名 | 角色 | 建議尺寸 |
|------|------|----------|
| `char_elder.png` | 村長 | 300×600（透明背景） |
| `char_merchant.png` | 商人艾德 | 300×600（透明背景） |
| `char_guard.png` | 守衛長 | 300×600（透明背景） |
| `char_demon.png` | 暗影惡魔 | 300×600（透明背景） |
| `char_spirit.png` | 古老精靈 | 300×600（透明背景） |
| `char_ally.png` | 冒險者莉娜 | 300×600（透明背景） |

> **提示**：圖片未提供也沒關係！遊戲會以純色佔位背景繼續運行。

---

## 遊戲內容

### 劇情結構（4章）

- **第一章**：晨曦村的危機 — 調查廢墟、救出守衛長
- **第二章**：暗影之門 — 對戰幽冥魔將、獲得第二塊碎片
- **第三章**：精靈的試煉 — 北方遺跡、獲得暗影聖劍（可選）
- **第四章**：暗影的終結 — 最終決戰

### 分支結局

- **真實結局**：完成所有支線劇情（救村莊 + 遇到盟友）
- **普通結局**：完成主線但跳過部分支線

### 系統功能

| 功能 | 操作方式 |
|------|----------|
| 開啟背包 | 快捷列點擊「背包」|
| 查看狀態 | 快捷列點擊「狀態」|
| 存檔 | 右鍵選單或快捷列「存檔」|
| 讀檔 | 右鍵選單或快捷列「讀檔」|
| 戰鬥 | 選擇「攻擊」/「技能」/「道具」/「逃跑」|

---

## 遊戲截圖預覽（佔位色說明）

未放圖片時的佔位顏色：
- 標題畫面：深藍黑 `#0d0d1e`
- 森林：深綠 `#0a1a0a`
- 村莊：深棕 `#1a1205`
- 廢墟/地下城：接近純黑

---

## 擴展開發建議

1. **加入音樂**：在 `game/audio/` 放置 `.ogg` 或 `.mp3`，在 `script.rpy` 中加入 `play music "audio/bgm_forest.ogg"`
2. **加入音效**：`play sound "audio/sfx_sword.wav"` 在攻擊時播放
3. **加入更多章節**：在 `script.rpy` 末尾繼續寫 `label chapter5_xxx:`
4. **加入更多敵人**：在 `battle.rpy` 的 `start_battle()` 中設定不同參數
5. **加入商店更多道具**：在 `define.rpy` 的 `item_db` 中新增條目
