# 職業立繪 (Swan Class Portraits)

4 隻天鵝紙娃娃，SVG 向量檔（檔案小、可放大、可疊裝備）。

## 檔案

- `warrior.svg` — 戰士鵝（紅頭巾 + 鐵胸甲 + 兇眼眉）
- `archer.svg`  — 弓手鵝（綠斗篷帽 + 葉子飾 + 短袍）
- `mage.svg`    — 法師鵝（紫袍 + 巫師星星帽 + 紫色光暈）
- `paladin.svg` — 聖騎鵝（紅披風 + 金十字胸甲 + 頭頂光環）

## 共通設計（所有 4 隻天鵝）

- viewBox: `0 0 200 250`
- 白羽毛 + 橘嘴 + 蹼足
- 頭頂呆毛、雙頰腮紅、害羞下垂眉、害羞小嘴
- 翅膀末端對齊 `(50,160)` 與 `(150,160)`，跟 `assets/equipment/*.svg` 自動疊合

## 怎麼疊裝備

```html
<div class="paper-doll">
  <img src="assets/equipment/armor-glow.svg"/>  <!-- 最底，盔甲光暈 -->
  <img src="assets/classes/warrior.svg"/>        <!-- 角色底圖 -->
  <img src="assets/equipment/shield.svg"/>       <!-- 盾 -->
  <img src="assets/equipment/sword.svg"/>        <!-- 武器 -->
  <img src="assets/equipment/crown.svg"/>        <!-- 飾品在最上 -->
</div>

<style>
.paper-doll { position: relative; width: 200px; height: 250px; }
.paper-doll img { position: absolute; inset: 0; width: 100%; height: 100%; }
</style>
```

`quest.html` 已串好 — 只要 `image: 'assets/classes/{klass}.svg'` 路徑對，就會載到。
