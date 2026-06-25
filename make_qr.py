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

# ---------------- 群組轉傳版（含小騎士）----------------
def make_share():
    W = 900; cx = W // 2
    ri, rh = rider_img(320)
    rtop = 286
    q = 460; qy = rtop + rh + 26
    cta_y = qy + q + 74; url_y = qy + q + 122
    ly = qy + q + 162; pill_y = ly + 76
    H = int(pill_y + 50 + 56)
    img = vgrad(W, H, PINKBG, MINTBG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W-40, H-40], radius=48, fill=WHITE)
    ctext(d, cx, 132, "外送跑單小幫手", f(FB, 56), PINK)
    ctext(d, cx, 198, "每天跑單的時薪、收入、里程，一鍵算好", f(FR, 27), INK2)
    dots_center(d, cx, 252, f(FB, 24))
    img.paste(ri, (cx - 320 // 2, rtop), ri)
    qx = cx - q // 2
    d.rounded_rectangle([qx-22, qy-22, qx+q+22, qy+q+22], radius=28, outline=PINKBG, width=4, fill=WHITE)
    img.paste(qr_img(q, DARK), (qx, qy))
    ctext(d, cx, cta_y, "手機掃一掃，免費開始記帳", f(FB, 34), PINK)
    ctext(d, cx, url_y, "guanhung7484.github.io/delivery-tracker-v2", f(FR, 23), INK2)
    d.line([110, ly, W-110, ly], fill=PINKBG, width=3)
    ctext(d, cx, ly+46, "by Daniel　免費分享給大家用", f(FB, 27), INK)
    pill_t = "LINE：guanhung"; pf = f(FB, 26); pw = d.textlength(pill_t, font=pf)
    px0 = cx - (pw+44)/2
    d.rounded_rectangle([px0, pill_y, px0+pw+44, pill_y+50], radius=25, fill=LINE_G)
    d.text((cx, pill_y+25), pill_t, font=pf, fill=WHITE, anchor="mm")
    img.save(OUT_DIR + r"\分享圖_群組轉傳.png")
    print("saved 群組轉傳")

# ---------------- 貼上 Q版小騎士插圖（向量渲染圖）----------------
RIDER = OUT_DIR + r"\小騎士.png"
def paste_rider(img, cx, top, width):
    r = Image.open(RIDER).convert("RGBA")
    r = r.crop(r.getbbox())                       # 去掉透明邊
    h = round(width * r.height / r.width)
    r = r.resize((width, h), Image.LANCZOS)
    img.paste(r, (cx - width//2, top), r)
    return h

def rider_img(width):
    r = Image.open(RIDER).convert("RGBA"); r = r.crop(r.getbbox())
    h = round(width * r.height / r.width)
    return r.resize((width, h), Image.LANCZOS), h

def dots_center(d, cx, y, fp):
    items = [("foodpanda", PINK), ("Uber Eats", GREEN), ("Lalamove", ORANGE)]
    ws = [d.textlength(n, font=fp) for n, _ in items]
    total = sum(ws) + 38 * (len(items) - 1) + 26 * len(items)
    x = cx - total / 2
    for (name, col), w in zip(items, ws):
        d.ellipse([x, y - 9, x + 18, y + 9], fill=col); x += 26
        d.text((x, y), name, font=fp, fill=INK, anchor="lm"); x += w + 38

# ---------------- 機車貼紙版（含插圖，依圖高自動排版避免重疊）----------------
def make_sticker():
    W = 820; cx = W // 2
    rw = 360
    r = Image.open(RIDER).convert("RGBA"); r = r.crop(r.getbbox())
    rh = round(rw * r.height / r.width); r = r.resize((rw, rh), Image.LANCZOS)
    rtop = 184
    scan_y = rtop + rh + 54
    q = 460; qy = scan_y + 56
    sub_y = qy + q + 44
    url_y = sub_y + 40
    pill_y = url_y + 42
    H = pill_y + 48 + 30
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([14, 14, W-14, H-14], radius=44, outline=PINK, width=14)
    d.rounded_rectangle([60, 70, W-60, 168], radius=26, fill=PINK)
    ctext(d, cx, 119, "外送跑單小幫手", f(FB, 50), WHITE)
    img.paste(r, (cx - rw//2, rtop), r)
    ctext(d, cx, scan_y, "掃我！免費記帳", f(FB, 52), INK)
    qx = cx - q//2
    d.rounded_rectangle([qx-18, qy-18, qx+q+18, qy+q+18], radius=22, outline=(235,235,235), width=4)
    img.paste(qr_img(q, DARK), (qx, qy))
    ctext(d, cx, sub_y, "記錄每天時薪 · 收入 · 里程", f(FB, 30), INK2)
    ctext(d, cx, url_y, "guanhung7484.github.io/delivery-tracker-v2", f(FR, 22), INK2)
    pill_t = "by Daniel　LINE：guanhung"; pf = f(FB, 25); pw = d.textlength(pill_t, font=pf)
    px0 = cx - (pw+44)/2
    d.rounded_rectangle([px0, pill_y, px0+pw+44, pill_y+48], radius=24, fill=LINE_G)
    d.text((cx, pill_y+24), pill_t, font=pf, fill=WHITE, anchor="mm")
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

# ---------------- 橫式 banner（小騎士 | QR | 文字 三欄）----------------
def make_banner():
    W, H = 1200, 630
    img = hgrad(W, H, PINKBG, MINTBG)
    d = ImageDraw.Draw(img)
    # 左：小騎士
    ri, rh = rider_img(250)
    img.paste(ri, (26, (H - rh)//2), ri)
    # 中：QR 白卡
    q = 310; qx = 320; qy = (H - q)//2
    d.rounded_rectangle([qx-26, qy-26, qx+q+26, qy+q+26], radius=26, fill=WHITE)
    img.paste(qr_img(q, DARK), (qx, qy))
    # 右：文字
    X = 690
    d.text((X, 142), "外送跑單小幫手", font=f(FB, 46), fill=PINK, anchor="lm")
    d.text((X, 200), "每天跑單時薪、收入、里程，一鍵算好", font=f(FR, 22), fill=INK2, anchor="lm")
    dots_row(d, X, 252, f(FB, 18))
    d.text((X, 314), "手機掃一掃，免費開始記帳", font=f(FB, 30), fill=PINK, anchor="lm")
    d.text((X, 362), "guanhung7484.github.io/delivery-tracker-v2", font=f(FR, 17), fill=INK2, anchor="lm")
    d.line([X, 404, W-54, 404], fill=PINKBG, width=3)
    d.text((X, 452), "by Daniel", font=f(FB, 26), fill=INK, anchor="lm")
    pt = "LINE：guanhung"; pf = f(FB, 24); pw = d.textlength(pt, font=pf)
    bx = X + d.textlength("by Daniel", font=f(FB, 26)) + 24
    d.rounded_rectangle([bx, 430, bx+pw+38, 476], radius=23, fill=LINE_G)
    d.text((bx+19, 453), pt, font=pf, fill=WHITE, anchor="lm")
    img.save(OUT_DIR + r"\分享圖_橫式banner.png")
    print("saved 橫式banner")

# ---------------- 去背版（透明背景，含小騎士）----------------
def make_transparent():
    W = 760; cx = W // 2
    ri, rh = rider_img(260)
    rtop = 226
    q = 430; qy = rtop + rh + 22
    cta_y = qy + q + 66; url_y = qy + q + 110; pill_y = url_y + 36
    H = int(pill_y + 48 + 30)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # 全透明背景
    d = ImageDraw.Draw(img)
    ctext(d, cx, 92, "外送跑單小幫手", f(FB, 50), PINK)
    ctext(d, cx, 148, "每天跑單時薪、收入、里程，一鍵算好", f(FR, 24), INK2)
    dots_center(d, cx, 192, f(FB, 22))
    img.alpha_composite(ri, (cx - 260 // 2, rtop))
    qx = cx - q // 2
    d.rounded_rectangle([qx-24, qy-24, qx+q+24, qy+q+24], radius=24, fill=(255,255,255,255), outline=PINK, width=4)
    img.paste(qr_img(q, DARK).convert("RGBA"), (qx, qy))
    ctext(d, cx, cta_y, "手機掃一掃，免費開始記帳", f(FB, 32), PINK)
    ctext(d, cx, url_y, "guanhung7484.github.io/delivery-tracker-v2", f(FR, 22), INK2)
    pt = "by Daniel　LINE：guanhung"; pf = f(FB, 25); pw = d.textlength(pt, font=pf)
    px0 = cx - (pw+44)/2
    d.rounded_rectangle([px0, pill_y, px0+pw+44, pill_y+48], radius=24, fill=LINE_G)
    d.text((cx, pill_y+24), pt, font=pf, fill=WHITE, anchor="mm")
    img.save(OUT_DIR + r"\分享圖_去背透明.png")
    print("saved 去背透明")

make_share()
make_sticker()
make_banner()
make_transparent()
print("DONE")
