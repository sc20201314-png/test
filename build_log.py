import re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor

URL = "https://online.fliphtml5.com/nrsqe/ydxd/"
src = open("黃粱一夢_繪本內容.md", encoding="utf-8").read()
B = src.split("## B.")[1]
prompts = re.findall(r"\*\*(圖 \d｜[^\*]+?)\*\*[^\n]*\n```\n(.*?)\n```", B, re.S)
assert len(prompts) == 8, len(prompts)
usage = {"圖 8": "封面（直式 3:4）"}

L = []  # (style, text)
def h(t): L.append(("h", t))
def p(t): L.append(("p", t))
def c_(t): L.append(("c", t))

L.append(("t", "《黃粱一夢》數位繪本：AI 指令紀錄"))
p("作業：AI 生成融入中文學習——跨入圖文創作大門")
p(f"數位繪本網址（FlipHTML5）：{URL}")
p("原著：唐・沈既濟〈枕中記〉｜畫風：剪紙／版畫風")
h("一、給語言模型（Claude，Anthropic）的指令")
p("1. 上傳作業說明截圖，請 AI 協助完成「從中國古典或現代文學作品中節選一篇小故事，製作結合文字與至少五張圖像的數位繪本」。")
p("2. 選擇故事：回答「黃粱一夢」（選項：桃花源記、黃粱一夢、畫龍點睛、背影）。")
p("3. 選擇畫風：回答「剪紙／版畫風」（選項：中國水墨淡彩、溫暖童書插畫、日系動畫風、剪紙／版畫風）。")
p("4. 指令：「給我所有圖片的提示詞」。")
p("語言模型產出：")
p("・將〈枕中記〉改寫成 8 頁兒童可讀的繪本文字（含封面、版權頁、結尾）。")
p("・規劃分鏡，並撰寫 8 段圖像生成提示詞（見下方第二部分）。")
h("二、給圖像生成模型的指令（共 8 段，統一剪紙／版畫風格）")
for title, body in prompts:
    n = title.split("｜")[0]
    c_(f"【{title}】" + (f"　用途：{usage[n]}" if n in usage else "　用途：內頁插圖"))
    c_(body)
h("三、說明")
p("・圖 1～7 為內頁插圖，圖 8 為封面，共 8 張圖像，皆以上列提示詞生成。")
p("・版權頁、封面、排版與 PDF 輸出由 AI 協助完成，並上傳至 FlipHTML5 出版。")

# markdown
with open("指令紀錄.md", "w", encoding="utf-8") as f:
    for s, t in L:
        if s == "t": f.write(f"# {t}\n\n")
        elif s == "h": f.write(f"\n## {t}\n\n")
        elif s == "c": f.write(("```\n" + t + "\n```\n\n") if not t.startswith("【") else f"**{t}**\n\n")
        else: f.write(t + "\n\n")

# pdf
pdfmetrics.registerFont(TTFont("ZH", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
W, H = 210 * mm, 297 * mm
M = 18 * mm
RED = HexColor("#A31515"); INK = HexColor("#222222"); GREY = HexColor("#555555")
cv = canvas.Canvas("指令紀錄.pdf", pagesize=(W, H)); cv.setTitle("黃粱一夢 AI 指令紀錄")
def wrap(t, size, maxw):
    out, cur = [], ""
    for ch in t:
        if cv.stringWidth(cur + ch, "ZH", size) > maxw:
            out.append(cur); cur = ch
        else: cur += ch
    return out + ([cur] if cur else [])
y = H - M
def need(n):
    global y
    if y - n < M:
        cv.showPage(); y = H - M
for s, t in L:
    size, col, lead, ind = {"t": (20, RED, 30, 0), "h": (14, RED, 24, 0), "p": (11, INK, 18, 0), "c": (9.5, GREY, 15, 4 * mm)}[s]
    if s == "h": y -= 6
    for ln in wrap(t, size, W - 2 * M - ind):
        need(lead); cv.setFont("ZH", size); cv.setFillColor(col); cv.drawString(M + ind, y, ln); y -= lead
    y -= 4 if s == "c" else 2
cv.save(); print("ok")
