#!/usr/bin/env python3
"""
Hisiri Mahjong — Modern Pixel Art Generator (Paper-Doll System)

紙娃娃分層架構：
  base/      底身（白鵝、暗鵝）
  layers/
    head/    帽子/頭巾/光環/角
    body/    胸甲/西裝/圍裙/法袍
    hand_l/  左手物件（盾/弓/便當盒/平底鍋/酒杯）
    hand_r/  右手物件（劍/法杖/廚刀/麵碗）
    fx/      氣場/翅膀/火焰/紅眼等特效層
  classes/   合成好的玩家角色（base + 對應裝備）
  bosses/    合成好的 Boss
  skills/    技能 icon（單張）

Anchor 規格（所有層都對齊這些座標）：
  畫布:        96×96
  頭中心:      (48, 33)
  身體中心:    (48, 66)
  左手 / 翼端: (~22, 72)
  右手 / 翼端: (~74, 72)
  腳:         (40, 86) (56, 86)

執行：python3 generate_pixel_art.py
"""

import os
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(__file__), 'modern')
DIRS = {
    'base':       os.path.join(ROOT, 'base'),
    'head':       os.path.join(ROOT, 'layers', 'head'),
    'body':       os.path.join(ROOT, 'layers', 'body'),
    'hand_l':     os.path.join(ROOT, 'layers', 'hand_l'),
    'hand_r':     os.path.join(ROOT, 'layers', 'hand_r'),
    'fx':         os.path.join(ROOT, 'layers', 'fx'),
    'classes':    os.path.join(ROOT, 'classes'),
    'bosses':     os.path.join(ROOT, 'bosses'),
    'skills':     os.path.join(ROOT, 'skills'),
}
for p in DIRS.values():
    os.makedirs(p, exist_ok=True)

W, H = 96, 96   # 畫布
SCALE = 4       # 預覽放大倍率


# ---------- helpers ----------
def new_layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def compose(layers):
    """alpha 疊加多層"""
    out = new_layer()
    for L in layers:
        out = Image.alpha_composite(out, L)
    return out


def save(img, category, name):
    """同時存 native (96×96) 與 _x4 預覽 (384×384)"""
    path = os.path.join(DIRS[category], f'{name}.png')
    img.save(path)
    big = img.resize((W * SCALE, H * SCALE), Image.NEAREST)
    big.save(os.path.join(DIRS[category], f'{name}_x4.png'))


# ====================================================================
# BASE BODIES — 底身天鵝（無任何裝備）
# ====================================================================

def base_swan(palette='white'):
    """白鵝底身。palette='white' 普通；'dark' 暗灰（給宵夜鵝、龍鵝用）"""
    if palette == 'white':
        c1, c2, c3, hl = (220, 220, 228), (240, 240, 245), (252, 252, 255), (255, 255, 255)
        eye_c = (20, 20, 25)
        beak_c1, beak_c2 = (255, 165, 50), (255, 195, 80)
        beak_shadow = (180, 100, 20)
    elif palette == 'dark':
        c1, c2, c3, hl = (60, 60, 75), (95, 95, 110), (125, 125, 140), (160, 160, 175)
        eye_c = (200, 30, 30)
        beak_c1, beak_c2 = (130, 75, 20), (170, 110, 40)
        beak_shadow = (60, 30, 10)
    else:  # green dragon body
        c1, c2, c3, hl = (10, 50, 35), (15, 85, 55), (25, 130, 90), (60, 180, 130)
        eye_c = (255, 220, 60)
        beak_c1, beak_c2 = (255, 165, 50), (255, 195, 80)
        beak_shadow = (180, 100, 20)

    img = new_layer()
    d = ImageDraw.Draw(img)

    # 影子
    d.ellipse([18, 86, 78, 92], fill=(0, 0, 0, 80))

    # 蹼足
    d.polygon([(36, 76), (32, 86), (44, 86), (40, 76)], fill=beak_c1)
    d.polygon([(56, 76), (52, 86), (64, 86), (60, 76)], fill=beak_c1)
    d.polygon([(40, 80), (40, 86), (44, 86), (44, 80)], fill=beak_shadow)
    d.polygon([(52, 80), (52, 86), (56, 86), (56, 80)], fill=beak_shadow)

    # 身體（蛋形 3 層陰影）
    d.ellipse([26, 54, 70, 80], fill=c1)
    d.ellipse([28, 56, 68, 78], fill=c2)
    d.ellipse([30, 58, 66, 76], fill=c3)
    d.ellipse([34, 60, 44, 66], fill=hl)

    # 翅膀
    d.polygon([(28, 60), (18, 72), (26, 78), (32, 72)], fill=c1)
    d.polygon([(68, 60), (78, 72), (70, 78), (64, 72)], fill=c1)
    d.line([(24, 65), (28, 70)], fill=c2, width=1)
    d.line([(72, 65), (68, 70)], fill=c2, width=1)

    # 脖子（S 型曲線分兩層）
    d.polygon([(42, 54), (38, 42), (44, 34), (52, 34), (54, 42), (50, 54)], fill=c2)
    d.polygon([(43, 52), (40, 42), (45, 36), (51, 36), (53, 42), (49, 52)], fill=c3)

    # 頭
    d.ellipse([36, 22, 60, 44], fill=c2)
    d.ellipse([37, 23, 59, 43], fill=c3)
    d.ellipse([39, 25, 47, 30], fill=hl)  # 高光

    # 嘴喙
    d.polygon([(58, 32), (70, 31), (70, 38), (58, 38)], fill=beak_c1)
    d.polygon([(58, 33), (68, 32), (68, 37), (58, 37)], fill=beak_c2)
    d.line([(58, 35), (68, 35)], fill=beak_shadow, width=1)

    # 眼睛
    d.ellipse([52, 30, 56, 34], fill=eye_c)
    d.point([(54, 31)], fill=(255, 255, 255))

    return img


# ====================================================================
# HEAD LAYERS — 帽子 / 頭巾 / 光環 / 角（畫在頭部 y=14-30 區）
# ====================================================================

def head_red_headband():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.rectangle([34, 22, 58, 28], fill=(180, 35, 35))
    d.rectangle([34, 22, 58, 24], fill=(220, 60, 60))
    d.line([(34, 28), (32, 32)], fill=(180, 35, 35), width=2)
    d.line([(36, 30), (34, 34)], fill=(140, 25, 25), width=1)
    # 呆毛
    d.line([(46, 22), (45, 18)], fill=(252, 252, 255), width=1)
    d.line([(47, 22), (47, 17)], fill=(252, 252, 255), width=1)
    return img


def head_archer_hood():
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 綠色兜帽
    d.polygon([(36, 26), (34, 18), (40, 12), (50, 10), (58, 14), (60, 24)],
              fill=(34, 100, 60))
    d.polygon([(38, 24), (37, 18), (42, 14), (50, 12), (56, 16), (58, 22)],
              fill=(60, 140, 90))
    # 邊緣
    d.line([(36, 26), (60, 24)], fill=(20, 70, 40), width=1)
    # 棕邊
    d.line([(40, 12), (50, 10)], fill=(110, 70, 30), width=1)
    return img


def head_paladin_halo():
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 金色光環
    d.ellipse([34, 12, 62, 22], outline=(255, 215, 60), width=2)
    d.ellipse([36, 13, 60, 21], outline=(255, 240, 140), width=1)
    # 中心十字裝飾在前額
    d.rectangle([46, 26, 50, 32], fill=(255, 215, 60))
    d.rectangle([44, 28, 52, 30], fill=(255, 215, 60))
    d.point([(48, 29)], fill=(255, 255, 220))
    return img


def head_star_hat():
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 紫色巫師帽（尖塔）
    d.polygon([(34, 22), (50, 4), (60, 22)], fill=(60, 30, 110))
    d.polygon([(36, 22), (50, 8), (58, 22)], fill=(110, 60, 180))
    # 帽簷
    d.rectangle([30, 22, 64, 26], fill=(40, 20, 80))
    d.rectangle([30, 22, 64, 24], fill=(80, 40, 140))
    # 星星
    d.point([(48, 14)], fill=(255, 240, 80))
    d.point([(47, 13)], fill=(255, 240, 80))
    d.point([(49, 13)], fill=(255, 240, 80))
    d.point([(48, 12)], fill=(255, 255, 255))
    d.point([(48, 16)], fill=(255, 240, 80))
    # 月牙裝飾
    d.point([(54, 18)], fill=(220, 220, 240))
    return img


def head_chef_hat():
    """早餐鵝廚師帽（高蓬鬆）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.ellipse([30, 18, 66, 24], fill=(255, 255, 255))
    d.polygon([(34, 22), (32, 6), (40, 4), (48, 8), (56, 4), (64, 6), (62, 22)],
              fill=(255, 255, 255))
    d.polygon([(36, 18), (38, 8), (44, 6), (52, 8), (58, 8), (60, 18)],
              fill=(245, 245, 250))
    d.line([(40, 10), (42, 18)], fill=(220, 220, 225), width=1)
    d.line([(48, 8), (48, 18)], fill=(220, 220, 225), width=1)
    d.line([(56, 10), (54, 18)], fill=(220, 220, 225), width=1)
    return img


def head_chef_hat_french():
    """晚餐鵝法式廚師帽（矮）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.ellipse([32, 18, 64, 24], fill=(255, 255, 255))
    d.polygon([(34, 22), (36, 12), (48, 10), (60, 12), (62, 22)],
              fill=(245, 245, 250))
    # 金邊
    d.rectangle([34, 20, 62, 23], fill=(255, 200, 60))
    d.rectangle([34, 20, 62, 21], fill=(255, 240, 140))
    return img


def head_pajama_hair():
    """宵夜鵝亂翹頭髮"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 灰白翹毛
    d.polygon([(38, 24), (36, 14), (40, 12), (42, 22)], fill=(95, 95, 110))
    d.polygon([(46, 24), (44, 8), (48, 6), (50, 22)], fill=(125, 125, 140))
    d.polygon([(54, 24), (56, 12), (58, 14), (56, 22)], fill=(95, 95, 110))
    return img


def head_crown():
    """皇冠（鵝皇）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 冠基底
    d.rectangle([32, 20, 64, 26], fill=(255, 200, 60))
    d.rectangle([32, 20, 64, 22], fill=(255, 240, 140))
    # 冠尖
    d.polygon([(34, 20), (36, 8), (40, 18)], fill=(255, 200, 60))
    d.polygon([(40, 20), (44, 6), (48, 18)], fill=(255, 215, 80))
    d.polygon([(46, 20), (48, 2), (52, 2), (54, 20)], fill=(255, 220, 80))
    d.polygon([(52, 20), (54, 6), (58, 18)], fill=(255, 215, 80))
    d.polygon([(58, 20), (60, 8), (64, 18)], fill=(255, 200, 60))
    # 中央寶石
    d.ellipse([47, 6, 53, 12], fill=(220, 30, 50))
    d.point([(49, 8)], fill=(255, 200, 200))
    # 兩側藍寶石
    d.point([(43, 12)], fill=(50, 130, 240))
    d.point([(53, 12)], fill=(50, 130, 240))
    return img


def head_dragon_horns():
    """龍角（古龍鵝）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 左角
    d.polygon([(36, 26), (32, 14), (38, 8), (40, 22)], fill=(60, 30, 10))
    d.polygon([(37, 25), (34, 16), (38, 12), (39, 22)], fill=(140, 80, 30))
    # 右角
    d.polygon([(56, 22), (58, 8), (64, 14), (60, 26)], fill=(60, 30, 10))
    d.polygon([(57, 22), (58, 12), (62, 16), (59, 25)], fill=(140, 80, 30))
    return img


# ====================================================================
# BODY LAYERS — 身體裝備（畫在身體 y=58-78 區）
# ====================================================================

def body_warrior_chest():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.rectangle([34, 60, 62, 76], fill=(110, 110, 125))
    d.rectangle([35, 61, 61, 75], fill=(140, 140, 155))
    d.line([(48, 60), (48, 76)], fill=(70, 70, 85), width=1)
    for cx in [38, 58]:
        d.ellipse([cx-1, 64, cx+1, 66], fill=(60, 60, 70))
    return img


def body_archer_vest():
    """皮甲 + 箭袋"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主皮甲
    d.polygon([(32, 60), (64, 60), (66, 78), (30, 78)], fill=(110, 70, 30))
    d.polygon([(34, 62), (62, 62), (64, 76), (32, 76)], fill=(150, 100, 50))
    # 綠色腰帶
    d.rectangle([30, 70, 66, 73], fill=(34, 100, 60))
    d.rectangle([46, 70, 50, 73], fill=(255, 200, 60))  # 金扣
    # 縫線
    d.line([(48, 62), (48, 70)], fill=(80, 50, 20), width=1)
    return img


def body_paladin_armor():
    """白金聖騎士胸甲"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 白甲
    d.rectangle([32, 60, 64, 78], fill=(220, 220, 230))
    d.rectangle([34, 62, 62, 76], fill=(245, 245, 252))
    # 金邊
    d.rectangle([32, 60, 64, 62], fill=(255, 200, 60))
    d.rectangle([32, 76, 64, 78], fill=(255, 200, 60))
    # 中央十字
    d.rectangle([46, 64, 50, 74], fill=(255, 200, 60))
    d.rectangle([42, 67, 54, 71], fill=(255, 200, 60))
    d.rectangle([47, 65, 49, 73], fill=(255, 240, 140))
    return img


def body_mage_robe():
    """紫色長袍"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主袍
    d.polygon([(28, 58), (68, 58), (72, 80), (24, 80)], fill=(60, 30, 110))
    d.polygon([(30, 60), (66, 60), (70, 78), (26, 78)], fill=(110, 60, 180))
    # 金邊
    d.line([(28, 58), (68, 58)], fill=(255, 200, 60), width=1)
    d.line([(28, 78), (68, 78)], fill=(255, 200, 60), width=1)
    # 符文
    d.point([(40, 70)], fill=(255, 240, 80))
    d.point([(48, 68)], fill=(255, 240, 80))
    d.point([(56, 70)], fill=(255, 240, 80))
    d.point([(44, 74)], fill=(255, 240, 80))
    d.point([(52, 74)], fill=(255, 240, 80))
    return img


def body_chef_apron():
    """早餐鵝橙圍裙 + 煎蛋"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.polygon([(30, 60), (66, 60), (70, 80), (26, 80)], fill=(255, 145, 30))
    d.polygon([(32, 62), (64, 62), (68, 78), (28, 78)], fill=(255, 175, 60))
    d.line([(34, 60), (32, 50)], fill=(180, 90, 20), width=1)
    d.line([(62, 60), (64, 50)], fill=(180, 90, 20), width=1)
    d.rectangle([26, 70, 70, 73], fill=(255, 200, 80))
    d.rectangle([45, 70, 51, 73], fill=(140, 70, 15))
    # 煎蛋
    d.ellipse([40, 64, 56, 70], fill=(255, 252, 240))
    d.ellipse([44, 65, 52, 69], fill=(255, 200, 60))
    d.point([(46, 66)], fill=(255, 240, 180))
    return img


def body_business_suit():
    """午餐鵝深藍西裝 + 領帶"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 西裝外套
    d.polygon([(28, 58), (40, 56), (48, 64), (56, 56), (68, 58), (70, 80), (26, 80)],
              fill=(20, 30, 75))
    d.polygon([(30, 60), (40, 58), (48, 66), (56, 58), (66, 60), (68, 78), (28, 78)],
              fill=(35, 50, 110))
    # 白襯衫
    d.polygon([(44, 60), (52, 60), (52, 78), (44, 78)], fill=(245, 245, 252))
    # 領帶
    d.polygon([(46, 60), (50, 60), (51, 66), (52, 78), (44, 78), (45, 66)],
              fill=(220, 80, 30))
    d.polygon([(47, 62), (49, 62), (50, 66), (51, 76), (45, 76), (46, 66)],
              fill=(255, 130, 50))
    # 鈕釦
    d.point([(38, 68)], fill=(255, 200, 60))
    d.point([(38, 74)], fill=(255, 200, 60))
    return img


def body_chef_coat_french():
    """晚餐鵝白色法式廚師服 + 金邊"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主服裝
    d.polygon([(30, 60), (66, 60), (68, 80), (28, 80)], fill=(220, 220, 230))
    d.polygon([(32, 62), (64, 62), (66, 78), (30, 78)], fill=(245, 245, 252))
    # 金邊
    d.line([(30, 60), (66, 60)], fill=(255, 200, 60), width=1)
    d.line([(40, 60), (40, 80)], fill=(255, 200, 60), width=1)
    d.line([(56, 60), (56, 80)], fill=(255, 200, 60), width=1)
    # 雙排扣
    for y in [64, 68, 72, 76]:
        d.point([(38, y)], fill=(255, 200, 60))
        d.point([(58, y)], fill=(255, 200, 60))
    # 領巾（金）
    d.polygon([(44, 60), (52, 60), (50, 64), (46, 64)], fill=(255, 200, 60))
    return img


def body_pajamas_torn():
    """宵夜鵝破爛睡衣（暗色）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主睡衣
    d.polygon([(28, 60), (68, 60), (70, 80), (26, 80)], fill=(40, 50, 70))
    d.polygon([(30, 62), (66, 62), (68, 78), (28, 78)], fill=(70, 80, 100))
    # 條紋
    for y in [66, 70, 74]:
        d.line([(30, y), (66, y)], fill=(50, 60, 80), width=1)
    # 破洞
    d.polygon([(38, 70), (42, 73), (40, 76)], fill=(20, 25, 40))
    d.polygon([(56, 65), (60, 68), (58, 72)], fill=(20, 25, 40))
    # 鈕釦
    d.point([(48, 65)], fill=(20, 25, 40))
    d.point([(48, 70)], fill=(20, 25, 40))
    d.point([(48, 75)], fill=(20, 25, 40))
    return img


def body_emperor_chest():
    """鵝皇胸甲（金羽紋）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 金色 V 領護甲
    d.polygon([(38, 60), (58, 60), (54, 68), (48, 76), (42, 68)], fill=(255, 200, 60))
    d.polygon([(40, 62), (56, 62), (52, 68), (48, 74), (44, 68)], fill=(255, 240, 140))
    # 胸口寶石
    d.ellipse([46, 64, 50, 68], fill=(220, 30, 50))
    d.point([(47, 65)], fill=(255, 200, 200))
    return img


def body_dragon_scales():
    """古龍鵝鱗片胸"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 黃肚
    d.ellipse([36, 60, 60, 80], fill=(220, 160, 30))
    d.ellipse([38, 62, 58, 78], fill=(255, 200, 60))
    # 鱗片紋
    for x, y in [(42, 64), (46, 66), (50, 64), (54, 66), (42, 70), (46, 72), (50, 70), (54, 72), (44, 74), (48, 76), (52, 74)]:
        d.point([(x, y)], fill=(180, 110, 20))
    return img


# ====================================================================
# RIGHT HAND ITEMS — 右手物件（畫在右翼端 x=70-90, y=30-60）
# ====================================================================

def hand_r_sword():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.rectangle([72, 50, 76, 58], fill=(80, 60, 40))           # 柄
    d.rectangle([70, 48, 78, 50], fill=(170, 130, 50))          # 護手
    d.rectangle([72, 32, 76, 50], fill=(220, 220, 230))         # 刃
    d.line([(74, 32), (74, 48)], fill=(255, 255, 255), width=1) # 刃光
    d.line([(73, 35), (73, 47)], fill=(180, 180, 195), width=1)
    return img


def hand_r_holy_sword():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.rectangle([72, 50, 76, 58], fill=(255, 200, 60))             # 金柄
    d.polygon([(68, 48), (80, 48), (80, 50), (68, 50)], fill=(255, 240, 140))  # 護手
    d.rectangle([72, 30, 76, 50], fill=(245, 245, 252))            # 刃
    d.rectangle([73, 30, 75, 50], fill=(255, 255, 255))            # 刃光
    # 神聖光點
    d.point([(70, 36)], fill=(255, 240, 140))
    d.point([(78, 42)], fill=(255, 240, 140))
    return img


def hand_r_staff():
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 杖身
    d.rectangle([74, 40, 76, 70], fill=(80, 50, 20))
    d.rectangle([74, 40, 75, 70], fill=(140, 90, 40))
    # 寶珠
    d.ellipse([70, 30, 80, 40], fill=(110, 60, 180))
    d.ellipse([72, 32, 78, 38], fill=(160, 100, 220))
    d.point([(74, 33)], fill=(220, 200, 255))
    # 法力光暈
    d.point([(68, 32)], fill=(180, 100, 220))
    d.point([(82, 32)], fill=(180, 100, 220))
    d.point([(75, 26)], fill=(220, 200, 255))
    return img


def hand_r_chef_knife():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.rectangle([72, 50, 76, 58], fill=(255, 200, 60))   # 金柄
    d.polygon([(70, 32), (78, 32), (78, 50), (72, 50)], fill=(220, 220, 230))
    d.line([(74, 32), (74, 50)], fill=(255, 255, 255), width=1)
    d.point([(78, 36)], fill=(255, 255, 255))
    return img


def hand_r_ramen_bowl():
    """宵夜鵝抱著的麵碗（在身體前方而非側邊）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 麵碗
    d.polygon([(36, 64), (60, 64), (62, 78), (34, 78)], fill=(140, 70, 20))
    d.polygon([(37, 66), (59, 66), (61, 76), (35, 76)], fill=(180, 100, 30))
    # 麵體
    d.ellipse([36, 62, 60, 68], fill=(255, 220, 80))
    d.ellipse([38, 63, 58, 67], fill=(255, 200, 60))
    # 蛋
    d.ellipse([42, 63, 50, 67], fill=(255, 252, 240))
    d.ellipse([44, 64, 48, 66], fill=(255, 200, 60))
    # 蔥
    d.point([(54, 64)], fill=(40, 180, 80))
    # 麵碗紋
    d.line([(36, 70), (60, 70)], fill=(110, 50, 10), width=1)
    return img


# ====================================================================
# LEFT HAND ITEMS — 左手物件（畫在左翼端 x=4-28, y=30-60）
# ====================================================================

def hand_l_shield():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.ellipse([10, 50, 30, 78], fill=(110, 110, 125))
    d.ellipse([11, 51, 29, 77], fill=(170, 170, 185))
    d.rectangle([19, 54, 21, 74], fill=(255, 200, 60))
    d.rectangle([14, 62, 26, 64], fill=(255, 200, 60))
    d.ellipse([18, 62, 22, 66], fill=(220, 30, 50))
    return img


def hand_l_bow():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.line([(8, 32), (4, 50), (8, 68)], fill=(110, 70, 30), width=2)
    d.line([(9, 34), (5, 50), (9, 66)], fill=(150, 100, 50), width=1)
    d.line([(8, 32), (8, 68)], fill=(220, 220, 230), width=1)
    d.line([(8, 50), (24, 50)], fill=(110, 70, 30), width=1)
    d.polygon([(24, 48), (28, 50), (24, 52)], fill=(220, 220, 230))
    d.point([(10, 49)], fill=(180, 35, 35))
    d.point([(10, 51)], fill=(180, 35, 35))
    return img


def hand_l_lunchbox():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.rectangle([6, 56, 28, 76], fill=(255, 220, 130))
    d.rectangle([7, 57, 27, 75], fill=(255, 240, 180))
    d.rectangle([6, 56, 28, 60], fill=(220, 30, 50))
    d.rectangle([10, 52, 24, 56], fill=(110, 70, 30))
    d.line([(14, 52), (14, 56)], fill=(80, 50, 20), width=1)
    d.line([(20, 52), (20, 56)], fill=(80, 50, 20), width=1)
    d.ellipse([12, 64, 18, 70], fill=(255, 255, 255))
    d.rectangle([13, 66, 17, 68], fill=(40, 40, 50))
    d.point([(22, 66)], fill=(220, 30, 50))
    d.point([(22, 70)], fill=(40, 180, 80))
    return img


def hand_l_frying_pan():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.ellipse([4, 36, 26, 50], fill=(40, 40, 45))
    d.ellipse([5, 37, 25, 49], fill=(60, 60, 65))
    d.ellipse([7, 38, 23, 46], fill=(40, 40, 45))
    d.rectangle([24, 42, 30, 46], fill=(80, 50, 20))
    d.line([(28, 44), (32, 60)], fill=(40, 30, 10), width=2)
    d.point([(10, 40)], fill=(140, 140, 150))
    return img


def hand_l_wine_glass():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.polygon([(10, 38), (22, 38), (22, 50), (18, 54), (14, 54), (10, 50)],
              fill=(180, 180, 190, 200))
    d.polygon([(11, 38), (21, 38), (21, 49), (17, 52), (15, 52), (11, 49)],
              fill=(220, 220, 235, 200))
    d.polygon([(12, 40), (20, 40), (20, 49), (17, 52), (15, 52), (12, 49)],
              fill=(140, 20, 30))
    d.polygon([(13, 41), (19, 41), (19, 47), (16, 50), (14, 47)],
              fill=(190, 40, 50))
    d.line([(14, 42), (18, 42)], fill=(220, 100, 110), width=1)
    d.line([(16, 54), (16, 64)], fill=(180, 180, 190), width=1)
    d.ellipse([12, 64, 20, 66], fill=(180, 180, 190))
    return img


# ====================================================================
# FX LAYERS — 特效層
# ====================================================================

def fx_royal_aura():
    img = new_layer()
    d = ImageDraw.Draw(img)
    for r in range(0, 40, 4):
        alpha = max(0, 80 - r * 2)
        d.ellipse([48-r, 48-r, 48+r, 48+r], outline=(60, 130, 240, alpha), width=1)
    for px in [(20, 30), (76, 30), (16, 60), (80, 60), (48, 14)]:
        d.point([px], fill=(255, 240, 140))
    return img


def fx_dark_aura():
    img = new_layer()
    d = ImageDraw.Draw(img)
    for r in range(8, 40, 3):
        alpha = max(0, 70 - r)
        d.ellipse([48-r, 48-r, 48+r, 48+r], outline=(110, 50, 180, alpha), width=1)
    for px in [(18, 20), (78, 22), (12, 50), (84, 52), (20, 80), (76, 80)]:
        d.point([px], fill=(140, 80, 220))
    return img


def fx_emperor_wings():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.polygon([(28, 58), (8, 50), (2, 60), (10, 70), (4, 78), (24, 76), (32, 70)],
              fill=(220, 220, 230))
    d.polygon([(28, 60), (10, 54), (8, 62), (14, 70), (10, 76), (24, 74), (30, 70)],
              fill=(245, 245, 252))
    d.line([(10, 58), (24, 64)], fill=(255, 200, 60), width=1)
    d.line([(8, 66), (22, 70)], fill=(255, 200, 60), width=1)
    d.polygon([(68, 58), (88, 50), (94, 60), (86, 70), (92, 78), (72, 76), (64, 70)],
              fill=(220, 220, 230))
    d.polygon([(68, 60), (86, 54), (88, 62), (82, 70), (86, 76), (72, 74), (66, 70)],
              fill=(245, 245, 252))
    d.line([(86, 58), (72, 64)], fill=(255, 200, 60), width=1)
    d.line([(88, 66), (74, 70)], fill=(255, 200, 60), width=1)
    return img


def fx_dragon_wings():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.polygon([(28, 58), (4, 48), (2, 56), (8, 60), (4, 64), (10, 70), (4, 76),
               (16, 76), (20, 70), (32, 68)], fill=(15, 60, 35))
    d.polygon([(28, 60), (8, 52), (10, 60), (14, 64), (12, 70), (24, 70), (32, 68)],
              fill=(20, 100, 60))
    d.polygon([(68, 58), (92, 48), (94, 56), (88, 60), (92, 64), (86, 70), (92, 76),
               (80, 76), (76, 70), (64, 68)], fill=(15, 60, 35))
    d.polygon([(68, 60), (88, 52), (86, 60), (82, 64), (84, 70), (72, 70), (64, 68)],
              fill=(20, 100, 60))
    return img


def fx_dragon_fire():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.polygon([(70, 32), (84, 28), (92, 32), (84, 38), (90, 42), (80, 40), (72, 38)],
              fill=(220, 60, 30))
    d.polygon([(72, 33), (82, 30), (88, 33), (82, 37), (78, 38)], fill=(255, 145, 30))
    d.polygon([(74, 34), (80, 32), (84, 34), (80, 36)], fill=(255, 220, 60))
    d.point([(80, 34)], fill=(255, 252, 220))
    d.point([(86, 26)], fill=(255, 200, 60))
    d.point([(94, 36)], fill=(220, 60, 30))
    return img


def fx_midnight_red_eyes():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.ellipse([52, 30, 56, 34], fill=(220, 30, 30))
    d.ellipse([53, 31, 55, 33], fill=(255, 100, 100))
    d.line([(50, 36), (56, 36)], fill=(40, 0, 0), width=1)
    return img


def fx_midnight_steam():
    img = new_layer()
    d = ImageDraw.Draw(img)
    d.line([(40, 50), (38, 44), (40, 38)], fill=(140, 80, 220, 180), width=1)
    d.line([(48, 50), (46, 42), (48, 36)], fill=(110, 50, 180, 180), width=1)
    d.line([(56, 50), (58, 44), (56, 38)], fill=(140, 80, 220, 180), width=1)
    return img


# ====================================================================
# COMPOSED CHARACTERS
# ====================================================================

def make_warrior():
    return compose([base_swan('white'), body_warrior_chest(), hand_r_sword(), head_red_headband()])


def make_archer():
    return compose([base_swan('white'), body_archer_vest(), hand_l_bow(), head_archer_hood()])


def make_paladin():
    return compose([base_swan('white'), body_paladin_armor(), hand_l_shield(), hand_r_holy_sword(), head_paladin_halo()])


def make_mage():
    return compose([base_swan('white'), body_mage_robe(), hand_r_staff(), head_star_hat()])


def make_breakfast():
    return compose([base_swan('white'), body_chef_apron(), hand_l_frying_pan(), head_chef_hat()])


def make_lunch():
    return compose([base_swan('white'), body_business_suit(), hand_l_lunchbox()])


def make_dinner():
    return compose([base_swan('white'), body_chef_coat_french(), hand_l_wine_glass(), hand_r_chef_knife(), head_chef_hat_french()])


def make_midnight():
    return compose([fx_dark_aura(), base_swan('dark'), body_pajamas_torn(), hand_r_ramen_bowl(),
                    fx_midnight_steam(), head_pajama_hair(), fx_midnight_red_eyes()])


def make_emperor():
    return compose([fx_royal_aura(), fx_emperor_wings(), base_swan('white'), body_emperor_chest(), head_crown()])


def make_dragon():
    return compose([fx_dragon_wings(), base_swan('green'), body_dragon_scales(), fx_dragon_fire(), head_dragon_horns()])


# ====================================================================
# SKILL ICONS（64×64）
# ====================================================================

def skill_icon(draw_inner, ring_color, bg_inner, bg_outer):
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 2, 62, 62], fill=bg_outer)
    d.ellipse([2, 2, 62, 62], outline=ring_color, width=2)
    d.ellipse([8, 8, 56, 56], fill=bg_inner)
    draw_inner(d)
    return img


def skill_fire():
    def inner(d):
        d.polygon([(32, 54), (24, 50), (18, 42), (16, 32), (20, 24), (24, 28), (24, 18),
                   (32, 10), (36, 18), (40, 24), (44, 18), (44, 28), (48, 32), (48, 42), (42, 50)],
                  fill=(220, 50, 30))
        d.polygon([(32, 50), (26, 46), (22, 38), (22, 30), (26, 26), (28, 30), (30, 22),
                   (32, 16), (36, 22), (38, 30), (42, 26), (42, 38), (38, 46)],
                  fill=(255, 145, 30))
        d.polygon([(32, 46), (28, 42), (26, 36), (28, 30), (32, 24), (36, 30), (38, 36), (36, 42)],
                  fill=(255, 220, 60))
        d.polygon([(32, 38), (29, 34), (32, 28), (35, 34)], fill=(255, 250, 220))
        for px in [(12, 18), (50, 18), (8, 32), (54, 36), (14, 50)]:
            d.point([px], fill=(255, 200, 80))
    return skill_icon(inner, (255, 200, 60), (110, 30, 30), (40, 10, 10))


def skill_lightning():
    def inner(d):
        d.polygon([(36, 12), (24, 32), (32, 32), (22, 52), (40, 30), (32, 30)],
                  fill=(220, 220, 240))
        d.polygon([(35, 14), (26, 30), (32, 30), (24, 48), (38, 32), (32, 32)],
                  fill=(255, 240, 140))
        for x1, y1, x2, y2 in [(48, 16, 54, 12), (48, 48, 54, 52),
                                (16, 16, 12, 12), (16, 48, 12, 52)]:
            d.line([(x1, y1), (x2, y2)], fill=(220, 220, 240), width=1)
        for px in [(52, 30), (12, 30), (32, 8)]:
            d.point([px], fill=(255, 255, 255))
    return skill_icon(inner, (60, 130, 240), (30, 50, 110), (10, 20, 50))


def skill_ice():
    def inner(d):
        d.line([(32, 12), (32, 52)], fill=(180, 220, 255), width=2)
        d.line([(14, 22), (50, 42)], fill=(180, 220, 255), width=2)
        d.line([(14, 42), (50, 22)], fill=(180, 220, 255), width=2)
        d.ellipse([28, 28, 36, 36], fill=(220, 240, 255))
        d.ellipse([30, 30, 34, 34], fill=(60, 150, 220))
        for x, y in [(32, 16), (32, 48), (18, 22), (46, 42), (18, 42), (46, 22)]:
            d.point([(x, y)], fill=(255, 255, 255))
    return skill_icon(inner, (60, 200, 240), (10, 50, 80), (5, 25, 50))


def skill_blood():
    def inner(d):
        d.polygon([(32, 12), (22, 30), (20, 42), (24, 50), (32, 54), (40, 50), (44, 42), (42, 30)],
                  fill=(180, 30, 30))
        d.polygon([(32, 16), (24, 32), (24, 42), (28, 48), (32, 50), (36, 48), (40, 42), (40, 32)],
                  fill=(220, 50, 50))
        d.line([(28, 24), (28, 36)], fill=(255, 150, 150), width=1)
        d.polygon([(14, 38), (12, 44), (14, 48), (16, 44)], fill=(180, 30, 30))
        d.polygon([(50, 38), (48, 44), (50, 48), (52, 44)], fill=(180, 30, 30))
        d.point([(18, 20)], fill=(180, 30, 30))
        d.point([(46, 20)], fill=(180, 30, 30))
    return skill_icon(inner, (220, 50, 50), (60, 10, 10), (30, 0, 0))


def skill_holy():
    def inner(d):
        for x1, y1, x2, y2 in [(32, 8, 32, 56), (8, 32, 56, 32),
                                (16, 16, 48, 48), (48, 16, 16, 48)]:
            d.line([(x1, y1), (x2, y2)], fill=(255, 240, 140), width=1)
        d.ellipse([20, 20, 44, 44], fill=(255, 250, 220, 200))
        d.ellipse([24, 24, 40, 40], fill=(255, 255, 255, 220))
        d.rectangle([30, 18, 34, 46], fill=(255, 200, 60))
        d.rectangle([20, 28, 44, 32], fill=(255, 200, 60))
        d.rectangle([31, 18, 33, 46], fill=(255, 255, 255))
        d.rectangle([20, 29, 44, 31], fill=(255, 255, 255))
        d.ellipse([30, 28, 34, 32], fill=(255, 200, 60))
        d.point([(31, 29)], fill=(255, 255, 255))
    return skill_icon(inner, (255, 200, 60), (140, 100, 30), (40, 30, 10))


def skill_death():
    def inner(d):
        d.ellipse([18, 14, 46, 42], fill=(220, 220, 235))
        d.ellipse([20, 16, 44, 40], fill=(245, 245, 252))
        d.polygon([(22, 38), (24, 46), (32, 48), (40, 46), (42, 38), (38, 42), (32, 44), (26, 42)],
                  fill=(220, 220, 235))
        d.ellipse([22, 22, 28, 28], fill=(20, 0, 30))
        d.ellipse([36, 22, 42, 28], fill=(20, 0, 30))
        d.ellipse([23, 23, 27, 27], fill=(160, 60, 220))
        d.ellipse([37, 23, 41, 27], fill=(160, 60, 220))
        d.point([(25, 24)], fill=(255, 240, 140))
        d.point([(39, 24)], fill=(255, 240, 140))
        d.polygon([(32, 30), (30, 36), (34, 36)], fill=(20, 0, 30))
        d.line([(28, 42), (28, 46)], fill=(80, 80, 90), width=1)
        d.line([(36, 42), (36, 46)], fill=(80, 80, 90), width=1)
        d.line([(32, 44), (32, 48)], fill=(80, 80, 90), width=1)
        for px in [(12, 16), (52, 16), (8, 50), (56, 50)]:
            d.point([px], fill=(160, 60, 220))
    return skill_icon(inner, (160, 60, 220), (50, 10, 80), (20, 0, 40))


def save_skill(img, name):
    path = os.path.join(DIRS['skills'], f'{name}.png')
    img.save(path)
    big = img.resize((64 * 4, 64 * 4), Image.NEAREST)
    big.save(os.path.join(DIRS['skills'], f'{name}_x4.png'))


# ====================================================================
# MAIN
# ====================================================================

if __name__ == '__main__':
    for n in ['white', 'dark', 'green']:
        save(base_swan(n), 'base', f'swan_{n}')
    for n, fn in [('red_headband', head_red_headband), ('archer_hood', head_archer_hood),
        ('paladin_halo', head_paladin_halo), ('star_hat', head_star_hat),
        ('chef_hat', head_chef_hat), ('chef_hat_french', head_chef_hat_french),
        ('pajama_hair', head_pajama_hair), ('crown', head_crown),
        ('dragon_horns', head_dragon_horns)]:
        save(fn(), 'head', n)
    for n, fn in [('warrior_chest', body_warrior_chest), ('archer_vest', body_archer_vest),
        ('paladin_armor', body_paladin_armor), ('mage_robe', body_mage_robe),
        ('chef_apron', body_chef_apron), ('business_suit', body_business_suit),
        ('chef_coat_french', body_chef_coat_french), ('pajamas_torn', body_pajamas_torn),
        ('emperor_chest', body_emperor_chest), ('dragon_scales', body_dragon_scales)]:
        save(fn(), 'body', n)
    for n, fn in [('sword', hand_r_sword), ('holy_sword', hand_r_holy_sword),
        ('staff', hand_r_staff), ('chef_knife', hand_r_chef_knife),
        ('ramen_bowl', hand_r_ramen_bowl)]:
        save(fn(), 'hand_r', n)
    for n, fn in [('shield', hand_l_shield), ('bow', hand_l_bow),
        ('lunchbox', hand_l_lunchbox), ('frying_pan', hand_l_frying_pan),
        ('wine_glass', hand_l_wine_glass)]:
        save(fn(), 'hand_l', n)
    for n, fn in [('royal_aura', fx_royal_aura), ('dark_aura', fx_dark_aura),
        ('emperor_wings', fx_emperor_wings), ('dragon_wings', fx_dragon_wings),
        ('dragon_fire', fx_dragon_fire), ('midnight_red_eyes', fx_midnight_red_eyes),
        ('midnight_steam', fx_midnight_steam)]:
        save(fn(), 'fx', n)
    for n, fn in [('warrior', make_warrior), ('archer', make_archer),
        ('paladin', make_paladin), ('mage', make_mage)]:
        save(fn(), 'classes', n)
    for n, fn in [('boss_breakfast', make_breakfast), ('boss_lunch', make_lunch),
        ('boss_dinner', make_dinner), ('boss_midnight', make_midnight),
        ('boss_emperor', make_emperor), ('boss_dragon', make_dragon)]:
        save(fn(), 'bosses', n)
    for n, fn in [('skill_fire', skill_fire), ('skill_lightning', skill_lightning),
        ('skill_ice', skill_ice), ('skill_blood', skill_blood),
        ('skill_holy', skill_holy), ('skill_death', skill_death)]:
        save_skill(fn(), n)
    import sys
    sys.stderr.write('ALL DONE\n')
