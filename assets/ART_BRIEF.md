# 🎨 Hisiri Mahjong — 美術製作簡報
> 給美術 Co-worker 的完整 AI 生圖 Prompt 指引

---

## 一、遊戲風格概覽

| 項目 | 說明 |
|---|---|
| 遊戲類型 | 瀏覽器 RPG，回合制戰鬥 |
| 整體美術調性 | **暗色系 Fantasy RPG**，帶有輕鬆幽默感（Boss 都是鵝） |
| UI 配色 | 深紫 `#3b0764`、亮紫 `#7c3aed`、深藍 `#1e1b4b`、暗底 `#0f172a` |
| 強調色 | 金黃 `#fbbf24`、粉紅 `#f43f5e`、翡翠 `#10b981` |
| 角色風格 | **2D 卡通向量風**，線條清晰，適度陰影，非寫實 |
| Boss 風格 | **人形鵝擬人化**，帶有各自主題道具（食物、武器等） |
| 輸出格式 | **PNG，透明背景（Alpha channel）** |
| 建議尺寸 | 角色立繪 `300×400px`，Boss `400×400px`，技能特效 `256×256px` |

---

## 二、統一 Style Prompt（每張圖都要加）

```
2D game character art, flat vector style with soft shading,
clean outlines, transparent background,
dark fantasy RPG aesthetic, vibrant colors,
game-ready sprite, front-facing or 3/4 view,
no background, high contrast, sharp edges
```

**負面 Prompt（Negative）：**
```
realistic, 3D render, photograph, blurry, background scene,
watermark, text, logo, multiple characters in one image,
nsfw, extra limbs, deformed
```

---

## 三、玩家角色（Classes）

### 🤺 戰士（Warrior）
- **造型**：重甲騎士，手持巨劍，體型壯碩
- **配色**：深紅 `#dc2626` + 深灰鋼鐵 `#374151`
- **特徵**：肩甲厚重，腰帶有鵝紋路裝飾，表情凶猛

```
[STYLE_PROMPT]
heavy armored warrior, wielding a large two-handed sword,
crimson and dark steel armor, muscular build,
shoulder pauldrons with goose emblem,
fierce expression, RPG game character
```

---

### 🧝 弓手（Archer）
- **造型**：輕裝精靈系，手持長弓，身形輕盈
- **配色**：翡翠綠 `#10b981` + 棕木色 `#92400e`
- **特徵**：箭袋掛背後，披風飄逸，耳朵微尖

```
[STYLE_PROMPT]
agile archer character, holding a longbow, light leather armor,
emerald green and brown color scheme, quiver on back,
flowing cape, slightly pointed ears, nimble pose, RPG game character
```

---

### ⚔️ 聖騎士（Paladin）
- **造型**：神聖騎士，手持光盾 + 聖劍，全身白金甲
- **配色**：白金 `#fbbf24` + 聖光藍白 `#dbeafe`
- **特徵**：盾牌有十字聖光紋，盔甲有羽翼裝飾

```
[STYLE_PROMPT]
holy paladin knight, one hand holding a divine shield with cross emblem,
other hand with a glowing holy sword, white and gold armor,
blue holy light aura, angelic wing decorations on armor, RPG game character
```

---

### 🧙 法師（Mage）
- **造型**：長袍法師，手持法杖，頭戴星形帽
- **配色**：深紫 `#7c3aed` + 星光銀 `#c4b5fd`
- **特徵**：法杖頂端發光寶珠，袍上有符文

```
[STYLE_PROMPT]
fantasy mage wizard, long purple robe with rune patterns,
holding a glowing magical staff with crystal orb,
pointed star hat, purple and silver color scheme, mystical aura, RPG game character
```

---

## 四、個人王 Boss（PERSONAL BOSSES）

> **風格規則**：Boss 全部是**擬人化的鵝**，穿著與主題相關的服裝，表情誇張有個性

---

### 🍳 早餐鵝（Breakfast Goose）Lv.30
- **主題**：早餐店老闆鵝
- **造型**：白色大鵝，戴廚師帽，圍裙上有煎蛋圖案，手持平底鍋
- **配色**：白 + 橙黃 `#f59e0b` + 淡藍
- **表情**：精神飽滿、挑眉

```
[STYLE_PROMPT]
anthropomorphic goose boss wearing a chef apron with sunny-side-up egg pattern,
white chef hat, holding a frying pan as weapon,
white feathers, orange beak, energetic happy expression,
breakfast kitchen theme, RPG boss character, front-facing
```

---

### 🍱 午餐鵝（Lunch Goose）Lv.30
- **主題**：商務午餐鵝
- **造型**：穿西裝的鵝，手持便當盒，另一手打領帶
- **配色**：深藍西裝 + 白衬衫 + 橘色領帶
- **表情**：疲憊上班族、眼神空洞

```
[STYLE_PROMPT]
anthropomorphic goose boss wearing a dark blue business suit,
holding a lunch box as weapon, white dress shirt, orange tie,
tired office worker expression, hollow eyes,
white feathers, orange beak, RPG boss character, front-facing
```

---

### 🍷 晚餐鵝（Dinner Goose）Lv.30
- **主題**：高級餐廳主廚鵝
- **造型**：法式主廚服，手持紅酒杯 + 主廚刀，燭光暈染
- **配色**：白廚師服 + 深紅 `#7f1d1d` + 金邊裝飾
- **表情**：優雅傲慢、閉眼輕笑

```
[STYLE_PROMPT]
anthropomorphic goose boss as an elegant French chef,
white chef coat with gold trim, holding a wine glass in one hand
and a chef knife in the other, candlelight warm glow,
dark red and gold color scheme, arrogant elegant smile,
RPG boss character, front-facing
```

---

### 🍜 宵夜鵝（Midnight Goose）Lv.35 ⭐ 最強個人王
- **主題**：深夜泡麵鬼鵝
- **造型**：穿睡衣的鬼鵝，眼圈深黑，手持巨大泡麵碗，蒸氣繚繞
- **配色**：灰白睡衣 + 深紫黑光環 `#3b0764` + 紅眼
- **表情**：詭異狂笑，半閉血紅眼

```
[STYLE_PROMPT]
anthropomorphic goose boss as a midnight demon, wearing tattered pajamas,
dark circles under glowing red eyes, holding an enormous ramen bowl,
steam swirling like dark magic, purple-black dark aura,
white and dark grey feathers, sinister grinning expression,
late night horror theme, RPG boss character, front-facing
```

---

## 五、世界王 Boss（WORLD BOSSES）

> 世界王更巨大、更威嚴，不需要完全擬人，可以半獸形態

---

### 🦢 鵝皇（Goose Emperor）
- **造型**：巨大白鵝，頭戴皇冠，雙翼展開，霸氣
- **配色**：純白羽毛 + 金冠 `#fbbf24` + 藍光氣場
- **體型**：比玩家大 3 倍

```
[STYLE_PROMPT]
giant majestic goose emperor boss, enormous white feathered wings spread wide,
golden crown on head, royal blue energy aura,
commanding pose, pure white plumage, orange beak,
towering presence, RPG world boss, semi-realistic fantasy style
```

---

### 🐉 古龍鵝（Dragon Goose）
- **造型**：龍鱗覆蓋的鵝，噴火，尾巴有龍尾
- **配色**：深墨綠鱗片 `#064e3b` + 火焰橘紅 + 金眼
- **特徵**：翅膀是龍翼而非鳥翼

```
[STYLE_PROMPT]
dragon-goose hybrid boss, goose body with dark green dragon scales,
dragon wings instead of feathers, breathing orange fire,
golden dragon eyes, long dragon tail, massive size,
dark green and fire orange color scheme, RPG world boss
```

---

## 六、技能特效圖示（Skill Icons）

**格式：256×256 px，圓形或方形圖示，深色背景配亮色特效**

| 技能 | 風格描述 |
|---|---|
| 🔥 火焰系 | 橘紅火焰漩渦，中心白熱 |
| ⚡ 閃電系 | 藍白電弧，放射狀 |
| ❄️ 冰霜系 | 水藍冰晶，六角雪花 |
| 🩸 流血系 | 深紅血滴，滴落效果 |
| 💫 神聖系 | 金黃光柱，十字光芒 |
| ☠️ 死亡系 | 紫黑骷髏光環 |

```
[SKILL_ICON_BASE_PROMPT]
game skill icon, circular badge design, glowing magical effect,
dark background, vibrant neon colors, fantasy RPG style,
256x256 pixel, clean sharp edges, no text
```

---

## 七、戰鬥特效（Battle VFX）

| 特效 | 說明 | Prompt 關鍵字 |
|---|---|---|
| 普攻打擊 | 白光斜線 | `slash impact, white light streak, motion blur` |
| 暴擊 | 金色爆裂星形 | `critical hit explosion, golden burst, star shaped` |
| 受傷閃紅 | 紅色衝擊波 | `damage impact, red shockwave, blood splatter` |
| 技能釋放 | 依屬性不同 | 參考技能顏色 |
| 死亡 | 光粒子消散 | `character dissolving into light particles, fade out` |

---

## 八、製作優先順序建議

1. **個人王 Boss × 4**（早餐/午餐/晚餐/宵夜鵝）— 最常出現
2. **玩家角色立繪 × 4**（戰士/弓手/聖騎士/法師）— 戰鬥主角
3. **世界王 Boss × 2**（鵝皇/古龍鵝）— 大型戰鬥
4. **技能特效圖示**（各 8~10 個）
5. **戰鬥 VFX 動態圖**（GIF 或 APNG）

---

## 九、整合說明（給開發者）

素材完成後提供給開發者（用 Claude Code），會：
- 把圖片整合進戰鬥介面
- 加入攻擊/受傷/待機 CSS 動畫
- 配上傷害數字飄出特效
- 調整戰鬥 log 格式配合新美術

**交付規格：**
- 格式：`PNG`，透明背景
- 命名規則：`warrior.png`、`boss_breakfast.png`、`skill_fire.png`
- 放入 `assets/classes/`、`assets/bosses/`、`assets/skills/` 資料夾
