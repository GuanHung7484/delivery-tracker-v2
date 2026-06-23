# -*- coding: utf-8 -*-
"""產生兩張可愛 QR 海報：群組轉傳版 + 機車貼紙版"""
import qrcode
from PIL import Image, ImageDraw, ImageFont

URL = "https://guanhung7484.github.io/delivery-tracker-v2/"
OUT_DIR = r"C:\Users\231489\外送每日跑單費用與里程試算(第二版)"

PINK   = (225, 29, 116)
PINK2  = (255, 95, 162)
PINKBG = (255, 217, 232)
MINTBG = (205, 243, 227)
GREEN  = (15, 157, 104)
LINE_G = (6, 199, 85)
ORANGE = (255, 122, 24)
INK    = (51, 50, 58)
INK2   = (122, 118, 130)
DARK   = (34, 34, 34)
WHITE  = (255, 255, 255)

FB = r"C:\Windows\Fonts\msjhbd.ttc"   # 粗體
FR = r"C:\Windows\Fonts\msjh.ttc"     # 一般
def f(path, size): return ImageFont.truetype(path, size)

def qr_img(px, fill=DARK):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(URL); qr.make(fit=True)
    im = qr.make_image(fill_color=fill, back_color="white").convert("RGB")
    return im.resize((px, px), Image.NEAREST)

def vgrad(w, h, top, bot):
    base = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(base)
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return base

def ctext(d, cx, y, text, font, fill):
    d.text((cx, y), text, font=font, fill=fill, anchor="mm")

# ---------------- 群組轉傳版 ----------------
def make_share():
    W, H = 900, 1180
    img = vgrad(W, H, PINKBG, MINTBG)
    d = ImageDraw.Draw(img)
    # 內白卡
    d.rounded_rectangle([40, 40, W-40, H-40], radius=48, fill=WHITE)
    cx = W // 2
    ctext(d, cx, 130, "🛵 外送跑單小幫手".replace("🛵 ", ""), f(FB, 56), PINK)
    ctext(d, cx, 196, "每天跑單的時薪、收入、里程，一鍵算好", f(FR, 27), INK2)
    # 三平台色點
    dots = [("foodpanda", PINK), ("Uber Eats", GREEN), ("Lalamove", ORANGE)]
    fp = f(FB, 24); total = 0; gaps = []
    for name, _ in dots:
        w = d.textlength(name, font=fp); gaps.append(w); total += w
    spacing = 38; total += spacing * (len(dots) - 1) + 26 * len(dots)
    x = cx - total / 2
    for (name, col), w in zip(dots, gaps):
        d.ellipse([x, 250-9, x+18, 250+9], fill=col); x += 26
        d.text((x, 250), name, font=fp, fill=INK, anchor="lm"); x += w + spacing
    # QR
    q = 470; qx = cx - q//2; qy = 310
    d.rounded_rectangle([qx-22, qy-22, qx+q+22, qy+q+22], radius=28, outline=PINKBG, width=4, fill=WHITE)
    img.paste(qr_img(q, DARK), (qx, qy))
    # CTA
    ctext(d, cx, qy+q+78, "手機掃一掃，免費開始記帳", f(FB, 34), PINK)
    ctext(d, cx, qy+q+128, "guanhung7484.github.io/delivery-tracker-v2", f(FR, 23), INK2)
    # 分隔線
    ly = qy+q+170; d.line([110, ly, W-110, ly], fill=PINKBG, width=3)
    # 署名 + LINE
    ctext(d, cx, ly+48, "by Daniel　免費分享給大家用 🙂".replace(" 🙂",""), f(FB, 27), INK)
    pill_t = "LINE：guanhung"; pf = f(FB, 26); pw = d.textlength(pill_t, font=pf)
    px0 = cx - (pw+44)/2; py0 = ly+78
    d.rounded_rectangle([px0, py0, px0+pw+44, py0+50], radius=25, fill=LINE_G)
    d.text((cx, py0+25), pill_t, font=pf, fill=WHITE, anchor="mm")
    img.save(OUT_DIR + r"\分享圖_群組轉傳.png")
    print("saved 群組轉傳")

# ---------------- Q版外送員騎機車插圖 ----------------
def mascot(d, ax, ay):
    """以 (ax,ay) 為左上，畫約 460x300 插圖；機車面向左、外送箱在右後方"""
    P=(255,95,162); PD=(225,29,116); M=(34,201,138); MD=(15,157,104)
    OR=(255,122,24); ORD=(214,80,10); SK=(255,224,196); IK=(40,38,46)
    WH=(255,255,255); WHL=(43,43,43); GY=(207,201,214)
    for yy in (150,185,220):                                   # 速度線
        d.line([(ax+410, ay+yy),(ax+462, ay+yy)], fill=P, width=7)
    bx0,by0,bx1,by1 = ax+300, ay+120, ax+402, ay+222          # 外送箱
    d.polygon([(bx0,by0),(bx0+22,by0-22),(bx1+22,by0-22),(bx1,by0)], fill=PD)
    d.polygon([(bx1,by0),(bx1+22,by0-22),(bx1+22,by1-22),(bx1,by1)], fill=(190,18,92))
    d.rounded_rectangle([bx0,by0,bx1,by1], radius=12, fill=P, outline=PD, width=5)
    d.ellipse([ax+330, ay+150, ax+345, ay+165], fill=WH)
    d.ellipse([ax+360, ay+150, ax+375, ay+165], fill=WH)
    d.arc([ax+330, ay+165, ax+375, ay+200], 20, 160, fill=WH, width=5)
    for cx in (ax+110, ax+300):                                # 輪子
        d.ellipse([cx-46, ay+204, cx+46, ay+296], fill=WHL)
        d.ellipse([cx-20, ay+230, cx+20, ay+270], fill=GY)
        d.ellipse([cx-7, ay+243, cx+7, ay+257], fill=IK)
    d.rounded_rectangle([ax+200, ay+205, ax+320, ay+262], radius=26, fill=M, outline=MD, width=5)
    d.rounded_rectangle([ax+120, ay+232, ax+235, ay+260], radius=10, fill=MD)
    d.polygon([(ax+118, ay+250),(ax+150, ay+250),(ax+120, ay+135),(ax+92, ay+138)], fill=M, outline=MD)
    d.rounded_rectangle([ax+205, ay+188, ax+315, ay+212], radius=12, fill=IK)
    d.line([(ax+78, ay+132),(ax+128, ay+150)], fill=IK, width=10)
    d.ellipse([ax+70, ay+124, ax+90, ay+144], fill=IK)
    d.line([(ax+250, ay+205),(ax+175, ay+245)], fill=OR, width=26)   # 腿
    d.ellipse([ax+165, ay+238, ax+190, ay+260], fill=IK)             # 鞋
    d.polygon([(ax+205, ay+205),(ax+265, ay+205),(ax+235, ay+120),(ax+195, ay+128)], fill=OR, outline=ORD)
    d.line([(ax+205, ay+135),(ax+95, ay+140)], fill=OR, width=20)    # 手臂
    d.ellipse([ax+85, ay+130, ax+110, ay+155], fill=SK)             # 手
    hx, hy = ax+175, ay+92
    d.ellipse([hx-36, hy-36, hx+36, hy+36], fill=SK)               # 臉
    d.chord([hx-40, hy-44, hx+40, hy+30], 180, 360, fill=P, outline=PD, width=4)  # 帽
    d.rectangle([hx-40, hy-8, hx+40, hy+2], fill=P)
    d.ellipse([hx-18, hy+2, hx-8, hy+14], fill=IK)                 # 眼
    d.ellipse([hx+8, hy+2, hx+18, hy+14], fill=IK)
    d.ellipse([hx-26, hy+12, hx-16, hy+22], fill=(255,150,170))    # 腮紅
    d.ellipse([hx+16, hy+12, hx+26, hy+22], fill=(255,150,170))
    d.arc([hx-12, hy+14, hx+12, hy+30], 20, 160, fill=IK, width=4) # 嘴

# ---------------- 機車貼紙版（含插圖）----------------
def make_sticker():
    W, H = 820, 1300
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([14, 14, W-14, H-14], radius=44, outline=PINK, width=14)
    cx = W // 2
    d.rounded_rectangle([60, 70, W-60, 168], radius=26, fill=PINK)
    ctext(d, cx, 119, "外送跑單小幫手", f(FB, 50), WHITE)
    mascot(d, 150, 185)
    ctext(d, cx, 540, "掃我！免費記帳", f(FB, 52), INK)
    q = 470; qx = cx - q//2; qy = 590
    d.rounded_rectangle([qx-18, qy-18, qx+q+18, qy+q+18], radius=22, outline=(235,235,235), width=4)
    img.paste(qr_img(q, DARK), (qx, qy))
    ctext(d, cx, 1100, "記錄每天時薪 · 收入 · 里程", f(FB, 30), INK2)
    ctext(d, cx, 1142, "guanhung7484.github.io/delivery-tracker-v2", f(FR, 22), INK2)
    pill_t = "by Daniel　LINE：guanhung"; pf = f(FB, 25); pw = d.textlength(pill_t, font=pf)
    px0 = cx - (pw+44)/2; py0 = 1178
    d.rounded_rectangle([px0, py0, px0+pw+44, py0+48], radius=24, fill=LINE_G)
    d.text((cx, py0+24), pill_t, font=pf, fill=WHITE, anchor="mm")
    img.save(OUT_DIR + r"\分享圖_機車貼紙.png")
    print("saved 機車貼紙")

def hgrad(w, h, left, right):
    base = Image.new("RGB", (w, h), left)
    d = ImageDraw.Draw(base)
    for x in range(w):
        t = x / max(1, w - 1)
        c = tuple(int(left[i] + (right[i] - left[i]) * t) for i in range(3))
        d.line([(x, 0), (x, h)], fill=c)
    return base

def dots_row(d, x0, y, fp):
    dots = [("foodpanda", PINK), ("Uber Eats", GREEN), ("Lalamove", ORANGE)]
    x = x0
    for name, col in dots:
        d.ellipse([x, y-9, x+18, y+9], fill=col); x += 26
        d.text((x, y), name, font=fp, fill=INK, anchor="lm")
        x += d.textlength(name, font=fp) + 34
    return x

# ---------------- 橫式 banner ----------------
def make_banner():
    W, H = 1200, 630
    img = hgrad(W, H, PINKBG, MINTBG)
    d = ImageDraw.Draw(img)
    # 左：白卡 + QR
    d.rounded_rectangle([54, 70, 560, 560], radius=44, fill=WHITE)
    q = 400; qx = 54 + (506 - q)//2; qy = 70 + (490 - q)//2
    img.paste(qr_img(q, DARK), (qx, qy))
    # 右：文字（左對齊 x=620）
    X = 620
    d.text((X, 150), "外送跑單小幫手", font=f(FB, 60), fill=PINK, anchor="lm")
    d.text((X, 214), "每天跑單的時薪、收入、里程，一鍵算好", font=f(FR, 27), fill=INK2, anchor="lm")
    dots_row(d, X, 268, f(FB, 23))
    d.text((X, 348), "手機掃一掃，免費開始記帳", font=f(FB, 38), fill=PINK, anchor="lm")
    d.text((X, 404), "guanhung7484.github.io/delivery-tracker-v2", font=f(FR, 24), fill=INK2, anchor="lm")
    d.line([X, 452, W-70, 452], fill=PINKBG, width=3)
    d.text((X, 506), "by Daniel", font=f(FB, 28), fill=INK, anchor="lm")
    pt = "LINE：guanhung"; pf = f(FB, 26); pw = d.textlength(pt, font=pf)
    bx = X + d.textlength("by Daniel", font=f(FB, 28)) + 28
    d.rounded_rectangle([bx, 484, bx+pw+40, 532], radius=24, fill=LINE_G)
    d.text((bx+20, 508), pt, font=pf, fill=WHITE, anchor="lm")
    img.save(OUT_DIR + r"\分享圖_橫式banner.png")
    print("saved 橫式banner")

# ---------------- 去背版（透明背景）----------------
def make_transparent():
    W, H = 760, 1000
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # 全透明背景
    d = ImageDraw.Draw(img)
    cx = W // 2
    ctext(d, cx, 96, "外送跑單小幫手", f(FB, 50), PINK)
    ctext(d, cx, 152, "每天跑單時薪、收入、里程，一鍵算好", f(FR, 24), INK2)
    fp = f(FB, 22)
    total = sum(d.textlength(n, font=fp) for n, _ in
               [("foodpanda", 0), ("Uber Eats", 0), ("Lalamove", 0)]) + 3*26 + 2*34
    dots_row(d, cx - total/2, 198, fp)
    q = 430; qx = cx - q//2; qy = 248
    # QR 保留白底方框（掃描必要的留白），讓它可疊在任何底色上
    d.rounded_rectangle([qx-24, qy-24, qx+q+24, qy+q+24], radius=24, fill=(255,255,255,255), outline=PINK, width=4)
    img.paste(qr_img(q, DARK).convert("RGBA"), (qx, qy))
    ctext(d, cx, qy+q+70, "手機掃一掃，免費開始記帳", f(FB, 32), PINK)
    ctext(d, cx, qy+q+116, "guanhung7484.github.io/delivery-tracker-v2", f(FR, 22), INK2)
    pt = "by Daniel　LINE：guanhung"; pf = f(FB, 25); pw = d.textlength(pt, font=pf)
    px0 = cx - (pw+44)/2; py0 = H-110
    d.rounded_rectangle([px0, py0, px0+pw+44, py0+48], radius=24, fill=LINE_G)
    d.text((cx, py0+24), pt, font=pf, fill=WHITE, anchor="mm")
    img.save(OUT_DIR + r"\分享圖_去背透明.png")
    print("saved 去背透明")

make_share()
make_sticker()
make_banner()
make_transparent()
print("DONE")
