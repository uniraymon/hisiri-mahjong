# 🎨 Hisiri Mahjong — 美術交付（V3 動感版）
> 給 Claude Code 接手用的整合說明

## 0. 重點摘要

- **風格**：現代精緻像素 + 3/4 視角動感戰鬥姿勢
- **格式**：PNG，96×96 native（角色/Boss）、64×64 native（技能 icon）；每張另附 `_x4` 預覽圖
- **特色**：深色描邊、5 級陰影、動感速度線、每隻角色獨特姿勢
- **重要**：V3 為單張立繪（每隻獨立姿勢），**不再走紙娃娃換裝**。換裝若有需要請走 V1 路徑（保留在 `png/modern/`）。

---

## 1. 主要交付路徑

```
mahjong/art/png/modern_v3/
├── classes/                      ★ 玩家角色立繪
│   ├── warrior.png               戰士天鵝（弓步舉劍）
│   ├── archer.png                弓手天鵝（拉弓瞄準）
│   ├── paladin.png               聖騎天鵝（舉盾持聖劍）
│   └── mage.png                  法師天鵝（法杖高舉詠唱）
│
├── bosses/                       ★ Boss
│   ├── boss_breakfast.png        早餐鵝（揮鍋猛擊）
│   ├── boss_lunch.png            午餐鵝（疲憊提便當）
│   ├── boss_dinner.png           晚餐鵝（雙手酒杯+刀）
│   ├── boss_midnight.png         宵夜鵝（紫黑邪氣紅眼）
│   ├── boss_emperor.png          鵝皇（巨翼王者）
│   └── boss_dragon.png           古龍鵝（龍翼噴火）
│
├── skills/                       技能圖示
│   ├── skill_fire.png            🔥 火焰螺旋
│   ├── skill_lightning.png       ⚡ 閃電
│   ├── skill_ice.png             ❄️ 冰霜
│   ├── skill_blood.png           🩸 流血漩渦
│   ├── skill_holy.png            💫 神聖光柱
│   └── skill_death.png           ☠️ 怒吼骷髏
│
├── preview.html                  V3 角色 gallery 預覽頁
└── (生成腳本 generate_v3_all.py 在 png/ 上層)
```

每張 PNG 都有兩種尺寸：
- `xxx.png`     — native 96×96（或技能 64×64），**遊戲實際使用**
- `xxx_x4.png`  — 放大 4×，預覽用

備用版本（V1 紙娃娃換裝，保留參考）：`mahjong/art/png/modern/`

---

## 2. 整合到 `quest.html`

### 2.1 角色 / Boss 資料新增 `art` 欄位

```js
// 玩家角色
const CLASSES = {
  warrior:  { ..., image: 'art/png/modern_v3/classes/warrior.png' },
  archer:   { ..., image: 'art/png/modern_v3/classes/archer.png' },
  paladin:  { ..., image: 'art/png/modern_v3/classes/paladin.png' },
  mage:     { ..., image: 'art/png/modern_v3/classes/mage.png' },
};

// Boss（quest.html 第 3398 行起）
{
  id: 'breakfast_goose', name: '早餐鵝', icon: '🍳',
  art: 'art/png/modern_v3/bosses/boss_breakfast.png',   // ⬅ 新增
  ...
},
{ id: 'lunch_goose',    name: '午餐鵝', icon: '🍱',
  art: 'art/png/modern_v3/bosses/boss_lunch.png', ... },
{ id: 'dinner_goose',   name: '晚餐鵝', icon: '🍷',
  art: 'art/png/modern_v3/bosses/boss_dinner.png', ... },
{ id: 'midnight_goose', name: '宵夜鵝', icon: '🍜',
  art: 'art/png/modern_v3/bosses/boss_midnight.png', ... },
// 世界王
{ id: 'dragon_goose', ...,
  art: 'art/png/modern_v3/bosses/boss_dragon.png' },
```

### 2.2 渲染：用 `<img>` 顯示

```js
const iconHtml = boss.art
  ? `<img class="boss-art" src="${boss.art}" alt="${boss.name}">`
  : `<div class="boss-icon">${boss.icon}</div>`;
```

### 2.3 必加 CSS（**最重要**）

```css
/* 沒這條像素圖會被瀏覽器糊掉 */
.boss-art, .class-art, .skill-art {
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
.boss-art {
  width: 96px;
  height: 96px;
}
.boss-card .boss-art {
  width: 192px;
  height: 192px;
  filter: drop-shadow(0 4px 12px rgba(124, 58, 237, 0.4));
}
.skill-art {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
```

### 2.4 戰鬥動畫

```css
@keyframes boss-attack {
  0%, 100% { transform: translateX(0) scaleX(1); }
  30% { transform: translateX(-8px) scale(1.05); }
  60% { transform: translateX(12px) scaleX(1.02); }
}
@keyframes boss-hurt {
  0%, 100% { filter: drop-shadow(0 4px 12px rgba(124,58,237,0.4)); }
  50% { filter: drop-shadow(0 0 20px #ef4444) brightness(1.4); }
}
@keyframes boss-cast {
  0%, 100% { filter: drop-shadow(0 4px 12px rgba(124,58,237,0.4)); }
  50% { filter: drop-shadow(0 0 25px #fbbf24) brightness(1.3); }
}
.boss-art.attacking { animation: boss-attack 0.5s ease; }
.boss-art.hurt      { animation: boss-hurt   0.4s ease; }
.boss-art.casting   { animation: boss-cast   0.7s ease; }
```

戰鬥 log 觸發時：
```js
bossArtEl.classList.add('attacking');
setTimeout(() => bossArtEl.classList.remove('attacking'), 500);
```

---

## 3. 技能圖示整合

```js
const SKILL_ELEMENTS = {
  fire:      'art/png/modern_v3/skills/skill_fire.png',
  lightning: 'art/png/modern_v3/skills/skill_lightning.png',
  ice:       'art/png/modern_v3/skills/skill_ice.png',
  blood:     'art/png/modern_v3/skills/skill_blood.png',
  holy:      'art/png/modern_v3/skills/skill_holy.png',
  death:     'art/png/modern_v3/skills/skill_death.png',
};

function renderSkill(skill) {
  const iconUrl = SKILL_ELEMENTS[skill.element];
  return `
    <div class="skill-row">
      ${iconUrl ? `<img class="skill-art" src="${iconUrl}">` : ''}
      <span class="skill-name">${skill.name}</span>
    </div>
  `;
}
```

---

## 4. 受傷數字飄出

```css
@keyframes dmg-float {
  0%   { opacity: 0; transform: translateY(0) scale(0.7); }
  20%  { opacity: 1; transform: translateY(-10px) scale(1.1); }
  100% { opacity: 0; transform: translateY(-60px) scale(1); }
}
.dmg-num {
  position: absolute; pointer-events: none;
  font-weight: 900; font-size: 22px;
  text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
  animation: dmg-float 0.9s ease forwards;
}
.dmg-num.crit { color: #fbbf24; font-size: 32px; text-shadow: 0 0 8px #ef4444; }
.dmg-num.normal { color: #fef3c7; }
.dmg-num.heal { color: #10b981; }
```

```js
function showDamage(targetEl, amount, type='normal') {
  const el = document.createElement('div');
  el.className = `dmg-num ${type}`;
  el.textContent = amount;
  el.style.left = `${30 + Math.random()*40}%`;
  el.style.top = '20%';
  targetEl.appendChild(el);
  setTimeout(() => el.remove(), 900);
}
```

---

## 5. 給 Claude Code 的具體 TODO

按優先順序：

1. ⬜ **加 `image-rendering: pixelated` CSS**（§2.3）— 沒這條什麼都白搭
2. ⬜ 在 `quest.html` 的 `BOSSES`、`WORLD_BOSSES` 物件加 `art:` 欄位（§2.1）
3. ⬜ 修改 boss / class 卡片渲染，用 `<img class="boss-art">` 顯示 PNG（§2.2）
4. ⬜ 加上 `.boss-art.attacking / .hurt / .casting` 動畫 class（§2.4）
5. ⬜ 加上技能元素 → PNG 對應表（§3）
6. ⬜ 加上受傷數字飄出（§4）

完成 1～4 戰鬥畫面就會有質感。5～6 是錦上添花。

---

## 6. 風格規格速查

| 項目         | 尺寸       | 主色                                | 用途                       |
|--------------|------------|--------------------------------------|----------------------------|
| 玩家角色     | 96×96 PNG  | 白底 + 各職業色                      | 角色立繪、頭像             |
| Boss 立繪    | 96×96 PNG  | 各 Boss 主題色                       | 戰鬥畫面主視覺             |
| 世界王       | 96×96 PNG  | 自帶藍/火光環                        | 戰鬥畫面，建議放大 2.5×    |
| 技能圖示     | 64×64 PNG  | 暗底 + 鮮色，圓徽章                  | 技能列表                   |

Anchor 規格（給未來改動用）：
- 畫布 96×96
- 頭中心 ≈ (45, 33)
- 身體中心 ≈ (45, 68)
- 主武器在右翼上方（x=66+, y=30-50）
- 副武器/盾在左翼下方（x=2-30, y=50-70）

---

## 7. 重新生成 / 修改

要改色、調姿勢、加新角色，全都改 `mahjong/art/png/generate_v3_all.py` 一個檔。

```bash
cd mahjong/art/png
python3 generate_v3_all.py
```

每個角色都有自己的 `xxx_v3()` 函式，獨立可改。

---

## 8. 已知限制

- **沒有換裝系統**：V3 每隻角色姿勢都不同，equipment 概念不適用。如果遊戲需要換裝，請改用 V1 版本（`png/modern/`，紙娃娃分層）。
- **單一姿勢**：目前每個角色只有一張立繪（攻擊預備姿）。如果要 idle/attack/hurt 多 frame 動畫，需要為每隻多畫幾張，由你/Claude Code 決定要不要做。
- **方向固定**：所有角色嘴朝右。要左右翻轉用 CSS `transform: scaleX(-1)`。

---

**製作說明**：純 Python+PIL 程式化生成，所有像素都是程式碼定義的，可以無限重新生成。比起 AI 生圖，可控、一致、可程式化。
