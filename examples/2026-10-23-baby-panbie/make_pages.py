# -*- coding: utf-8 -*-
"""育儿手册风 6 页渲染：米白纸+纸纹+暖棕字+PIL手绘元素，无粗边框，逐页版式不同。"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1440
PAPER = (250, 245, 236)
CARD = (255, 253, 248)
INK = (74, 53, 36)
SUB = (138, 113, 92)
LINE = (229, 217, 200)
ORANGE = (232, 131, 58)
GREEN = (123, 160, 91)
YELLOW = (217, 164, 65)
RED = (192, 80, 60)
CREAM = (246, 236, 220)

F_TITLE = "/home/hatch/workspace/fonts/ZCOOLKuaiLe.ttf"
F_SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
F_SANSB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
F_HAND = "/home/hatch/workspace/fonts/MaShanZheng.ttf"

def font(path, size):
    return ImageFont.truetype(path, size, index=2) if path.endswith(".ttc") else ImageFont.truetype(path, size)

def paper():
    img = Image.new("RGB", (W, H), PAPER)
    rnd = random.Random(42)
    px = img.load()
    for _ in range(26000):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r, g, b = px[x, y]
        d = rnd.choice([-7, -5, 5, 7])
        px[x, y] = (max(0, r + d), max(0, g + d), max(0, b + d))
    return img

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if d.textlength(cur + ch, font=f) <= maxw:
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur: lines.append(cur)
    return lines

def text_block(d, xy, text, f, fill=INK, maxw=900, lh=1.5, **kw):
    x, y = xy
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill, **kw)
        y += f.size * lh
    return y

def card(d, box, fill=CARD, radius=26, outline=LINE, shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        d.rounded_rectangle([x0 + 5, y0 + 8, x1 + 5, y1 + 8], radius, fill=(238, 228, 210))
    d.rounded_rectangle(box, radius, fill=fill, outline=outline, width=2)

def dot(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

def wobble_line(d, x0, x1, y, color=ORANGE, width=5, seed=7):
    rnd = random.Random(seed)
    pts = [(x, y + rnd.randint(-2, 2)) for x in range(x0, x1, 14)]
    d.line(pts, fill=color, width=width, joint="curve")

def star(d, cx, cy, r=13, color=ORANGE):
    import math
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=color)

def moon(d, cx, cy, r=26, color=YELLOW):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    d.ellipse([cx - r * 0.15, cy - r * 1.15, cx + r * 1.5, cy + r * 0.4], fill=PAPER)

def draw_mixed(d, x, y, text, size, fill=INK):
    cx = x
    for ch in text:
        f = font(F_SANSB, int(size * 0.96)) if (ch.isascii() and (ch.isdigit() or ch in "-+")) else font(F_TITLE, size)
        d.text((cx, y), ch, font=f, fill=fill)
        cx += d.textlength(ch, font=f)
    return cx

def header(d, title, sub=None, doodle=None):
    size = 57
    while size > 40:
        w = sum(d.textlength(ch, font=font(F_SANSB, int(size * 0.96)) if (ch.isascii() and (ch.isdigit() or ch in "-+")) else font(F_TITLE, size)) for ch in title)
        if w <= 876: break
        size -= 3
    y = 92
    endx = draw_mixed(d, 64, y, title, size)
    wobble_line(d, 68, int(min(endx, 1020)), y + size + 26, seed=len(title))
    if doodle == "star":
        star(d, 986, 108, 15); star(d, 934, 76, 10, YELLOW)
    if doodle == "moon":
        moon(d, 978, 104, 26)
    y += size + 62
    if sub:
        y = text_block(d, (64, y), sub, font(F_SANS, 30), fill=SUB, maxw=940, lh=1.45) + 6
    return y

def foot(d, num, label):
    f1 = font(F_HAND, 28)
    d.text((64, H - 68), "妈妈随身手册", font=f1, fill=SUB)
    x = 64 + d.textlength("妈妈随身手册", font=f1) + 10
    d.text((x, H - 64), num + " · " + label, font=font(F_SANS, 25), fill=SUB)

def footnote(d, text, y=None):
    if y is None: y = H - 118
    f = font(F_HAND, 37)
    tw = d.textlength(text, font=f)
    pad = 26
    d.rounded_rectangle([(W - tw) / 2 - pad, y - 10, (W + tw) / 2 + pad, y + 58], 24, fill=CREAM)
    d.text(((W - tw) / 2, y), text, font=f, fill=(166, 96, 32))

OUT = "/home/hatch/workspace/xiaohongshu/2026-10-23-baby-panbie/"

# ---------- P1 总览 ----------
img = paper(); d = ImageDraw.Draw(img)
y = header(d, "0-3岁宝宝出现这些情况，先别慌", "先观察？咨询医生？还是需要及时处理？", doodle="star")
groups = [
    (GREEN, "可以先观察", "精神好、能吃能玩能睡\n某一顿吃得少 ／ 一次便便颜色变了 ／ 偶尔一晚睡不踏实"),
    (YELLOW, "建议咨询医生", "吃得少连着好几天 ／ 睡不好连续一周\n便秘、排便很费劲 ／ 拿不准、心里没底的时候"),
    (RED, "需要及时就医", "发热还精神蔫、不爱动 ／ 吐和泻，还不肯喝水\n呼吸急促或不对劲 ／ 叫不醒、反应明显异常"),
]
for color, label, body in groups:
    card(d, (56, y, 1024, y + 218))
    dot(d, 116, y + 52, 17, color)
    d.text((152, y + 24), label, font=font(F_SANSB, 38), fill=INK)
    text_block(d, (100, y + 88), body, font(F_SANS, 30), fill=(102, 80, 60), maxw=880, lh=1.5)
    y += 242
text_block(d, (64, y + 8), "这篇把吃饭、睡眠、便便、发热四种常见情况都整理好了。遇事按颜色对号入座，心里先有个谱。", font(F_SANS, 29), fill=SUB, maxw=950, lh=1.5)
foot(d, "01", "总览")
img.save(OUT + "p1.png")

# ---------- P2 吃饭 ----------
img = paper(); d = ImageDraw.Draw(img)
y = header(d, "突然吃得少，不一定就是生病", doodle="star")
items = [
    ("某一顿吃得少", "精神、活动都正常，先看一整天的总量，不盯这一顿。"),
    ("连着几顿明显减少", "一起看喝水和奶量、尿量、精神状态，有没有别的症状。"),
    ("拒绝喝奶、喝水", "偶尔一次先安抚再试；持续明显减少，要提高关注。"),
    ("吃得少 ＋ 精神差", "别只当成“厌奶、挑食”，建议及时咨询医生。"),
    ("吃得少 ＋ 吐/泻/高热", "多个异常一起出现，必要时及时就医。"),
]
for i, (head, body) in enumerate(items, 1):
    card(d, (56, y, 1024, y + 168))
    d.ellipse([92, y + 34, 156, y + 98], outline=ORANGE, width=4)
    num = str(i); nf = font(F_TITLE, 38)
    d.text((124 - d.textlength(num, font=nf) / 2, y + 44), num, font=nf, fill=ORANGE)
    d.text((186, y + 26), head, font=font(F_SANSB, 35), fill=INK)
    text_block(d, (186, y + 82), body, font(F_SANS, 29), fill=(102, 80, 60), maxw=800, lh=1.4)
    y += 188
footnote(d, "判断宝宝状态，不要只盯着一顿饭。")
foot(d, "02", "吃饭喝奶")
img.save(OUT + "p2.png")

# ---------- P3 睡眠 ----------
img = paper(); d = ImageDraw.Draw(img)
y = header(d, "宝宝突然睡不好，先看看是不是这些原因", doodle="moon")
reasons = ["出牙期不舒服", "白天睡多或睡少了", "白天活动量突然变大", "换了环境、换了带的人", "穿盖太热或太冷", "睡前吃太饱，或饿了", "作息被打乱（出行、来客）", "身体不舒服的前兆"]
fx = font(F_SANS, 30)
for i, r in enumerate(reasons):
    cx = 56 + (i % 2) * 492; cy = y + (i // 2) * 104
    card(d, (cx, cy, cx + 476, cy + 84), radius=20)
    dot(d, cx + 36, cy + 42, 8, ORANGE)
    d.text((cx + 60, cy + 24), r, font=fx, fill=INK)
y += 4 * 104 + 26
card(d, (56, y, 1024, y + 330))
d.text((100, y + 30), "什么时候需要特别注意？", font=font(F_SANSB, 36), fill=RED)
text_block(d, (100, y + 96), "睡眠异常的同时，还伴随：精神明显异常、呼吸不对劲、持续高热、反复呕吐。", font(F_SANS, 30), fill=(102, 80, 60), maxw=880, lh=1.55)
text_block(d, (100, y + 218), "就不要只当“睡眠问题”，要看宝宝的整体状态，拿不准就咨询医生。", font(F_SANS, 30), fill=(102, 80, 60), maxw=880, lh=1.55)
d.text((64, 1130), "先排查一圈原因，再决定要不要慌。", font=font(F_HAND, 36), fill=(166, 96, 32))
foot(d, "03", "睡眠")
img.save(OUT + "p3.png")

# ---------- P4 便便 ----------
img = paper(); d = ImageDraw.Draw(img)
y = header(d, "宝宝便便发生变化，别只看颜色", doodle="star")
card(d, (56, y, 1024, y + 330))
dot(d, 116, y + 54, 15, GREEN)
d.text((152, y + 26), "可以先观察的变化", font=font(F_SANSB, 37), fill=INK)
obs = ["换了奶粉、加了新辅食，颜色和性状跟着变", "短时间内，次数多一点或少一点", "吃了带颜色的食物（火龙果、胡萝卜等）"]
ty = y + 100
for t in obs:
    dot(d, 122, ty + 22, 7, GREEN)
    ty = text_block(d, (152, ty), t, font(F_SANS, 30), fill=(102, 80, 60), maxw=830, lh=1.4) + 12
y += 362
card(d, (56, y, 1024, y + 480))
dot(d, 116, y + 54, 15, YELLOW)
d.text((152, y + 26), "值得关注", font=font(F_SANSB, 37), fill=INK)
watch = ["明显持续腹泻，一天比一天多", "便中反复出现血丝、大量黏液", "明显便秘，排便非常困难、哭闹", "尿量明显减少，尿布总是干干的", "同时精神状态变差"]
ty = y + 100
for t in watch:
    dot(d, 122, ty + 22, 7, YELLOW)
    ty = text_block(d, (152, ty), t, font(F_SANS, 30), fill=(102, 80, 60), maxw=830, lh=1.4) + 12
footnote(d, "连续的变化 ＋ 整体状态，比一次便便更重要。", y=H - 150)
foot(d, "04", "大便小便")
img.save(OUT + "p4.png")

# ---------- P5 发烧 ----------
img = paper(); d = ImageDraw.Draw(img)
y = header(d, "宝宝发热，最重要的不是只盯着温度数字", doodle="star")
card(d, (56, y, 1024, y + 640))
d.text((100, y + 28), "发热时，先看这 7 件事", font=font(F_SANSB, 36), fill=INK)
checks = [
    ("精神状态", "还能玩，还是蔫蔫的"),
    ("呼吸", "是否平稳，有没有急促"),
    ("喝奶喝水", "能不能正常喝进去"),
    ("尿量", "是否和平时差不多"),
    ("呕吐腹泻", "有没有反复出现"),
    ("皮疹", "身上有没有异常皮疹"),
    ("反应", "是否明显嗜睡、反应异常"),
]
ty = y + 96
for head, body in checks:
    d.rounded_rectangle([100, ty + 6, 136, ty + 42], 9, outline=ORANGE, width=4)
    d.text((158, ty), head, font=font(F_SANSB, 31), fill=INK)
    hw = d.textlength(head, font=font(F_SANSB, 31))
    d.text((158 + hw + 22, ty + 2), body, font=font(F_SANS, 29), fill=(102, 80, 60))
    ty += 76
y += 672
d.rounded_rectangle([56, y, 1024, y + 128], 24, fill=(250, 234, 226))
text_block(d, (100, y + 24), "年龄越小，出现发热越要谨慎，尤其是小月龄宝宝，别在家硬扛观察。", font(F_SANSB, 31), fill=RED, maxw=880, lh=1.45)
footnote(d, "拿不准，宁可咨询儿科医生，也不要只靠网上信息判断。", y=H - 150)
foot(d, "05", "发烧")
img.save(OUT + "p5.png")

# ---------- P6 流程 ----------
img = paper(); d = ImageDraw.Draw(img)
y = header(d, "记住这套判断顺序", "遇事先按这个顺序过一遍，心里就不慌了。", doodle="star")
steps = [
    ("先看精神状态", "能玩、能笑、眼神有光，先放一半心"),
    ("再看吃喝、尿量、活动", "都跟平时差不多，多半可以先观察"),
    ("有没有持续加重？", "一两天没缓解，还越来越明显"),
    ("有没有多个异常同时出现？", "发热＋呕吐＋精神差，别凑齐了再行动"),
    ("不确定 → 咨询专业人士", "问医生，比在家猜一晚上强"),
]
for i, (head, body) in enumerate(steps, 1):
    card(d, (56, y, 1024, y + 128))
    nf = font(F_TITLE, 40)
    d.ellipse([92, y + 32, 160, y + 100], fill=ORANGE)
    num = str(i)
    d.text((126 - d.textlength(num, font=nf) / 2, y + 42), num, font=nf, fill=(255, 255, 255))
    d.text((190, y + 22), head, font=font(F_SANSB, 34), fill=INK)
    d.text((190, y + 72), body, font=font(F_SANS, 28), fill=(102, 80, 60))
    y += 128
    if i < 5:
        af = font(F_SANSB, 34)
        d.text((W / 2 - d.textlength("↓", font=af) / 2, y + 2), "↓", font=af, fill=ORANGE)
        y += 52
y += 18
text_block(d, (64, y), "育儿最难的不是记住所有知识，\n而是知道什么时候可以观察，什么时候不能再等。", font(F_HAND, 40), fill=(166, 96, 32), maxw=950, lh=1.5)
footnote(d, "建议收藏，需要的时候再回来看看。", y=H - 150)
foot(d, "06", "判断顺序")
img.save(OUT + "p6.png")
print("done 6 pages")
