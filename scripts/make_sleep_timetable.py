# -*- coding: utf-8 -*-
"""示例排版脚本：《宝宝睡得越久越好吗？0-12 个月睡眠时间表》

栏目搭配：③极简信息图（现代杂志版）为主 + P1 混搭①真实生活摄影感 + P5 混搭⑥生活抓拍感。
做法：AI 只生成无文字的实拍感照片（examples/sleep-timetable/assets/），
全部中文用 PIL + 思源黑体精准排版，冷白底、无边框、深青单一强调色。

运行：
    pip install -r requirements.txt
    python3 make_sleep_timetable.py
输出到 examples/sleep-timetable/output/p1.png ~ p6.png（900x1200）。

字体：优先使用系统 Noto Sans CJK（.ttc 需 index=2 取简体中文），
否则从仓库 fonts/ 目录读取，下载方式见 fonts/README.md。
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "examples" / "sleep-timetable" / "assets"
OUT = ROOT / "examples" / "sleep-timetable" / "output"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 900, 1200
BG = (248, 249, 249)
INK = (32, 38, 42)
GREY = (110, 119, 123)
LINE = (217, 222, 220)
TEAL = (20, 102, 92)
WHITE = (255, 255, 255)


def _load(candidates, size):
    for path, index in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(str(path), size, index=index)
            except Exception:
                continue
    raise FileNotFoundError("未找到可用字体，请按 fonts/README.md 下载 Noto Sans CJK 后放入 fonts/ 目录")


def b(s):
    return _load([
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 2),
        (ROOT / "fonts" / "NotoSansCJK-Bold.ttc", 2),
        (ROOT / "fonts" / "NotoSansCJK-Bold.otf", 0),
        ("/System/Library/Fonts/PingFang.ttc", 0),
    ], s)


def r(s):
    return _load([
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2),
        (ROOT / "fonts" / "NotoSansCJK-Regular.ttc", 2),
        (ROOT / "fonts" / "NotoSansCJK-Regular.otf", 0),
        ("/System/Library/Fonts/PingFang.ttc", 0),
    ], s)


def tw(d, t, f):
    bb = d.textbbox((0, 0), t, font=f); return bb[2] - bb[0]


def lt(d, x, y, t, f, c):
    d.text((x, y), t, font=f, fill=c); return tw(d, t, f)


def ct(d, y, t, f, c):
    w = tw(d, t, f); d.text(((W - w) // 2, y), t, font=f, fill=c); return w


def hline(d, y, x0=64, x1=836, c=LINE, wdt=2):
    d.line([(x0, y), (x1, y)], fill=c, width=wdt)


def header(d, tag, note="参考范围"):
    lt(d, 64, 80, tag, b(34), TEAL)
    w = tw(d, note, r(26)); d.text((836 - w, 90), note, font=r(26), fill=GREY)
    hline(d, 148)


def crop_fill(img, w, h, focus_y=0.5):
    """按目标比例裁剪，focus_y 为源图纵向焦点（0-1）"""
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = int(focus_y * nh - h / 2)
    y = max(0, min(nh - h, y))
    return img.crop((x, y, x + w, y + h))


COVER = ASSETS / "cover-photo.webp"
NIGHT = ASSETS / "night-photo.webp"

# ============ P1 封面：实拍照片 + 杂志式排字 ============
img = crop_fill(Image.open(COVER).convert("RGB"), W, H, focus_y=0.60)
# 底部浅色渐显罩（保证标题可读）
mask = Image.new("L", (1, H), 0)
for y in range(H):
    if y < 660: a = 0
    elif y < 990: a = int(238 * (y - 660) / 330)
    else: a = 244
    mask.putpixel((0, y), a)
mask = mask.resize((W, H))
img = Image.composite(Image.new("RGB", (W, H), (250, 250, 249)), img, mask)
d = ImageDraw.Draw(img)
lt(d, 64, 856, "宝宝每天到底", b(88), INK)
lt(d, 64, 962, "睡多久？", b(88), INK)
d.rectangle([(66, 1078), (190, 1083)], fill=TEAL)
lt(d, 64, 1096, "0-12个月睡眠时间表", b(40), TEAL)
lt(d, 470, 1108, "新手妈妈建议收藏", r(28), GREY)
img.save(OUT / "p1.png"); print("p1 ok")

# ============ P2 总览：交替式极简时间轴 ============
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
header(d, "0—12个月 · 总览")
lt(d, 64, 182, "0-12个月，", b(56), INK)
lt(d, 64, 254, "一眼看懂睡眠变化", b(56), INK)
AXIS = 616
d.line([(80, AXIS), (820, AXIS)], fill=TEAL, width=3)
nodes = [
    ("0个月", "14-17", "昼夜不分\n睡醒了就吃奶", True),
    ("3个月", "14-17", "开始分昼夜\n夜醒还比较多", False),
    ("6个月", "12-15", "白天小睡约3次\n夜里连睡变长", True),
    ("9个月", "12-15", "白天小睡2-3次\n夜醒可能反复", False),
    ("12个月", "11-14", "白天小睡2次\n作息接近大人", True),
]
xs = [105, 275, 445, 615, 785]
for (age, hrs, note, up), x in zip(nodes, xs):
    d.ellipse([x - 11, AXIS - 11, x + 11, AXIS + 11], fill=TEAL, outline=WHITE, width=3)
    if up:
        w1 = tw(d, age, b(42)); d.text((x - w1 // 2, AXIS - 82), age, font=b(42), fill=INK)
        wf = tw(d, hrs, b(62)) + 4 + tw(d, "小时", b(38))
        sx = max(64, min(x - wf // 2, 836 - wf))
        lt(d, sx, AXIS - 168, hrs, b(62), TEAL)
        lt(d, sx + tw(d, hrs, b(62)) + 4, AXIS - 146, "小时", b(38), TEAL)
        for i, ln in enumerate(note.split("\n")):
            cx = tw(d, ln, r(26))
            d.text((x - cx // 2, AXIS - 268 + i * 40), ln, font=r(26), fill=GREY)
    else:
        w1 = tw(d, age, b(42)); d.text((x - w1 // 2, AXIS + 34), age, font=b(42), fill=INK)
        wf = tw(d, hrs, b(62)) + 4 + tw(d, "小时", b(38))
        sx = max(64, min(x - wf // 2, 836 - wf))
        lt(d, sx, AXIS + 92, hrs, b(62), TEAL)
        lt(d, sx + tw(d, hrs, b(62)) + 4, AXIS + 114, "小时", b(38), TEAL)
        for i, ln in enumerate(note.split("\n")):
            cx = tw(d, ln, r(26))
            d.text((x - cx // 2, AXIS + 196 + i * 40), ln, font=r(26), fill=GREY)
hline(d, 1052)
ct(d, 1078, "比参考范围多一点、少一点，都不代表不正常", r(27), GREY)
img.save(OUT / "p2.png"); print("p2 ok")

# ============ P3 0-3个月：数字英雄区 ============
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
header(d, "0-3个月")
lt(d, 64, 196, "睡眠很碎，很正常", b(58), INK)
lt(d, 60, 316, "14-17", b(196), INK)
lt(d, 60 + tw(d, "14-17", b(196)) + 12, 316 + 196 - 78, "小时", b(64), TEAL)
lt(d, 64, 540, "一天总睡眠参考范围（白天小睡 ＋ 夜里）", r(28), GREY)
hline(d, 632)
rows = [
    ("01", "昼夜节律还在建立，分不清白天黑夜"),
    ("02", "一次睡两三个小时就醒，是常态"),
    ("03", "夜醒次数多很常见，不用跟别人比"),
]
y = 686
for num, t in rows:
    lt(d, 64, y, num, b(38), TEAL)
    lt(d, 168, y + 2, t, r(39), INK)
    y += 98
hline(d, 992)
ct(d, 1024, "睡得碎，不代表睡不好", b(42), TEAL)
img.save(OUT / "p3.png"); print("p3 ok")

# ============ P4 4-6个月：左右对照 ============
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
header(d, "4-6个月")
lt(d, 64, 196, "开始慢慢规律", b(58), INK)
lt(d, 64, 282, "总睡眠参考约 12-15 小时", r(28), GREY)
d.line([(450, 396), (450, 856)], fill=LINE, width=2)


def col(x, head, items):
    lt(d, x, 396, head, b(44), INK)
    d.rectangle([(x + 2, 462), (x + 54, 467)], fill=TEAL)
    yy = 512
    for it in items:
        d.ellipse([x + 2, yy + 16, x + 12, yy + 26], fill=TEAL)
        for j, seg in enumerate(it):
            lt(d, x + 30, yy + j * 52, seg, r(35), INK)
        yy += 128


col(64, "白天", [["小睡变得有规律"], ["一天大约 3 次"], ["时间慢慢能", "固定下来"]])
col(486, "夜里", [["连续睡的时间变长"], ["有的宝宝能连睡", "5-6 小时"], ["夜醒慢慢变少"]])
hline(d, 916)
ct(d, 948, "偶尔又频繁夜醒？可能是睡眠倒退", r(36), INK)
ct(d, 1004, "多在 4 个月左右出现，过一阵会稳下来", r(29), GREY)
img.save(OUT / "p4.png"); print("p4 ok")

# ============ P5 7-9个月：夜拍照片 + 观察记录 ============
img = Image.new("RGB", (W, H), BG)
ph = crop_fill(Image.open(NIGHT).convert("RGB"), W, 690, focus_y=0.30)
img.paste(ph, (0, 0))
d = ImageDraw.Draw(img)
lt(d, 64, 724, "7-9个月", b(32), TEAL)
lt(d, 216, 730, "妈妈观察记录", r(28), GREY)
lt(d, 64, 778, "最近怎么又睡不好了？", b(46), INK)
ct(d, 884, "学翻身 · 练爬行 · 出牙不舒服 · 分离焦虑", r(36), INK)
ct(d, 946, "都是这个阶段在长的本事", r(29), GREY)
ct(d, 1012, "不一定是作息养坏了", b(44), TEAL)
img.save(OUT / "p5.png"); print("p5 ok")

# ============ P6 10-12个月：极简清单 + 结论 ============
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
header(d, "10-12个月")
lt(d, 64, 196, "别只盯着睡眠数字", b(56), INK)
lt(d, 64, 282, "比时长更该看的 4 件事", r(29), GREY)
items = [
    ("白天精神状态", "醒着时有精神、爱玩"),
    ("吃奶、进食情况", "吃得香，不抗拒"),
    ("生长发育", "身高体重稳步在长"),
    ("长期睡眠情况", "看一周，别只看一天"),
]
iy = 372
for name, note in items:
    d.rounded_rectangle([(64, iy), (106, iy + 42)], radius=10, fill=TEAL)
    d.line([(76, iy + 21), (84, iy + 30), (96, iy + 12)], fill=WHITE, width=5, joint="curve")
    w = lt(d, 140, iy - 2, name, b(40), INK)
    lt(d, 140 + w + 26, iy + 8, note, r(29), GREY)
    iy += 104
hline(d, 812)
ct(d, 852, "睡眠表是参考，", b(56), INK)
ct(d, 928, "不是宝宝的考试成绩。", b(56), TEAL)
d.rounded_rectangle([(64, 1046), (836, 1138)], radius=20, fill=TEAL)
ct(d, 1070, "你家宝宝现在几个月？一天睡多久？", b(35), WHITE)
img.save(OUT / "p6.png"); print("p6 ok")
print("ALL DONE ->", OUT)
