#!/usr/bin/env python3
"""
第二批 16 件裝備：
  5 帽 — top_hat / straw / bunny_ears / pumpkin / halo_dark
  6 武 — dagger / warhammer / axe / wand / umbrella / fishing_rod
  5 衣 — ninja / kimono / beach / doctor / tuxedo

放進 mahjong/art/png/modern/layers/{head,hand_r,body}/
"""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(__file__), 'modern', 'layers')
HEAD = os.path.join(ROOT, 'head')
HAND_R = os.path.join(ROOT, 'hand_r')
BODY = os.path.join(ROOT, 'body')

W, H = 96, 96


def add_outline(img, color=(15, 15, 25, 255)):
    alpha = img.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(3))
    outline = Image.new('RGBA', img.size, color)
    outline.putalpha(dilated)
    return Image.alpha_composite(outline, img)


def new_layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def save(img, folder, name):
    img = add_outline(img)
    img.save(os.path.join(folder, f'{name}.png'))
    big = img.resize((W * 4, H * 4), Image.NEAREST)
    big.save(os.path.join(folder, f'{name}_x4.png'))


# === 5 HATS ===
def hat_top_hat():
    """紳士黑色高頂禮帽"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 帽簷
    d.rectangle([28, 26, 64, 30], fill=(20, 20, 30))
    d.rectangle([29, 26, 63, 28], fill=(60, 60, 75))
    d.rectangle([29, 26, 63, 27], fill=(110, 110, 125))
    # 帽身
    d.rectangle([34, 8, 58, 26], fill=(20, 20, 30))
    d.rectangle([35, 9, 57, 26], fill=(60, 60, 75))
    d.rectangle([36, 10, 56, 18], fill=(80, 80, 95))
    # 帽帶（紅色緞帶）
    d.rectangle([34, 22, 58, 24], fill=(80, 5, 5))
    d.rectangle([34, 22, 58, 23], fill=(180, 35, 35))
    d.rectangle([45, 22, 49, 26], fill=(255, 200, 60))
    # 高光
    d.line([(36, 12), (36, 22)], fill=(140, 140, 155), width=1)
    return img


def hat_straw():
    """草帽 — 寬簷，黃褐色"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 寬大帽簷
    d.ellipse([22, 24, 70, 32], fill=(140, 90, 30))
    d.ellipse([23, 25, 69, 31], fill=(220, 160, 60))
    d.ellipse([24, 25, 68, 30], fill=(255, 200, 100))
    # 帽頂
    d.ellipse([34, 10, 58, 26], fill=(140, 90, 30))
    d.ellipse([35, 11, 57, 25], fill=(220, 160, 60))
    d.ellipse([36, 12, 56, 22], fill=(255, 200, 100))
    # 草帽編織紋
    for y in [14, 18, 22]:
        d.line([(36, y), (56, y)], fill=(140, 90, 30), width=1)
    for x in [40, 46, 52]:
        d.line([(x, 12), (x, 22)], fill=(140, 90, 30), width=1)
    # 紅色花朵裝飾
    d.ellipse([54, 18, 60, 24], fill=(80, 5, 5))
    d.ellipse([55, 19, 59, 23], fill=(220, 30, 50))
    d.point([(57, 21)], fill=(255, 240, 100))
    return img


def hat_bunny_ears():
    """可愛兔耳"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 左耳
    d.ellipse([34, 0, 42, 26], fill=(180, 180, 195))
    d.ellipse([35, 1, 41, 25], fill=(245, 245, 252))
    # 左耳粉紅內側
    d.ellipse([36, 4, 40, 22], fill=(220, 80, 130))
    d.ellipse([37, 5, 39, 21], fill=(255, 150, 200))
    # 右耳
    d.ellipse([54, 0, 62, 26], fill=(180, 180, 195))
    d.ellipse([55, 1, 61, 25], fill=(245, 245, 252))
    d.ellipse([56, 4, 60, 22], fill=(220, 80, 130))
    d.ellipse([57, 5, 59, 21], fill=(255, 150, 200))
    # 中間蝴蝶結
    d.polygon([(46, 22), (44, 18), (44, 26), (46, 24), (50, 24), (52, 26), (52, 18), (50, 22)],
              fill=(120, 15, 25))
    d.polygon([(45, 19), (45, 25), (51, 25), (51, 19)], fill=(220, 30, 50))
    d.ellipse([47, 22, 49, 24], fill=(255, 200, 60))
    return img


def hat_pumpkin():
    """萬聖節南瓜頭（戴在頭上的迷你款）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 南瓜身
    d.ellipse([30, 10, 66, 32], fill=(140, 60, 5))
    d.ellipse([31, 11, 65, 31], fill=(220, 90, 20))
    d.ellipse([32, 12, 64, 30], fill=(255, 145, 30))
    # 瓜紋（垂直線）
    d.line([(38, 12), (38, 30)], fill=(140, 60, 5), width=1)
    d.line([(48, 11), (48, 31)], fill=(140, 60, 5), width=1)
    d.line([(58, 12), (58, 30)], fill=(140, 60, 5), width=1)
    # 蒂頭（綠）
    d.rectangle([46, 6, 50, 12], fill=(20, 70, 40))
    d.rectangle([47, 7, 49, 12], fill=(34, 100, 60))
    d.line([(50, 6), (54, 4)], fill=(20, 70, 40), width=1)
    # 鬼臉（雕刻）
    # 三角眼
    d.polygon([(38, 18), (44, 18), (41, 22)], fill=(20, 0, 30))
    d.polygon([(52, 18), (58, 18), (55, 22)], fill=(20, 0, 30))
    # 鋸齒嘴
    d.polygon([(40, 26), (42, 24), (44, 26), (46, 24), (48, 26), (50, 24), (52, 26), (54, 24), (56, 26)],
              fill=(20, 0, 30))
    # 眼洞發光
    d.point([(41, 20)], fill=(255, 200, 60))
    d.point([(55, 20)], fill=(255, 200, 60))
    return img


def hat_halo_dark():
    """暗黑墮落光環（反派用）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 環體（深紫黑）
    d.ellipse([32, 10, 64, 22], outline=(20, 0, 40), width=2)
    d.ellipse([33, 11, 63, 21], outline=(60, 30, 110), width=1)
    d.ellipse([34, 12, 62, 20], outline=(110, 50, 180), width=1)
    # 邪氣黑刺
    for ang in [0, 60, 120, 180, 240, 300]:
        import math
        cx, cy = 48, 16
        x1 = cx + 18 * math.cos(math.radians(ang))
        y1 = cy + 6 * math.sin(math.radians(ang))
        x2 = cx + 22 * math.cos(math.radians(ang))
        y2 = cy + 8 * math.sin(math.radians(ang))
        d.line([(x1, y1), (x2, y2)], fill=(20, 0, 40), width=2)
        d.point([(x2, y2)], fill=(160, 100, 220))
    # 紫光粒子
    d.point([(28, 8)], fill=(160, 100, 220))
    d.point([(68, 8)], fill=(160, 100, 220))
    d.point([(28, 24)], fill=(110, 50, 180))
    d.point([(68, 24)], fill=(110, 50, 180))
    d.point([(48, 4)], fill=(220, 200, 255))
    return img


# === 6 WEAPONS ===
def wpn_dagger():
    """匕首（小巧鋒利）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 短刃
    d.polygon([(72, 36), (76, 36), (78, 24), (74, 20), (70, 24)], fill=(40, 40, 55))
    d.polygon([(73, 36), (75, 36), (77, 25), (74, 22), (71, 25)], fill=(110, 110, 125))
    d.polygon([(74, 36), (74, 25), (75, 25), (75, 36)], fill=(220, 220, 235))
    d.point([(75, 22)], fill=(255, 255, 255))
    # 護手
    d.rectangle([69, 36, 79, 40], fill=(80, 50, 20))
    d.rectangle([70, 37, 78, 39], fill=(180, 130, 30))
    d.rectangle([70, 37, 78, 38], fill=(255, 200, 60))
    # 刀柄
    d.rectangle([72, 40, 76, 50], fill=(80, 5, 5))
    d.rectangle([73, 41, 75, 49], fill=(180, 35, 35))
    # 柄頭寶石
    d.ellipse([70, 50, 78, 56], fill=(20, 0, 40))
    d.ellipse([71, 51, 77, 55], fill=(110, 60, 180))
    d.ellipse([72, 52, 76, 54], fill=(160, 100, 220))
    d.point([(73, 53)], fill=(255, 255, 255))
    return img


def wpn_warhammer():
    """戰錘 — 巨大方頭"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 錘頭（大方塊）
    d.rectangle([62, 8, 86, 32], fill=(40, 40, 55))
    d.rectangle([63, 9, 85, 31], fill=(80, 80, 95))
    d.rectangle([64, 10, 84, 22], fill=(140, 140, 155))
    d.rectangle([66, 12, 82, 16], fill=(180, 180, 195))
    # 錘頭金屬釘
    for cx in [66, 72, 78, 82]:
        d.point([(cx, 14)], fill=(220, 220, 235))
        d.point([(cx, 26)], fill=(40, 40, 55))
    # 錘頭中央符文
    d.line([(72, 18), (74, 22), (72, 26)], fill=(220, 30, 50), width=1)
    d.line([(76, 18), (74, 22), (76, 26)], fill=(220, 30, 50), width=1)
    # 把手
    d.rectangle([72, 32, 76, 64], fill=(40, 25, 5))
    d.rectangle([73, 33, 75, 63], fill=(110, 70, 30))
    d.line([(74, 33), (74, 63)], fill=(150, 100, 50), width=1)
    # 把手綁繩
    for y in [38, 44, 50, 56]:
        d.rectangle([71, y, 77, y+1], fill=(80, 5, 5))
    return img


def wpn_axe():
    """戰斧 — 雙刃"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 把手
    d.rectangle([72, 12, 76, 64], fill=(40, 25, 5))
    d.rectangle([73, 13, 75, 63], fill=(110, 70, 30))
    d.line([(74, 13), (74, 63)], fill=(150, 100, 50), width=1)
    # 斧頭主體（大弧形雙刃）
    # 上刃
    d.polygon([(72, 16), (76, 16), (88, 20), (92, 14), (84, 8), (76, 12)], fill=(40, 40, 55))
    d.polygon([(72, 17), (76, 17), (86, 20), (90, 16), (84, 11), (76, 13)], fill=(110, 110, 125))
    d.polygon([(74, 14), (84, 12), (90, 16), (84, 18), (76, 16)], fill=(180, 180, 195))
    d.line([(84, 8), (92, 14)], fill=(220, 220, 235), width=1)
    # 下刃
    d.polygon([(72, 28), (76, 28), (88, 32), (92, 38), (84, 44), (76, 36)], fill=(40, 40, 55))
    d.polygon([(72, 29), (76, 29), (86, 32), (90, 36), (84, 41), (76, 35)], fill=(110, 110, 125))
    d.polygon([(74, 32), (84, 34), (90, 36), (84, 40), (76, 36)], fill=(180, 180, 195))
    d.line([(84, 44), (92, 38)], fill=(220, 220, 235), width=1)
    # 中央金屬環
    d.rectangle([70, 22, 78, 26], fill=(180, 130, 30))
    d.rectangle([71, 22, 77, 25], fill=(255, 200, 60))
    return img


def wpn_wand():
    """小魔杖（精緻短杖）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 杖身
    d.rectangle([73, 30, 75, 60], fill=(40, 25, 5))
    d.rectangle([73, 31, 74, 59], fill=(110, 70, 30))
    # 螺旋花紋
    for y in [36, 42, 48, 54]:
        d.point([(73, y)], fill=(80, 50, 20))
        d.point([(75, y+1)], fill=(80, 50, 20))
    # 杖頂金邊
    d.rectangle([70, 26, 78, 30], fill=(180, 130, 30))
    d.rectangle([71, 27, 77, 29], fill=(255, 200, 60))
    # 寶石（粉紅星形）
    d.polygon([(74, 14), (76, 18), (80, 18), (77, 20), (78, 24), (74, 22), (70, 24), (71, 20), (68, 18), (72, 18)],
              fill=(120, 15, 25))
    d.polygon([(74, 16), (76, 19), (78, 19), (76, 20), (77, 23), (74, 21), (71, 23), (72, 20), (70, 19), (72, 19)],
              fill=(220, 30, 100))
    d.polygon([(74, 17), (75, 20), (75, 21), (74, 20)], fill=(255, 100, 200))
    d.point([(74, 19)], fill=(255, 255, 255))
    # 魔法粒子
    d.point([(66, 14)], fill=(255, 200, 200))
    d.point([(82, 14)], fill=(255, 200, 200))
    d.point([(68, 24)], fill=(220, 80, 130))
    d.point([(80, 24)], fill=(220, 80, 130))
    return img


def wpn_umbrella():
    """雨傘（彈幕風武器）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 傘骨架（深色）
    d.polygon([(62, 24), (74, 8), (86, 24)], fill=(40, 40, 55))
    # 傘面（紅黑條紋）
    d.polygon([(64, 24), (74, 10), (84, 24)], fill=(80, 5, 5))
    d.polygon([(65, 24), (74, 12), (83, 24)], fill=(180, 35, 35))
    # 條紋
    d.line([(70, 24), (72, 12)], fill=(80, 5, 5), width=1)
    d.line([(76, 12), (78, 24)], fill=(80, 5, 5), width=1)
    d.line([(74, 12), (74, 24)], fill=(255, 200, 60), width=1)
    # 傘頂尖
    d.point([(74, 8)], fill=(255, 200, 60))
    d.point([(74, 9)], fill=(255, 240, 140))
    # 傘骨末端
    d.point([(64, 24)], fill=(40, 40, 55))
    d.point([(74, 24)], fill=(40, 40, 55))
    d.point([(84, 24)], fill=(40, 40, 55))
    # 傘柄
    d.rectangle([73, 24, 75, 56], fill=(20, 20, 30))
    d.rectangle([73, 25, 74, 55], fill=(110, 70, 30))
    # 把手（彎勾）
    d.line([(74, 56), (78, 60)], fill=(20, 20, 30), width=2)
    d.line([(78, 60), (78, 64)], fill=(20, 20, 30), width=2)
    d.line([(78, 64), (74, 64)], fill=(20, 20, 30), width=2)
    return img


def wpn_fishing_rod():
    """釣竿（鵝鵝最強娛樂武器）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 竿身（從手到上方）
    d.line([(72, 50), (84, 8)], fill=(40, 25, 5), width=2)
    d.line([(73, 50), (84, 10)], fill=(110, 70, 30), width=1)
    d.line([(74, 49), (83, 12)], fill=(150, 100, 50), width=1)
    # 把手
    d.rectangle([70, 50, 78, 64], fill=(80, 5, 5))
    d.rectangle([71, 51, 77, 63], fill=(180, 35, 35))
    # 把手金屬環
    d.rectangle([70, 54, 78, 56], fill=(180, 130, 30))
    d.rectangle([71, 54, 77, 55], fill=(255, 200, 60))
    # 線輪（reel）
    d.ellipse([62, 48, 70, 56], fill=(40, 40, 55))
    d.ellipse([63, 49, 69, 55], fill=(110, 110, 125))
    d.ellipse([64, 50, 68, 54], fill=(180, 130, 30))
    d.point([(66, 52)], fill=(255, 200, 60))
    # 釣魚線（從竿頂垂下）
    d.line([(84, 8), (90, 36)], fill=(180, 180, 195), width=1)
    d.line([(85, 9), (91, 35)], fill=(220, 220, 235), width=1)
    # 魚鉤
    d.line([(90, 36), (92, 40)], fill=(40, 40, 55), width=1)
    d.line([(92, 40), (90, 42)], fill=(40, 40, 55), width=1)
    d.point([(90, 42)], fill=(220, 220, 235))
    # 浮標
    d.ellipse([88, 32, 92, 36], fill=(80, 5, 5))
    d.ellipse([89, 33, 91, 35], fill=(220, 30, 50))
    d.point([(90, 34)], fill=(255, 200, 200))
    return img


# === 5 BODIES ===
def body_ninja():
    """忍者裝（黑衣加紅腰帶）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 黑衣主體
    d.polygon([(28, 58), (24, 80), (60, 82), (66, 58)], fill=(15, 15, 25))
    d.polygon([(30, 60), (26, 78), (58, 80), (64, 60)], fill=(40, 40, 55))
    d.polygon([(32, 62), (28, 76), (56, 78), (62, 62)], fill=(60, 60, 75))
    # 衣領 V 字（白）
    d.polygon([(40, 58), (48, 70), (52, 58)], fill=(15, 15, 25))
    d.polygon([(41, 58), (48, 68), (51, 58)], fill=(180, 180, 195))
    d.polygon([(42, 58), (48, 66), (50, 58)], fill=(245, 245, 252))
    # 紅腰帶（寬）
    d.rectangle([28, 70, 64, 78], fill=(80, 5, 5))
    d.rectangle([29, 70, 63, 77], fill=(180, 35, 35))
    d.rectangle([29, 70, 63, 72], fill=(220, 80, 80))
    # 腰帶結
    d.rectangle([42, 68, 54, 80], fill=(80, 5, 5))
    d.rectangle([43, 69, 53, 79], fill=(180, 35, 35))
    d.line([(44, 71), (52, 71)], fill=(120, 15, 25), width=1)
    d.line([(44, 76), (52, 76)], fill=(120, 15, 25), width=1)
    # 忍者紋章（背後仿，胸前圓圈）
    d.ellipse([45, 62, 51, 68], fill=(15, 15, 25))
    d.ellipse([46, 63, 50, 67], fill=(180, 35, 35))
    d.point([(48, 65)], fill=(255, 200, 60))
    # 護腕（隱約可見）
    d.rectangle([26, 64, 30, 70], fill=(180, 35, 35))
    d.rectangle([62, 64, 66, 70], fill=(180, 35, 35))
    return img


def body_kimono():
    """和服（粉紅櫻花）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主和服（粉紅）
    d.polygon([(28, 58), (24, 82), (66, 84), (62, 58)], fill=(180, 60, 110))
    d.polygon([(30, 60), (26, 80), (64, 82), (60, 60)], fill=(220, 90, 140))
    d.polygon([(32, 62), (28, 78), (62, 80), (58, 62)], fill=(255, 150, 200))
    d.polygon([(34, 64), (32, 74), (58, 76), (56, 64)], fill=(255, 200, 220))
    # V 字交叉領（白）
    d.polygon([(38, 58), (44, 68), (52, 68), (58, 58), (54, 58), (48, 64), (42, 58)], fill=(180, 180, 195))
    d.polygon([(39, 58), (45, 67), (51, 67), (57, 58), (53, 58), (48, 63), (43, 58)], fill=(245, 245, 252))
    # 寬腰帶（金色綁帶）
    d.rectangle([28, 72, 64, 78], fill=(140, 90, 20))
    d.rectangle([29, 72, 63, 77], fill=(220, 160, 60))
    d.rectangle([29, 72, 63, 73], fill=(255, 200, 100))
    # 腰帶結（蝴蝶結在後 -> 模擬大花飾）
    d.polygon([(40, 70), (44, 66), (52, 66), (56, 70), (52, 78), (44, 78)], fill=(120, 60, 5))
    d.polygon([(41, 71), (45, 67), (51, 67), (55, 71), (51, 77), (45, 77)], fill=(255, 200, 60))
    d.ellipse([46, 70, 50, 74], fill=(180, 130, 30))
    d.point([(48, 72)], fill=(255, 240, 140))
    # 櫻花圖案
    for x, y in [(34, 66), (56, 66), (40, 80), (52, 80), (46, 76)]:
        d.point([(x, y)], fill=(255, 255, 255))
        d.point([(x-1, y)], fill=(255, 200, 220))
        d.point([(x+1, y)], fill=(255, 200, 220))
        d.point([(x, y-1)], fill=(255, 200, 220))
        d.point([(x, y+1)], fill=(255, 200, 220))
    return img


def body_beach():
    """海灘短褲 + 比基尼上衣（夏天泳裝鵝）"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 上身：紅色比基尼上衣（小一點）
    d.polygon([(36, 58), (34, 64), (40, 66), (44, 62)], fill=(80, 5, 5))
    d.polygon([(37, 59), (35, 63), (39, 65), (43, 62)], fill=(220, 30, 50))
    d.polygon([(52, 62), (56, 66), (62, 64), (60, 58)], fill=(80, 5, 5))
    d.polygon([(53, 62), (56, 65), (61, 64), (59, 59)], fill=(220, 30, 50))
    # 比基尼帶
    d.line([(40, 58), (38, 56)], fill=(80, 5, 5), width=1)
    d.line([(56, 58), (58, 56)], fill=(80, 5, 5), width=1)
    d.line([(44, 62), (52, 62)], fill=(80, 5, 5), width=1)
    # 黃色波浪海灘短褲
    d.polygon([(28, 68), (26, 82), (66, 82), (64, 68)], fill=(140, 90, 5))
    d.polygon([(30, 70), (28, 80), (64, 80), (62, 70)], fill=(220, 160, 30))
    d.polygon([(32, 72), (30, 78), (62, 78), (60, 72)], fill=(255, 200, 60))
    # 波浪花紋
    for y, x_start in [(72, 32), (76, 32)]:
        for i in range(0, 30, 6):
            cx = x_start + i
            d.line([(cx, y), (cx+2, y-2), (cx+4, y), (cx+6, y-2)], fill=(60, 130, 240), width=1)
    # 短褲腰帶
    d.rectangle([28, 68, 64, 70], fill=(60, 30, 5))
    d.point([(46, 69)], fill=(255, 255, 255))
    d.point([(50, 69)], fill=(255, 255, 255))
    return img


def body_doctor():
    """醫生白袍 + 聽診器"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 白袍主體
    d.polygon([(28, 58), (24, 82), (66, 84), (62, 58)], fill=(180, 180, 195))
    d.polygon([(30, 60), (26, 80), (64, 82), (60, 60)], fill=(220, 220, 235))
    d.polygon([(32, 62), (28, 78), (62, 80), (58, 62)], fill=(245, 245, 252))
    d.polygon([(32, 62), (30, 76), (60, 78), (58, 62)], fill=(255, 255, 255))
    # 領口
    d.polygon([(40, 58), (44, 64), (52, 64), (56, 58)], fill=(180, 180, 195))
    d.polygon([(41, 58), (45, 63), (51, 63), (55, 58)], fill=(245, 245, 252))
    # 鈕扣排
    for cy in [66, 70, 74]:
        d.ellipse([46, cy-1, 50, cy+2], fill=(40, 40, 55))
        d.point([(48, cy)], fill=(180, 180, 195))
    # 胸前口袋（藍）
    d.rectangle([34, 66, 42, 72], fill=(20, 50, 130))
    d.rectangle([35, 67, 41, 71], fill=(60, 130, 240))
    # 口袋上的筆
    d.rectangle([36, 64, 38, 70], fill=(20, 0, 30))
    d.point([(37, 64)], fill=(220, 30, 50))
    # 聽診器（V 形，從脖子到胸前）
    d.line([(40, 58), (44, 70)], fill=(20, 20, 30), width=2)
    d.line([(56, 58), (52, 70)], fill=(20, 20, 30), width=2)
    d.line([(41, 58), (45, 70)], fill=(40, 40, 55), width=1)
    d.line([(55, 58), (51, 70)], fill=(40, 40, 55), width=1)
    # 聽診器圓盤
    d.ellipse([44, 70, 52, 76], fill=(40, 40, 55))
    d.ellipse([45, 71, 51, 75], fill=(110, 110, 125))
    d.ellipse([46, 72, 50, 74], fill=(180, 180, 195))
    # 醫療紅十字（胸口）
    d.rectangle([55, 66, 59, 72], fill=(220, 30, 50))
    d.rectangle([53, 68, 61, 70], fill=(220, 30, 50))
    return img


def body_tuxedo():
    """燕尾服紳士裝"""
    img = new_layer()
    d = ImageDraw.Draw(img)
    # 主黑色燕尾服
    d.polygon([(28, 58), (24, 82), (66, 84), (62, 58)], fill=(15, 15, 25))
    d.polygon([(30, 60), (26, 80), (64, 82), (60, 60)], fill=(40, 40, 55))
    d.polygon([(32, 62), (28, 78), (62, 80), (58, 62)], fill=(60, 60, 75))
    # 翻領（深色）
    d.polygon([(40, 58), (32, 80), (40, 76), (44, 64)], fill=(15, 15, 25))
    d.polygon([(41, 58), (35, 76), (40, 74), (44, 65)], fill=(80, 80, 95))
    d.polygon([(56, 58), (64, 80), (56, 76), (52, 64)], fill=(15, 15, 25))
    d.polygon([(55, 58), (61, 76), (56, 74), (52, 65)], fill=(80, 80, 95))
    # 白襯衫（中央 V 區）
    d.polygon([(44, 58), (44, 78), (52, 78), (52, 58)], fill=(180, 180, 195))
    d.polygon([(45, 58), (45, 77), (51, 77), (51, 58)], fill=(245, 245, 252))
    # 黑領結
    d.polygon([(44, 58), (42, 56), (42, 64), (44, 62), (52, 62), (54, 64), (54, 56), (52, 58)],
              fill=(15, 15, 25))
    d.polygon([(43, 57), (43, 63), (45, 61), (51, 61), (53, 63), (53, 57)], fill=(40, 40, 55))
    d.point([(48, 60)], fill=(80, 80, 95))
    # 鈕扣（金）
    d.ellipse([47, 68, 49, 70], fill=(180, 130, 30))
    d.point([(48, 69)], fill=(255, 200, 60))
    d.ellipse([47, 72, 49, 74], fill=(180, 130, 30))
    d.point([(48, 73)], fill=(255, 200, 60))
    # 紅花胸針
    d.ellipse([35, 64, 41, 70], fill=(80, 5, 5))
    d.ellipse([36, 65, 40, 69], fill=(220, 30, 50))
    d.ellipse([37, 66, 39, 68], fill=(255, 100, 100))
    d.point([(38, 67)], fill=(255, 255, 200))
    return img


# === Main ===
if __name__ == '__main__':
    import sys
    log = sys.stderr

    log.write('Hats:\n')
    for n, fn in [('hat_top_hat', hat_top_hat), ('hat_straw', hat_straw),
                  ('hat_bunny_ears', hat_bunny_ears), ('hat_pumpkin', hat_pumpkin),
                  ('hat_halo_dark', hat_halo_dark)]:
        save(fn(), HEAD, n)
        log.write(f'  {n}\n')

    log.write('Weapons:\n')
    for n, fn in [('wpn_dagger', wpn_dagger), ('wpn_warhammer', wpn_warhammer),
                  ('wpn_axe', wpn_axe), ('wpn_wand', wpn_wand),
                  ('wpn_umbrella', wpn_umbrella), ('wpn_fishing_rod', wpn_fishing_rod)]:
        save(fn(), HAND_R, n)
        log.write(f'  {n}\n')

    log.write('Bodies:\n')
    for n, fn in [('body_ninja', body_ninja), ('body_kimono', body_kimono),
                  ('body_beach', body_beach), ('body_doctor', body_doctor),
                  ('body_tuxedo', body_tuxedo)]:
        save(fn(), BODY, n)
        log.write(f'  {n}\n')

    log.write('\nALL EXTRA-2 DONE\n')
