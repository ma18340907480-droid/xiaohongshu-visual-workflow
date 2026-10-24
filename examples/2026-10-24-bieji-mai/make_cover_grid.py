# -*- coding: utf-8 -*-
"""V3 九宫格封面（版式 E：中心标题＋八张实物细节）
8 格全部裁切自本篇已生成的真实感底图（实物/局部特写，无真人全景），
每格底部短标签「品类：结论」；中心格为标题视觉中心。"""
import glob
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/hatch/workspace/xiaohongshu/2026-10-24-bieji-mai/base"
OUT = "/home/hatch/workspace/xiaohongshu/2026-10-24-bieji-mai/p1-grid.jpg"
FONTS = "/home/hatch/workspace/fonts"
F_TITLE = f"{FONTS}/ZCOOLKuaiLe.ttf"
F_HAND = f"{FONTS}/MaShanZheng.ttf"

W, H, GAP = 1080, 1440, 12
CW = (W - GAP * 2) // 3          # 352
CH = (H - GAP * 2) // 3          # 472
BG = (247, 237, 220)
CREAM = (255, 248, 236)
BROWN_D = (74, 50, 33)
ORANGE = (224, 116, 44)

def font(p, s):
    return ImageFont.truetype(p, s)

def load(n):
    p = glob.glob(f"{BASE}/*p{n}-base-0-*.jpg")[0]
    return Image.open(p).convert("RGB")

# (底图编号, 裁切框, 标签)
cells = [
    (2, (90, 330, 650, 1077), "衣服：别囤太多"),
    (2, (760, 330, 1320, 1077), "鞋子：会走再买"),
    (3, (40, 1000, 600, 1747), "玩具：少而精"),
    (4, (520, 1045, 1080, 1792), "辅食碗勺：先基础款"),
    None,  # 中心标题格
    (4, (60, 300, 620, 1047), "辅食工具：别买整套"),
    (5, (540, 640, 1100, 1387), "婴儿车：重量重要"),
    (1, (580, 900, 1140, 1647), "收纳：别先囤盒"),
    (4, (690, 660, 1250, 1407), "分装清洁：够用就行"),
]

canvas = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(canvas)

for i, cell in enumerate(cells):
    r, c = divmod(i, 3)
    x, y = c * (CW + GAP), r * (CH + GAP)
    if cell is None:
        # 中心标题格
        tile = Image.new("RGB", (CW, CH), CREAM)
        td = ImageDraw.Draw(tile)
        td.rounded_rectangle([86, 36, 266, 88], 10, fill=(246, 178, 107))
        td.text((176, 62), "避坑清单", font=font(F_HAND, 32), fill=BROWN_D, anchor="mm")
        td.text((176, 128), "宝宝0–3岁", font=font(F_TITLE, 57), fill=BROWN_D, anchor="mm")
        td.text((176, 200), "这些东西", font=font(F_TITLE, 57), fill=BROWN_D, anchor="mm")
        td.text((176, 276), "别急着买！", font=font(F_TITLE, 66), fill=ORANGE, anchor="mm")
        td.line([36, 356, 316, 356], fill=(216, 190, 150), width=3)
        td.text((176, 396), "衣服、鞋子、玩具、辅食、婴儿车", font=font(F_HAND, 22), fill=(120, 92, 64), anchor="mm")
        canvas.paste(tile, (x, y))
        continue
    n, box, label = cell
    src = load(n).crop(box).resize((CW, CH), Image.LANCZOS)
    canvas.paste(src, (x, y))
    # 底部标签条
    strip = Image.new("RGBA", (CW, 62), (255, 248, 236, 225))
    canvas.paste(strip, (x, y + CH - 62), strip)
    d = ImageDraw.Draw(canvas)
    d.text((x + CW // 2, y + CH - 31), label, font=font(F_HAND, 35), fill=BROWN_D, anchor="mm")

canvas.save(OUT, quality=92)
print("saved", OUT)
