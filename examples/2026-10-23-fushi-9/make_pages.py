# -*- coding: utf-8 -*-
"""6个月辅食9样 · 9页成品合成：AI无字底图 + PIL中文排版 1080x1440"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE = "/home/hatch/workspace/xiaohongshu/2026-10-23-fushi-9/base/"
OUT = "/home/hatch/workspace/xiaohongshu/2026-10-23-fushi-9/"
W, H = 1080, 1440
KUAILE = "/home/hatch/workspace/fonts/ZCOOLKuaiLe.ttf"
MASHAN = "/home/hatch/workspace/fonts/MaShanZheng.ttf"

BROWN = (74, 52, 40)
DBROWN = (56, 38, 28)
ORANGE = (222, 118, 47)
GREEN = (110, 142, 96)
CREAM = (250, 245, 236)
GRAYB = (120, 104, 92)

def F(font, size):
    return ImageFont.truetype(font, size)

def fit_crop(img, tw, th, cx=0.5, cy=0.5):
    iw, ih = img.size
    r = tw / th
    if iw / ih > r:
        cw = int(ih * r); ch = ih
    else:
        cw = iw; ch = int(iw / r)
    x0 = int(min(max(cx * iw - cw / 2, 0), iw - cw))
    y0 = int(min(max(cy * ih - ch / 2, 0), ih - ch))
    return img.crop((x0, y0, x0 + cw, y0 + ch)).resize((tw, th), Image.LANCZOS)

def grain(img, amt=6):
    noise = Image.effect_noise(img.size, 12).convert("L")
    img = img.convert("RGB")
    return Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.03)

def sharpen(img):
    return ImageEnhance.Sharpness(img).enhance(1.25)

def text(draw, xy, s, font, fill=BROWN, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)

def chip(base, xy, s, font, fill=(255, 252, 246), tcol=BROWN, pad=18, alpha=235):
    d = ImageDraw.Draw(base)
    tw = d.textlength(s, font=font)
    th = font.size * 1.5
    x, y = xy
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([x, y, x + tw + pad * 2, y + th], radius=22, fill=fill + (alpha,))
    base.alpha_composite(ov)
    d = ImageDraw.Draw(base)
    d.text((x + pad, y + th / 2), s, font=font, fill=tcol, anchor="lm")
    return (x, y, x + tw + pad * 2, y + th)

def arrow(draw, p0, p1, col=(160, 90, 50), wdt=5):
    draw.line([p0, p1], fill=col, width=wdt)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for da in (2.6, -2.6):
        draw.line([p1, (p1[0] + 26 * math.cos(ang + da), p1[1] + 26 * math.sin(ang + da))], fill=col, width=wdt)

def star(draw, cx, cy, r, fill=(232, 145, 42)):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)

SHEET = Image.open(BASE + "media-generation-sheet4-0-1923c812-e93b-4d15-b4e8-a42954f850eb.webp").convert("RGB")
COVER = Image.open(BASE + "media-generation-cover-0-b29c9eca-6297-4858-817e-c4e57ba245b4.webp").convert("RGB")
GRID = Image.open(BASE + "media-generation-grid9-0-6abb2c8b-1030-4993-8f6d-4327b4daa341.webp").convert("RGB")
FEED = Image.open(BASE + "media-generation-feeding-0-08b6d24c-23ed-4d69-abd7-4d70e1909dff.webp").convert("RGB")

TL = SHEET.crop((0, 0, 960, 640))       # 餐桌全景（备用）
TR = SHEET.crop((960, 0, 1920, 640))    # 买多整理
BL = SHEET.crop((0, 640, 960, 1280))    # 超市
BR = SHEET.crop((960, 640, 1920, 1280)) # 厨房制作

# ---------------- P1 封面 ----------------
p = fit_crop(COVER, W, H, cx=0.5, cy=0.45).convert("RGBA")
d = ImageDraw.Draw(p)
hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
hd.rounded_rectangle([118, 372, 962, 464], radius=26, fill=(255, 214, 130, 150))
p.alpha_composite(hl); d = ImageDraw.Draw(p)
text(d, (W / 2, 92), "6个月开始辅食", F(KUAILE, 92), DBROWN, "ma")
text(d, (W / 2, 214), "别急着买一堆！", F(KUAILE, 110), ORANGE, "ma")
text(d, (W / 2, 384), "真正高频的其实就这9样", F(KUAILE, 78), DBROWN, "ma")
d.line([(300, 496), (780, 490)], fill=ORANGE, width=7)
chip(p, (64, 1300), "先存下来，买之前照着看一遍", F(MASHAN, 40))
p.convert("RGB").save(OUT + "p1.jpg", quality=90)

# ---------------- P2 为什么买多 ----------------
p = Image.new("RGBA", (W, H), CREAM + (255,))
d = ImageDraw.Draw(p)
text(d, (64, 62), "刚开始辅食，真的很容易买多", F(KUAILE, 62), DBROWN)
text(d, (64, 148), "桌上这一堆，一大半是当时「怕不够用」囤的", F(MASHAN, 40), GRAYB)
photo = TR.resize((1080, 720), Image.LANCZOS)
p.alpha_composite(photo.convert("RGBA"), (0, 400))
d = ImageDraw.Draw(p)
# 标注（照片区 y 400-1120；照片内坐标换算：x*1080/960 不变比例缩放 1.125）
notes = [
    ((36, 268), "这个后面再买", (215, 560)),     # 纸箱
    (("R", 268), "小瓶小罐，这个看需求", (880, 700)),  # 罐子
    ((36, 1180), "模具，这个先不用急", (470, 880)),    # 模具
    (("R", 1180), "碗和勺，这个真的高频", (700, 1010)), # 碗勺
]
_tmpd = ImageDraw.Draw(p)
for (nx, ny), s, tgt in notes:
    if nx == "R":
        wdt = _tmpd.textlength(s, font=F(MASHAN, 40)) + 36
        nx = int(W - 36 - wdt)
    box = chip(p, (nx, ny), s, F(MASHAN, 40))
    d = ImageDraw.Draw(p)
    sx = box[0] + (box[2] - box[0]) / 2
    sy = box[1] + (box[3] - box[1]) / 2
    start = (sx, box[3] + 6) if ny < 600 else (sx, box[1] - 6)
    arrow(d, start, tgt)
text(d, (64, 1330), "真正每天反复用的，其实没那么多", F(MASHAN, 42), BROWN)
p.convert("RGB").save(OUT + "p2.jpg", quality=90)

# ---------------- P3 九宫格 ----------------
p = Image.new("RGBA", (W, H), CREAM + (255,))
d = ImageDraw.Draw(p)
text(d, (W / 2, 44), "6个月辅食高频用品｜9宫格", F(KUAILE, 60), DBROWN, "ma")
text(d, (W / 2, 122), "都是每天会碰到的东西，不用一次买贵买全", F(MASHAN, 37), GRAYB, "ma")
g = GRID.resize((1080, 1080), Image.LANCZOS).convert("RGBA")
p.alpha_composite(g, (0, 196))
d = ImageDraw.Draw(p)
cells = [
    ("辅食碗", "吸盘底，不容易掀翻"), ("辅食勺", "软头小勺，喂入口刚好"), ("防水围兜", "有兜兜，掉的能接住"),
    ("宝宝餐椅", "能独坐后用，系好安全带"), ("辅食剪", "食物剪小块，防呛噎"), ("储存盒", "多做一点，分装冷冻"),
    ("小毛巾", "擦嘴擦手，消耗最快"), ("防水罩衣", "怕脏再入，看需求"), ("制作工具", "蒸锅＋料理棒就够"),
]
cell = 360
for i, (name, use) in enumerate(cells):
    r, c = divmod(i, 3)
    x0, y0 = c * cell, 196 + r * cell
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rectangle([x0, y0 + cell - 92, x0 + cell, y0 + cell], fill=(255, 252, 246, 225))
    p.alpha_composite(ov)
    d = ImageDraw.Draw(p)
    d.ellipse([x0 + 14, y0 + cell - 82, x0 + 58, y0 + cell - 38], fill=ORANGE)
    text(d, (x0 + 36, y0 + cell - 60), str(i + 1), F(KUAILE, 30), (255, 255, 255), "mm")
    text(d, (x0 + 72, y0 + cell - 76), name, F(KUAILE, 35), DBROWN)
    text(d, (x0 + 72, y0 + cell - 38), use, F(MASHAN, 27), GRAYB)
text(d, (W / 2, 1300), "每一格都是一张真实生活里的小照片", F(MASHAN, 36), GRAYB, "ma")
p.convert("RGB").save(OUT + "p3.jpg", quality=90)

# ---------------- P4 优先级 ----------------
p = Image.new("RGBA", (W, H), CREAM + (255,))
d = ImageDraw.Draw(p)
text(d, (64, 52), "如果预算有限，先买什么？", F(KUAILE, 64), DBROWN)
band = fit_crop(BR, 1080, 360, cx=0.5, cy=0.4)
p.alpha_composite(band.convert("RGBA"), (0, 148))
tiers = [
    ("优先准备", ORANGE, "辅食碗、勺、围兜、餐椅、小毛巾等清洁用品", "每天都要用，先把这几样备齐"),
    ("看需求购买", GREEN, "辅食剪、储存盒、制作工具", "看家里吃饭的节奏，再慢慢补也不迟"),
    ("真的不用急着囤", GRAYB, "大量辅食模具、一堆小瓶小盒、复杂的「辅食神器」", "用不上几个，先别被颜值带跑"),
]
y = 540
for title, col, items, note in tiers:
    d.rounded_rectangle([64, y, 1016, y + 240], radius=26, fill=(255, 255, 255), outline=col, width=3)
    d.rounded_rectangle([64, y, 384, y + 66], radius=26, fill=col)
    text(d, (224, y + 33), title, F(KUAILE, 38), (255, 255, 255), "mm")
    text(d, (92, y + 108), items, F(MASHAN, 39), BROWN)
    text(d, (92, y + 182), note, F(MASHAN, 33), GRAYB)
    y += 262
text(d, (64, y + 2), "每个家庭情况不一样，按自己家的节奏来就行", F(MASHAN, 38), BROWN)
p.convert("RGB").save(OUT + "p4.jpg", quality=90)

# ---------------- P5 超市 ----------------
p = sharpen(grain(fit_crop(BL, W, H, cx=0.55, cy=0.5))).convert("RGBA")
d = ImageDraw.Draw(p)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(ov).rectangle([0, 0, W, 240], fill=(40, 28, 20, 90))
p.alpha_composite(ov); d = ImageDraw.Draw(p)
text(d, (W / 2, 66), "看到这些，真的很容易买上头", F(KUAILE, 66), (255, 255, 255), "ma")
tags = ["买之前先想想使用频率", "不是「宝宝专用」就一定更好", "先买高频的"]
ty = 1120
for t in tags:
    tw = d.textlength(t, font=F(MASHAN, 42))
    chip(p, ((W - tw - 36) / 2, ty), t, F(MASHAN, 42))
    ty += 96
p.convert("RGB").save(OUT + "p5.jpg", quality=90)

# ---------------- P6 先别囤 ----------------
p = Image.new("RGBA", (W, H), CREAM + (255,))
band = fit_crop(TR, 1080, 560, cx=0.5, cy=0.55)
p.alpha_composite(band.convert("RGBA"), (0, 0))
d = ImageDraw.Draw(p)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(ov).rectangle([0, 430, W, 560], fill=(250, 245, 236, 200))
p.alpha_composite(ov); d = ImageDraw.Draw(p)
text(d, (64, 452), "这些我反而建议先别囤", F(KUAILE, 62), DBROWN)
rows = [
    ("成套辅食模具", "刚开始吃的是泥糊，造型暂时还用不上"),
    ("小分装瓶一买一打", "一顿吃不了几口，先有几个够用就行"),
    ("花哨小工具全套", "感温勺、各种杯子，属于加分项，不是第一顺位"),
    ("专门的大件辅食机", "家里有蒸锅＋料理棒的话，可以先缓一缓"),
]
y = 620
for name, why in rows:
    d.ellipse([70, y + 16, 92, y + 38], fill=ORANGE)
    text(d, (116, y), name, F(KUAILE, 46), DBROWN)
    text(d, (116, y + 62), why, F(MASHAN, 38), GRAYB)
    y += 168
d.rounded_rectangle([64, y + 6, 1016, y + 96], radius=22, fill=(255, 238, 220))
text(d, (W / 2, y + 51), "不是不能买，是刚开始真的用不了这么多", F(MASHAN, 40), BROWN, "mm")
p.convert("RGB").save(OUT + "p6.jpg", quality=90)

# ---------------- P7 使用场景 ----------------
p = fit_crop(FEED, W, H, cx=0.4, cy=0.45).convert("RGBA")
grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grad)
for i in range(300):
    gd.line([(0, H - 300 + i), (W, H - 300 + i)], fill=(30, 20, 14, int(150 * i / 300)))
p.alpha_composite(grad); d = ImageDraw.Draw(p)
text(d, (W / 2, H - 218), "真正高频的东西", F(MASHAN, 52), (255, 255, 255), "ma")
text(d, (W / 2, H - 148), "往往就是每天反复用的这几样", F(MASHAN, 52), (255, 255, 255), "ma")
p.convert("RGB").save(OUT + "p7.jpg", quality=90)

# ---------------- P8 收藏总结 ----------------
p = Image.new("RGBA", (W, H), CREAM + (255,))
d = ImageDraw.Draw(p)
text(d, (W / 2, 58), "6个月辅食用品精简版", F(KUAILE, 68), DBROWN, "ma")
text(d, (W / 2, 140), "截图存下来，买之前对一遍", F(MASHAN, 38), GRAYB, "ma")
secs = [
    (5, "优先准备", ORANGE, ["辅食碗 ＋ 辅食勺", "防水围兜", "宝宝餐椅", "小毛巾 / 棉柔巾"]),
    (4, "看需求", GREEN, ["辅食剪", "储存盒", "防水罩衣", "制作工具（先用家里现成的）"]),
    (3, "后面再买", GRAYB, ["辅食模具", "多余的小瓶小盒", "复杂的「辅食神器」"]),
]
y = 226
for n, title, col, items in secs:
    hh = 96 + len(items) * 74
    d.rounded_rectangle([64, y, 1016, y + hh], radius=26, fill=(255, 255, 255), outline=col, width=3)
    for i in range(n):
        star(d, 116 + i * 52, y + 52, 20, fill=col if col != GRAYB else (178, 150, 110))
    text(d, (404, y + 52), title, F(KUAILE, 44), DBROWN, "lm")
    iy = y + 108
    for it in items:
        d.ellipse([92, iy + 20, 106, iy + 34], fill=col)
        text(d, (124, iy), it, F(MASHAN, 44), BROWN)
        iy += 74
    y += hh + 34
text(d, (W / 2, y + 8), "使用频率比颜值重要，先买每天要用的", F(MASHAN, 40), BROWN, "ma")
p.convert("RGB").save(OUT + "p8.jpg", quality=90)

# ---------------- P9 互动 ----------------
p = fit_crop(FEED, W, H, cx=0.78, cy=0.55).convert("RGBA")
d = ImageDraw.Draw(p)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
od.rounded_rectangle([70, 480, 1010, 830], radius=30, fill=(255, 252, 246, 235))
p.alpha_composite(ov); d = ImageDraw.Draw(p)
text(d, (W / 2, 540), "你家宝宝开始辅食以后", F(KUAILE, 56), DBROWN, "ma")
text(d, (W / 2, 622), "最后发现哪个东西最常用？", F(KUAILE, 56), ORANGE, "ma")
text(d, (W / 2, 716), "想看看大家真实使用率最高的是哪一个", F(MASHAN, 38), GRAYB, "ma")
p.convert("RGB").save(OUT + "p9.jpg", quality=90)

print("all pages done")
