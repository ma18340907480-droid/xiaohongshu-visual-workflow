# -*- coding: utf-8 -*-
"""《宝宝0–3岁，这些东西真的别急着买》6 张成品图 PIL 排字
封面优先原则首篇：P1 = 知识清单封面（标题+5 条核心结论+真实场景照片）。
底图为按真实参考原创重制的摄影图，中文全部 PIL 排版。"""
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1440
BASE = "/home/hatch/workspace/xiaohongshu/2026-10-24-bieji-mai/base"
OUT = "/home/hatch/workspace/xiaohongshu/2026-10-24-bieji-mai"
FONTS = "/home/hatch/workspace/fonts"
F_TITLE = f"{FONTS}/ZCOOLKuaiLe.ttf"      # 站酷快乐体（标题）
F_HAND = f"{FONTS}/MaShanZheng.ttf"       # 马善政体（手写正文）
F_NUM = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"  # 徽章数字

CREAM = (255, 248, 236)
CREAM_A = (255, 248, 236, 242)
BROWN = (90, 63, 44)
BROWN_D = (74, 50, 33)
ORANGE = (224, 116, 44)
ORANGE_SOFT = (246, 178, 107, 150)
GREEN = (110, 138, 96)
TAPE = (250, 230, 190, 200)

def font(path, size):
    return ImageFont.truetype(path, size)

def load_base(n):
    p = glob.glob(f"{BASE}/*p{n}-base-0-*.jpg")[0]
    im = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)
    return im

def panel(im, box, fill=CREAM_A, radius=28, shadow=True):
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        x0, y0, x1, y1 = box
        sd.rounded_rectangle([x0 + 6, y0 + 10, x1 + 6, y1 + 10], radius, fill=(90, 60, 30, 60))
        im.paste(Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(8))).convert("RGB"), (0, 0))
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle(box, radius, fill=fill)
    im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"), (0, 0))
    return ImageDraw.Draw(im)

def tape(im, cx, cy, w, h, angle=-2, fill=TAPE):
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(t)
    td.rectangle([0, 0, w, h], fill=fill)
    t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    im.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)

def text_rot(im, xy, s, fnt, fill, angle=0, anchor="mm"):
    if angle == 0:
        d = ImageDraw.Draw(im)
        d.text(xy, s, font=fnt, fill=fill, anchor=anchor)
        return
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bbox = d0.textbbox((0, 0), s, font=fnt)
    tw, th = bbox[2] - bbox[0] + 30, bbox[3] - bbox[1] + 30
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((15 - bbox[0], 15 - bbox[1]), s, font=fnt, fill=fill)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    x, y = xy
    im.paste(layer, (int(x - layer.width / 2), int(y - layer.height / 2)), layer)

def highlight(im, x, y, w, h, color=ORANGE_SOFT):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([x, y, x + w, y + h], 10, fill=color)
    im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"), (0, 0))

def badge(d, cx, cy, r, num, fill=ORANGE):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    f = ImageFont.truetype(F_NUM, int(r * 1.05), index=2)
    d.text((cx, cy - 2), num, font=f, fill=(255, 255, 255), anchor="mm")

def save(im, name):
    im.save(f"{OUT}/{name}", quality=92)
    print("saved", name)

# ---------------- P1 封面知识卡 ----------------
im = load_base(1)
d = ImageDraw.Draw(im)
# 顶部眉题胶带
tape(im, 300, 92, 430, 62, -2)
d = ImageDraw.Draw(im)
text_rot(im, (300, 92), "0–3岁用品避坑清单", font(F_HAND, 40), BROWN_D, -2)
# 主标题（墙面区）
TF = font(F_TITLE, 92)
d.text((58, 138), "宝宝0–3岁", font=TF, fill=BROWN_D)
seg1, seg2 = "这些东西真的", "别急着买！"
w1 = d.textlength(seg1, font=TF)
highlight(im, 50, 250, int(w1 + d.textlength(seg2, font=TF)) + 20, 106)
d.text((58, 246), seg1, font=TF, fill=BROWN_D)
d.text((58 + w1, 246), seg2, font=TF, fill=ORANGE)
d.text((62, 376), "很多都是“看起来很需要”", font=font(F_HAND, 46), fill=BROWN)
# 底部清单卡
d = panel(im, (46, 946, 1034, 1400))
rows = [
    ("衣服", "59、66码别大量囤，长得飞快"),
    ("鞋子", "不会走之前，真的不用急着买"),
    ("玩具", "少而精，比堆满一地更实用"),
    ("辅食", "先买基础工具，别一次买整套"),
    ("婴儿车", "重量，比“高级感”重要得多"),
]
y = 982
for cat, txt in rows:
    d.rounded_rectangle([78, y + 2, 208, y + 58], 14, fill=ORANGE)
    d.text((143, y + 30), cat, font=font(F_TITLE, 36), fill=(255, 255, 255), anchor="mm")
    d.text((232, y + 30), txt, font=font(F_HAND, 41), fill=BROWN_D, anchor="lm")
    y += 84
save(im, "p1.jpg")

# ---------------- P2 衣服＋鞋子 ----------------
im = load_base(2)
d = ImageDraw.Draw(im)
tape(im, 268, 84, 470, 72, -2)
tape(im, 812, 84, 470, 72, 2)
badge(d, 92, 84, 34, "1")
d.text((268, 84), "衣服别囤太多", font=font(F_TITLE, 50), fill=BROWN_D, anchor="mm")
badge(d, 636, 84, 34, "2")
d.text((812, 84), "鞋子别买太早", font=font(F_TITLE, 50), fill=BROWN_D, anchor="mm")
# 手写批注
text_rot(im, (258, 300), "59、66码少买几件", font(F_HAND, 40), BROWN_D, -2)
text_rot(im, (258, 352), "前几个月长得飞快", font(F_HAND, 40), BROWN_D, -2)
text_rot(im, (822, 300), "不会走之前", font(F_HAND, 40), BROWN_D, 2)
text_rot(im, (822, 352), "软底袜鞋就够了", font(F_HAND, 40), BROWN_D, 2)
# 底部面板
d = panel(im, (46, 1096, 1034, 1406))
d.text((84, 1128), "更实用的选法：", font=font(F_TITLE, 44), fill=ORANGE)
lines = [
    "连体衣 ＞ 复杂套装，开襟、侧开 ＞ 套头",
    "柔软、方便换尿布 ＞ 只追求好看",
    "学走路以后，再按脚型和使用场景慢慢选",
]
y = 1196
for ln in lines:
    d.rectangle([88, y + 14, 106, y + 32], fill=ORANGE)
    d.text((124, y), ln, font=font(F_HAND, 41), fill=BROWN_D)
    y += 66
save(im, "p2.jpg")

# ---------------- P3 玩具 ----------------
im = load_base(3)
d = ImageDraw.Draw(im)
tape(im, 330, 86, 560, 76, -2)
badge(d, 96, 86, 36, "3")
d.text((330, 86), "玩具不是越多越好", font=font(F_TITLE, 54), fill=BROWN_D, anchor="mm")
# 批注标签
panel(im, (46, 1050, 730, 1176), radius=22)
d = ImageDraw.Draw(im)
d.text((78, 1072), "反复玩的其实就这几样：", font=font(F_HAND, 38), fill=BROWN_D)
d.text((78, 1118), "球、积木、布书、叠叠乐、抓握玩具", font=font(F_HAND, 37), fill=BROWN_D)
panel(im, (560, 190, 1028, 308), radius=22)
d = ImageDraw.Draw(im)
d.text((586, 212), "发光、唱歌、功能复杂的，", font=font(F_HAND, 38), fill=BROWN_D)
d.text((586, 258), "往往新鲜不了几天", font=font(F_HAND, 38), fill=BROWN_D)
# 底部核心句
core = "玩具再多，也代替不了陪伴"
cw = ImageDraw.Draw(im).textlength(core, font=font(F_TITLE, 56))
highlight(im, int(540 - cw / 2) - 12, 1300, int(cw) + 24, 96)
d = ImageDraw.Draw(im)
d.text((540, 1348), core, font=font(F_TITLE, 56), fill=BROWN_D, anchor="mm")
save(im, "p3.jpg")

# ---------------- P4 辅食＋清洁 ----------------
im = load_base(4)
d = panel(im, (46, 36, 1034, 236))
badge(d, 104, 86, 32, "4")
d.text((152, 86), "辅食神器别一次买一整套", font=font(F_TITLE, 47), fill=BROWN_D, anchor="lm")
badge(d, 104, 172, 32, "5")
d.text((152, 172), "清洁设备也别无限升级", font=font(F_TITLE, 47), fill=BROWN_D, anchor="lm")
# 物品小标签
tags = [("蒸", 128, 660), ("压", 880, 560), ("搅", 168, 986), ("分装", 872, 1052)]
for s, tx, ty in tags:
    tape(im, tx, ty, 108 if len(s) == 1 else 148, 58, -3 if tx < 500 else 3)
    text_rot(im, (tx, ty), s, font(F_TITLE, 38), BROWN_D, -3 if tx < 500 else 3)
# 底部面板
d = panel(im, (46, 1170, 1034, 1406))
d.text((84, 1198), "刚开始：蒸、煮、搅、压碎、分装，够用就行", font=font(F_HAND, 40), fill=BROWN_D)
d.text((84, 1258), "先看宝宝真正需要什么，再慢慢补", font=font(F_HAND, 40), fill=BROWN_D)
hl = d.textlength("不要把育儿变成一场设备军备竞赛", font=font(F_TITLE, 46))
highlight(im, 78, 1322, int(hl) + 14, 66)
d = ImageDraw.Draw(im)
d.text((84, 1332), "不要把育儿变成一场设备军备竞赛", font=font(F_TITLE, 46), fill=BROWN_D)
save(im, "p4.jpg")

# ---------------- P5 婴儿车 ----------------
im = load_base(5)
d = ImageDraw.Draw(im)
tape(im, 428, 84, 764, 78, -2)
badge(d, 92, 84, 36, "6")
d.text((452, 84), "婴儿车别只看“高级感”", font=font(F_TITLE, 50), fill=BROWN_D, anchor="mm")
# 底部清单面板
d = panel(im, (46, 1052, 1034, 1406))
d.text((84, 1082), "每天用起来，这些比外观重要：", font=font(F_TITLE, 42), fill=ORANGE)
chips = ["重量", "折叠方式", "收纳体积", "避震", "靠背调节", "遮阳", "上下楼方便"]
x, y = 84, 1150
d = ImageDraw.Draw(im)
for c in chips:
    wch = int(d.textlength(c, font=font(F_HAND, 38))) + 44
    if x + wch > 1000:
        x, y = 84, y + 76
    d.rounded_rectangle([x, y, x + wch, y + 58], 29, outline=GREEN, width=3)
    d.text((x + wch / 2, y + 29), c, font=font(F_HAND, 38), fill=BROWN_D, anchor="mm")
    x += wch + 22
hl = d.textlength("一个人带娃先想：我能不能自己搬得动？", font=font(F_HAND, 42))
highlight(im, 78, 1328, int(hl) + 14, 64)
d = ImageDraw.Draw(im)
d.text((84, 1338), "一个人带娃先想：我能不能自己搬得动？", font=font(F_HAND, 42), fill=BROWN_D)
save(im, "p5.jpg")

# ---------------- P6 收藏总结 ----------------
im = load_base(6)
d = ImageDraw.Draw(im)
d.text((70, 92), "买之前，先问自己3句话", font=font(F_TITLE, 66), fill=BROWN_D)
qs = [
    ("1", "真的每天会用吗？"),
    ("2", "不用它，有没有替代方案？"),
    ("3", "宝宝长大后，会不会马上闲置？"),
]
y = 250
for num, q in qs:
    badge(d, 116, y + 36, 36, num)
    d.text((180, y), q, font=font(F_HAND, 56), fill=BROWN_D)
    y += 128
d.text((70, y + 16), "三个问题都答不上来——", font=font(F_HAND, 46), fill=BROWN)
highlight(im, 64, y + 88, 300, 108)
d = ImageDraw.Draw(im)
d.text((76, y + 96), "先别买。", font=font(F_TITLE, 76), fill=ORANGE)
# 底部小字（置物板上方墙面）
d = panel(im, (46, 1188, 1034, 1352))
d.text((84, 1222), "育儿不是把家里塞满“宝宝用品”，", font=font(F_HAND, 40), fill=BROWN_D)
d.text((84, 1280), "而是慢慢找到真正适合自己家宝宝的东西。", font=font(F_HAND, 40), fill=BROWN_D)
save(im, "p6.jpg")
print("done")
