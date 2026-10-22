# -*- coding: utf-8 -*-
"""
小红书笔记《生完孩子才发现，真正累的不是带娃》排版脚本
栏目：④情绪故事感 + ①真实生活摄影感（全摄影底图 + PIL 精准排字，逐页不同版式）
成品：1080x1440 (3:4)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "examples", "mama-mental-load"))
W, H = 1080, 1440

SERIF_B = ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", 2)
SERIF_R = ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 2)
SANS_R = ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2)
HAND = (os.path.expanduser("~/workspace/fonts/MaShanZheng.ttf"), 0)

BROWN = (74, 56, 38)        # 暖棕（浅底大字）
BROWN_SOFT = (107, 84, 62)  # 柔棕（小字）
CREAM = (255, 248, 236)     # 暖白（深底大字）
CREAM_SOFT = (240, 228, 205)


def font(spec, size):
    path, idx = spec
    return ImageFont.truetype(path, size, index=idx)


def load(name):
    im = Image.open(os.path.join(BASE, "assets", name)).convert("RGB")
    return im.resize((W, H), Image.LANCZOS)


def t(draw, xy, s, f, fill, shadow=None, soff=(2, 3), anchor="la", spacing=0):
    x, y = xy
    if shadow:
        draw.text((x + soff[0], y + soff[1]), s, font=f, fill=shadow, anchor=anchor, spacing=spacing)
    draw.text((x, y), s, font=f, fill=fill, anchor=anchor, spacing=spacing)


def rotated_text(img, center, s, f, fill, angle):
    tile = Image.new("RGBA", (1000, 160), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.text((500, 80), s, font=f, fill=fill + (255,), anchor="mm")
    tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(tile, (int(center[0] - tile.width / 2), int(center[1] - tile.height / 2)), tile)


def vgrad(img, y0, y1, color, amax, from_top=False):
    """竖向渐变罩：用 1px 宽竖条拉伸，避免条纹"""
    strip = Image.new("RGBA", (1, H), (0, 0, 0, 0))
    px = strip.load()
    for y in range(H):
        if from_top:
            a = int(amax * max(0.0, 1 - (y - y0) / max(1, (y1 - y0)))) if y < y1 else 0
        else:
            a = int(amax * max(0.0, (y - y0) / max(1, (y1 - y0)))) if y > y0 else 0
        px[0, y] = color + (a,)
    ov = strip.resize((W, H))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


# ---------------- P1：封面（上方暖墙大字 + 手写小字） ----------------
def page1():
    im = load("p1_base.webp")
    d = ImageDraw.Draw(im)
    f_big = font(SERIF_B, 94)
    t(d, (70, 88), "生完孩子才发现", f_big, BROWN)
    t(d, (70, 206), "真正累的不是带娃", f_big, BROWN)
    t(d, (74, 344), "是脑子里永远有一件事没做完。", font(HAND, 42), (96, 72, 48))
    im.save(os.path.join(BASE, "p1.png"))


# ---------------- P2：杂志式散排（左墙留白） ----------------
def page2():
    im = load("p2_base.webp")
    d = ImageDraw.Draw(im)
    f_big = font(SERIF_B, 96)
    t(d, (72, 84), "他是不是", f_big, BROWN)
    t(d, (72, 200), "哪里不正常？", f_big, BROWN)
    f_s = font(SERIF_R, 34)
    items = [("吃得少", (150, 520), -3), ("睡不好", (205, 640), 2),
             ("还不会走", (140, 760), -2), ("晚上总醒", (215, 880), 3),
             ("别人家的宝宝，又学会新东西了", (218, 1030), -2)]
    for s, c, a in items:
        fs = font(SERIF_R, 29) if len(s) > 5 else f_s
        rotated_text(im, c, s, fs, BROWN_SOFT, a)
    im.save(os.path.join(BASE, "p2.png"))


# ---------------- P3：深夜刷手机（顶部大字 + 右侧手写搜索词） ----------------
def page3():
    im = load("p3_base.webp")
    d = ImageDraw.Draw(im)
    f_big = font(SERIF_B, 88)
    sh = (10, 16, 26)
    t(d, (76, 92), "宝宝睡了，", f_big, CREAM, shadow=sh)
    t(d, (76, 204), "妈妈却没睡。", f_big, CREAM, shadow=sh)
    f_h = font(HAND, 46)
    qs = [("「几个月翻身？」", (415, 438), -2), ("「一天吃多少？」", (430, 570), 2),
          ("「总翻身正常吗？」", (408, 674), -1)]
    for s, c, a in qs:
        rotated_text(im, c, s, f_h, CREAM_SOFT, a)
    d = ImageDraw.Draw(im)
    t(d, (716, 742), "越搜，越焦虑。", font(HAND, 34), (206, 188, 160))
    im.save(os.path.join(BASE, "p3.png"))


# ---------------- P4：暖阳抱抱（底部地板留白大字） ----------------
def page4():
    im = load("p4_base.webp")
    im = vgrad(im, 980, 1440, (255, 244, 224), 110)
    d = ImageDraw.Draw(im)
    f = font(SERIF_B, 60)
    t(d, (70, 1148), "后来才发现，", f, BROWN)
    t(d, (70, 1240), "孩子真的不需要100分的妈妈。", font(SERIF_B, 57), BROWN)
    im.save(os.path.join(BASE, "p4.png"))


# ---------------- P5：喂饭图（上方大留白，四行小字） ----------------
def page5():
    im = load("p5_base.webp")
    d = ImageDraw.Draw(im)
    f = font(SERIF_R, 47)
    lines = [("有人抱抱他，", 96), ("有人陪他吃饭，", 128),
             ("有人在他摔倒时说「没关系」，", 96), ("有人在他害怕时，站在身边。", 128)]
    y = 150
    for s, x in lines:
        t(d, (x, y), s, f, (90, 70, 50))
        y += 108
    im.save(os.path.join(BASE, "p5.png"))


# ---------------- P6：牵手背影收尾（底部渐变罩 + 白字） ----------------
def page6():
    im = load("p6_base.webp")
    im = vgrad(im, 900, 1440, (43, 32, 22), 165)
    d = ImageDraw.Draw(im)
    f_big = font(SERIF_B, 74)
    sh = (30, 22, 14)
    t(d, (540, 1062), "养孩子没有标准答案。", f_big, CREAM, shadow=sh, anchor="ma")
    t(d, (540, 1168), "妈妈也不用每天考试。", f_big, CREAM, shadow=sh, anchor="ma")
    t(d, (540, 1300), "如果你也有过这种感觉，评论区告诉我。", font(HAND, 36), CREAM_SOFT, shadow=sh, anchor="ma")
    im.save(os.path.join(BASE, "p6.png"))


if __name__ == "__main__":
    page1(); page2(); page3(); page4(); page5(); page6()
    print("done p1-p6")
