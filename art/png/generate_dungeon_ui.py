#!/usr/bin/env python3
"""
5 張地下城探險 UI 美工
深紫金 + 魔幻光效 + Q 版 pixel art

設計尺寸 → 輸出（NEAREST 放大）：
  dungeon-banner.png   240×135  → 1200×675  (16:9 ×5)
  treasure-vault.png   128×128  → 512×512   (1:1 ×4)
  rarity-cards.png     480×96   → 2400×480  (5:1 ×5)
  open-box.png         200×150  → 800×600   (4:3 ×4)
  trade-scene.png      240×135  → 1200×675  (16:9 ×5)

輸出：WEBSITE/assets/dungeon/
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                     '..', '..', '..', 'assets', 'dungeon'))
os.makedirs(OUT, exist_ok=True)


# ---------- helpers ----------
def add_outline(img, color=(20, 0, 40, 255), filter_size=3):
    alpha = img.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(filter_size))
    outline = Image.new('RGBA', img.size, color)
    outline.putalpha(dilated)
    return Image.alpha_composite(outline, img)


def save_scaled(img, name, scale):
    """存原圖（pixel art native）+ 放大版（NEAREST）"""
    target = (img.width * scale, img.height * scale)
    big = img.resize(target, Image.NEAREST)
    big.save(os.path.join(OUT, f'{name}.png'))


# 共用色板
DEEP_PURPLE = [(15, 5, 30), (25, 10, 50), (40, 15, 75), (60, 25, 110), (90, 40, 150)]
PURPLE_GLOW = [(110, 50, 180), (160, 100, 220), (220, 200, 255), (255, 255, 255)]
GOLD = [(80, 40, 5), (140, 90, 20), (200, 150, 40), (255, 200, 60), (255, 240, 140)]
CYAN = [(10, 50, 100), (40, 130, 220), (100, 200, 255), (200, 240, 255)]
GREEN = [(15, 60, 35), (40, 130, 80), (80, 200, 130), (180, 255, 220)]
GRAY = [(40, 40, 50), (90, 90, 110), (150, 150, 170), (200, 200, 220)]
RED = [(80, 5, 15), (180, 35, 35), (255, 100, 100), (255, 200, 200)]


def gradient_bg(img, top_color, bottom_color):
    """垂直漸層背景"""
    d = ImageDraw.Draw(img)
    W, H = img.size
    for y in range(H):
        t = y / H
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))


def magic_particles(d, points, palette=PURPLE_GLOW):
    """畫魔法粒子（小亮點 + 暈光）"""
    for x, y, s in points:
        if s >= 2:
            d.ellipse([x-s, y-s, x+s, y+s], fill=palette[0])
            d.ellipse([x-s+1, y-s+1, x+s-1, y+s-1], fill=palette[1])
        d.point([(x, y)], fill=palette[-1])
        if s >= 1:
            d.point([(x-1, y)], fill=palette[2])
            d.point([(x+1, y)], fill=palette[2])
            d.point([(x, y-1)], fill=palette[2])
            d.point([(x, y+1)], fill=palette[2])


# ====================================================================
# 第 1 張：dungeon-banner（240×135）封面主視覺
# ====================================================================
def make_dungeon_banner():
    img = Image.new('RGBA', (240, 135), (0, 0, 0, 0))
    gradient_bg(img, (15, 5, 30), (40, 15, 75))
    d = ImageDraw.Draw(img)

    # 遠景符文光紋（淡）
    for x in range(20, 220, 40):
        d.line([(x, 50), (x+4, 54), (x, 58), (x-4, 54), (x, 50)], fill=(60, 30, 110, 200), width=1)
    for x in range(35, 220, 40):
        d.ellipse([x-3, 70, x+3, 76], outline=(80, 40, 130, 180), width=1)

    # 中央拱門石塊（左右兩柱 + 拱頂）
    # 左石柱
    d.rectangle([72, 50, 92, 115], fill=(50, 40, 60))
    d.rectangle([74, 52, 90, 113], fill=(85, 70, 95))
    d.rectangle([74, 52, 90, 56], fill=(110, 90, 120))
    # 左柱紋
    for y in [60, 75, 90, 105]:
        d.rectangle([74, y, 90, y+2], fill=(50, 40, 60))
    # 右石柱
    d.rectangle([148, 50, 168, 115], fill=(50, 40, 60))
    d.rectangle([150, 52, 166, 113], fill=(85, 70, 95))
    d.rectangle([150, 52, 166, 56], fill=(110, 90, 120))
    for y in [60, 75, 90, 105]:
        d.rectangle([150, y, 166, y+2], fill=(50, 40, 60))

    # 拱頂石（半圓 + 中央楔石）
    for r in range(40, 30, -2):
        d.arc([80, 30-r//4, 160, 70-r//4], 180, 0, fill=(70, 55, 85), width=2)
    d.arc([80, 26, 160, 72], 180, 0, fill=(60, 45, 75), width=4)
    d.arc([82, 28, 158, 70], 180, 0, fill=(110, 90, 120), width=2)
    # 楔石（中央）
    d.polygon([(116, 26), (124, 26), (128, 38), (112, 38)], fill=(60, 45, 75))
    d.polygon([(118, 28), (122, 28), (126, 36), (114, 36)], fill=(110, 90, 120))
    # 楔石上的符文
    d.point([(120, 32)], fill=(255, 200, 60))
    d.point([(120, 34)], fill=(255, 240, 140))

    # 拱門內陰影（深邃）
    d.polygon([(92, 56), (148, 56), (148, 115), (92, 115)], fill=(8, 0, 20))
    # 拱門內光（從深處透出的紫光）
    for r in range(28, 0, -2):
        a = 60 - r * 2
        if a > 0:
            d.ellipse([120-r, 85-r//2, 120+r, 85+r//2], fill=(60, 30, 110, max(0, a)))
    d.ellipse([116, 80, 124, 92], fill=(110, 50, 180, 150))
    d.ellipse([118, 82, 122, 90], fill=(160, 100, 220))

    # 左紫水晶柱
    d.polygon([(40, 40), (52, 50), (50, 115), (38, 115)], fill=(40, 15, 75))
    d.polygon([(42, 44), (50, 52), (48, 113), (40, 113)], fill=(90, 40, 150))
    d.polygon([(43, 46), (48, 54), (46, 110), (43, 110)], fill=(160, 100, 220))
    d.polygon([(44, 48), (46, 56), (45, 105), (44, 105)], fill=(220, 200, 255))
    # 水晶尖端
    d.polygon([(38, 42), (42, 28), (46, 32), (52, 42)], fill=(40, 15, 75))
    d.polygon([(40, 40), (42, 30), (44, 32), (48, 40)], fill=(90, 40, 150))
    d.polygon([(42, 38), (43, 32), (46, 38)], fill=(160, 100, 220))
    d.point([(44, 34)], fill=(255, 255, 255))
    # 水晶光暈
    for r in range(14, 4, -2):
        a = 50 - r * 2
        d.ellipse([44-r, 50-r, 44+r, 50+r], fill=(160, 100, 220, max(0, a)))

    # 右紫水晶柱（鏡像）
    d.polygon([(200, 40), (188, 50), (190, 115), (202, 115)], fill=(40, 15, 75))
    d.polygon([(198, 44), (190, 52), (192, 113), (200, 113)], fill=(90, 40, 150))
    d.polygon([(197, 46), (192, 54), (194, 110), (197, 110)], fill=(160, 100, 220))
    d.polygon([(196, 48), (194, 56), (195, 105), (196, 105)], fill=(220, 200, 255))
    d.polygon([(202, 42), (198, 28), (194, 32), (188, 42)], fill=(40, 15, 75))
    d.polygon([(200, 40), (198, 30), (196, 32), (192, 40)], fill=(90, 40, 150))
    d.polygon([(198, 38), (197, 32), (194, 38)], fill=(160, 100, 220))
    d.point([(196, 34)], fill=(255, 255, 255))
    for r in range(14, 4, -2):
        a = 50 - r * 2
        d.ellipse([196-r, 50-r, 196+r, 50+r], fill=(160, 100, 220, max(0, a)))

    # 石階（拱門前）
    d.rectangle([72, 113, 168, 119], fill=(50, 40, 60))
    d.rectangle([72, 115, 168, 117], fill=(85, 70, 95))
    d.rectangle([64, 119, 176, 125], fill=(40, 30, 50))
    d.rectangle([64, 121, 176, 123], fill=(75, 60, 85))
    d.rectangle([56, 125, 184, 131], fill=(30, 20, 40))
    d.rectangle([56, 127, 184, 129], fill=(65, 50, 75))

    # === Q 版鵝英雄（站在台階上） ===
    # 影子
    d.ellipse([108, 115, 132, 119], fill=(0, 0, 0, 120))
    # 蹼足（金色靴子）
    d.polygon([(112, 105), (108, 116), (118, 116), (116, 105)], fill=GOLD[1])
    d.polygon([(113, 106), (109, 115), (117, 115), (115, 106)], fill=GOLD[3])
    d.polygon([(124, 105), (122, 116), (132, 116), (128, 105)], fill=GOLD[1])
    d.polygon([(125, 106), (123, 115), (131, 115), (127, 106)], fill=GOLD[3])
    # 身體（白鵝胖 Q 版）
    d.ellipse([104, 78, 136, 108], fill=(220, 220, 235))
    d.ellipse([105, 79, 135, 107], fill=(245, 245, 252))
    d.ellipse([106, 80, 134, 106], fill=(255, 255, 255))
    # 金色胸甲
    d.polygon([(108, 86), (104, 102), (136, 102), (132, 86)], fill=GOLD[0])
    d.polygon([(109, 87), (105, 101), (135, 101), (131, 87)], fill=GOLD[1])
    d.polygon([(110, 88), (107, 100), (133, 100), (130, 88)], fill=GOLD[3])
    d.polygon([(110, 88), (109, 92), (131, 92), (130, 88)], fill=GOLD[4])
    # 胸口寶石
    d.ellipse([117, 92, 123, 98], fill=RED[0])
    d.ellipse([118, 93, 122, 97], fill=RED[1])
    d.point([(120, 94)], fill=RED[3])
    # 翅膀
    d.polygon([(104, 86), (98, 96), (102, 102), (108, 96)], fill=(220, 220, 235))
    d.polygon([(105, 88), (101, 94), (104, 100), (107, 96)], fill=(245, 245, 252))
    d.polygon([(136, 86), (142, 96), (138, 102), (132, 96)], fill=(220, 220, 235))
    d.polygon([(135, 88), (139, 94), (136, 100), (133, 96)], fill=(245, 245, 252))
    # 脖子
    d.polygon([(114, 78), (112, 70), (116, 64), (124, 64), (128, 70), (126, 78)], fill=(245, 245, 252))
    # 頭（大圓 Q 版）
    d.ellipse([108, 50, 132, 72], fill=(220, 220, 235))
    d.ellipse([109, 51, 131, 71], fill=(245, 245, 252))
    d.ellipse([110, 52, 130, 70], fill=(255, 255, 255))
    # 高光
    d.ellipse([112, 54, 118, 60], fill=(255, 255, 255))
    # 嘴喙
    d.polygon([(126, 60), (138, 58), (138, 66), (134, 70), (126, 68)], fill=GOLD[1])
    d.polygon([(127, 61), (136, 59), (136, 65), (132, 68), (127, 67)], fill=GOLD[3])
    # 大眼（Q 版）
    d.ellipse([116, 56, 122, 64], fill=(0, 0, 0))
    d.ellipse([117, 57, 121, 63], fill=(40, 15, 75))
    d.ellipse([118, 58, 120, 60], fill=(255, 255, 255))
    # 笑嘴
    d.line([(126, 67), (130, 68)], fill=(120, 60, 5), width=1)
    # 金頭盔
    d.polygon([(108, 56), (108, 44), (114, 38), (126, 38), (132, 44), (132, 56)], fill=GOLD[0])
    d.polygon([(110, 54), (110, 46), (115, 40), (125, 40), (130, 46), (130, 54)], fill=GOLD[2])
    d.polygon([(110, 50), (110, 46), (115, 40), (125, 40), (130, 46), (130, 50)], fill=GOLD[3])
    # 頭盔頂羽毛（紅）
    d.polygon([(122, 38), (118, 28), (120, 26), (124, 30), (126, 36)], fill=RED[0])
    d.polygon([(121, 36), (118, 30), (120, 28), (124, 32), (125, 35)], fill=RED[1])
    d.polygon([(120, 34), (120, 30), (122, 32)], fill=RED[2])

    # 小劍（右手）
    d.rectangle([136, 88, 140, 96], fill=GOLD[0])
    d.rectangle([137, 89, 139, 95], fill=GOLD[2])
    d.rectangle([134, 86, 142, 88], fill=GOLD[1])
    d.rectangle([135, 86, 141, 87], fill=GOLD[3])
    d.polygon([(138, 86), (138, 64), (140, 60), (138, 60), (136, 64), (136, 86), (138, 86)], fill=(180, 180, 195))
    d.polygon([(138, 86), (138, 66), (139, 62), (138, 62), (137, 66), (137, 86)], fill=(245, 245, 252))
    d.point([(138, 62)], fill=(255, 255, 255))
    d.point([(138, 68)], fill=(255, 255, 255))

    # 飄散魔法光粒
    particles = [
        (20, 30, 1), (220, 28, 1), (15, 80, 1), (225, 75, 1),
        (60, 25, 2), (185, 20, 2), (30, 100, 2), (210, 105, 2),
        (50, 60, 1), (190, 65, 1), (165, 35, 1), (75, 40, 1),
        (10, 60, 1), (230, 50, 1)
    ]
    magic_particles(d, particles)

    # 額外大光點
    for cx, cy in [(180, 35), (60, 90), (220, 90)]:
        for r in range(4, 0, -1):
            a = 40 + r * 30
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 240, 140, min(255, a)))
        d.point([(cx, cy)], fill=(255, 255, 255))

    return img


# ====================================================================
# 第 2 張：treasure-vault（128×128）寶物庫圖示
# ====================================================================
def make_treasure_vault():
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    gradient_bg(img, (25, 10, 50), (40, 15, 75))
    d = ImageDraw.Draw(img)

    # 放射光柱
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x2 = int(64 + 60 * math.cos(rad))
        y2 = int(64 + 60 * math.sin(rad))
        d.line([(64, 64), (x2, y2)], fill=(110, 50, 180, 60), width=1)

    # 中央光暈
    for r in range(50, 10, -4):
        a = max(0, 80 - (50-r)*2)
        d.ellipse([64-r, 64-r, 64+r, 64+r], fill=(255, 200, 60, a // 2))

    # 寶箱底（暗色）
    d.rectangle([30, 78, 98, 110], fill=(50, 30, 10))
    d.rectangle([32, 80, 96, 108], fill=(100, 60, 20))
    d.rectangle([32, 80, 96, 84], fill=(140, 90, 30))
    # 寶箱木紋
    for x in [40, 50, 60, 70, 80, 90]:
        d.line([(x, 84), (x, 108)], fill=(60, 35, 15), width=1)
    # 寶箱金邊條
    d.rectangle([30, 78, 98, 80], fill=GOLD[1])
    d.rectangle([30, 78, 98, 79], fill=GOLD[3])
    d.rectangle([30, 106, 98, 110], fill=GOLD[1])
    d.rectangle([30, 106, 98, 108], fill=GOLD[3])
    d.rectangle([30, 92, 98, 94], fill=GOLD[1])
    # 寶箱鎖（中央）
    d.rectangle([58, 88, 70, 100], fill=GOLD[0])
    d.rectangle([59, 89, 69, 99], fill=GOLD[2])
    d.rectangle([60, 90, 68, 98], fill=GOLD[3])
    d.ellipse([62, 92, 66, 96], fill=GOLD[0])
    d.point([(64, 94)], fill=(20, 0, 30))

    # 寶箱蓋（打開的，向後方）
    d.polygon([(30, 78), (98, 78), (104, 50), (24, 50)], fill=(50, 30, 10))
    d.polygon([(32, 76), (96, 76), (100, 52), (28, 52)], fill=(100, 60, 20))
    d.polygon([(34, 74), (94, 74), (96, 54), (32, 54)], fill=(140, 90, 30))
    # 蓋上金邊
    d.polygon([(30, 78), (98, 78), (104, 50), (24, 50)], outline=GOLD[2], width=1)
    d.line([(24, 50), (104, 50)], fill=GOLD[3], width=1)
    # 蓋內側（漏出來的金光）
    d.polygon([(36, 72), (92, 72), (94, 58), (34, 58)], fill=(255, 200, 60, 200))
    d.polygon([(40, 68), (88, 68), (90, 62), (38, 62)], fill=(255, 240, 140))

    # === 寶物從寶箱湧出 ===
    # 中央最大：金鵝蛋
    d.ellipse([55, 30, 73, 56], fill=GOLD[0])
    d.ellipse([56, 31, 72, 55], fill=GOLD[1])
    d.ellipse([57, 32, 71, 54], fill=GOLD[3])
    d.ellipse([59, 34, 69, 48], fill=GOLD[4])
    d.ellipse([60, 35, 64, 40], fill=(255, 255, 255))
    # 金蛋光暈
    for r in range(20, 8, -2):
        a = max(0, 60 - (20-r)*4)
        d.ellipse([64-r, 42-r, 64+r, 42+r], fill=(255, 240, 140, a))

    # 左上：紫色魔晶
    d.polygon([(30, 32), (38, 26), (44, 34), (40, 48), (32, 50), (26, 42)], fill=DEEP_PURPLE[1])
    d.polygon([(32, 34), (38, 28), (42, 34), (38, 46), (32, 48), (28, 42)], fill=DEEP_PURPLE[4])
    d.polygon([(33, 36), (38, 30), (40, 36), (37, 44), (33, 46), (30, 40)], fill=PURPLE_GLOW[1])
    d.polygon([(34, 38), (37, 32), (38, 38), (36, 42)], fill=PURPLE_GLOW[2])
    d.point([(36, 36)], fill=(255, 255, 255))
    # 魔晶光暈
    for r in range(12, 4, -2):
        a = max(0, 60 - (12-r)*4)
        d.ellipse([35-r, 38-r, 35+r, 38+r], fill=(160, 100, 220, a))

    # 右上：青藍閃電碎片
    d.polygon([(88, 28), (96, 32), (104, 30), (98, 44), (92, 48), (86, 40)], fill=CYAN[0])
    d.polygon([(89, 30), (95, 33), (102, 32), (96, 42), (92, 46), (87, 40)], fill=CYAN[1])
    d.polygon([(90, 32), (94, 34), (100, 34), (95, 40), (91, 44), (89, 40)], fill=CYAN[2])
    d.polygon([(91, 34), (94, 36), (96, 38), (93, 40)], fill=CYAN[3])
    # 閃電紋路
    d.line([(86, 30), (90, 36), (88, 40)], fill=CYAN[3], width=1)
    d.line([(98, 30), (94, 38), (100, 42)], fill=CYAN[3], width=1)
    # 光暈
    for r in range(12, 4, -2):
        a = max(0, 60 - (12-r)*4)
        d.ellipse([93-r, 38-r, 93+r, 38+r], fill=(100, 200, 255, a))

    # 左下：翠綠玉石
    d.polygon([(20, 60), (28, 58), (34, 64), (32, 72), (24, 74), (18, 68)], fill=GREEN[0])
    d.polygon([(22, 62), (28, 60), (32, 64), (30, 72), (24, 72), (20, 68)], fill=GREEN[1])
    d.polygon([(24, 64), (28, 62), (30, 66), (28, 70), (24, 70), (22, 66)], fill=GREEN[2])
    d.point([(26, 65)], fill=GREEN[3])

    # 右下：灰色碎石
    d.polygon([(96, 62), (104, 60), (108, 66), (106, 72), (98, 74), (94, 68)], fill=GRAY[0])
    d.polygon([(98, 64), (104, 62), (106, 66), (104, 72), (98, 72), (96, 68)], fill=GRAY[1])
    d.polygon([(100, 66), (104, 64), (104, 70), (100, 70), (98, 68)], fill=GRAY[2])
    # 碎石裂紋
    d.line([(99, 65), (102, 70)], fill=GRAY[0], width=1)
    d.line([(102, 64), (104, 68)], fill=GRAY[0], width=1)

    # 星星與光芒效果
    stars = [(20, 20, 2), (108, 20, 2), (18, 100, 2), (110, 105, 2),
             (50, 18, 1), (78, 22, 1), (108, 60, 1), (18, 80, 1)]
    for x, y, s in stars:
        d.polygon([(x, y-s-1), (x+s, y-1), (x+s+1, y), (x+s, y+1),
                   (x, y+s+1), (x-s, y+1), (x-s-1, y), (x-s, y-1)],
                  fill=(255, 255, 255))
        d.point([(x, y)], fill=GOLD[3])

    return img


# ====================================================================
# 第 3 張：rarity-cards（480×96）五稀有度橫幅
# ====================================================================
def make_rarity_cards():
    img = Image.new('RGBA', (480, 96), (0, 0, 0, 0))
    gradient_bg(img, (15, 5, 30), (25, 10, 50))
    d = ImageDraw.Draw(img)

    # 每張卡 96×96，左右留 0px 邊距
    cards = [
        # (name_zh, border_color_dark, border_color_light, glow_color, icon_type)
        ('鵝王',   GOLD[0],   GOLD[3],   GOLD[4],         'orb'),
        ('傳說',   DEEP_PURPLE[1], PURPLE_GLOW[1], PURPLE_GLOW[2], 'crystal'),
        ('閃光',   CYAN[0],   CYAN[2],   CYAN[3],         'lightning'),
        ('普通',   GREEN[0],  GREEN[2],  GREEN[3],        'jade'),
        ('極鵝',   GRAY[0],   GRAY[1],   GRAY[2],         'stone'),
    ]

    for i, (name, c_dark, c_light, c_glow, icon) in enumerate(cards):
        x0 = i * 96
        cx = x0 + 48
        cy = 48
        # 卡片陰影背景
        d.rectangle([x0+4, 6, x0+92, 90], fill=(8, 0, 20))
        # 卡片內部漸層深色
        for y in range(8, 90):
            t = (y-8) / 82
            r = int(20 * (1-t) + 8 * t)
            g = int(10 * (1-t) + 4 * t)
            b = int(40 * (1-t) + 20 * t)
            d.line([(x0+6, y), (x0+90, y)], fill=(r, g, b))
        # 卡片邊框（雙層）
        d.rectangle([x0+4, 6, x0+92, 90], outline=c_dark, width=2)
        d.rectangle([x0+6, 8, x0+90, 88], outline=c_light, width=1)
        # 邊框角落裝飾
        for ax, ay in [(x0+8, 10), (x0+88, 10), (x0+8, 86), (x0+88, 86)]:
            d.point([(ax, ay)], fill=c_glow)
        # 邊框光暈
        for ox in range(0, 4):
            d.line([(x0+4-ox, 6+ox), (x0+4-ox, 90-ox)], fill=c_dark + (200-ox*40,))

        # 中央光暈
        for r in range(30, 5, -3):
            a = max(0, 100 - (30-r)*4)
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c_glow + (a // 3,))

        # 圖示
        if icon == 'orb':
            # 琥珀金光環寶珠
            d.ellipse([cx-16, cy-16, cx+16, cy+16], fill=GOLD[0])
            d.ellipse([cx-15, cy-15, cx+15, cy+15], fill=GOLD[1])
            d.ellipse([cx-13, cy-13, cx+13, cy+13], fill=GOLD[3])
            d.ellipse([cx-10, cy-10, cx+8, cy+6], fill=GOLD[4])
            d.ellipse([cx-8, cy-8, cx+2, cy-2], fill=(255, 255, 255))
            # 光環
            d.ellipse([cx-22, cy-22, cx+22, cy+22], outline=GOLD[3], width=1)
            d.ellipse([cx-25, cy-25, cx+25, cy+25], outline=GOLD[2], width=1)
            # 戲劇性閃光
            for ang in [30, 90, 150, 210, 270, 330]:
                rad = math.radians(ang)
                x1 = cx + int(28 * math.cos(rad))
                y1 = cy + int(28 * math.sin(rad))
                x2 = cx + int(34 * math.cos(rad))
                y2 = cy + int(34 * math.sin(rad))
                d.line([(x1, y1), (x2, y2)], fill=GOLD[4], width=1)
                d.point([(x2, y2)], fill=(255, 255, 255))
        elif icon == 'crystal':
            # 旋轉深紫魔晶
            d.polygon([(cx, cy-20), (cx+12, cy-8), (cx+10, cy+10), (cx, cy+18),
                       (cx-10, cy+10), (cx-12, cy-8)], fill=DEEP_PURPLE[1])
            d.polygon([(cx, cy-18), (cx+10, cy-7), (cx+8, cy+8), (cx, cy+16),
                       (cx-8, cy+8), (cx-10, cy-7)], fill=DEEP_PURPLE[4])
            d.polygon([(cx, cy-16), (cx+8, cy-6), (cx+6, cy+6), (cx, cy+14),
                       (cx-6, cy+6), (cx-8, cy-6)], fill=PURPLE_GLOW[1])
            d.polygon([(cx, cy-10), (cx+4, cy-2), (cx, cy+8), (cx-4, cy-2)], fill=PURPLE_GLOW[2])
            d.point([(cx-2, cy-6)], fill=(255, 255, 255))
            # 神秘光暈紋
            d.line([(cx, cy-20), (cx, cy-26)], fill=PURPLE_GLOW[2], width=1)
            d.line([(cx-12, cy-8), (cx-18, cy-12)], fill=PURPLE_GLOW[2], width=1)
            d.line([(cx+12, cy-8), (cx+18, cy-12)], fill=PURPLE_GLOW[2], width=1)
        elif icon == 'lightning':
            # 青藍閃電碎片
            d.polygon([(cx-12, cy-18), (cx+4, cy-10), (cx-2, cy-2), (cx+8, cy+4),
                       (cx-4, cy+18), (cx-6, cy+4), (cx-12, cy)], fill=CYAN[0])
            d.polygon([(cx-10, cy-16), (cx+2, cy-10), (cx-2, cy-2), (cx+6, cy+4),
                       (cx-4, cy+16), (cx-5, cy+4), (cx-10, cy+1)], fill=CYAN[1])
            d.polygon([(cx-8, cy-14), (cx+0, cy-8), (cx-2, cy-2), (cx+4, cy+4),
                       (cx-4, cy+14), (cx-4, cy+4)], fill=CYAN[2])
            d.polygon([(cx-6, cy-12), (cx-2, cy-6), (cx-4, cy-2), (cx+2, cy+2), (cx-2, cy+10), (cx-3, cy+2)], fill=CYAN[3])
            d.point([(cx-4, cy-8)], fill=(255, 255, 255))
            # 電弧（外圍）
            for x1, y1, x2, y2 in [(cx-22, cy-10, cx-26, cy-14), (cx+18, cy-2, cx+24, cy+2),
                                    (cx-20, cy+8, cx-26, cy+12), (cx+20, cy+14, cx+26, cy+10)]:
                d.line([(x1, y1), (x2, y2)], fill=CYAN[3], width=1)
                d.point([(x2, y2)], fill=(255, 255, 255))
        elif icon == 'jade':
            # 翠綠玉石護符（菱形）
            d.polygon([(cx, cy-16), (cx+14, cy), (cx, cy+16), (cx-14, cy)], fill=GREEN[0])
            d.polygon([(cx, cy-14), (cx+12, cy), (cx, cy+14), (cx-12, cy)], fill=GREEN[1])
            d.polygon([(cx, cy-12), (cx+10, cy), (cx, cy+12), (cx-10, cy)], fill=GREEN[2])
            d.polygon([(cx, cy-8), (cx+6, cy), (cx, cy+8), (cx-6, cy)], fill=GREEN[3])
            d.point([(cx-2, cy-4)], fill=(255, 255, 255))
            # 護符鏈（金色細鏈裝飾）
            d.line([(cx-14, cy), (cx-18, cy-4)], fill=GOLD[3], width=1)
            d.line([(cx+14, cy), (cx+18, cy-4)], fill=GOLD[3], width=1)
            d.line([(cx, cy-16), (cx, cy-22)], fill=GOLD[3], width=1)
        elif icon == 'stone':
            # 灰色龜裂石片（黯淡）
            d.polygon([(cx-14, cy-12), (cx+12, cy-10), (cx+14, cy+8), (cx-12, cy+12), (cx-16, cy)], fill=GRAY[0])
            d.polygon([(cx-12, cy-10), (cx+10, cy-8), (cx+12, cy+6), (cx-10, cy+10), (cx-14, cy)], fill=GRAY[1])
            d.polygon([(cx-10, cy-8), (cx+8, cy-6), (cx+10, cy+4), (cx-8, cy+8)], fill=GRAY[2])
            # 龜裂紋
            d.line([(cx-8, cy-4), (cx-2, cy+4)], fill=GRAY[0], width=1)
            d.line([(cx+2, cy-6), (cx+6, cy+2)], fill=GRAY[0], width=1)
            d.line([(cx-2, cy+4), (cx+4, cy+6)], fill=GRAY[0], width=1)
            d.point([(cx-4, cy-2)], fill=GRAY[3])

        # 卡片底部稀有度標籤
        d.rectangle([x0+8, 76, x0+88, 86], fill=c_dark)
        d.rectangle([x0+9, 77, x0+87, 85], fill=c_light)
        # 「鵝王」之類字（用 dot matrix 簡單表示一個橢圓 + 高光）
        d.ellipse([x0+44, 79, x0+52, 83], fill=c_glow)
        d.point([(x0+48, 81)], fill=(255, 255, 255))

        # 卡片頂部「★」級別標記（黃星）
        star_count = [5, 4, 3, 2, 1][i]
        for si in range(star_count):
            sx = x0 + 14 + si * 14
            sy = 18
            d.polygon([(sx, sy-3), (sx+2, sy-1), (sx+3, sy), (sx+2, sy+1),
                       (sx, sy+3), (sx-2, sy+1), (sx-3, sy), (sx-2, sy-1)],
                      fill=GOLD[3])
            d.point([(sx, sy)], fill=(255, 255, 255))

    return img


# ====================================================================
# 第 4 張：open-box（200×150）開箱驚喜場景
# ====================================================================
def make_open_box():
    img = Image.new('RGBA', (200, 150), (0, 0, 0, 0))
    gradient_bg(img, (25, 10, 50), (40, 15, 75))
    d = ImageDraw.Draw(img)

    # 石祭壇（後方）
    d.rectangle([40, 30, 160, 100], fill=(40, 30, 50))
    d.rectangle([42, 32, 158, 98], fill=(70, 55, 80))
    d.rectangle([42, 32, 158, 38], fill=(95, 75, 105))
    # 祭壇紋路
    for x in [55, 80, 120, 145]:
        d.line([(x, 32), (x, 98)], fill=(40, 30, 50), width=1)
    for y in [48, 64, 80]:
        d.line([(42, y), (158, y)], fill=(40, 30, 50), width=1)
    # 祭壇符文
    d.ellipse([95, 65, 105, 75], outline=PURPLE_GLOW[1], width=1)
    d.point([(100, 70)], fill=PURPLE_GLOW[2])

    # 地面
    d.rectangle([0, 100, 200, 150], fill=(20, 10, 40))
    d.rectangle([0, 100, 200, 105], fill=(40, 25, 65))

    # === 5×4 = 20 個禮物盒 ===
    box_w, box_h = 12, 12
    start_x, start_y = 96, 38
    for row in range(4):
        for col in range(5):
            bx = start_x + col * 16
            by = start_y + row * 14
            if row == 1 and col == 2:
                # 這個正在爆開！跳過畫盒（爆炸放後面）
                continue
            # 盒子主體
            color_idx = (row + col) % 3
            box_colors = [
                ((40, 15, 75), (90, 40, 150), (160, 100, 220)),
                ((80, 40, 5), (180, 130, 30), (255, 200, 60)),
                ((10, 50, 100), (40, 130, 220), (100, 200, 255)),
            ][color_idx]
            d.rectangle([bx, by, bx+box_w, by+box_h], fill=box_colors[0])
            d.rectangle([bx+1, by+1, bx+box_w-1, by+box_h-1], fill=box_colors[1])
            d.rectangle([bx+1, by+1, bx+box_w-1, by+4], fill=box_colors[2])
            # 緞帶
            d.rectangle([bx+5, by, bx+7, by+box_h], fill=GOLD[2])
            d.rectangle([bx+5, by, bx+7, by+box_h], outline=GOLD[3], width=1)
            d.rectangle([bx, by+5, bx+box_w, by+7], fill=GOLD[2])
            # 蝴蝶結
            d.polygon([(bx+5, by), (bx+3, by-2), (bx+3, by+2), (bx+5, by+1)], fill=GOLD[2])
            d.polygon([(bx+7, by), (bx+9, by-2), (bx+9, by+2), (bx+7, by+1)], fill=GOLD[2])
            # 微光
            d.point([(bx+3, by+3)], fill=(255, 255, 255, 200))

    # === 爆炸的禮物盒（row=1, col=2，位置約在 128, 52） ===
    bx, by = 128, 52
    # 爆開的盒底
    d.polygon([(bx-4, by+12), (bx, by+8), (bx+12, by+8), (bx+16, by+12), (bx+14, by+14), (bx-2, by+14)],
              fill=GOLD[0])
    d.polygon([(bx-2, by+10), (bx+2, by+9), (bx+10, by+9), (bx+14, by+10), (bx+12, by+13), (bx+0, by+13)],
              fill=GOLD[2])
    # 中心爆炸白光（巨大光球）
    for r in range(30, 5, -3):
        a = max(0, 200 - (30-r)*8)
        d.ellipse([bx+6-r, by+6-r, bx+6+r, by+6+r], fill=(255, 255, 255, a // 3))
    d.ellipse([bx-4, by-4, bx+16, by+16], fill=(255, 240, 140, 220))
    d.ellipse([bx, by, bx+12, by+12], fill=(255, 255, 255))

    # 金色鵝羽毛噴出（多片）
    feathers = [
        (bx-10, by-12, -20), (bx+6, by-18, 5), (bx+22, by-14, 25),
        (bx-16, by-2, -45), (bx+24, by-2, 45),
        (bx-12, by+10, -60), (bx+22, by+12, 60),
    ]
    for fx, fy, ang in feathers:
        rad = math.radians(ang)
        # 羽毛形狀（橢圓 + 尖端）
        d.ellipse([fx-2, fy-4, fx+2, fy+4], fill=GOLD[0])
        d.ellipse([fx-1, fy-3, fx+1, fy+3], fill=GOLD[3])
        d.line([(fx, fy+4), (fx + int(2*math.cos(rad)), fy + 8 + int(2*math.sin(rad)))], fill=GOLD[1], width=1)
        d.point([(fx, fy)], fill=(255, 255, 255))

    # 「✨ 鵝王級！」文字框（在爆炸上方）
    tx, ty = 100, 16
    # 文字框背景
    d.rectangle([tx-2, ty-2, tx+72, ty+14], fill=(40, 15, 75))
    d.rectangle([tx, ty, tx+70, ty+12], fill=GOLD[0])
    d.rectangle([tx+1, ty+1, tx+69, ty+11], fill=GOLD[3])
    d.rectangle([tx+1, ty+1, tx+69, ty+5], fill=GOLD[4])
    # 星星（左）
    sx, sy = tx+8, ty+6
    d.polygon([(sx, sy-3), (sx+2, sy-1), (sx+3, sy), (sx+2, sy+1),
               (sx, sy+3), (sx-2, sy+1), (sx-3, sy), (sx-2, sy-1)],
              fill=(255, 255, 255))
    # 「鵝王級」字塊（簡化為色塊圖案）
    for cx in [tx+18, tx+28, tx+38, tx+48, tx+58]:
        d.rectangle([cx-3, ty+3, cx+3, ty+9], fill=(60, 20, 5))
        d.point([(cx, ty+6)], fill=(255, 240, 140))
    # 「！」
    d.rectangle([tx+64, ty+3, tx+66, ty+8], fill=(255, 255, 255))
    d.rectangle([tx+64, ty+9, tx+66, ty+10], fill=(255, 255, 255))

    # === Q 版角色（左前方） ===
    chx, chy = 28, 90
    # 影子
    d.ellipse([chx-8, chy+22, chx+10, chy+26], fill=(0, 0, 0, 120))
    # 蹼足
    d.polygon([(chx-3, chy+14), (chx-5, chy+22), (chx+1, chy+22), (chx, chy+14)], fill=GOLD[1])
    d.polygon([(chx+3, chy+14), (chx+1, chy+22), (chx+7, chy+22), (chx+6, chy+14)], fill=GOLD[1])
    # 身體（Q 版圓胖）
    d.ellipse([chx-8, chy-2, chx+10, chy+16], fill=(220, 220, 235))
    d.ellipse([chx-7, chy-1, chx+9, chy+15], fill=(245, 245, 252))
    d.ellipse([chx-6, chy, chx+8, chy+14], fill=(255, 255, 255))
    # 紫袍
    d.polygon([(chx-7, chy+2), (chx-9, chy+16), (chx+11, chy+16), (chx+9, chy+2)], fill=DEEP_PURPLE[1])
    d.polygon([(chx-6, chy+3), (chx-8, chy+15), (chx+10, chy+15), (chx+8, chy+3)], fill=DEEP_PURPLE[4])
    # 金腰帶
    d.rectangle([chx-8, chy+10, chx+10, chy+12], fill=GOLD[2])
    d.rectangle([chx-8, chy+10, chx+10, chy+11], fill=GOLD[3])
    # 頭
    d.ellipse([chx-7, chy-16, chx+9, chy], fill=(220, 220, 235))
    d.ellipse([chx-6, chy-15, chx+8, chy-1], fill=(245, 245, 252))
    d.ellipse([chx-5, chy-14, chx+7, chy-2], fill=(255, 255, 255))
    # 嘴喙
    d.polygon([(chx+5, chy-8), (chx+11, chy-9), (chx+11, chy-4), (chx+5, chy-5)], fill=GOLD[2])
    d.polygon([(chx+5, chy-7), (chx+10, chy-8), (chx+10, chy-5), (chx+5, chy-6)], fill=GOLD[3])
    # 興奮大眼（睜大發亮）
    d.ellipse([chx-3, chy-12, chx+1, chy-6], fill=(0, 0, 0))
    d.ellipse([chx-2, chy-11, chx, chy-7], fill=(255, 240, 140))
    d.ellipse([chx-2, chy-11, chx-1, chy-9], fill=(255, 255, 255))
    # 眼角閃光
    d.point([(chx-3, chy-12)], fill=(255, 255, 255))
    # 興奮的嘴（張開的笑）
    d.ellipse([chx+5, chy-5, chx+9, chy-3], fill=(120, 60, 5))
    d.line([(chx+5, chy-4), (chx+9, chy-4)], fill=(255, 100, 100), width=1)

    # === 周圍小愛心 ===
    hearts = [(20, 50), (60, 30), (180, 70), (170, 130), (15, 110)]
    for hx, hy in hearts:
        # 心形 = 兩個圓 + 三角
        d.ellipse([hx-2, hy-1, hx, hy+1], fill=RED[1])
        d.ellipse([hx, hy-1, hx+2, hy+1], fill=RED[1])
        d.polygon([(hx-2, hy+1), (hx+2, hy+1), (hx, hy+3)], fill=RED[1])
        d.point([(hx-1, hy)], fill=RED[2])

    # === 星星 ===
    stars = [(50, 18, 2), (170, 18, 2), (160, 110, 1), (40, 130, 1),
             (80, 8, 1), (160, 35, 1), (50, 80, 1), (155, 90, 1)]
    for x, y, s in stars:
        d.polygon([(x, y-s-1), (x+s, y-1), (x+s+1, y), (x+s, y+1),
                   (x, y+s+1), (x-s, y+1), (x-s-1, y), (x-s, y-1)],
                  fill=GOLD[3])
        d.point([(x, y)], fill=(255, 255, 255))

    return img


# ====================================================================
# 第 5 張：trade-scene（240×135）玩家交易場景
# ====================================================================
def make_trade_scene():
    img = Image.new('RGBA', (240, 135), (0, 0, 0, 0))
    gradient_bg(img, (40, 20, 60), (60, 30, 80))
    d = ImageDraw.Draw(img)

    # 石壁走廊（後牆 + 兩側牆）
    # 後牆
    d.rectangle([20, 30, 220, 115], fill=(50, 35, 60))
    d.rectangle([22, 32, 218, 113], fill=(75, 55, 85))
    # 後牆磚紋
    for y in [50, 70, 90]:
        d.line([(22, y), (218, y)], fill=(50, 35, 60), width=1)
    for row, y_start in enumerate([32, 50, 70, 90]):
        offset = 0 if row % 2 == 0 else 12
        for x in range(22 + offset, 218, 24):
            d.line([(x, y_start), (x, y_start+18)], fill=(50, 35, 60), width=1)

    # 兩側壁柱（深色）
    d.rectangle([0, 0, 22, 135], fill=(25, 10, 40))
    d.rectangle([218, 0, 240, 135], fill=(25, 10, 40))
    d.rectangle([2, 2, 20, 133], fill=(45, 25, 65))
    d.rectangle([220, 2, 238, 133], fill=(45, 25, 65))

    # 走廊頂（拱形）
    for x in range(20, 220, 2):
        t = abs(x - 120) / 100
        h = int(30 - 15 * (1 - t * t))
        d.line([(x, 0), (x, h)], fill=(20, 5, 35))
    d.arc([20, 0, 220, 50], 180, 0, fill=GOLD[1], width=1)

    # 地板
    d.rectangle([0, 115, 240, 135], fill=(35, 20, 55))
    d.rectangle([0, 115, 240, 117], fill=GOLD[1])
    d.rectangle([0, 117, 240, 119], fill=(55, 40, 75))
    # 地磚紋
    for x in [50, 100, 150, 200]:
        d.line([(x, 119), (x, 135)], fill=(20, 10, 35), width=1)

    # 暖色金紫氛圍光（從中央漫出）
    for r in range(70, 20, -5):
        a = max(0, 50 - (70-r)*2)
        d.ellipse([120-r, 80-r//2, 120+r, 80+r//2], fill=GOLD[3] + (a // 3,))

    # === 左角色（Q 版） ===
    lx, ly = 78, 95
    # 影子
    d.ellipse([lx-10, ly+22, lx+10, ly+26], fill=(0, 0, 0, 120))
    # 蹼足
    d.polygon([(lx-4, ly+14), (lx-6, ly+22), (lx, ly+22), (lx-1, ly+14)], fill=GOLD[1])
    d.polygon([(lx+2, ly+14), (lx+1, ly+22), (lx+7, ly+22), (lx+6, ly+14)], fill=GOLD[1])
    # 身體
    d.ellipse([lx-9, ly-2, lx+11, ly+16], fill=(220, 220, 235))
    d.ellipse([lx-8, ly-1, lx+10, ly+15], fill=(245, 245, 252))
    d.ellipse([lx-7, ly, lx+9, ly+14], fill=(255, 255, 255))
    # 紫袍
    d.polygon([(lx-8, ly+3), (lx-10, ly+16), (lx+12, ly+16), (lx+10, ly+3)], fill=DEEP_PURPLE[1])
    d.polygon([(lx-7, ly+4), (lx-9, ly+15), (lx+11, ly+15), (lx+9, ly+4)], fill=DEEP_PURPLE[3])
    # 頭
    d.ellipse([lx-8, ly-16, lx+10, ly], fill=(220, 220, 235))
    d.ellipse([lx-7, ly-15, lx+9, ly-1], fill=(245, 245, 252))
    d.ellipse([lx-6, ly-14, lx+8, ly-2], fill=(255, 255, 255))
    # 嘴喙
    d.polygon([(lx+6, ly-8), (lx+12, ly-9), (lx+12, ly-4), (lx+6, ly-5)], fill=GOLD[2])
    d.polygon([(lx+6, ly-7), (lx+11, ly-8), (lx+11, ly-5), (lx+6, ly-6)], fill=GOLD[3])
    # 大眼
    d.ellipse([lx-3, ly-12, lx+1, ly-6], fill=(0, 0, 0))
    d.ellipse([lx-2, ly-11, lx, ly-7], fill=(40, 15, 75))
    d.point([(lx-2, ly-11)], fill=(255, 255, 255))
    # 微笑
    d.line([(lx+6, ly-4), (lx+9, ly-3)], fill=(120, 60, 5), width=1)
    # 紫晶在右手（伸到中央）
    crx, cry = lx + 22, ly + 6
    d.polygon([(crx, cry-8), (crx+5, cry-2), (crx+4, cry+6), (crx, cry+10),
               (crx-4, cry+6), (crx-5, cry-2)], fill=DEEP_PURPLE[1])
    d.polygon([(crx, cry-6), (crx+4, cry-2), (crx+3, cry+5), (crx, cry+9),
               (crx-3, cry+5), (crx-4, cry-2)], fill=PURPLE_GLOW[1])
    d.polygon([(crx, cry-4), (crx+3, cry-1), (crx+2, cry+4), (crx, cry+7),
               (crx-2, cry+4), (crx-3, cry-1)], fill=PURPLE_GLOW[2])
    d.point([(crx-1, cry-2)], fill=(255, 255, 255))
    # 紫晶光暈
    for r in range(12, 4, -2):
        a = max(0, 60 - (12-r)*4)
        d.ellipse([crx-r, cry-r, crx+r, cry+r], fill=(160, 100, 220, a))

    # === 右角色（Q 版，鏡像） ===
    rx, ry = 162, 95
    d.ellipse([rx-10, ry+22, rx+10, ry+26], fill=(0, 0, 0, 120))
    d.polygon([(rx-4, ry+14), (rx-6, ry+22), (rx, ry+22), (rx-1, ry+14)], fill=GOLD[1])
    d.polygon([(rx+2, ry+14), (rx+1, ry+22), (rx+7, ry+22), (rx+6, ry+14)], fill=GOLD[1])
    # 身體
    d.ellipse([rx-11, ry-2, rx+9, ry+16], fill=(220, 220, 235))
    d.ellipse([rx-10, ry-1, rx+8, ry+15], fill=(245, 245, 252))
    d.ellipse([rx-9, ry, rx+7, ry+14], fill=(255, 255, 255))
    # 綠袍（換個顏色與左邊角色區隔）
    d.polygon([(rx-10, ry+3), (rx-12, ry+16), (rx+10, ry+16), (rx+8, ry+3)], fill=GREEN[0])
    d.polygon([(rx-9, ry+4), (rx-11, ry+15), (rx+9, ry+15), (rx+7, ry+4)], fill=GREEN[1])
    # 頭
    d.ellipse([rx-10, ry-16, rx+8, ry], fill=(220, 220, 235))
    d.ellipse([rx-9, ry-15, rx+7, ry-1], fill=(245, 245, 252))
    d.ellipse([rx-8, ry-14, rx+6, ry-2], fill=(255, 255, 255))
    # 嘴喙（朝左）
    d.polygon([(rx-6, ry-8), (rx-12, ry-9), (rx-12, ry-4), (rx-6, ry-5)], fill=GOLD[2])
    d.polygon([(rx-6, ry-7), (rx-11, ry-8), (rx-11, ry-5), (rx-6, ry-6)], fill=GOLD[3])
    # 大眼（朝左）
    d.ellipse([rx-1, ry-12, rx+3, ry-6], fill=(0, 0, 0))
    d.ellipse([rx, ry-11, rx+2, ry-7], fill=(15, 60, 35))
    d.point([(rx, ry-11)], fill=(255, 255, 255))
    # 微笑
    d.line([(rx-6, ry-4), (rx-9, ry-3)], fill=(120, 60, 5), width=1)
    # 金鵝羽護符在左手（伸到中央）
    ffx, ffy = rx - 22, ry + 6
    # 羽毛形狀
    d.ellipse([ffx-3, ffy-8, ffx+3, ffy+8], fill=GOLD[0])
    d.ellipse([ffx-2, ffy-7, ffx+2, ffy+7], fill=GOLD[2])
    d.ellipse([ffx-1, ffy-6, ffx+1, ffy+6], fill=GOLD[3])
    d.line([(ffx, ffy-8), (ffx, ffy+8)], fill=GOLD[1], width=1)
    # 羽毛紋
    for ly_local in [-5, -2, 1, 4]:
        d.line([(ffx-2, ffy+ly_local), (ffx+2, ffy+ly_local)], fill=GOLD[1], width=1)
    # 羽毛底部金鏈
    d.line([(ffx, ffy-10), (ffx-2, ffy-12), (ffx+2, ffy-12)], fill=GOLD[2], width=1)
    d.point([(ffx, ffy-12)], fill=(255, 255, 255))
    # 護符光暈
    for r in range(12, 4, -2):
        a = max(0, 60 - (12-r)*4)
        d.ellipse([ffx-r, ffy-r, ffx+r, ffy+r], fill=GOLD[3] + (a,))

    # === 中央交換閃光特效 ===
    mid_x, mid_y = 120, 100
    # 中央大光球（混合紫金）
    for r in range(18, 4, -3):
        a = max(0, 120 - (18-r)*8)
        d.ellipse([mid_x-r, mid_y-r//2, mid_x+r, mid_y+r//2], fill=(255, 240, 140, a // 2))
    d.ellipse([mid_x-6, mid_y-3, mid_x+6, mid_y+3], fill=(255, 255, 255))
    # 交換閃光「><」線
    for ang in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(ang)
        x1 = mid_x + int(8 * math.cos(rad))
        y1 = mid_y + int(4 * math.sin(rad))
        x2 = mid_x + int(18 * math.cos(rad))
        y2 = mid_y + int(8 * math.sin(rad))
        d.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 200), width=1)
        d.point([(x2, y2)], fill=GOLD[4])

    # 中央愛心
    for hx, hy in [(120, 80)]:
        d.ellipse([hx-4, hy-2, hx, hy+2], fill=RED[1])
        d.ellipse([hx, hy-2, hx+4, hy+2], fill=RED[1])
        d.polygon([(hx-4, hy+2), (hx+4, hy+2), (hx, hy+6)], fill=RED[1])
        d.point([(hx-2, hy)], fill=RED[3])

    # 飄散的愛心、星星
    extras = [(40, 30, 'star'), (200, 30, 'star'), (60, 50, 'heart'),
              (180, 60, 'heart'), (110, 30, 'star'), (130, 35, 'heart'),
              (100, 60, 'star'), (140, 70, 'star')]
    for x, y, t in extras:
        if t == 'star':
            d.polygon([(x, y-2), (x+1, y-1), (x+2, y), (x+1, y+1),
                       (x, y+2), (x-1, y+1), (x-2, y), (x-1, y-1)],
                      fill=GOLD[3])
            d.point([(x, y)], fill=(255, 255, 255))
        else:
            d.ellipse([x-2, y-1, x, y+1], fill=RED[1])
            d.ellipse([x, y-1, x+2, y+1], fill=RED[1])
            d.polygon([(x-2, y+1), (x+2, y+1), (x, y+3)], fill=RED[1])

    # 走廊深處光點（製造透視感）
    for cx, cy in [(70, 60), (170, 60), (40, 100), (200, 100)]:
        d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=GOLD[3] + (180,))
        d.point([(cx, cy)], fill=(255, 255, 255))

    return img


# ====================================================================
# Main
# ====================================================================

if __name__ == '__main__':
    import sys
    log = sys.stderr

    save_scaled(make_dungeon_banner(),   'dungeon-banner', 5)
    log.write('  dungeon-banner (1200x675)\n')

    save_scaled(make_treasure_vault(),   'treasure-vault', 4)
    log.write('  treasure-vault (512x512)\n')

    save_scaled(make_rarity_cards(),     'rarity-cards', 5)
    log.write('  rarity-cards (2400x480)\n')

    save_scaled(make_open_box(),         'open-box', 4)
    log.write('  open-box (800x600)\n')

    save_scaled(make_trade_scene(),      'trade-scene', 5)
    log.write('  trade-scene (1200x675)\n')

    log.write('\nALL DUNGEON UI DONE\n')
