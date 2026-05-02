# mahjong/assets — 鵝鵝紙娃娃素材

```
assets/
├── classes/                 4 隻職業天鵝（角色底圖）
│   ├── warrior.svg          戰士鵝
│   ├── archer.svg           弓手鵝
│   ├── mage.svg             法師鵝
│   ├── paladin.svg          聖騎鵝
│   └── README.md
├── equipment/               9 件裝備（疊在角色上）
│   ├── sword.svg            鐵劍       武器位 (右手, x=150)
│   ├── holy-sword.svg       聖劍       武器位 (右手)
│   ├── bow.svg              長弓       武器位 (左手, x=50)
│   ├── staff.svg            法杖       武器位 (右手)
│   ├── shield.svg           圓盾       盾位 (左手)
│   ├── helmet.svg           頭盔       頭部
│   ├── crown.svg            皇冠       頭頂飾品
│   ├── wing-amulet.svg      翼護符     頭頂飾品
│   └── armor-glow.svg       盔甲光暈   全身底層光環
└── preview.html             互動式預覽（直接打開看效果）
```

## 規格

- 全部 SVG，viewBox `0 0 200 250`
- 角色與裝備座標已對齊：翅膀末端在 `(50,160)` / `(150,160)`，飾品錨點在 `(100,18)`
- 換句話說：把任何 base + 任意裝備疊在同一容器（絕對定位），就能拼出紙娃娃，不用調位置

## 串好的地方

`quest.html` 中 `CLASSES` 物件的 `image` 欄位已指向 `assets/classes/{klass}.svg`，重整就會看到。
