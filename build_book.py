from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from PIL import Image

pdfmetrics.registerFont(TTFont("ZH", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))

W, H = 180 * mm, 250 * mm
CREAM = HexColor("#F3E3C3")
RED = HexColor("#A31515")
INK = HexColor("#2B1B12")

PAGES = [
    ("邯鄲道上的客店", "images/fig1.jpg", [
        "唐朝開元年間，在邯鄲的路邊，有一間小小的客店。",
        "年輕的讀書人盧生，穿著一身舊衣裳，坐在板凳上唉聲嘆氣：「大丈夫活在世上，應該建功立業、出將入相。可我到現在，還在田裡種地，真是窮困啊！」",
        "坐在對面的老道士呂翁，摸著白鬍子，靜靜地聽著。"]),
    ("一個青瓷枕", "images/fig2.jpg", [
        "這時，店主人正在灶上蒸一鍋黃粱飯。",
        "呂翁從袋子裡拿出一個青瓷枕頭，兩端各有一個圓圓的小孔。「枕著它睡一會兒吧，」他微笑著說，「它能讓你得到想要的一切。」",
        "盧生打了個呵欠，把頭靠上枕頭——那小孔竟越變越大，大得像一扇門。"]),
    ("金榜題名，娶得佳人", "images/fig3.jpg", [
        "盧生走進小孔，眼前出現一座氣派的大宅院。",
        "他娶了名門崔家美麗的女兒，第二年又考中進士，穿上紅色官袍，騎著白馬遊街。一路上鑼鼓喧天，人人都向他道賀。盧生心想：「原來好日子，就是這個樣子！」"]),
    ("出將入相", "images/fig4.jpg", [
        "盧生的官越做越大。",
        "邊疆的敵人來犯，皇帝派他帶兵出征。他站上城牆指揮大軍，打了一場又一場勝仗，開拓了千里疆土。凱旋回朝時，百姓夾道歡迎，皇帝封他做了宰相。"]),
    ("一夕之間，跌落谷底", "images/fig5.jpg", [
        "可是，嫉妒他的人越來越多。",
        "有人誣告盧生謀反，官兵連夜把他捉進大牢。妻子哭得說不出話來。盧生望著窗外，想起從前在家鄉種田的日子：「如果當初只穿粗布衣、騎著小馬走在邯鄲道上，那該有多好啊……」"]),
    ("榮華到老", "images/fig6.jpg", [
        "後來，皇帝查明了真相，讓盧生重新回到朝廷。",
        "他再次當上宰相，享盡榮華富貴。五個兒子都做了大官，孫子十幾個，家中堆滿了金銀珠寶。就這樣過了五十多年，盧生老了、病了，在一片哭聲中，慢慢閉上了眼睛……"]),
    ("黃粱還沒熟", "images/fig7.jpg", [
        "「啊！」盧生猛然坐起來。",
        "他還躺在那間小客店裡，呂翁就坐在身旁，店主人掀開鍋蓋——那鍋黃粱飯，竟然還沒有煮熟！",
        "「難道……這一切都是一場夢？」呂翁笑著說：「人生的得失、榮辱、生死，不也都是這樣嗎？」"]),
]

END = ["盧生沉默了很久，終於明白：得到的會失去，榮耀會褪色，再長的一生，也不過是一鍋黃粱飯的時間。",
       "他向呂翁深深一拜：「謝謝您，讓我看清了人生。」說完，便踏上邯鄲道，回家去了。"]

COPYRIGHT = [
    "書名：黃粱一夢：一個枕頭裡的一生",
    "原著：唐・沈既濟〈枕中記〉",
    "改寫・編輯：〇〇〇（系級、學號）",
    "文字協作：Claude（Anthropic 語言模型）",
    "圖像生成：AI 圖像生成模型（剪紙／版畫風）",
    "出版平台：FlipHTML5",
    "出版日期：2026 年 10 月",
    "課程：AI 生成融入中文學習（東海大學）",
    "",
    "原著〈枕中記〉為公有領域作品。本書之改寫文字與 AI 生成圖像僅供課堂作業使用，未經同意請勿轉載或作商業用途。",
]


def bg(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def wrap(c, text, font, size, maxw):
    lines, cur = [], ""
    for ch in text:
        if c.stringWidth(cur + ch, font, size) > maxw:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def draw_paras(c, paras, x, y, maxw, size=13.5, lead=22, color=INK):
    c.setFillColor(color)
    c.setFont("ZH", size)
    for p in paras:
        for ln in wrap(c, p, "ZH", size, maxw):
            c.drawString(x, y, ln)
            y -= lead
        y -= lead * 0.35
    return y


def centered(c, text, y, size, color=INK):
    c.setFillColor(color)
    c.setFont("ZH", size)
    c.drawCentredString(W / 2, y, text)


c = canvas.Canvas("黃粱一夢.pdf", pagesize=(W, H))
c.setTitle("黃粱一夢：一個枕頭裡的一生")
c.setAuthor("〇〇〇")

# 封面
im = Image.open("images/cover.jpg")
bg(c)
ih = H
iw = ih * im.width / im.height
c.drawImage("images/cover.jpg", (W - iw) / 2, 0, iw, ih)
centered(c, "黃 粱 一 夢", H - 31 * mm, 34, RED)
centered(c, "一個枕頭裡的一生", H - 42 * mm, 14, INK)
c.showPage()

# 版權頁
bg(c)
centered(c, "版 權 頁", H - 45 * mm, 22, RED)
draw_paras(c, COPYRIGHT, 28 * mm, H - 75 * mm, W - 56 * mm, size=12.5, lead=21)
c.showPage()

# 內頁
for n, (title, img, paras) in enumerate(PAGES, 1):
    bg(c)
    margin = 12 * mm
    iw = W - 2 * margin
    im = Image.open(img)
    ih = iw * im.height / im.width
    top = H - 12 * mm
    c.drawImage(img, margin, top - ih, iw, ih)
    y = top - ih - 13 * mm
    c.setFillColor(RED)
    c.setFont("ZH", 18)
    c.drawString(margin, y, title)
    y -= 11 * mm
    draw_paras(c, paras, margin, y, iw)
    c.setFillColor(RED)
    c.setFont("ZH", 10)
    c.drawCentredString(W / 2, 8 * mm, f"— {n} —")
    c.showPage()

# 結尾
bg(c)
centered(c, "夢 醒 之 後", H - 80 * mm, 26, RED)
draw_paras(c, END, 28 * mm, H - 105 * mm, W - 56 * mm, size=14, lead=25)
centered(c, "——全書完——", 60 * mm, 16, RED)
c.showPage()

c.save()
print("ok")
