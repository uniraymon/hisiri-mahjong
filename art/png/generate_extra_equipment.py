#!/usr/bin/env python3
"""
13 件新裝備（紙娃娃用）
  5 帽：crown / mage / knight / demon / flower
  4 武：sword_gold / staff_void / bow_flame / scythe
  4 衣：knight_plate / robe_mage / demon_lord / casual

風格：深黑描邊 + 4-8 色 + 對齊 V1 紙娃娃 anchor (96×96)
輸出位置：mahjong/art/png/modern/layers/{head,hand_r,body}/
"""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(__file__), 'modern', 'layers')
HEAD = os.path.join(ROOT, 'head')
HAND_R = os.path.join(ROOT, 'hand_r')
BODY = os.path.join(ROOT, 'body')
for p in [HEAD, HAND_R, BODY]:
    os.makedirs(p, exist_ok=True)

W, H = 96, 96


def add_outline(img, color=(15, 15, 25, 255)):
    alpha = img.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(3))
    outline = Image.new('RGBA', img.size, color)
    outline.putalpha(dilated)
    return Image.alpha_composite(outline, img)


def new_layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def save(img, folder, name, outline=True):
    if outline:
        img = add_outline(img)
    img.save(os.path.join(folder, f'{name}.png'))
    big = img.resize((W * 4, H * 4), Image.NEAREST)
    big.save(os.path.join(folder, f'{name}_x4.png'))


# ====================================================================
# 帽子（頭部 anchor，y=4-30）
# ====================================================================

def hat_crown():
    """金色皇冠，三層階梯，中間紅寶石"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 第一層基底
    d.rectangle([32, 24, 64, 28], fill=(180, 130, 30))
    d.rectangle([32, 24, 64, 26], fill=(255, 200, 60))
    d.rectangle([33, 24, 63, 25], fill=(255, 240, 140))
    # 第二層階梯
    d.rectangle([35, 18, 61, 24], fill=(180, 130, 30))
    d.rectangle([36, 19, 60, 23], fill=(255, 200, 60))
    d.rectangle([36, 19, 60, 20], fill=(255, 240, 140))
    # 第三層階梯（最上）
    d.rectangle([39, 12, 57, 18], fill=(180, 130, 30))
    d.rectangle([40, 13, 56, 17], fill=(255, 200, 60))
    d.rectangle([40, 13, 56, 14], fill=(255, 240, 140))
    # 中央紅寶石
    d.ellipse([44, 8, 52, 14], fill=(120, 15, 25))
    d.ellipse([45, 9, 51, 13], fill=(220, 30, 50))
    d.ellipse([46, 10, 49, 12], fill=(255, 100, 100))
    d.point([(46, 10)], fill=(255, 200, 200))
    # 兩側小藍寶石
    d.ellipse([34, 20, 38, 24], fill=(15, 50, 130))
    d.ellipse([35, 21, 37, 23], fill=(50, 130, 240))
    d.ellipse([58, 20, 62, 24], fill=(15, 50, 130))
    d.ellipse([59, 21, 61, 23], fill=(50, 130, 240))
    return img


def hat_mage():
    """高筒巫師帽 — 深紫色 + 星星"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 帽簷
    d.rectangle([28, 24, 64, 28], fill=(20, 0, 40))
    d.rectangle([29, 24, 63, 26], fill=(60, 30, 110))
    d.rectangle([29, 24, 63, 25], fill=(110, 60, 180))
    # 帽身（高筒）
    d.rectangle([36, 8, 56, 24], fill=(20, 0, 40))
    d.rectangle([37, 9, 55, 24], fill=(60, 30, 110))
    d.rectangle([38, 10, 54, 14], fill=(110, 60, 180))
    # 帽身條紋裝飾
    d.line([(38, 16), (54, 16)], fill=(40, 20, 80), width=1)
    d.line([(38, 20), (54, 20)], fill=(40, 20, 80), width=1)
    # 微光細點
    d.point([(42, 12)], fill=(220, 200, 255))
    d.point([(50, 18)], fill=(180, 150, 220))
    d.point([(44, 22)], fill=(220, 200, 255))
    # 帽尖星星（5 角星）
    d.polygon([(46, 0), (47, 4), (51, 4), (48, 6), (49, 10), (46, 8), (43, 10), (44, 6), (41, 4), (45, 4)],
              fill=(180, 130, 30))
    d.polygon([(46, 1), (47, 4), (50, 4), (48, 6), (49, 9), (46, 7), (43, 9), (44, 6), (42, 4), (45, 4)],
              fill=(255, 200, 60))
    d.polygon([(46, 2), (47, 5), (49, 5), (47, 6), (48, 8), (46, 7), (44, 8), (45, 6), (43, 5), (45, 5)],
              fill=(255, 240, 140))
    d.point([(46, 5)], fill=(255, 255, 255))
    return img


def hat_knight():
    """銀灰騎士頭盔 + 護面甲"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 頭盔主體（圓弧）
    d.ellipse([32, 6, 62, 32], fill=(60, 60, 75))
    d.ellipse([34, 8, 60, 30], fill=(110, 110, 125))
    d.ellipse([35, 9, 59, 22], fill=(150, 150, 165))
    d.ellipse([37, 10, 50, 16], fill=(200, 200, 215))
    # 頭盔頂尖（小三角）
    d.polygon([(45, 0), (51, 0), (48, 6)], fill=(60, 60, 75))
    d.polygon([(46, 1), (50, 1), (48, 6)], fill=(110, 110, 125))
    # 頭盔頂紅羽毛
    d.polygon([(43, 4), (39, 0), (40, 8), (44, 6)], fill=(120, 15, 25))
    d.polygon([(44, 5), (41, 1), (42, 7), (44, 6)], fill=(220, 30, 50))
    # 護面甲（鎖鏈狀）
    d.rectangle([34, 22, 60, 32], fill=(60, 60, 75))
    d.rectangle([35, 23, 59, 31], fill=(110, 110, 125))
    # 眼縫
    d.rectangle([38, 24, 44, 26], fill=(0, 0, 0))
    d.rectangle([52, 24, 58, 26], fill=(0, 0, 0))
    # 眼縫紅光
    d.point([(40, 25)], fill=(220, 30, 50))
    d.point([(54, 25)], fill=(220, 30, 50))
    # 護面甲鉚釘
    for x in [37, 41, 45, 49, 53, 57]:
        d.point([(x, 30)], fill=(200, 200, 215))
    # 通氣孔
    d.line([(46, 28), (50, 28)], fill=(40, 40, 55), width=1)
    d.line([(45, 30), (51, 30)], fill=(40, 40, 55), width=1)
    return img


def hat_demon():
    """黑色惡魔角 + 紫光角尖"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 左角（向外彎曲）
    d.polygon([(36, 26), (28, 14), (24, 4), (28, 2), (32, 8), (38, 18), (40, 24)], fill=(20, 20, 30))
    d.polygon([(37, 25), (30, 14), (26, 6), (28, 4), (32, 10), (38, 18), (40, 23)], fill=(40, 40, 55))
    d.polygon([(38, 24), (32, 14), (29, 8), (32, 8), (38, 18), (39, 22)], fill=(70, 70, 90))
    # 角紋路
    d.line([(32, 12), (36, 18)], fill=(20, 20, 30), width=1)
    d.line([(30, 18), (36, 22)], fill=(20, 20, 30), width=1)
    # 左角尖紫光
    d.ellipse([22, 0, 30, 8], fill=(110, 50, 180, 180))
    d.ellipse([24, 1, 28, 6], fill=(160, 100, 220, 220))
    d.point([(26, 2)], fill=(220, 200, 255))
    d.point([(26, 4)], fill=(255, 255, 255))

    # 右角（鏡像）
    d.polygon([(60, 26), (68, 14), (72, 4), (68, 2), (64, 8), (58, 18), (56, 24)], fill=(20, 20, 30))
    d.polygon([(59, 25), (66, 14), (70, 6), (68, 4), (64, 10), (58, 18), (56, 23)], fill=(40, 40, 55))
    d.polygon([(58, 24), (64, 14), (67, 8), (64, 8), (58, 18), (57, 22)], fill=(70, 70, 90))
    d.line([(64, 12), (60, 18)], fill=(20, 20, 30), width=1)
    d.line([(66, 18), (60, 22)], fill=(20, 20, 30), width=1)
    # 右角尖紫光
    d.ellipse([66, 0, 74, 8], fill=(110, 50, 180, 180))
    d.ellipse([68, 1, 72, 6], fill=(160, 100, 220, 220))
    d.point([(70, 2)], fill=(220, 200, 255))
    d.point([(70, 4)], fill=(255, 255, 255))

    # 中央邪氣紫光點
    d.point([(48, 6)], fill=(160, 100, 220))
    d.point([(48, 8)], fill=(110, 50, 180))
    return img


def hat_flower():
    """粉紅 + 淡黃花環"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 環底（綠葉）
    d.ellipse([32, 18, 64, 30], outline=(20, 70, 40), width=2)
    d.ellipse([33, 19, 63, 29], outline=(34, 100, 60), width=1)
    # 葉片裝飾
    for x, y in [(34, 24), (62, 24), (38, 28), (58, 28), (40, 18), (56, 18)]:
        d.polygon([(x-2, y), (x, y-2), (x+2, y), (x, y+2)], fill=(34, 100, 60))
        d.point([(x, y)], fill=(60, 140, 90))

    # 粉紅花（左、右、中）
    for cx, cy in [(36, 16), (60, 16), (48, 12)]:
        # 花瓣
        d.ellipse([cx-4, cy-3, cx-1, cy+1], fill=(220, 50, 100))
        d.ellipse([cx+1, cy-3, cx+4, cy+1], fill=(220, 50, 100))
        d.ellipse([cx-3, cy-5, cx, cy-1], fill=(220, 50, 100))
        d.ellipse([cx, cy-5, cx+3, cy-1], fill=(220, 50, 100))
        d.ellipse([cx-3, cy+1, cx, cy+5], fill=(220, 50, 100))
        d.ellipse([cx, cy+1, cx+3, cy+5], fill=(220, 50, 100))
        # 高光
        d.ellipse([cx-3, cy-3, cx-1, cy], fill=(255, 150, 200))
        d.ellipse([cx-2, cy-4, cx, cy-1], fill=(255, 180, 220))
        # 花心（淡黃）
        d.ellipse([cx-2, cy-1, cx+2, cy+2], fill=(255, 240, 100))
        d.point([(cx, cy)], fill=(255, 255, 200))

    # 淡黃花（中間 2 個小）
    for cx, cy in [(42, 22), (54, 22)]:
        d.ellipse([cx-2, cy-1, cx, cy+2], fill=(255, 240, 100))
        d.ellipse([cx, cy-1, cx+2, cy+2], fill=(255, 240, 100))
        d.ellipse([cx-1, cy-2, cx+1, cy], fill=(255, 240, 100))
        d.ellipse([cx-1, cy+1, cx+1, cy+3], fill=(255, 240, 100))
        d.point([(cx, cy)], fill=(255, 200, 30))
    return img


# ====================================================================
# 武器（hand_r anchor，x=66-92, y=4-58）
# ====================================================================

def wpn_sword_gold():
    """發光金色大劍"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 光暈（先畫底）
    d.ellipse([62, 24, 86, 50], fill=(255, 240, 140, 60))
    d.ellipse([66, 28, 82, 46], fill=(255, 220, 80, 80))
    # 劍柄（皮革+金）
    d.rectangle([72, 50, 76, 60], fill=(60, 35, 15))
    d.rectangle([73, 51, 75, 59], fill=(110, 70, 30))
    # 柄頭（金圓）
    d.ellipse([70, 58, 78, 66], fill=(180, 130, 30))
    d.ellipse([71, 59, 77, 65], fill=(255, 200, 60))
    d.ellipse([72, 60, 76, 64], fill=(255, 240, 140))
    d.point([(73, 61)], fill=(255, 255, 255))
    # 護手（大金十字）
    d.rectangle([64, 46, 84, 50], fill=(180, 130, 30))
    d.rectangle([65, 47, 83, 49], fill=(255, 200, 60))
    d.rectangle([66, 47, 82, 48], fill=(255, 240, 140))
    # 護手兩端
    d.polygon([(64, 46), (60, 44), (60, 52), (64, 50)], fill=(255, 200, 60))
    d.polygon([(84, 46), (88, 44), (88, 52), (84, 50)], fill=(255, 200, 60))
    d.polygon([(60, 45), (62, 47), (62, 49), (60, 51)], fill=(255, 240, 140))
    d.polygon([(88, 45), (86, 47), (86, 49), (88, 51)], fill=(255, 240, 140))
    # 劍刃（金色發光大劍）
    d.polygon([(70, 46), (78, 46), (76, 8), (74, 4), (72, 8)], fill=(180, 130, 30))
    d.polygon([(71, 46), (77, 46), (75, 10), (74, 6), (73, 10)], fill=(255, 200, 60))
    d.polygon([(72, 46), (76, 46), (75, 14), (73, 14)], fill=(255, 240, 140))
    d.line([(74, 14), (74, 44)], fill=(255, 255, 255), width=1)
    # 劍中央血槽
    d.line([(73, 18), (73, 42)], fill=(220, 180, 80), width=1)
    d.line([(75, 18), (75, 42)], fill=(220, 180, 80), width=1)
    # 劍身金色光點
    d.point([(74, 18)], fill=(255, 255, 255))
    d.point([(74, 28)], fill=(255, 255, 255))
    d.point([(74, 38)], fill=(255, 255, 255))
    # 光暈光點
    d.point([(64, 20)], fill=(255, 240, 140))
    d.point([(86, 28)], fill=(255, 240, 140))
    d.point([(64, 36)], fill=(255, 220, 80))
    d.point([(86, 12)], fill=(255, 220, 80))
    return img


def wpn_staff_void():
    """深紫色虛空法杖 + 懸浮魔法球"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 法杖身
    d.rectangle([72, 26, 76, 64], fill=(20, 0, 40))
    d.rectangle([73, 27, 75, 63], fill=(60, 30, 110))
    d.line([(74, 27), (74, 63)], fill=(110, 60, 180), width=1)
    # 法杖頂端的金屬扣（環）
    d.rectangle([70, 22, 78, 26], fill=(20, 0, 40))
    d.rectangle([71, 23, 77, 25], fill=(60, 30, 110))
    d.rectangle([71, 23, 77, 24], fill=(110, 60, 180))
    # 杖底金尾
    d.rectangle([71, 62, 77, 66], fill=(60, 35, 15))
    d.rectangle([72, 63, 76, 65], fill=(255, 200, 60))

    # 懸浮魔法球（大紫球，浮在法杖上方）
    d.ellipse([66, 6, 84, 24], fill=(20, 0, 40))   # 外光
    d.ellipse([68, 8, 82, 22], fill=(60, 30, 110))
    d.ellipse([69, 9, 81, 21], fill=(110, 60, 180))
    d.ellipse([70, 10, 80, 20], fill=(160, 100, 220))
    d.ellipse([72, 12, 78, 18], fill=(220, 200, 255))
    d.point([(73, 13)], fill=(255, 255, 255))
    d.point([(74, 13)], fill=(255, 255, 255))
    # 球體紫光環
    d.ellipse([62, 4, 88, 26], outline=(110, 50, 180, 180), width=1)

    # 漂浮虛空粒子
    d.point([(66, 4)], fill=(160, 100, 220))
    d.point([(86, 6)], fill=(160, 100, 220))
    d.point([(64, 16)], fill=(110, 60, 180))
    d.point([(88, 18)], fill=(110, 60, 180))
    d.point([(62, 26)], fill=(160, 100, 220))
    d.point([(86, 26)], fill=(160, 100, 220))

    # 法杖中段魔法符文
    d.point([(74, 36)], fill=(160, 100, 220))
    d.point([(74, 44)], fill=(160, 100, 220))
    d.point([(74, 52)], fill=(160, 100, 220))
    return img


def wpn_bow_flame():
    """火焰橘色弓 + 弦上火焰"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 弓身（橘紅 3 段弧）
    d.line([(70, 16), (78, 30), (82, 44), (78, 58), (70, 72)], fill=(120, 30, 5), width=2)
    d.line([(71, 18), (77, 30), (81, 44), (77, 58), (71, 70)], fill=(220, 90, 20), width=1)
    d.line([(72, 20), (76, 30), (80, 44), (76, 58), (72, 68)], fill=(255, 145, 30), width=1)
    # 弓握處
    d.line([(76, 40), (84, 40)], fill=(80, 20, 5), width=1)
    d.line([(76, 48), (84, 48)], fill=(80, 20, 5), width=1)
    # 弓兩端裝飾
    d.ellipse([68, 14, 72, 18], fill=(255, 200, 60))
    d.ellipse([68, 70, 72, 74], fill=(255, 200, 60))

    # 弦
    d.line([(70, 16), (70, 72)], fill=(255, 252, 220), width=1)

    # 火焰特效（沿弦）
    # 弦上小火焰
    for cy in [22, 32, 44, 56, 66]:
        d.polygon([(68, cy-2), (66, cy), (68, cy+2), (70, cy+1), (72, cy-1)], fill=(220, 50, 30))
        d.polygon([(69, cy-1), (68, cy), (69, cy+1), (71, cy+1), (71, cy-1)], fill=(255, 145, 30))
        d.point([(70, cy)], fill=(255, 220, 60))

    # 兩端大火焰
    d.polygon([(64, 12), (60, 16), (66, 18), (72, 14), (70, 10)], fill=(220, 50, 30))
    d.polygon([(66, 14), (62, 16), (66, 17), (70, 14), (68, 12)], fill=(255, 145, 30))
    d.point([(66, 14)], fill=(255, 220, 60))
    d.polygon([(64, 76), (60, 72), (66, 70), (72, 74), (70, 78)], fill=(220, 50, 30))
    d.polygon([(66, 74), (62, 72), (66, 71), (70, 74), (68, 76)], fill=(255, 145, 30))
    d.point([(66, 74)], fill=(255, 220, 60))

    # 火星粒子
    d.point([(60, 28)], fill=(255, 200, 60))
    d.point([(58, 50)], fill=(220, 60, 30))
    d.point([(86, 22)], fill=(255, 200, 60))
    d.point([(86, 60)], fill=(220, 60, 30))
    return img


def wpn_scythe():
    """黑色死神鐮刀 + 紫能量"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 杖身（黑）
    d.line([(72, 8), (76, 70)], fill=(20, 20, 30), width=3)
    d.line([(73, 10), (76, 68)], fill=(50, 50, 65), width=1)
    d.line([(74, 12), (75, 66)], fill=(80, 80, 95), width=1)
    # 杖底
    d.ellipse([72, 66, 80, 74], fill=(20, 20, 30))
    d.ellipse([73, 67, 79, 73], fill=(60, 30, 110))
    d.ellipse([74, 68, 78, 72], fill=(160, 100, 220))
    # 杖柄裝飾
    d.rectangle([70, 28, 78, 32], fill=(20, 20, 30))
    d.rectangle([71, 29, 77, 31], fill=(60, 30, 110))
    # 刀片（彎曲大刃，靠右上）
    # 主刀身
    d.polygon([(74, 8), (90, 4), (94, 12), (88, 18), (76, 14)], fill=(20, 20, 30))
    d.polygon([(75, 9), (88, 6), (92, 12), (86, 16), (76, 13)], fill=(50, 50, 65))
    d.polygon([(76, 10), (86, 8), (90, 12), (84, 14), (78, 12)], fill=(80, 80, 95))
    # 刀刃（紫能量邊）
    d.line([(76, 10), (90, 4)], fill=(160, 100, 220), width=1)
    d.line([(75, 9), (88, 4)], fill=(220, 200, 255), width=1)
    # 刀刃上紫光粒子
    d.point([(82, 7)], fill=(255, 255, 255))
    d.point([(86, 9)], fill=(220, 200, 255))
    d.point([(78, 9)], fill=(160, 100, 220))
    # 紫能量飄散
    d.point([(92, 14)], fill=(160, 100, 220))
    d.point([(94, 18)], fill=(110, 50, 180))
    d.point([(60, 22)], fill=(110, 50, 180))
    # 杖中段繩索/裝飾
    d.line([(70, 38), (78, 36)], fill=(120, 15, 25), width=1)
    d.line([(70, 40), (78, 38)], fill=(180, 35, 35), width=1)
    return img


# ====================================================================
# 服裝（body anchor，x=28-66, y=58-78）
# ====================================================================

def body_knight_plate():
    """全套銀色板甲 + 厚重肩甲"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主胸甲
    d.polygon([(28, 60), (24, 80), (60, 82), (66, 60)], fill=(60, 60, 75))
    d.polygon([(30, 62), (26, 78), (58, 80), (64, 62)], fill=(110, 110, 125))
    d.polygon([(32, 64), (28, 76), (56, 78), (62, 64)], fill=(150, 150, 165))
    d.polygon([(32, 64), (30, 70), (60, 72), (62, 64)], fill=(180, 180, 195))
    # 中央分線
    d.line([(46, 62), (44, 80)], fill=(40, 40, 55), width=1)
    d.line([(47, 62), (47, 80)], fill=(180, 180, 195), width=1)
    # 厚重左肩甲（突出於身體）
    d.ellipse([22, 56, 38, 70], fill=(40, 40, 55))
    d.ellipse([23, 57, 37, 69], fill=(110, 110, 125))
    d.ellipse([24, 58, 36, 66], fill=(150, 150, 165))
    d.ellipse([26, 58, 32, 62], fill=(200, 200, 215))
    # 左肩甲鉚釘
    d.point([(26, 64)], fill=(60, 60, 75))
    d.point([(34, 64)], fill=(60, 60, 75))
    # 厚重右肩甲
    d.ellipse([56, 56, 72, 70], fill=(40, 40, 55))
    d.ellipse([57, 57, 71, 69], fill=(110, 110, 125))
    d.ellipse([58, 58, 70, 66], fill=(150, 150, 165))
    d.ellipse([62, 58, 68, 62], fill=(200, 200, 215))
    d.point([(60, 64)], fill=(60, 60, 75))
    d.point([(68, 64)], fill=(60, 60, 75))
    # 胸前中央十字（金）
    d.rectangle([45, 66, 49, 76], fill=(180, 130, 30))
    d.rectangle([41, 69, 53, 73], fill=(180, 130, 30))
    d.rectangle([46, 66, 48, 76], fill=(255, 200, 60))
    d.rectangle([41, 70, 53, 72], fill=(255, 200, 60))
    # 鉚釘排
    for cx in [34, 60]:
        d.ellipse([cx-1, 70, cx+1, 72], fill=(40, 40, 55))
        d.point([(cx, 71)], fill=(220, 220, 235))
    # 腰帶
    d.rectangle([28, 76, 64, 80], fill=(60, 35, 15))
    d.rectangle([29, 77, 63, 79], fill=(110, 70, 30))
    d.rectangle([45, 76, 51, 80], fill=(255, 200, 60))
    d.rectangle([46, 77, 50, 79], fill=(255, 240, 140))
    return img


def body_robe_mage():
    """深色法師長袍 + 金色滾邊"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主長袍（深紫黑）
    d.polygon([(26, 58), (20, 82), (66, 84), (62, 58)], fill=(15, 0, 30))
    d.polygon([(28, 60), (22, 80), (64, 82), (60, 60)], fill=(40, 10, 70))
    d.polygon([(30, 62), (24, 78), (62, 80), (58, 62)], fill=(60, 30, 110))
    d.polygon([(32, 64), (26, 76), (58, 78), (56, 64)], fill=(80, 50, 140))
    # V 領
    d.polygon([(40, 58), (44, 70), (48, 70), (52, 58)], fill=(15, 0, 30))
    d.polygon([(41, 58), (45, 68), (47, 68), (51, 58)], fill=(40, 10, 70))
    # 金色滾邊（領口）
    d.line([(40, 58), (52, 58)], fill=(180, 130, 30), width=1)
    d.line([(40, 60), (44, 70)], fill=(255, 200, 60), width=1)
    d.line([(52, 60), (48, 70)], fill=(255, 200, 60), width=1)
    # 金色滾邊（中央）
    d.rectangle([45, 70, 47, 80], fill=(180, 130, 30))
    d.rectangle([46, 70, 47, 80], fill=(255, 200, 60))
    # 金色滾邊（下擺）
    d.line([(20, 82), (66, 84)], fill=(180, 130, 30), width=1)
    d.line([(22, 80), (64, 82)], fill=(255, 200, 60), width=1)
    # 金色滾邊（左右側）
    d.line([(26, 58), (20, 82)], fill=(255, 200, 60), width=1)
    d.line([(62, 58), (66, 82)], fill=(255, 200, 60), width=1)
    # 符文裝飾
    for x, y in [(36, 70), (52, 70), (38, 76), (50, 76), (44, 74)]:
        d.point([(x, y)], fill=(255, 240, 80))
        d.point([(x+1, y)], fill=(255, 200, 60))
    # 中央寶石
    d.ellipse([44, 64, 50, 70], fill=(120, 15, 25))
    d.ellipse([45, 65, 49, 69], fill=(220, 30, 50))
    d.point([(46, 66)], fill=(255, 100, 100))
    return img


def body_demon_lord():
    """黑紅魔王裝 + 肩膀尖刺"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主胸甲（黑紅）
    d.polygon([(28, 60), (24, 80), (60, 82), (66, 60)], fill=(20, 0, 0))
    d.polygon([(30, 62), (26, 78), (58, 80), (64, 62)], fill=(60, 5, 5))
    d.polygon([(32, 64), (28, 76), (56, 78), (62, 64)], fill=(120, 15, 25))
    # 中央暗紅紋（胸口邪氣）
    d.polygon([(40, 64), (40, 78), (44, 78), (44, 70), (50, 70), (50, 78), (54, 78), (54, 64)], fill=(60, 5, 5))
    d.polygon([(42, 66), (42, 76), (44, 76), (44, 72), (50, 72), (50, 76), (52, 76), (52, 66)], fill=(180, 35, 35))
    # 中央邪氣眼（紫紅）
    d.ellipse([45, 67, 49, 71], fill=(80, 0, 80))
    d.ellipse([46, 68, 48, 70], fill=(220, 30, 50))
    d.point([(47, 69)], fill=(255, 200, 60))
    # 尖刺左肩（4 根）
    for x in [22, 26, 30, 34]:
        d.polygon([(x-1, 60), (x+1, 60), (x, 50)], fill=(20, 0, 0))
        d.polygon([(x, 60), (x+1, 60), (x, 52)], fill=(60, 5, 5))
        d.polygon([(x, 56), (x+0.5, 56)], fill=(120, 15, 25))
        d.point([(x, 50)], fill=(220, 30, 50))   # 尖端血色
    # 尖刺右肩（4 根）
    for x in [56, 60, 64, 68]:
        d.polygon([(x-1, 60), (x+1, 60), (x, 50)], fill=(20, 0, 0))
        d.polygon([(x, 60), (x+1, 60), (x, 52)], fill=(60, 5, 5))
        d.point([(x, 50)], fill=(220, 30, 50))
    # 肩甲底（黑色厚重）
    d.ellipse([18, 56, 36, 66], fill=(20, 0, 0))
    d.ellipse([19, 57, 35, 65], fill=(60, 5, 5))
    d.ellipse([20, 58, 34, 64], fill=(80, 20, 20))
    d.ellipse([54, 56, 72, 66], fill=(20, 0, 0))
    d.ellipse([55, 57, 71, 65], fill=(60, 5, 5))
    d.ellipse([56, 58, 70, 64], fill=(80, 20, 20))
    # 紅紋路（甲面裂痕）
    d.line([(34, 66), (38, 70), (32, 74)], fill=(120, 15, 25), width=1)
    d.line([(58, 66), (54, 70), (60, 74)], fill=(120, 15, 25), width=1)
    # 腰帶（暗紅+黑）
    d.rectangle([28, 78, 64, 82], fill=(20, 0, 0))
    d.rectangle([29, 79, 63, 81], fill=(80, 5, 5))
    d.rectangle([45, 78, 51, 82], fill=(120, 15, 25))
    d.point([(48, 80)], fill=(220, 30, 50))
    return img


def body_casual():
    """白 T 恤 + 牛仔褲（休閒）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 白 T 恤上半
    d.polygon([(30, 58), (28, 70), (62, 70), (60, 58)], fill=(180, 180, 195))
    d.polygon([(31, 59), (29, 69), (61, 69), (59, 59)], fill=(220, 220, 235))
    d.polygon([(32, 60), (30, 68), (60, 68), (58, 60)], fill=(245, 245, 252))
    # T 恤領口
    d.polygon([(42, 58), (44, 64), (48, 64), (50, 58)], fill=(180, 180, 195))
    d.polygon([(43, 58), (45, 63), (47, 63), (49, 58)], fill=(220, 220, 235))
    # T 恤短袖
    d.polygon([(28, 60), (24, 64), (28, 68), (32, 66)], fill=(180, 180, 195))
    d.polygon([(29, 60), (26, 64), (29, 67), (31, 65)], fill=(220, 220, 235))
    d.polygon([(62, 60), (66, 64), (62, 68), (58, 66)], fill=(180, 180, 195))
    d.polygon([(61, 60), (64, 64), (61, 67), (59, 65)], fill=(220, 220, 235))
    # T 恤圖案（簡單的笑臉）
    d.ellipse([42, 64, 48, 70], fill=(255, 200, 60))
    d.ellipse([43, 65, 47, 69], fill=(255, 240, 140))
    d.point([(44, 66)], fill=(20, 20, 30))
    d.point([(46, 66)], fill=(20, 20, 30))
    d.line([(44, 68), (46, 68)], fill=(20, 20, 30), width=1)

    # 牛仔褲
    d.polygon([(30, 70), (26, 82), (60, 82), (62, 70)], fill=(15, 30, 70))
    d.polygon([(31, 71), (28, 81), (58, 81), (61, 71)], fill=(40, 60, 110))
    d.polygon([(32, 72), (30, 80), (56, 80), (58, 72)], fill=(70, 100, 160))
    # 牛仔褲分縫
    d.line([(46, 70), (44, 82)], fill=(15, 30, 70), width=1)
    d.line([(45, 72), (44, 82)], fill=(110, 140, 200), width=1)
    # 口袋線
    d.line([(34, 74), (38, 74)], fill=(15, 30, 70), width=1)
    d.line([(54, 74), (58, 74)], fill=(15, 30, 70), width=1)
    # 牛仔釘
    d.point([(36, 74)], fill=(255, 200, 60))
    d.point([(56, 74)], fill=(255, 200, 60))
    # 腰帶
    d.rectangle([28, 70, 64, 72], fill=(60, 35, 15))
    d.rectangle([29, 70, 63, 71], fill=(110, 70, 30))
    d.rectangle([45, 70, 51, 73], fill=(255, 200, 60))
    return img


# ====================================================================
# Main
# ====================================================================

if __name__ == '__main__':
    import sys
    log = sys.stderr

    log.write('=== Hats ===\n')
    for n, fn in [('hat_crown', hat_crown), ('hat_mage', hat_mage),
                  ('hat_knight', hat_knight), ('hat_demon', hat_demon),
                  ('hat_flower', hat_flower)]:
        save(fn(), HEAD, n)
        log.write(f'  {n}\n')

    log.write('=== Weapons ===\n')
    for n, fn in [('wpn_sword_gold', wpn_sword_gold), ('wpn_staff_void', wpn_staff_void),
                  ('wpn_bow_flame', wpn_bow_flame), ('wpn_scythe', wpn_scythe)]:
        save(fn(), HAND_R, n)
        log.write(f'  {n}\n')

    log.write('=== Bodies ===\n')
    for n, fn in [('body_knight_plate', body_knight_plate), ('body_robe_mage', body_robe_mage),
                  ('body_demon_lord', body_demon_lord), ('body_casual', body_casual)]:
        save(fn(), BODY, n)
        log.write(f'  {n}\n')

    log.write('\nALL EXTRA EQUIPMENT DONE\n')
