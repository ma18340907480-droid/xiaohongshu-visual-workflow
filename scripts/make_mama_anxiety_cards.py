# -*- coding: utf-8 -*-
"""
小红书高收藏知识卡《带娃最累的不是身体》——「妈妈安心指南 · 01」
内容全部来自原文《生完孩子才发现，真正累的不是带娃》，不新增知识点。
视觉：奶油底 + 圆角白卡 + 暖棕字 + 浅橙强调；逐页版式不同（封面照片/结论卡/清单卡/
深夜搜索页/照片陪伴页/误区对照/Checklist）。成品 1080x1440 (3:4)。
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "examples", "mama-anxiety-cards"))
W, H = 1080, 1440

BG = (251, 245, 234)
INK = (74, 56, 38)
SOFT = (122, 98, 72)
ORANGE = (198, 102, 32)
ORANGE_MID = (222, 130, 52)
ORANGE_SOFT = (253, 235, 217)
CARD = (255, 255, 255)
SHADOW = (240, 228, 206)
CREAM = (255, 248, 236)
CREAM_SOFT = (238, 224, 198)
GREEN = (125, 155, 87)
RED = (192, 91, 60)
DARK_BG = (43, 36, 30)
DARK_BAR = (70, 59, 49)

KUAILE = os.path.expanduser("~/workspace/fonts/ZCOOLKuaiLe.ttf")
HAND = os.path.expanduser("~/workspace/fonts/MaShanZheng.ttf")
SANS_B = ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 2)
SANS_R = ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2)


def F(path, size):
    return ImageFont.truetype(path, size)


def FS(spec, size):
    return ImageFont.truetype(spec[0], size, index=spec[1])


def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def card(img, box, r=28, fill=CARD):
    d = ImageDraw.Draw(img)
    rr(d, (box[0], box[1] + 8, box[2], box[3] + 8), r, fill=SHADOW)
    rr(d, box, r, fill=fill)
    return d


def series_pill(img, dark=False):
    d = ImageDraw.Draw(img, "RGBA")
    f = FS(SANS_B, 26)
    s = "妈妈安心指南 · 01"
    tw = d.textlength(s, font=f)
    rr(d, (64, 58, 64 + tw + 44, 58 + 52), 26, fill=ORANGE_SOFT if not dark else (70, 59, 49))
    d.text((64 + 22, 58 + 10), s, font=f, fill=ORANGE if not dark else CREAM_SOFT)


def header(img, title, sub=None, tsize=58):
    series_pill(img)
    d = ImageDraw.Draw(img)
    d.text((64, 138), title, font=F(KUAILE, tsize), fill=INK)
    if sub:
        d.text((66, 138 + tsize + 22), sub, font=FS(SANS_R, 28), fill=SOFT)


def check(d, cx, cy, r, color):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    s = r * 0.52
    d.line((cx - s, cy + 1, cx - s * 0.25, cy + s * 0.75), fill=(255, 255, 255), width=7)
    d.line((cx - s * 0.25, cy + s * 0.75, cx + s * 1.05, cy - s * 0.7), fill=(255, 255, 255), width=7)


def cross(d, cx, cy, r, color):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    s = r * 0.45
    d.line((cx - s, cy - s, cx + s, cy + s), fill=(255, 255, 255), width=7)
    d.line((cx - s, cy + s, cx + s, cy - s), fill=(255, 255, 255), width=7)


# ---------------- P1 封面 ----------------
def page1():
    im = Image.open(os.path.join(BASE, "assets/photo_p1.webp")).convert("RGB").resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.text((72, 118), "带娃最累的", font=F(KUAILE, 118), fill=INK)
    d.text((72, 256), "不是身体", font=F(KUAILE, 118), fill=ORANGE)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle((64, 56, 64 + 252, 108), radius=26, fill=(255, 251, 240, 225))
    od.text((86, 66), "妈妈安心指南 · 01", font=FS(SANS_B, 26), fill=INK)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    box = (72, 1176, 1008, 1340)
    rr(d, box, 30, fill=(255, 252, 245))
    d.text((108, 1204), "是脑子里，永远有一件事没做完", font=FS(SANS_B, 36), fill=INK)
    d.text((108, 1262), "写给每一个总怕自己做错的新手妈妈", font=FS(SANS_R, 28), fill=SOFT)
    im.save(os.path.join(BASE, "p1.png"))


# ---------------- P2 核心结论 ----------------
def page2():
    im = Image.new("RGB", (W, H), BG)
    header(im, "先记住这几句", "只看这一张，也能把心放下一半。")
    rows = [("1", "累的不只是身体，", "是脑子一刻停不下来"),
            ("2", "总怕做错，", "是因为你太在意他"),
            ("3", "孩子不需要", "100分的妈妈"),
            ("4", "没有标准答案，", "妈妈不用每天考试")]
    y = 330
    for n, l1, l2 in rows:
        d = card(im, (64, y, 1016, y + 196))
        d.ellipse((100, y + 58, 180, y + 138), fill=ORANGE_MID)
        d.text((140, y + 76), n, font=F(KUAILE, 46), fill=(255, 255, 255), anchor="ma")
        d.text((216, y + 38), l1, font=FS(SANS_B, 37), fill=INK)
        d.text((216, y + 96), l2, font=FS(SANS_B, 37), fill=INK)
        y += 196 + 26
    d = ImageDraw.Draw(im)
    d.text((540, y + 16), "这一张，先存下来。", font=F(HAND, 36), fill=SOFT, anchor="ma")
    im.save(os.path.join(BASE, "p2.png"))


# ---------------- P3 脑内待办清单 ----------------
def page3():
    im = Image.new("RGB", (W, H), BG)
    header(im, "妈妈的脑子里，装着多少事", None, tsize=52)
    rows = [("奶", (222, 130, 52), "吃饭的事", "奶粉还剩多少，今天辅食做什么"),
            ("睡", (232, 178, 76), "睡觉的事", "晚上又醒了，睡得够不够"),
            ("穿", (198, 152, 102), "穿衣的事", "出门穿这件，会不会冷"),
            ("医", (214, 120, 88), "健康的事", "疫苗的日子别错过，吃得少要不要紧"),
            ("比", (168, 132, 94), "比较的事", "别人家的宝宝，好像又快了一步")]
    y = 268
    for ch, color, label, desc in rows:
        d = card(im, (64, y, 1016, y + 168))
        d.ellipse((96, y + 38, 188, y + 130), fill=color)
        d.text((142, y + 56), ch, font=F(KUAILE, 46), fill=(255, 255, 255), anchor="ma")
        d.text((220, y + 34), label, font=FS(SANS_B, 36), fill=INK)
        d.text((220, y + 92), desc, font=FS(SANS_R, 30), fill=SOFT)
        y += 168 + 22
    d = ImageDraw.Draw(im)
    rr(d, (64, y + 6, 1016, y + 96), 24, fill=ORANGE_SOFT)
    d.text((540, y + 32), "不是事情太多，是每一件都放不下。", font=FS(SANS_B, 31), fill=INK, anchor="ma")
    im.save(os.path.join(BASE, "p3.png"))


# ---------------- P4 深夜搜索 ----------------
def page4():
    im = Image.new("RGB", (W, H), DARK_BG)
    series_pill(im, dark=True)
    d = ImageDraw.Draw(im)
    d.text((64, 138), "宝宝睡了，妈妈在搜什么", font=F(KUAILE, 56), fill=CREAM)
    qs = ["宝宝几个月会翻身？", "宝宝一天吃多少算够？", "睡觉总翻来覆去，正常吗？", "还不会走路，要紧吗？"]
    y = 268
    for q in qs:
        rr(d, (64, y, 1016, y + 106), 53, fill=DARK_BAR)
        d.ellipse((112, y + 32, 152, y + 72), outline=CREAM_SOFT, width=5)
        d.line((146, y + 66, 166, y + 86), fill=CREAM_SOFT, width=6)
        d.text((196, y + 32), q, font=FS(SANS_R, 35), fill=CREAM)
        y += 106 + 26
    d.text((66, y + 8), "越搜，越清醒；越搜，越焦虑。", font=F(HAND, 42), fill=(238, 205, 155))
    box = (64, 1010, 1016, 1352)
    d = card(im, box)
    d.text((104, 1052), "搜到的答案，", font=FS(SANS_B, 36), fill=INK)
    d.text((104, 1108), "没有一个适合所有宝宝。", font=FS(SANS_B, 36), fill=INK)
    d.text((104, 1184), "每个宝宝，都有自己的节奏。", font=FS(SANS_R, 31), fill=SOFT)
    d.text((104, 1240), "夜深了，先放下手机——你也需要睡觉。", font=FS(SANS_R, 31), fill=SOFT)
    im.save(os.path.join(BASE, "p4.png"))


# ---------------- P5 孩子真正需要的 ----------------
def page5():
    im = Image.open(os.path.join(BASE, "assets/photo_p5.webp")).convert("RGB").resize((W, H), Image.LANCZOS)
    strip = Image.new("RGBA", (1, H), (0, 0, 0, 0))
    spx = strip.load()
    for y in range(H):
        a = int(238 * max(0.0, (y - 840) / (H - 840))) if y > 840 else 0
        spx[0, y] = (251, 245, 234, a)
    ov = strip.resize((W, H))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    d.text((72, 92), "孩子要的，其实不多", font=F(KUAILE, 68), fill=INK)
    items = ["有人抱抱他", "有人陪他吃饭", "摔倒时，有人说「没关系」", "害怕时，有人站在身边"]
    y = 918
    for s in items:
        d.ellipse((84, y + 14, 108, y + 38), fill=ORANGE_MID)
        d.text((132, y), s, font=FS(SANS_B, 38), fill=INK)
        y += 84
    d.text((84, y + 10), "不多，但每一样都重要。", font=F(HAND, 36), fill=SOFT)
    im.save(os.path.join(BASE, "p5.png"))


# ---------------- P6 误区对照 ----------------
def page6():
    im = Image.new("RGB", (W, H), BG)
    header(im, "这几个念头，最耗妈妈", "焦虑冒头的时候，看看下面这句。")
    pairs = [("他自己玩得安静，是不是不正常", "安安静静地玩，是他在自己探索"),
             ("别人家会走了，我家是不是慢了", "每个宝宝节奏不同，慢一点也常见"),
             ("做不到面面俱到，就是不合格", "陪伴和回应，比完美更重要"),
             ("心里一慌，就想打开手机搜", "先抱抱他，慌会慢慢退下去")]
    y = 318
    for bad, good in pairs:
        d = card(im, (64, y, 1016, y + 238))
        cross(d, 116, y + 56, 27, RED)
        d.text((168, y + 34), bad, font=FS(SANS_R, 33), fill=SOFT)
        check(d, 116, y + 168, 27, GREEN)
        d.text((168, y + 146), good, font=FS(SANS_B, 34), fill=INK)
        y += 238 + 24
    im.save(os.path.join(BASE, "p6.png"))


# ---------------- P7 收藏 Checklist ----------------
def page7():
    im = Image.new("RGB", (W, H), BG)
    band = Image.open(os.path.join(BASE, "assets/photo_p7.webp")).convert("RGB")
    band = band.crop((0, 130, 1344, 755)).resize((1080, 502), Image.LANCZOS)
    im.paste(band, (0, 0))
    d = ImageDraw.Draw(im)
    d.text((64, 548), "这一篇，记住这几件事就够了", font=F(KUAILE, 52), fill=INK)
    items = ["累的是脑子，不是我做得不够好", "待办再多，一件一件慢慢来",
             "不跟别人家比节奏", "深夜少搜索，先好好睡觉", "抱抱、陪伴、回应，就够了"]
    y = 668
    for s in items:
        d = card(im, (64, y, 1016, y + 94), r=20)
        rr(d, (92, y + 25, 136, y + 69), 10, outline=ORANGE, width=5)
        d.text((164, y + 24), s, font=FS(SANS_B, 34), fill=INK)
        y += 94 + 18
    d = ImageDraw.Draw(im)
    rr(d, (64, y + 8, 1016, y + 118), 24, fill=ORANGE_SOFT)
    d.text((540, y + 30), "先收藏，下次焦虑时翻出来看看。", font=FS(SANS_B, 31), fill=INK, anchor="ma")
    d.text((540, y + 76), "妈妈安心指南 · 02 见", font=FS(SANS_R, 25), fill=SOFT, anchor="ma")
    im.save(os.path.join(BASE, "p7.png"))


if __name__ == "__main__":
    page1(); page2(); page3(); page4(); page5(); page6(); page7()
    print("done p1-p7")
