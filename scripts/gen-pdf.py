# -*- coding: utf-8 -*-
"""
T001 / T011 / T016 のPDFテンプレート（空欄 + 記入例）を reportlab で生成。
出力先: ../public/files/

実行方法:
  cd sites/template-free-jp/web
  python scripts/gen-pdf.py
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4, B5
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, gray, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

# 日本語フォント登録（明朝・ゴシック）
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))     # 明朝（縦書き等の伝統文書向け）
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))  # ゴシック（業務文書向け）

MIN = 'HeiseiMin-W3'
GO = 'HeiseiKakuGo-W5'

OUT_DIR = Path(__file__).parent.parent / "public" / "files"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 共通フッター（記入例のみ注意書きを表示。空欄テンプレは配布元表記なし）
def add_footer(c, page_w, is_example=False):
    if is_example:
        c.setFont(GO, 7)
        c.setFillColor(HexColor('#888888'))
        c.drawString(20*mm, 12*mm, "※ これは記入例です。実際の内容はご自身の状況に合わせて記入してください。")
        c.setFillColor(black)


# ==========================================================
# T001: 退職届 PDF
# ==========================================================

def pdf_taishokutodoke_a4_tategaki(filename, example=False):
    """A4縦書き退職届"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    # 縦書きは reportlab の制約で擬似縦書き（行ごとに縦並び）
    # ただし文字単位での縦書きを再現するのは難しいため、上から下へのレイアウトで近似する

    # 表題（中央上部）
    c.setFont(MIN, 24)
    c.drawCentredString(page_w/2, page_h - 35*mm, "退　職　届")

    # 提出日（右上）
    c.setFont(MIN, 11)
    if example:
        c.drawRightString(page_w - 30*mm, page_h - 60*mm, "令和 7 年 5 月 10 日")
    else:
        c.drawRightString(page_w - 30*mm, page_h - 60*mm, "令和　年　月　日")

    # 本文
    body_y = page_h - 80*mm
    c.setFont(MIN, 12)
    c.drawString(35*mm, body_y, "私事、")
    c.drawString(35*mm, body_y - 10*mm, "この度、一身上の都合により、")
    if example:
        c.drawString(35*mm, body_y - 20*mm, "令和 7 年 6 月 10 日をもって退職いたします。")
    else:
        c.drawString(35*mm, body_y - 20*mm, "令和　年　月　日をもって退職いたします。")

    # 所属・氏名
    sign_y = body_y - 50*mm
    c.setFont(MIN, 11)
    if example:
        c.drawString(120*mm, sign_y,           "所属：　営業部　第一課")
        c.drawString(120*mm, sign_y - 8*mm,    "氏名：　山田　太郎　　　　　　 印")
    else:
        c.drawString(120*mm, sign_y,           "所属：　　　　　　　　　　")
        c.drawString(120*mm, sign_y - 8*mm,    "氏名：　　　　　　　　　　　　 印")

    # 宛名（左下）
    addr_y = sign_y - 30*mm
    c.setFont(MIN, 11)
    if example:
        c.drawString(30*mm, addr_y,        "株式会社サンプル商事")
        c.drawString(30*mm, addr_y - 8*mm, "代表取締役　佐藤　次郎　殿")
    else:
        c.drawString(30*mm, addr_y,        "○○株式会社")
        c.drawString(30*mm, addr_y - 8*mm, "代表取締役　○○　○○　殿")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_taishokutodoke_a4_yokogaki(filename, example=False):
    """A4横書き退職届"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    # 表題
    c.setFont(GO, 22)
    c.drawCentredString(page_w/2, page_h - 30*mm, "退　職　届")

    # 提出日（右）
    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 25*mm, page_h - 55*mm, "令和 7 年 5 月 10 日")
    else:
        c.drawRightString(page_w - 25*mm, page_h - 55*mm, "令和　年　月　日")

    # 宛名（左）
    addr_y = page_h - 70*mm
    c.setFont(GO, 11)
    if example:
        c.drawString(25*mm, addr_y,        "株式会社サンプル商事")
        c.drawString(25*mm, addr_y - 8*mm, "代表取締役　佐藤　次郎　殿")
    else:
        c.drawString(25*mm, addr_y,        "○○株式会社")
        c.drawString(25*mm, addr_y - 8*mm, "代表取締役　○○　○○　殿")

    # 所属・氏名（右）
    sign_y = addr_y - 25*mm
    if example:
        c.drawRightString(page_w - 25*mm, sign_y,           "所属：　営業部　第一課")
        c.drawRightString(page_w - 25*mm, sign_y - 8*mm,    "氏名：　山田　太郎　　　 印")
    else:
        c.drawRightString(page_w - 25*mm, sign_y,           "所属：　　　　　　　　　　")
        c.drawRightString(page_w - 25*mm, sign_y - 8*mm,    "氏名：　　　　　　　　　 印")

    # 本文
    body_y = sign_y - 35*mm
    c.setFont(GO, 12)
    if example:
        c.drawString(25*mm, body_y, "　私事、この度、一身上の都合により、令和 7 年 6 月 10 日をもって")
        c.drawString(25*mm, body_y - 8*mm, "退職いたします。")
    else:
        c.drawString(25*mm, body_y, "　私事、この度、一身上の都合により、令和　年　月　日をもって")
        c.drawString(25*mm, body_y - 8*mm, "退職いたします。")
    c.drawString(25*mm, body_y - 25*mm, "以上")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_taishokutodoke_b5_tategaki(filename, example=False):
    """B5縦書き退職届"""
    page_w, page_h = B5
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=B5)

    c.setFont(MIN, 20)
    c.drawCentredString(page_w/2, page_h - 25*mm, "退　職　届")

    c.setFont(MIN, 10)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和 7 年 5 月 10 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和　年　月　日")

    body_y = page_h - 70*mm
    c.setFont(MIN, 11)
    c.drawString(28*mm, body_y, "私事、")
    c.drawString(28*mm, body_y - 9*mm, "この度、一身上の都合により、")
    if example:
        c.drawString(28*mm, body_y - 18*mm, "令和 7 年 6 月 10 日をもって退職いたします。")
    else:
        c.drawString(28*mm, body_y - 18*mm, "令和　年　月　日をもって退職いたします。")

    sign_y = body_y - 45*mm
    if example:
        c.drawString(95*mm, sign_y,           "所属：　営業部　第一課")
        c.drawString(95*mm, sign_y - 7*mm,    "氏名：　山田　太郎　　 印")
    else:
        c.drawString(95*mm, sign_y,           "所属：　　　　　　　　")
        c.drawString(95*mm, sign_y - 7*mm,    "氏名：　　　　　　　　 印")

    addr_y = sign_y - 25*mm
    if example:
        c.drawString(22*mm, addr_y,        "株式会社サンプル商事")
        c.drawString(22*mm, addr_y - 7*mm, "代表取締役　佐藤　次郎　殿")
    else:
        c.drawString(22*mm, addr_y,        "○○株式会社")
        c.drawString(22*mm, addr_y - 7*mm, "代表取締役　○○　○○　殿")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


# ==========================================================
# T011: 労働条件通知書 PDF
# ==========================================================

def _draw_table_row(c, x, y, label, value, label_w, value_w, row_h, font, font_size):
    """テーブル行を描画"""
    # 罫線
    c.setStrokeColor(HexColor('#888'))
    c.setLineWidth(0.5)
    c.rect(x, y, label_w, row_h, stroke=1, fill=0)
    c.rect(x + label_w, y, value_w, row_h, stroke=1, fill=0)
    # 背景（ラベル列）
    c.setFillColor(HexColor('#F5F0E8'))
    c.rect(x, y, label_w, row_h, stroke=0, fill=1)
    # テキスト
    c.setFillColor(black)
    c.setFont(font, font_size)
    c.drawString(x + 3*mm, y + row_h - 5*mm, label)
    # value (multi-line possible)
    if isinstance(value, list):
        for i, v in enumerate(value):
            c.drawString(x + label_w + 3*mm, y + row_h - 5*mm - i*4*mm, v)
    else:
        c.drawString(x + label_w + 3*mm, y + row_h - 5*mm, value)


def pdf_roudoujouken_seishain(filename, example=False):
    """労働条件通知書 正社員用"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 25*mm, "労働条件通知書")

    c.setFont(GO, 9)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 38*mm, "令和 7 年 5 月 10 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 38*mm, "令和　年　月　日")

    # 宛名
    c.setFont(GO, 11)
    if example:
        c.drawString(20*mm, page_h - 50*mm, "山田　太郎　殿")
    else:
        c.drawString(20*mm, page_h - 50*mm, "　　　　　　　殿")

    # 事業主
    c.setFont(GO, 9)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 60*mm, "事業所名称：株式会社サンプル商事")
        c.drawRightString(page_w - 20*mm, page_h - 65*mm, "所在地：東京都千代田区サンプル町1-2-3")
        c.drawRightString(page_w - 20*mm, page_h - 70*mm, "代表者：代表取締役　佐藤　次郎")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 60*mm, "事業所名称：")
        c.drawRightString(page_w - 20*mm, page_h - 65*mm, "所在地：")
        c.drawRightString(page_w - 20*mm, page_h - 70*mm, "代表者：")

    # テーブル（労働条件）
    items_blank = [
        ("契約期間", "期間の定めなし（無期労働契約）"),
        ("就業場所", "（雇入れ直後）　　　　／（変更の範囲）　　　　"),
        ("従事業務", "（雇入れ直後）　　　　／（変更の範囲）　　　　"),
        ("始業終業時刻", "始業 　時　分　／　終業 　時　分"),
        ("休憩時間", "　　時　分から　　時　分までの 　分"),
        ("所定外労働", "有 / 無"),
        ("休日", "毎週　曜日、国民の祝日、その他（　　　　）"),
        ("休暇", "年次有給休暇： 法定通り付与"),
        ("賃金（基本給）", "月給　　　　　円"),
        ("諸手当", "（内訳）"),
        ("固定残業代", "有（　　円・　時間相当） / 無"),
        ("賃金支払", "毎月　日締切・翌月　日支払"),
        ("退職事項", "定年制　歳／自己都合：退職する　日前に届出"),
        ("社会保険", "健康保険・厚生年金・雇用保険・労災保険"),
    ]
    items_example = [
        ("契約期間", "期間の定めなし（無期労働契約）"),
        ("就業場所", "（雇入れ直後）東京都千代田区サンプル町1-2-3 ／（変更の範囲）当社全事業所"),
        ("従事業務", "（雇入れ直後）営業／（変更の範囲）会社が定める業務"),
        ("始業終業時刻", "始業 9 時 0 分 ／ 終業 18 時 0 分"),
        ("休憩時間", "12 時 0 分から 13 時 0 分までの 60 分"),
        ("所定外労働", "有（時間外労働あり）"),
        ("休日", "毎週 土日曜日、国民の祝日、年末年始（12/30〜1/3）"),
        ("休暇", "年次有給休暇：法定通り付与（入社6ヶ月後10日）"),
        ("賃金（基本給）", "月給 250,000 円"),
        ("諸手当", "通勤手当：実費（上限月3万円）／役職手当：規定による"),
        ("固定残業代", "有（50,000 円・45 時間相当）"),
        ("賃金支払", "毎月 末日 締切・翌月 25 日支払"),
        ("退職事項", "定年制 60 歳／自己都合：退職する 30 日前に届出"),
        ("社会保険", "健康保険・厚生年金・雇用保険・労災保険"),
    ]
    items = items_example if example else items_blank

    table_top = page_h - 80*mm
    row_h = 8*mm
    label_w = 38*mm
    value_w = 132*mm
    for i, (k, v) in enumerate(items):
        y = table_top - (i+1)*row_h
        _draw_table_row(c, 20*mm, y, k, v, label_w, value_w, row_h, GO, 8.5)

    # 改正注記
    c.setFont(GO, 7)
    c.setFillColor(HexColor('#666'))
    c.drawString(20*mm, 20*mm, "※ 本通知書は労働基準法第15条に基づく書面交付の様式です。")
    c.drawString(20*mm, 16*mm, "※ 2024年4月改正により、就業場所・業務の「変更の範囲」明示が義務化されました。")
    c.setFillColor(black)

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_roudoujouken_keiyaku(filename, example=False):
    """労働条件通知書 契約社員用（有期）"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 25*mm, "労働条件通知書（契約社員用）")

    items = [
        ("契約期間", "期間の定めあり（　年　月　日 〜 　年　月　日）"),
        ("契約更新", "自動更新／更新する場合がある／更新しない"),
        ("更新の上限", "通算契約期間 　年・更新回数 　回"),
        ("無期転換", "5年超で無期転換申込権が発生"),
        ("就業場所", "（雇入れ直後）／（変更の範囲）"),
        ("従事業務", "（雇入れ直後）／（変更の範囲）"),
        ("始業終業時刻", "始業 　時　分／終業 　時　分"),
        ("休日・休暇", "毎週　曜日／年次有給休暇 法定通り"),
        ("賃金", "時給 　円／月給 　円"),
        ("賃金支払", "毎月　日締切・翌月　日支払"),
        ("退職", "契約期間満了で終了"),
        ("社会保険", "健康保険・厚生年金・雇用保険・労災保険"),
    ]

    table_top = page_h - 45*mm
    row_h = 9*mm
    label_w = 40*mm
    value_w = 130*mm
    for i, (k, v) in enumerate(items):
        y = table_top - (i+1)*row_h
        _draw_table_row(c, 20*mm, y, k, v, label_w, value_w, row_h, GO, 9)

    add_footer(c, page_w, False)
    c.showPage()
    c.save()


def pdf_roudoujouken_arbeit(filename, example=False):
    """労働条件通知書 アルバイト/パート用"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 25*mm, "労働条件通知書（アルバイト・パート用）")

    items = [
        ("契約期間", "期間の定めあり（　年　月　日 〜 　年　月　日）"),
        ("契約更新", "あり（更新条件：勤務態度・業務成績）／なし"),
        ("就業場所", "（雇入れ直後）／（変更の範囲）"),
        ("業務内容", "（例）販売業務／レジ業務／清掃／調理補助"),
        ("勤務時間", "シフト制（週　日・1日　時間程度）"),
        ("時給", "　　　円／時"),
        ("賃金支払", "毎月　日締切・翌月　日支払"),
        ("交通費", "有（実費・上限月　円）／無"),
        ("有給休暇", "雇入れ6ヶ月後・所定労働日数の8割以上出勤で付与"),
        ("社会保険", "週20時間以上：雇用保険／週30時間以上：健康保険・厚生年金"),
    ]

    table_top = page_h - 45*mm
    row_h = 9*mm
    label_w = 40*mm
    value_w = 130*mm
    for i, (k, v) in enumerate(items):
        y = table_top - (i+1)*row_h
        _draw_table_row(c, 20*mm, y, k, v, label_w, value_w, row_h, GO, 9)

    add_footer(c, page_w, False)
    c.showPage()
    c.save()


# ==========================================================
# T016: 業務委託契約書 PDF
# ==========================================================

def pdf_gyoumu_itaku(filename, contract_type, example=False):
    """業務委託契約書"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    # 表題
    c.setFont(GO, 16)
    c.drawCentredString(page_w/2, page_h - 25*mm, f"業務委託契約書（{contract_type}）")

    # 序文
    c.setFont(GO, 10)
    if example:
        intro_lines = [
            "株式会社サンプル商事（以下「甲」という）と山田　太郎（以下「乙」という）",
            "は、甲が乙に対し業務を委託することにつき、以下のとおり契約（以下「本契約」",
            "という）を締結する。",
        ]
    else:
        intro_lines = [
            "○○株式会社（以下「甲」という）と○○○○（以下「乙」という）は、",
            "甲が乙に対し業務を委託することにつき、以下のとおり契約（以下「本契約」",
            "という）を締結する。",
        ]
    for i, line in enumerate(intro_lines):
        c.drawString(20*mm, page_h - 40*mm - i*5*mm, line)

    # 条文
    if example:
        clauses = [
            ("第1条（業務内容）", "甲は乙に対し、以下の業務を委託し、乙はこれを受託する。\n（1）営業支援コンサルティング業務\n（2）営業資料の作成・改訂"),
            ("第2条（契約期間）", "本契約の有効期間は、令和7年6月1日から令和8年5月31日までとする。"),
            ("第3条（報酬）", "甲は乙に対し、本業務の対価として月額金 300,000 円（消費税別）を支払う。\n乙は毎月末日締めで請求書を発行し、甲は翌月末日までに乙の指定する銀行口座に振り込む。"),
            ("第4条（業務遂行）", "乙は善良な管理者の注意をもって本業務を遂行する。乙は本業務の遂行方法、時間、場所について自己の裁量で決定するものとし、甲は乙に対して具体的な指揮命令を行わない。"),
            ("第5条（知的財産権）", "本業務に伴い創出された成果物の知的財産権は、甲が乙に対し本契約に基づく対価を全額支払った時点で乙から甲に移転する。"),
            ("第6条（秘密保持）", "甲および乙は、本契約に関連して知り得た相手方の秘密情報を、相手方の事前の書面承諾なく第三者に開示・漏洩してはならない。"),
            ("第7条（損害賠償）", "本契約上の義務違反により相手方に損害を与えた場合、その損害（直接損害に限る）を賠償する。賠償額の上限は、直近12ヶ月分の報酬総額を超えないものとする。"),
            ("第8条（解除）", "相手方が本契約上の義務に違反し、相当期間の催告をしても是正されない場合、本契約を解除できる。"),
            ("第9条（協議事項）", "本契約に定めのない事項は、甲乙誠意をもって協議のうえ解決する。"),
            ("第10条（管轄）", "本契約は日本法に準拠し、東京地方裁判所を第一審の専属的合意管轄裁判所とする。"),
        ]
    else:
        clauses = [
            ("第1条（業務内容）", "甲は乙に対し、以下の業務を委託し、乙はこれを受託する。\n（1）　　　　　　　　　　\n（2）　　　　　　　　　　"),
            ("第2条（契約期間）", "本契約の有効期間は、令和　年　月　日から令和　年　月　日までとする。"),
            ("第3条（報酬）", "甲は乙に対し、本業務の対価として月額金 　　　　 円（消費税別）を支払う。"),
            ("第4条（業務遂行）", "乙は善良な管理者の注意をもって本業務を遂行する。乙は本業務の遂行方法、時間、場所について自己の裁量で決定するものとし、甲は乙に対して具体的な指揮命令を行わない。"),
            ("第5条（知的財産権）", "本業務に伴い創出された成果物の知的財産権は、甲が乙に対し本契約に基づく対価を全額支払った時点で乙から甲に移転する。"),
            ("第6条（秘密保持）", "甲および乙は、本契約に関連して知り得た相手方の秘密情報を、相手方の事前の書面承諾なく第三者に開示・漏洩してはならない。"),
            ("第7条（損害賠償）", "本契約上の義務違反により相手方に損害を与えた場合、その損害（直接損害に限る）を賠償する。賠償額の上限は、直近12ヶ月分の報酬総額を超えないものとする。"),
            ("第8条（解除）", "相手方が本契約上の義務に違反し、相当期間の催告をしても是正されない場合、本契約を解除できる。"),
            ("第9条（協議事項）", "本契約に定めのない事項は、甲乙誠意をもって協議のうえ解決する。"),
            ("第10条（管轄）", "本契約は日本法に準拠し、　地方裁判所を第一審の専属的合意管轄裁判所とする。"),
        ]

    y = page_h - 65*mm
    for title, body in clauses:
        c.setFont(GO, 10)
        c.drawString(20*mm, y, title)
        y -= 5*mm
        c.setFont(GO, 9)
        # 改行を考慮して描画
        for line in body.split('\n'):
            # 1行が長すぎる場合は60文字程度で折り返す
            wrapped = []
            current = ""
            for ch in line:
                current += ch
                if len(current) >= 50:
                    wrapped.append(current)
                    current = ""
            if current:
                wrapped.append(current)
            for w in wrapped:
                c.drawString(22*mm, y, w)
                y -= 4.5*mm
        y -= 2*mm
        # ページが満杯なら改ページ
        if y < 35*mm:
            add_footer(c, page_w, example)
            c.showPage()
            c.setFont(GO, 10)
            y = page_h - 25*mm

    # 末尾
    y -= 5*mm
    c.setFont(GO, 9)
    if example:
        c.drawString(20*mm, y, "本契約の成立を証するため、本書2通を作成し、甲乙記名押印のうえ各1通を保有する。")
        c.drawString(20*mm, y - 8*mm, "令和 7 年 5 月 10 日")
        y -= 18*mm
        c.setFont(GO, 10)
        c.drawString(20*mm, y, "（甲）東京都千代田区サンプル町1-2-3")
        c.drawString(20*mm, y - 5*mm, "　　　株式会社サンプル商事　代表取締役　佐藤　次郎　印")
        c.drawString(20*mm, y - 15*mm, "（乙）東京都新宿区サンプル町4-5-6")
        c.drawString(20*mm, y - 20*mm, "　　　山田　太郎　印")
    else:
        c.drawString(20*mm, y, "本契約の成立を証するため、本書2通を作成し、甲乙記名押印のうえ各1通を保有する。")
        c.drawString(20*mm, y - 8*mm, "令和　年　月　日")
        y -= 18*mm
        c.setFont(GO, 10)
        c.drawString(20*mm, y,        "（甲）　　　　　　　　　　　　　　　印")
        c.drawString(20*mm, y - 10*mm, "（乙）　　　　　　　　　　　　　　　印")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


# ==========================================================
# Main
# ==========================================================

# ==========================================================
# T002: 退職届 無料特化（T001 の派生・横書き or 縦書き）
# ==========================================================

def pdf_taishokutodoke_muryou_a4(filename, example=False):
    pdf_taishokutodoke_a4_yokogaki(filename, example=example)


def pdf_taishokutodoke_muryou_a4_tategaki(filename, example=False):
    pdf_taishokutodoke_a4_tategaki(filename, example=example)


# ==========================================================
# T007: 始末書 PDF
# ==========================================================

def pdf_shimatsusho(filename, kind, example=False):
    """始末書 PDF（汎用 / 遅刻 / 無断欠勤）"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(MIN, 22)
    c.drawCentredString(page_w/2, page_h - 30*mm, "始　末　書")

    c.setFont(GO, 10)
    if example:
        c.drawRightString(page_w - 25*mm, page_h - 50*mm, "令和 7 年 5 月 12 日")
    else:
        c.drawRightString(page_w - 25*mm, page_h - 50*mm, "令和　年　月　日")

    c.setFont(GO, 11)
    if example:
        c.drawString(25*mm, page_h - 65*mm, "株式会社サンプル商事")
        c.drawString(25*mm, page_h - 73*mm, "代表取締役　佐藤　次郎　殿")
    else:
        c.drawString(25*mm, page_h - 65*mm, "○○株式会社")
        c.drawString(25*mm, page_h - 73*mm, "代表取締役　○○　○○　殿")

    sign_y = page_h - 95*mm
    if example:
        c.drawRightString(page_w - 25*mm, sign_y,        "所属：　営業部　第一課")
        c.drawRightString(page_w - 25*mm, sign_y - 8*mm, "氏名：　山田　太郎　　 印")
    else:
        c.drawRightString(page_w - 25*mm, sign_y,        "所属：　　　　　　　　　")
        c.drawRightString(page_w - 25*mm, sign_y - 8*mm, "氏名：　　　　　　　　　 印")

    body_y = sign_y - 30*mm
    c.setFont(GO, 11)

    if kind == 'chikoku':  # 遅刻
        body_lines = [
            "　この度、私の不注意により下記のとおり遅刻いたしましたこと、",
            "深くお詫び申し上げます。",
            "",
            "【遅刻日時】",
            "  令和 7 年 5 月 11 日　9 時 35 分到着（始業 9:00）" if example else "  令和　年　月　日　　時　分到着",
            "",
            "【遅刻理由】",
            "  乗車予定の電車に遅延が発生し、振替輸送の手配が遅れたため。" if example else "  　　　　　　　　　　　　",
            "",
            "【再発防止策】",
            "  始業時刻の30分前までに出勤するよう、生活習慣を改善いたします。",
            "",
            "業務に支障をきたしましたこと重ねてお詫び申し上げます。",
            "今後二度とこのようなことが起こらぬよう、誠心誠意業務に従事することを誓います。",
        ]
    elif kind == 'mudankin':  # 無断欠勤
        body_lines = [
            "　この度、私の不徳の致すところにより、下記の通り無断にて",
            "欠勤いたしましたこと、深くお詫び申し上げます。",
            "",
            "【欠勤日】令和 7 年 5 月 11 日（月曜日）" if example else "【欠勤日】令和　年　月　日（　曜日）",
            "",
            "【欠勤理由】",
            "  体調不良により始業時刻前に連絡を入れる猶予がございませんでした。" if example else "  　　　　　　　　　　　",
            "",
            "【再発防止策】",
            "  体調管理を徹底し、緊急時には始業時刻前に必ず連絡を入れるよう徹底します。",
            "",
            "勝手な行動により多大なご迷惑をおかけしましたこと、重ねてお詫び申し上げます。",
        ]
    else:  # general 汎用
        body_lines = [
            "　この度、私の不注意により下記のような事態を引き起こしましたこと、",
            "深くお詫び申し上げます。",
            "",
            "【事案概要】",
            "  　　　　　　　　　　　　　　",
            "",
            "【発生原因】",
            "  　　　　　　　　　　　　　　",
            "",
            "【再発防止策】",
            "  　　　　　　　　　　　　　　",
            "",
            "今後はこのようなことが二度と起こらぬよう、十分に注意して業務に従事することを誓います。",
        ]

    for i, line in enumerate(body_lines):
        c.drawString(25*mm, body_y - i*5*mm, line)

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_shimatsusho_general(filename, example=False):
    pdf_shimatsusho(filename, 'general', example=example)

def pdf_shimatsusho_chikoku(filename, example=False):
    pdf_shimatsusho(filename, 'chikoku', example=example)


# ==========================================================
# T012: 雇用契約書 PDF
# ==========================================================

def pdf_koyou_keiyakusho(filename, kind_label, items, example=False):
    """雇用契約書 PDF"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 25*mm, f"雇用契約書（{kind_label}）")

    c.setFont(GO, 10)
    if example:
        c.drawString(20*mm, page_h - 42*mm, "株式会社サンプル商事（以下「甲」という）と山田　太郎（以下「乙」という）は、")
        c.drawString(20*mm, page_h - 47*mm, "甲が乙を雇用することにつき、以下のとおり雇用契約を締結する。")
    else:
        c.drawString(20*mm, page_h - 42*mm, "○○株式会社（以下「甲」という）と○○○○（以下「乙」という）は、")
        c.drawString(20*mm, page_h - 47*mm, "甲が乙を雇用することにつき、以下のとおり雇用契約を締結する。")

    table_top = page_h - 60*mm
    row_h = 8*mm
    label_w = 36*mm
    value_w = 134*mm
    for i, (k, v) in enumerate(items):
        y = table_top - (i+1)*row_h
        _draw_table_row(c, 20*mm, y, k, v, label_w, value_w, row_h, GO, 8.5)

    end_y = table_top - len(items)*row_h - 10*mm
    c.setFont(GO, 9)
    if example:
        c.drawString(20*mm, end_y, "本契約の成立を証するため、本書2通を作成し、甲乙各自署名押印のうえ各1通を保有する。")
        c.drawString(20*mm, end_y - 7*mm, "令和 7 年 5 月 1 日")
        c.setFont(GO, 10)
        c.drawString(20*mm, end_y - 18*mm, "（甲）東京都千代田区サンプル町1-2-3")
        c.drawString(20*mm, end_y - 23*mm, "　　　株式会社サンプル商事 代表取締役 佐藤 次郎 印")
        c.drawString(20*mm, end_y - 33*mm, "（乙）山田 太郎 印")
    else:
        c.drawString(20*mm, end_y, "本契約の成立を証するため、本書2通を作成し、甲乙各自署名押印のうえ各1通を保有する。")
        c.drawString(20*mm, end_y - 7*mm, "令和　年　月　日")
        c.setFont(GO, 10)
        c.drawString(20*mm, end_y - 18*mm, "（甲）　　　　　　　　　　　　　　　印")
        c.drawString(20*mm, end_y - 28*mm, "（乙）　　　　　　　　　　　　　　　印")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_koyou_keiyakusho_seishain(filename, example=False):
    if example:
        items = [
            ("契約期間", "期間の定めなし（無期労働契約）"),
            ("試用期間", "採用日から 3 ヶ月（賃金条件は本契約と同じ）"),
            ("就業場所", "（雇入れ直後）東京都千代田区サンプル町1-2-3 ／（変更の範囲）当社全事業所"),
            ("従事業務", "（雇入れ直後）営業／（変更の範囲）会社が定める業務"),
            ("始業終業", "始業 9 時 0 分／終業 18 時 0 分／休憩 60 分"),
            ("休日休暇", "毎週 土日曜日、国民の祝日／年次有給休暇 法定通り"),
            ("賃金", "基本給 月給 250,000 円／通勤手当（実費上限月3万円）"),
            ("固定残業代", "有（50,000 円・45 時間相当）"),
            ("賃金支払", "毎月 末日 締切・翌月 25 日支払（口座振込）"),
            ("退職", "定年制 60 歳／自己都合：退職する 30 日前に届出"),
            ("社会保険", "健康保険・厚生年金・雇用保険・労災保険"),
            ("競業避止義務", "在職中および退職後 1 年間、同業他社への就業を禁止"),
            ("秘密保持", "本契約に関連して知り得た秘密情報を第三者に開示しない"),
        ]
    else:
        items = [
            ("契約期間", "期間の定めなし（無期労働契約）"),
            ("試用期間", "採用日から　ヶ月"),
            ("就業場所", "（雇入れ直後）／（変更の範囲）"),
            ("従事業務", "（雇入れ直後）／（変更の範囲）"),
            ("始業終業", "始業 　時　分／終業 　時　分／休憩 　分"),
            ("休日休暇", "毎週　曜日／年次有給休暇 法定通り"),
            ("賃金", "基本給 月給 　円／諸手当"),
            ("固定残業代", "有（　円・　時間相当）／無"),
            ("賃金支払", "毎月　日締切・翌月　日支払"),
            ("退職", "定年制 　歳／自己都合：退職する　日前に届出"),
            ("社会保険", "健康保険・厚生年金・雇用保険・労災保険"),
            ("競業避止義務", "在職中および退職後　年間"),
            ("秘密保持", "秘密情報を第三者に開示しない"),
        ]
    pdf_koyou_keiyakusho(filename, "正社員", items, example=example)


def pdf_koyou_keiyakusho_keiyaku(filename, example=False):
    items = [
        ("契約期間", "期間の定めあり（　年　月　日 〜 　年　月　日）"),
        ("契約更新", "自動更新／更新する場合がある／更新しない"),
        ("更新の上限", "通算契約期間 　年・更新回数 　回"),
        ("無期転換", "5年超で無期転換申込権が発生（労契法18条）"),
        ("就業場所", "（雇入れ直後）／（変更の範囲）"),
        ("従事業務", "（雇入れ直後）／（変更の範囲）"),
        ("始業終業", "始業 　時　分／終業 　時　分"),
        ("休日休暇", "毎週　曜日／年次有給休暇 法定通り"),
        ("賃金", "時給／月給 　円"),
        ("賃金支払", "毎月　日締切・翌月　日支払"),
        ("退職", "契約期間満了で終了"),
        ("社会保険", "健康保険・厚生年金・雇用保険・労災保険"),
    ]
    pdf_koyou_keiyakusho(filename, "契約社員", items, example=example)


def pdf_koyou_keiyakusho_arbeit(filename, example=False):
    items = [
        ("契約期間", "期間の定めあり（　年　月　日 〜 　年　月　日）"),
        ("契約更新", "あり（更新条件：勤務態度・業務成績）／なし"),
        ("就業場所", "（雇入れ直後）／（変更の範囲）"),
        ("業務内容", "販売／レジ／清掃／調理補助"),
        ("勤務時間", "シフト制（週　日・1日　時間程度）"),
        ("時給", "　　　円／時"),
        ("賃金支払", "毎月　日締切・翌月　日支払"),
        ("交通費", "有（実費・上限月　円）／無"),
        ("有給休暇", "雇入れ6ヶ月後・所定労働日数の8割以上出勤で付与"),
        ("社会保険", "週20時間以上：雇用保険／週30時間以上：健康保険・厚生年金"),
    ]
    pdf_koyou_keiyakusho(filename, "アルバイト・パート", items, example=example)


# ==========================================================
# T023: 請求書（個人事業主）PDF
# ==========================================================
def pdf_seikyu_kojin(filename, example=False):
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(MIN, 22)
    c.drawCentredString(page_w/2, page_h - 25*mm, "請　求　書")

    c.setFont(GO, 10)
    if example:
        c.drawString(20*mm, page_h - 45*mm, "株式会社サンプル商事 御中")
        c.drawRightString(page_w - 20*mm, page_h - 45*mm, "請求日： 令和 7 年 5 月 31 日")
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "請求番号： INV-2026-0512")
        c.drawRightString(page_w - 20*mm, page_h - 55*mm, "支払期限： 令和 7 年 6 月 30 日")
    else:
        c.drawString(20*mm, page_h - 45*mm, "　　　　　　　御中")
        c.drawRightString(page_w - 20*mm, page_h - 45*mm, "請求日： 令和　年　月　日")
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "請求番号：")
        c.drawRightString(page_w - 20*mm, page_h - 55*mm, "支払期限： 令和　年　月　日")

    c.drawString(20*mm, page_h - 65*mm, "下記の通りご請求申し上げます。")

    # 明細表
    table_y = page_h - 80*mm
    headers = ["項目", "数量", "単価", "金額"]
    widths = [85, 25, 30, 30]  # mm
    x = 20*mm
    c.setFillColor(HexColor('#F0F0F0'))
    c.rect(x, table_y, sum(w*mm for w in widths), 8*mm, stroke=0, fill=1)
    c.setFillColor(black)
    c.setFont(GO, 9)
    cx = x
    for i, h in enumerate(headers):
        c.drawCentredString(cx + widths[i]*mm/2, table_y + 3*mm, h)
        c.setStrokeColor(HexColor('#888'))
        c.rect(cx, table_y, widths[i]*mm, 8*mm, stroke=1, fill=0)
        cx += widths[i]*mm

    # 明細行（example 時は記入済）
    rows = []
    if example:
        rows = [
            ("Webサイト制作（5月分）", "1", "300,000", "300,000"),
            ("コーディング修正対応", "5", "5,000", "25,000"),
            ("", "", "", ""),
        ]
    else:
        rows = [("","","","")]*5

    for row in rows:
        ry = table_y - 8*mm
        cx = x
        for i, val in enumerate(row):
            c.setStrokeColor(HexColor('#888'))
            c.rect(cx, ry, widths[i]*mm, 8*mm, stroke=1, fill=0)
            if val:
                c.setFont(GO, 8.5)
                if i == 0:
                    c.drawString(cx + 2*mm, ry + 3*mm, val)
                else:
                    c.drawRightString(cx + widths[i]*mm - 2*mm, ry + 3*mm, val)
            cx += widths[i]*mm
        table_y = ry

    # 合計
    sum_y = table_y - 18*mm
    c.setFont(GO, 9)
    if example:
        c.drawRightString(170*mm, sum_y,         "小計：　325,000 円")
        c.drawRightString(170*mm, sum_y - 5*mm,  "消費税(10%)：　32,500 円")
        c.drawRightString(170*mm, sum_y - 10*mm, "源泉徴収税(10.21%)：△ 33,182 円")
        c.setFont(GO, 11)
        c.drawRightString(170*mm, sum_y - 18*mm, "合計：　324,318 円")
    else:
        c.drawRightString(170*mm, sum_y,         "小計：　　　　円")
        c.drawRightString(170*mm, sum_y - 5*mm,  "消費税(10%)：　　円")
        c.drawRightString(170*mm, sum_y - 10*mm, "源泉徴収税(10.21%)：△　円")
        c.setFont(GO, 11)
        c.drawRightString(170*mm, sum_y - 18*mm, "合計：　　　　円")

    # 振込先 / 発行者
    info_y = sum_y - 35*mm
    c.setFont(GO, 9)
    c.drawString(20*mm, info_y, "【振込先】")
    if example:
        c.drawString(20*mm, info_y - 5*mm,  "銀行名：サンプル銀行  支店：渋谷支店  種別：普通  口座：1234567")
        c.drawString(20*mm, info_y - 10*mm, "口座名義：ヤマダ タロウ")
        c.drawString(20*mm, info_y - 15*mm, "適格請求書発行事業者番号： T1234567890123")
    else:
        c.drawString(20*mm, info_y - 5*mm,  "銀行名：　　　  支店：　　　  種別：普通／当座  口座：")
        c.drawString(20*mm, info_y - 10*mm, "口座名義：")
        c.drawString(20*mm, info_y - 15*mm, "適格請求書発行事業者番号： T")

    c.drawString(20*mm, info_y - 25*mm, "【発行者】")
    if example:
        c.drawString(20*mm, info_y - 30*mm, "氏名／屋号：山田 太郎")
        c.drawString(20*mm, info_y - 35*mm, "住所：東京都新宿区サンプル町4-5-6")
        c.drawString(20*mm, info_y - 40*mm, "電話：03-1234-5678   メール：yamada@example.com")
    else:
        c.drawString(20*mm, info_y - 30*mm, "氏名／屋号：")
        c.drawString(20*mm, info_y - 35*mm, "住所：")
        c.drawString(20*mm, info_y - 40*mm, "電話：")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


# ==========================================================
# T029: 見積書 PDF
# ==========================================================
def pdf_mitsumori(filename, example=False):
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(MIN, 22)
    c.drawCentredString(page_w/2, page_h - 25*mm, "見　積　書")

    c.setFont(GO, 10)
    if example:
        c.drawString(20*mm, page_h - 45*mm, "株式会社サンプル商事 御中")
        c.drawRightString(page_w - 20*mm, page_h - 45*mm, "見積日： 令和 7 年 5 月 12 日")
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "見積番号： Q-2026-0512")
        c.drawRightString(page_w - 20*mm, page_h - 55*mm, "有効期限： 発行日より 30 日間")
    else:
        c.drawString(20*mm, page_h - 45*mm, "　　　　　　　御中")
        c.drawRightString(page_w - 20*mm, page_h - 45*mm, "見積日： 令和　年　月　日")
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "見積番号：")
        c.drawRightString(page_w - 20*mm, page_h - 55*mm, "有効期限： 発行日より　日間")

    c.drawString(20*mm, page_h - 65*mm, "下記の通りお見積申し上げます。")

    table_y = page_h - 80*mm
    headers = ["項目", "数量", "単価", "金額"]
    widths = [85, 25, 30, 30]
    x = 20*mm
    c.setFillColor(HexColor('#F0F0F0'))
    c.rect(x, table_y, sum(w*mm for w in widths), 8*mm, stroke=0, fill=1)
    c.setFillColor(black)
    c.setFont(GO, 9)
    cx = x
    for i, h in enumerate(headers):
        c.drawCentredString(cx + widths[i]*mm/2, table_y + 3*mm, h)
        c.setStrokeColor(HexColor('#888'))
        c.rect(cx, table_y, widths[i]*mm, 8*mm, stroke=1, fill=0)
        cx += widths[i]*mm

    rows = []
    if example:
        rows = [
            ("Webサイト制作一式", "1", "500,000", "500,000"),
            ("レスポンシブ対応", "1", "100,000", "100,000"),
            ("", "", "", ""),
        ]
    else:
        rows = [("","","","")]*5

    for row in rows:
        ry = table_y - 8*mm
        cx = x
        for i, val in enumerate(row):
            c.setStrokeColor(HexColor('#888'))
            c.rect(cx, ry, widths[i]*mm, 8*mm, stroke=1, fill=0)
            if val:
                c.setFont(GO, 8.5)
                if i == 0:
                    c.drawString(cx + 2*mm, ry + 3*mm, val)
                else:
                    c.drawRightString(cx + widths[i]*mm - 2*mm, ry + 3*mm, val)
            cx += widths[i]*mm
        table_y = ry

    sum_y = table_y - 18*mm
    c.setFont(GO, 9)
    if example:
        c.drawRightString(170*mm, sum_y,         "小計：　600,000 円")
        c.drawRightString(170*mm, sum_y - 5*mm,  "消費税(10%)：　60,000 円")
        c.setFont(GO, 11)
        c.drawRightString(170*mm, sum_y - 13*mm, "合計：　660,000 円")
    else:
        c.drawRightString(170*mm, sum_y,         "小計：　　　　円")
        c.drawRightString(170*mm, sum_y - 5*mm,  "消費税(10%)：　　円")
        c.setFont(GO, 11)
        c.drawRightString(170*mm, sum_y - 13*mm, "合計：　　　　円")

    info_y = sum_y - 30*mm
    c.setFont(GO, 9)
    c.drawString(20*mm, info_y, "【発行者】")
    if example:
        c.drawString(20*mm, info_y - 5*mm,  "会社名／屋号：株式会社山田クリエイト")
        c.drawString(20*mm, info_y - 10*mm, "担当者：山田 太郎")
        c.drawString(20*mm, info_y - 15*mm, "住所：東京都新宿区サンプル町4-5-6")
        c.drawString(20*mm, info_y - 20*mm, "電話：03-1234-5678   メール：yamada@example.com")
    else:
        c.drawString(20*mm, info_y - 5*mm,  "会社名／屋号：")
        c.drawString(20*mm, info_y - 10*mm, "担当者：")
        c.drawString(20*mm, info_y - 15*mm, "住所：")
        c.drawString(20*mm, info_y - 20*mm, "電話：")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


# ==========================================================
# T035: 議事録 PDF
# ==========================================================
def pdf_gijiroku(filename, kind, example=False):
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    title_label = {'standard': '標準', '1on1': '1on1', 'brest': 'ブレスト'}.get(kind, '')
    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 25*mm, f"議　事　録（{title_label}）")

    if kind == '1on1':
        if example:
            items = [
                ("実施日時", "令和 7 年 5 月 12 日（月） 14:00 〜 14:30"),
                ("対象者", "山田 太郎"),
                ("実施者", "佐藤 次郎（マネージャー）"),
                ("前回からの進捗", "API 設計タスク完了・コードレビュー対応中"),
                ("業務面の話題", "新機能リリースのスケジュール調整"),
                ("個人面（キャリア）", "上半期の評価面談に向けて、目標達成度を確認"),
                ("課題・困りごと", "他チームとの連携が不足気味"),
                ("マネージャーfb", "良い質問が出ている。継続的に情報共有を"),
                ("ネクストアクション", "・週次定例で他チームと進捗共有（来週から）"),
                ("次回予定", "令和 7 年 5 月 26 日 14:00"),
            ]
        else:
            items = [
                ("実施日時", "令和　年　月　日（　） 　:　 〜 　:　"),
                ("対象者", ""),
                ("実施者", ""),
                ("前回からの進捗", ""),
                ("業務面の話題", ""),
                ("個人面（キャリア）", ""),
                ("課題・困りごと", ""),
                ("マネージャーfb", ""),
                ("ネクストアクション", "・"),
                ("次回予定", ""),
            ]
    else:  # standard or brest
        if example:
            items = [
                ("会議名", "プロダクト定例ミーティング"),
                ("日時", "令和 7 年 5 月 12 日（月） 10:00 〜 11:00"),
                ("場所", "本社 第3会議室 / Zoom"),
                ("出席者", "山田 太郎、佐藤 次郎、鈴木 三郎"),
                ("欠席者", "高橋 花子（出張）"),
                ("議題", "1. 新機能リリース計画\n2. ユーザーフィードバック共有\n3. 次回スプリント目標"),
                ("議事内容", "リリース日を 6/1 に決定。ベータユーザー10社のフィードバックを反映"),
                ("決定事項", "・リリース日：令和 7 年 6 月 1 日\n・ベータ拡大：10社→30社"),
                ("ToDo", "・リリースノート作成（担当：山田／期限：5/20）\n・ベータ追加募集（担当：佐藤／期限：5/15）"),
                ("次回予定", "令和 7 年 5 月 19 日（月） 10:00"),
                ("作成者", "山田 太郎"),
            ]
        else:
            items = [
                ("会議名", ""),
                ("日時", "令和　年　月　日（　） 　:　 〜 　:　"),
                ("場所", ""),
                ("出席者", ""),
                ("欠席者", ""),
                ("議題", "1. \n2. \n3. "),
                ("議事内容", ""),
                ("決定事項", "・\n・"),
                ("ToDo", "・　　　　（担当：　／期限：　）"),
                ("次回予定", ""),
                ("作成者", ""),
            ]

    table_top = page_h - 45*mm
    row_h = 11*mm
    label_w = 38*mm
    value_w = 132*mm
    for i, (k, v) in enumerate(items):
        y = table_top - (i+1)*row_h
        # value 改行を考慮
        lines = v.split('\n') if v else ['']
        actual_h = max(row_h, len(lines) * 5*mm + 4*mm)
        # ラベル背景
        c.setFillColor(HexColor('#F5F0E8'))
        c.rect(20*mm, y - (actual_h - row_h), label_w, actual_h, stroke=0, fill=1)
        c.setFillColor(black)
        c.setStrokeColor(HexColor('#888'))
        c.setLineWidth(0.5)
        c.rect(20*mm, y - (actual_h - row_h), label_w, actual_h, stroke=1, fill=0)
        c.rect(20*mm + label_w, y - (actual_h - row_h), value_w, actual_h, stroke=1, fill=0)
        c.setFont(GO, 9)
        c.drawString(20*mm + 2*mm, y + actual_h - 6*mm - (actual_h - row_h), k)
        for li, line in enumerate(lines):
            c.drawString(20*mm + label_w + 2*mm, y + actual_h - 6*mm - li*5*mm - (actual_h - row_h), line)
        # 次の行はこの actual_h を考慮
        table_top = y - (actual_h - row_h)

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_gijiroku_standard(filename, example=False): pdf_gijiroku(filename, 'standard', example=example)
def pdf_gijiroku_1on1(filename, example=False): pdf_gijiroku(filename, '1on1', example=example)


# ==========================================================
# T020: 秘密保持誓約書 PDF
# ==========================================================
def pdf_himitsuhoji(filename, kind, example=False):
    """秘密保持誓約書 PDF（雇用時 / 退職時）"""
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    title_label = "雇用時" if kind == 'nyusha' else "退職時"
    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 25*mm, f"秘密保持誓約書（{title_label}）")

    c.setFont(GO, 10)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 40*mm, "令和 7 年 5 月 1 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 40*mm, "令和　年　月　日")

    c.setFont(GO, 11)
    if example:
        c.drawString(20*mm, page_h - 55*mm, "株式会社サンプル商事")
        c.drawString(20*mm, page_h - 62*mm, "代表取締役 佐藤 次郎 殿")
    else:
        c.drawString(20*mm, page_h - 55*mm, "○○株式会社")
        c.drawString(20*mm, page_h - 62*mm, "代表取締役 ○○ ○○ 殿")

    sign_y = page_h - 85*mm
    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, sign_y,         "住所： 東京都新宿区サンプル町4-5-6")
        c.drawRightString(page_w - 20*mm, sign_y - 7*mm,  "氏名： 山田 太郎  印")
    else:
        c.drawRightString(page_w - 20*mm, sign_y,         "住所： 　　　　　　　　　　　　　")
        c.drawRightString(page_w - 20*mm, sign_y - 7*mm,  "氏名： 　　　　　　　　　　 印")

    if kind == 'nyusha':
        clauses = [
            ("第1条（秘密保持義務）",
             "私は、貴社における業務上知り得た下記の情報（以下「秘密情報」）について、貴社の事前の書面による承諾なく、第三者に開示・漏洩しない。\n（1）顧客情報・取引先情報　（2）財務情報・経営情報\n（3）人事情報・社員情報　（4）技術情報・営業ノウハウ\n（5）その他、貴社が秘密として指定した情報"),
            ("第2条（目的外使用の禁止）",
             "私は、秘密情報を業務遂行以外の目的で使用しない。"),
            ("第3条（複製の禁止）",
             "秘密情報を含む書類・電子データは、業務上必要な範囲を超えて複製しない。"),
            ("第4条（情報の返還）",
             "退職時、または貴社の指示があったときは、秘密情報を含む一切の書類・電子データを直ちに返還または破棄する。"),
            ("第5条（損害賠償）",
             "本誓約に違反し、貴社に損害を与えた場合、その損害を賠償する。"),
            ("第6条（有効期間）",
             "本誓約による秘密保持義務は、退職後も継続する。"),
        ]
    else:
        clauses = [
            ("第1条（情報の返還）",
             "私は、退職にあたり、在職中に取得した貴社の秘密情報・営業情報・顧客情報を含む一切の書類・電子データ・媒体を貴社に返還または破棄したことを確認する。"),
            ("第2条（秘密保持義務の継続）",
             "退職後も、在職中に知り得た秘密情報を第三者に開示・漏洩しない。"),
            ("第3条（競業避止義務）",
             "退職後 1 年間、貴社の同業他社に就業しない、または貴社と競合する事業を営まない。\n※ 期間・地域は合理的な範囲（最高裁判例に基づき 1〜2 年程度）で個別協議。"),
            ("第4条（顧客等への接触禁止）",
             "退職後 1 年間、在職中に取引した貴社の顧客・取引先に営業活動を行わない。"),
            ("第5条（損害賠償）",
             "本誓約に違反し、貴社に損害を与えた場合、その損害を賠償する。"),
            ("第6条（裁判管轄）",
             "本誓約に関する紛争は、貴社所在地を管轄する裁判所を専属的合意管轄裁判所とする。"),
        ]

    y = sign_y - 25*mm
    for title, body in clauses:
        c.setFont(GO, 10)
        c.drawString(20*mm, y, title)
        y -= 5*mm
        c.setFont(GO, 9)
        for line in body.split('\n'):
            wrapped = []
            current = ""
            for ch in line:
                current += ch
                if len(current) >= 50:
                    wrapped.append(current)
                    current = ""
            if current: wrapped.append(current)
            for w in wrapped:
                c.drawString(22*mm, y, w)
                y -= 4.5*mm
        y -= 2*mm
        if y < 35*mm:
            add_footer(c, page_w, example)
            c.showPage()
            y = page_h - 25*mm

    y -= 6*mm
    c.setFont(GO, 10)
    c.drawString(20*mm, y, "以上の通り誓約いたします。")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_himitsuhoji_nyusha(filename, example=False): pdf_himitsuhoji(filename, 'nyusha', example=example)
def pdf_himitsuhoji_taisha(filename, example=False): pdf_himitsuhoji(filename, 'taisha', example=example)


# ==========================================================
# T019: 秘密保持契約書（NDA）PDF — 双方向 / 片務
# ==========================================================
def pdf_nda(filename, kind='souhou', example=False):
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    title_label = "双方向" if kind == 'souhou' else "片務"
    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 25*mm, f"秘密保持契約書（{title_label}）")

    c.setFont(GO, 10)
    if kind == 'souhou':
        intro = "○○株式会社（以下「甲」という）と○○株式会社（以下「乙」という）は、両者間における取引に関連して開示する秘密情報の取扱いについて、次のとおり秘密保持契約を締結する。"
        if example:
            intro = "株式会社サンプル商事（以下「甲」という）と株式会社サンプル工業（以下「乙」という）は、両者間における新規取引に関連して開示する秘密情報の取扱いについて、次のとおり秘密保持契約を締結する。"
    else:
        intro = "○○株式会社（以下「開示者」という）と○○株式会社（以下「受領者」という）は、開示者から受領者に開示される秘密情報の取扱いについて、次のとおり秘密保持契約を締結する。"
        if example:
            intro = "株式会社サンプル商事（以下「開示者」という）と株式会社サンプル工業（以下「受領者」という）は、開示者から受領者に開示される秘密情報の取扱いについて、次のとおり秘密保持契約を締結する。"

    y = page_h - 38*mm
    for line in [intro[i:i+45] for i in range(0, len(intro), 45)]:
        c.drawString(20*mm, y, line)
        y -= 4.5*mm
    y -= 4*mm

    if kind == 'souhou':
        clauses = [
            ("第1条（秘密情報の定義）",
             "本契約において「秘密情報」とは、本取引に関連して甲または乙が相手方に開示する一切の情報のうち、書面または電子データにより秘密である旨を明示して開示されたもの、および口頭で開示された場合は開示後14日以内に書面で確認したものをいう。\n以下の情報は秘密情報に含まれない。\n（1）開示時に既に公知であった情報　（2）開示後、受領者の責によらず公知となった情報\n（3）受領者が独自に開発した情報　（4）正当な権限を有する第三者から守秘義務なく取得した情報"),
            ("第2条（秘密保持義務）",
             "甲および乙は、相互に開示された秘密情報について、相手方の事前の書面による承諾なく、第三者に開示または漏洩してはならない。"),
            ("第3条（目的外使用の禁止）",
             "甲および乙は、相手方から開示された秘密情報を本取引の遂行以外の目的で使用してはならない。"),
            ("第4条（複製の制限）",
             "甲および乙は、相手方から開示された秘密情報を、本取引の遂行に必要な範囲を超えて複製してはならない。"),
            ("第5条（情報の返還・廃棄）",
             "本契約終了時、または相手方から要求があったときは、開示された秘密情報を含む一切の書類・電子データ・媒体を、相手方の指示に従って返還または廃棄しなければならない。"),
            ("第6条（有効期間）",
             "本契約の有効期間は、本契約締結日から○年間とする。本契約終了後も第2条および第3条の規定は、本契約終了から○年間有効に存続する。"),
            ("第7条（損害賠償）",
             "甲または乙が本契約に違反し、相手方に損害を与えた場合、違反した当事者は相手方に対し、その損害を賠償する責を負う。"),
            ("第8条（合意管轄）",
             "本契約に関する紛争は、○○地方裁判所を第一審の専属的合意管轄裁判所とする。"),
            ("第9条（協議事項）",
             "本契約に定めなき事項、または本契約の解釈について疑義が生じた事項については、甲乙誠実に協議の上、解決する。"),
        ]
    else:
        clauses = [
            ("第1条（秘密情報の定義）",
             "本契約において「秘密情報」とは、開示者から受領者に開示される一切の情報のうち、書面・電子データ・口頭・有形媒体を問わず、開示者が秘密として指定した情報をいう。\n以下の情報は秘密情報に含まれない。\n（1）開示時に既に公知であった情報　（2）開示後、受領者の責によらず公知となった情報\n（3）受領者が独自に開発した情報　（4）正当な権限を有する第三者から守秘義務なく取得した情報"),
            ("第2条（秘密保持義務）",
             "受領者は、開示者から開示された秘密情報について、開示者の事前の書面による承諾なく、第三者に開示または漏洩してはならない。"),
            ("第3条（目的外使用の禁止）",
             "受領者は、開示者から開示された秘密情報を、本契約に定める目的以外に使用してはならない。"),
            ("第4条（複製の制限）",
             "受領者は、開示者から開示された秘密情報を、本契約に定める目的の達成に必要な範囲を超えて複製してはならない。"),
            ("第5条（情報の返還・廃棄）",
             "本契約終了時、または開示者から要求があったときは、受領者は開示された秘密情報を含む一切の書類・電子データ・媒体を、開示者の指示に従って返還または廃棄しなければならない。"),
            ("第6条（有効期間および存続）",
             "本契約の有効期間は、本契約締結日から○年間とする。本契約終了後も第2条および第3条の規定は、本契約終了から○年間有効に存続する。"),
            ("第7条（損害賠償）",
             "受領者が本契約に違反し、開示者に損害を与えた場合、その損害を賠償する責を負う。"),
            ("第8条（合意管轄）",
             "本契約に関する紛争は、開示者の所在地を管轄する地方裁判所を第一審の専属的合意管轄裁判所とする。"),
        ]

    for title, body in clauses:
        c.setFont(GO, 10)
        c.drawString(20*mm, y, title)
        y -= 5*mm
        c.setFont(GO, 9)
        for line in body.split('\n'):
            wrapped = []
            current = ""
            for ch in line:
                current += ch
                if len(current) >= 50:
                    wrapped.append(current)
                    current = ""
            if current:
                wrapped.append(current)
            for w in wrapped:
                c.drawString(22*mm, y, w)
                y -= 4.5*mm
        y -= 2*mm
        if y < 60*mm:
            add_footer(c, page_w, example)
            c.showPage()
            y = page_h - 25*mm

    y -= 6*mm
    c.setFont(GO, 10)
    c.drawString(20*mm, y, "本契約締結の証として、本書2通を作成し、各当事者1通ずつ保有する。")
    y -= 12*mm

    c.setFont(GO, 10)
    if example:
        c.drawRightString(page_w - 20*mm, y, "令和 7 年 5 月 1 日")
    else:
        c.drawRightString(page_w - 20*mm, y, "令和　年　月　日")
    y -= 10*mm

    label1 = "【甲】" if kind == 'souhou' else "【開示者】"
    label2 = "【乙】" if kind == 'souhou' else "【受領者】"

    c.setFont(GO, 10)
    if example:
        c.drawString(20*mm, y, f"{label1} 株式会社サンプル商事")
        y -= 5*mm
        c.drawString(20*mm, y, "    住所： 東京都千代田区サンプル町1-2-3")
        y -= 5*mm
        c.drawString(20*mm, y, "    代表者： 代表取締役 山田 太郎  印")
    else:
        c.drawString(20*mm, y, f"{label1} 住所： 　　　　　　　　　　　　　　")
        y -= 5*mm
        c.drawString(20*mm, y, "      会社名： 　　　　　　　　　　　　　")
        y -= 5*mm
        c.drawString(20*mm, y, "      代表者： 　　　　　　　　　　 印")
    y -= 10*mm

    if example:
        c.drawString(20*mm, y, f"{label2} 株式会社サンプル工業")
        y -= 5*mm
        c.drawString(20*mm, y, "    住所： 東京都港区サンプル町4-5-6")
        y -= 5*mm
        c.drawString(20*mm, y, "    代表者： 代表取締役 佐藤 次郎  印")
    else:
        c.drawString(20*mm, y, f"{label2} 住所： 　　　　　　　　　　　　　　")
        y -= 5*mm
        c.drawString(20*mm, y, "      会社名： 　　　　　　　　　　　　　")
        y -= 5*mm
        c.drawString(20*mm, y, "      代表者： 　　　　　　　　　　 印")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_nda_souhou(filename, example=False): pdf_nda(filename, 'souhou', example=example)
def pdf_nda_henmu(filename, example=False): pdf_nda(filename, 'henmu', example=example)


# ==========================================================
# Vol.2: T041 念書 / T054 日報 / T057 お礼状
# ==========================================================
def pdf_nensho(filename, example=False):
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 22)
    c.drawCentredString(page_w/2, page_h - 30*mm, "念　書")

    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和 7 年 5 月 1 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和　年　月　日")

    if example:
        c.drawString(20*mm, page_h - 65*mm, "山田　太郎　殿")
    else:
        c.drawString(20*mm, page_h - 65*mm, "○○　○○　殿")

    clauses = [
        ("第1条（債務の確認）",
         "私（以下「乙」という）は、甲（○○○○）に対し、下記の事項を約束いたします。" if not example else
         "私 佐藤次郎（以下「乙」という）は、貸主 山田太郎（以下「甲」という）に対し、下記の事項を約束いたします。"),
        ("第2条（履行の約束）",
         "・履行内容： （金額・期日・行為の内容を具体的に記載）\n・履行期限： 令和○年○月○日\n・履行方法： （振込・現金交付・実行行為等）" if not example else
         "・履行内容： 金 50万円の返還\n・履行期限： 令和 7 年 8 月 31 日\n・履行方法： 甲指定口座への銀行振込（振込手数料は乙負担）"),
        ("第3条（違反時の措置）",
         "上記の履行を怠った場合、甲は本念書を証拠として法的措置（民事訴訟・債権回収手続）を執ることができることを了承します。"),
        ("第4条（公正証書化への協力）",
         "甲が必要と認めた場合は、本念書を公正証書として作成することに協力します。"),
        ("第5条（連帯保証）",
         "（任意・連帯保証人を立てる場合に記載） 連帯保証人 ○○○○は、本念書に定める義務について、乙と連帯して責任を負います。"),
    ]

    y = page_h - 80*mm
    for title, body in clauses:
        c.setFont(GO, 10)
        c.drawString(20*mm, y, title)
        y -= 5*mm
        c.setFont(GO, 9)
        for line in body.split('\n'):
            wrapped, current = [], ""
            for ch in line:
                current += ch
                if len(current) >= 50:
                    wrapped.append(current); current = ""
            if current: wrapped.append(current)
            for w in wrapped:
                c.drawString(22*mm, y, w); y -= 4.5*mm
        y -= 2*mm
        if y < 50*mm:
            add_footer(c, page_w, example); c.showPage(); y = page_h - 25*mm

    y -= 8*mm
    c.setFont(GO, 10)
    if example:
        c.drawRightString(page_w - 20*mm, y, "住所： 東京都新宿区サンプル町2-3-4")
        y -= 5*mm
        c.drawRightString(page_w - 20*mm, y, "氏名： 佐藤 次郎  印")
    else:
        c.drawRightString(page_w - 20*mm, y, "住所： 　　　　　　　　　　　　　")
        y -= 5*mm
        c.drawRightString(page_w - 20*mm, y, "氏名： 　　　　　　　　　　 印")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_nippo(filename, example=False):
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 20)
    c.drawCentredString(page_w/2, page_h - 25*mm, "業 務 日 報")

    # ヘッダー情報
    c.setFont(GO, 10)
    y = page_h - 40*mm
    if example:
        rows = [
            ("日付：", "令和 7 年 5 月 5 日（月）", "氏名：", "山田 太郎"),
            ("所属：", "営業部 第一課", "天候：", "晴れ"),
            ("出勤：", "9:00", "退勤：", "18:30"),
        ]
    else:
        rows = [
            ("日付：", "令和　年　月　日（　）", "氏名：", "　　　　　　　"),
            ("所属：", "　　　　　　　　", "天候：", "　　"),
            ("出勤：", "　：　", "退勤：", "　：　"),
        ]
    for label1, val1, label2, val2 in rows:
        c.drawString(20*mm, y, label1 + val1)
        c.drawString(110*mm, y, label2 + val2)
        y -= 6*mm

    sections_blank = [
        ("■ 本日の業務内容（5W1Hで簡潔に）", ["1. ", "2. ", "3. "]),
        ("■ 達成事項・成果", ["・", "・"]),
        ("■ 課題・問題点", ["・", "・"]),
        ("■ 明日以降の予定", ["・", "・"]),
        ("■ 上司への確認事項", ["・"]),
    ]
    sections_example = [
        ("■ 本日の業務内容（5W1Hで簡潔に）", [
            "1. 9:00-11:00　A社訪問　契約条件の最終調整・見積書提示",
            "2. 13:00-15:00　社内会議　Q3売上計画の進捗共有",
            "3. 15:30-17:30　提案書作成　B社向け新規プロジェクト案",
        ]),
        ("■ 達成事項・成果", [
            "・A社契約条件で合意（年間 800万円・3年契約）",
            "・B社向け提案書 ドラフト完成（明日 上司レビュー予定）",
        ]),
        ("■ 課題・問題点", [
            "・A社の経理部門との支払条件交渉が未着手（次回 訪問時に対応）",
            "・社内会議が予定より30分超過（議題整理が不十分だった）",
        ]),
        ("■ 明日以降の予定", [
            "・5/6 09:00 提案書 上司レビュー → 修正",
            "・5/7 14:00 B社プレゼン本番",
        ]),
        ("■ 上司への確認事項", [
            "・A社契約書ドラフトの法務レビュー依頼の優先度",
        ]),
    ]
    sections = sections_example if example else sections_blank

    y -= 6*mm
    for title, lines in sections:
        c.setFont(GO, 11)
        c.drawString(20*mm, y, title)
        y -= 5*mm
        c.setFont(GO, 9)
        for line in lines:
            wrapped, current = [], ""
            for ch in line:
                current += ch
                if len(current) >= 55:
                    wrapped.append(current); current = ""
            if current: wrapped.append(current)
            for w in wrapped:
                c.drawString(22*mm, y, w); y -= 4.5*mm
        y -= 3*mm
        if y < 30*mm:
            add_footer(c, page_w, example); c.showPage(); y = page_h - 25*mm

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def _pdf_doc_with_clauses(filename, title_text, addressee, clauses, example=False, sign_label="氏名"):
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 22)
    c.drawCentredString(page_w/2, page_h - 30*mm, title_text)

    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和 7 年 5 月 5 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和　年　月　日")

    c.drawString(20*mm, page_h - 65*mm, addressee)

    y = page_h - 80*mm
    for title, body in clauses:
        c.setFont(GO, 10)
        c.drawString(20*mm, y, title); y -= 5*mm
        c.setFont(GO, 9)
        for line in body.split('\n'):
            wrapped, current = [], ""
            for ch in line:
                current += ch
                if len(current) >= 50:
                    wrapped.append(current); current = ""
            if current: wrapped.append(current)
            for w in wrapped:
                c.drawString(22*mm, y, w); y -= 4.5*mm
        y -= 2*mm
        if y < 50*mm:
            add_footer(c, page_w, example); c.showPage(); y = page_h - 25*mm

    y -= 8*mm
    c.setFont(GO, 10)
    if example:
        c.drawRightString(page_w - 20*mm, y, "住所： 東京都新宿区サンプル町2-3-4"); y -= 5*mm
        c.drawRightString(page_w - 20*mm, y, f"{sign_label}： 佐藤 次郎  印")
    else:
        c.drawRightString(page_w - 20*mm, y, "住所： 　　　　　　　　　　　　　"); y -= 5*mm
        c.drawRightString(page_w - 20*mm, y, f"{sign_label}： 　　　　　　　　　　 印")

    add_footer(c, page_w, example); c.showPage(); c.save()


def pdf_nensho_shiharai(filename, example=False):
    addressee = "山田　太郎　殿" if example else "○○　○○　殿"
    clauses = [
        ("第1条（債務の確認）",
         "私（以下「乙」という）は、貴殿（以下「甲」という）に対し、令和　年　月　日付けで発生した金 　万円の支払い債務を負っていることを確認します。" if not example else
         "私 佐藤次郎（以下「乙」という）は、貸主 山田太郎（以下「甲」という）に対し、令和 7 年 3 月 15 日付けで発生した金 50万円の支払い債務を負っていることを確認します。"),
        ("第2条（支払いの約束）",
         "上記債務について、下記の方法で確実に支払うことを約束いたします。\n・支払い方法： 一括 または 分割\n・支払い期日： 令和　年　月　日\n・支払い場所： 甲指定の銀行口座への振込（振込手数料は乙負担）" if not example else
         "上記債務について、下記の方法で確実に支払うことを約束いたします。\n・支払い方法： 分割（5回払い）\n・支払い期日： 令和 7 年 10 月 31 日（最終回）\n・支払い場所： 甲指定の銀行口座への振込（振込手数料は乙負担）"),
        ("第3条（分割払いの場合）",
         "分割払いとする場合、下記のスケジュールに従って支払います。\n・第1回： 令和　年　月　日 　万円\n・第2回： 令和　年　月　日 　万円\n・第3回： 令和　年　月　日 　万円" if not example else
         "・第1回： 令和 7 年 6 月 30 日 10万円\n・第2回： 令和 7 年 7 月 31 日 10万円\n・第3回： 令和 7 年 8 月 31 日 10万円\n・第4回： 令和 7 年 9 月 30 日 10万円\n・第5回： 令和 7 年 10 月 31 日 10万円"),
        ("第4条（遅延損害金）",
         "支払期日に遅延した場合、年率14.6％の遅延損害金を甲に支払うことに同意します。"),
        ("第5条（期限の利益喪失）",
         "1回でも支払いを怠った場合、残債務全額について期限の利益を失い、直ちに一括して支払うこととします。"),
        ("第6条（公正証書化への協力）",
         "甲が必要と認めた場合は、本念書を公正証書として作成することに協力します。"),
    ]
    _pdf_doc_with_clauses(filename, "念　書（支払い）", addressee, clauses, example=example, sign_label="氏名")


def pdf_nensho_kinsen(filename, example=False):
    addressee = "山田　太郎　殿" if example else "○○　○○　殿"
    clauses = [
        ("第1条（債務の承認）",
         "私（以下「乙」という）は、貴殿（以下「甲」という）に対し、下記金銭債務が存在することを承認いたします。\n・原契約日： 令和　年　月　日（金銭消費貸借）\n・原契約金額： 金 　万円\n・現在の残債務： 金 　万円" if not example else
         "私 佐藤次郎（以下「乙」という）は、貸主 山田太郎（以下「甲」という）に対し、下記金銭債務が存在することを承認いたします。\n・原契約日： 令和 4 年 6 月 1 日（金銭消費貸借）\n・原契約金額： 金 100万円\n・現在の残債務： 金 50万円"),
        ("第2条（消滅時効の援用放棄）",
         "本債務について、民法上の消滅時効を援用しないことを誓約します。本書面による債務の承認をもって、民法第152条第1項に基づき時効の更新が生じることに同意します。"),
        ("第3条（返済の約束）",
         "上記残債務について、令和　年　月　日までに、甲指定の銀行口座へ全額一括にて返済します。または、別紙「返済計画書」に従い分割返済します。" if not example else
         "上記残債務について、令和 7 年 12 月 31 日までに、甲指定の銀行口座へ全額一括にて返済します。"),
        ("第4条（連帯保証）",
         "（任意）連帯保証人 ○○　○○ は、本念書記載の債務について乙と連帯して責任を負います。"),
        ("第5条（違反時の措置）",
         "返済期日までに支払いがない場合、甲は本念書を証拠として、訴訟・強制執行を含む法的措置を執ることに乙は異議なく同意します。"),
    ]
    _pdf_doc_with_clauses(filename, "念　書（金銭・債務承認）", addressee, clauses, example=example, sign_label="氏名")


def _pdf_ininjo(filename, title, purpose_text, witness, example=False):
    """委任状の共通PDF生成"""
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 22)
    c.drawCentredString(page_w/2, page_h - 30*mm, title)

    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和 7 年 5 月 5 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和　年　月　日")

    y = page_h - 65*mm

    # 委任者
    c.setFont(GO, 11)
    c.drawString(20*mm, y, "【委任者】"); y -= 6*mm
    c.setFont(GO, 10)
    if example:
        c.drawString(22*mm, y, "住所： 東京都新宿区サンプル町1-2-3"); y -= 5*mm
        c.drawString(22*mm, y, "氏名： 山田 太郎  印"); y -= 5*mm
    else:
        c.drawString(22*mm, y, "住所： 　　　　　　　　　　　　　"); y -= 5*mm
        c.drawString(22*mm, y, "氏名： 　　　　　　　　　　 印"); y -= 5*mm
    y -= 3*mm

    # 受任者
    c.setFont(GO, 11)
    c.drawString(20*mm, y, "【受任者】"); y -= 6*mm
    c.setFont(GO, 10)
    if example:
        c.drawString(22*mm, y, "住所： 東京都渋谷区サンプル町4-5-6"); y -= 5*mm
        c.drawString(22*mm, y, "氏名： 山田 花子（妻）"); y -= 5*mm
    else:
        c.drawString(22*mm, y, "住所： 　　　　　　　　　　　　　"); y -= 5*mm
        c.drawString(22*mm, y, "氏名： 　　　　　　　　　　 "); y -= 5*mm
    y -= 6*mm

    # 委任の宣言
    c.setFont(GO, 10)
    c.drawString(20*mm, y, "私は、上記の者を代理人と定め、下記の事項に関する一切の権限を委任します。")
    y -= 8*mm

    # 委任事項
    c.setFont(GO, 11)
    c.drawString(20*mm, y, "【委任事項】"); y -= 6*mm
    c.setFont(GO, 9)
    for line in purpose_text.split('\n'):
        wrapped, current = [], ""
        for ch in line:
            current += ch
            if len(current) >= 50:
                wrapped.append(current); current = ""
        if current: wrapped.append(current)
        for w in wrapped:
            c.drawString(22*mm, y, w); y -= 4.5*mm
        if not line: y -= 2*mm

    y -= 5*mm
    c.setFont(GO, 9)
    for line in witness.split('\n'):
        wrapped, current = [], ""
        for ch in line:
            current += ch
            if len(current) >= 55:
                wrapped.append(current); current = ""
        if current: wrapped.append(current)
        for w in wrapped:
            c.drawString(20*mm, y, w); y -= 4.5*mm

    add_footer(c, page_w, example); c.showPage(); c.save()


def pdf_ininjo_sokai(filename, example=False):
    purpose = (
        "1. 議決権の行使に関する一切の権限\n"
        "2. 動議の提出および賛否表明\n"
        "3. その他、本総会の議事運営に関連する一切の事項\n\n"
        "■ 議決権行使指示\n"
        "・第1号議案： 賛成 / 反対 / 受任者一任\n"
        "・第2号議案： 賛成 / 反対 / 受任者一任\n"
        "・第3号議案： 賛成 / 反対 / 受任者一任"
    ) if not example else (
        "1. 議決権の行使に関する一切の権限\n"
        "2. 動議の提出および賛否表明\n"
        "3. その他、本総会の議事運営に関連する一切の事項\n\n"
        "■ 議決権行使指示\n"
        "・第1号議案（理事改選）： 賛成\n"
        "・第2号議案（管理費改定）： 反対\n"
        "・第3号議案（修繕計画）： 受任者一任"
    )
    witness = "本委任状は、令和 7 年 6 月 15 日開催の管理組合総会のためにのみ有効とし、他の用途には使用しないものとします。" if example else "本委任状は、令和　年　月　日開催の○○総会のためにのみ有効とし、他の用途には使用しないものとします。"
    _pdf_ininjo(filename, "委 任 状（総会用）", purpose, witness, example=example)


def pdf_ininjo_ginko(filename, example=False):
    purpose = (
        "下記の手続きおよびこれに付随する一切の事項。\n"
        "・口座開設 / 口座解約 / 残高証明書の発行\n"
        "・通帳・キャッシュカードの再発行\n"
        "・名義変更 / 住所変更\n"
        "・相続手続き（被相続人： 　　　　／死亡日：　　年　月　日）\n\n"
        "■ 対象口座\n"
        "・銀行名： 　　　　銀行 　　　　支店\n"
        "・口座種別： 普通／当座／定期\n"
        "・口座番号： 　　　　　　　　"
    ) if not example else (
        "下記の手続きおよびこれに付随する一切の事項。\n"
        "・残高証明書の発行（5/15基準日）\n"
        "・相続手続き（被相続人： 山田 太郎／死亡日： 令和 7 年 4 月 20 日）\n\n"
        "■ 対象口座\n"
        "・銀行名： サンプル銀行 新宿支店\n"
        "・口座種別： 普通\n"
        "・口座番号： 1234567"
    )
    witness = "本委任状の使用にあたっては、委任者の印鑑証明書（発行日から3ヶ月以内）および本人確認書類のコピーを添付するものとします。"
    _pdf_ininjo(filename, "委 任 状（銀行手続き用）", purpose, witness, example=example)


def pdf_ininjo_general(filename, example=False):
    purpose = (
        "下記の手続きおよびこれに付随する一切の事項。\n"
        "・（具体的な手続き内容を記載）\n"
        "・（提出書類の受領・押印を含む）\n"
        "・（必要に応じて費用の支払い）\n\n"
        "■ 委任の範囲\n"
        "本委任は、上記事項の完了をもって終了します。"
    ) if not example else (
        "下記の手続きおよびこれに付随する一切の事項。\n"
        "・住民票の写しおよび戸籍謄本の請求と受領\n"
        "・関連手数料の支払い\n\n"
        "■ 委任の範囲\n"
        "本委任は、上記事項の完了をもって終了します。"
    )
    witness = "本委任状は、令和 7 年 6 月 30 日までの間有効とし、必要に応じて本人確認書類のコピーを添付します。" if example else "本委任状は、令和　年　月　日までの間有効とし、必要に応じて本人確認書類のコピーを添付します。"
    _pdf_ininjo(filename, "委 任 状", purpose, witness, example=example)


def pdf_simple(filename, title, body_note, example=False):
    """Vol.3 法律書類用シンプルPDF（Word版が主・PDFは案内のみ）"""
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 24)
    c.drawCentredString(page_w/2, page_h - 30*mm, title)

    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和 7 年 5 月 6 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "令和　年　月　日")

    # 本文（簡易・印刷可能なテンプレ風）
    c.setFont(GO, 11)
    body_lines = [
        body_note,
        "",
        "【利用方法】",
        "1. Word版テンプレートをダウンロードして編集",
        "2. 必要事項を入力（記入例PDFを参照）",
        "3. 印刷・押印して関係者に交付",
        "",
        "【注意】",
        "・本テンプレートは一般的な書式の参考として提供しています。",
        "・個別事情に応じて、弁護士・行政書士等の専門家にご相談ください。",
        "・本書面は法的紛争に発展する可能性があるため、慎重に作成してください。",
    ]
    y = page_h - 70*mm
    for line in body_lines:
        c.drawString(25*mm, y, line); y -= 6.5*mm

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


def pdf_oreijo_english(filename, example=False):
    """お礼状 英語版"""
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 11)
    c.drawRightString(page_w - 20*mm, page_h - 25*mm, "May 5, 2026")
    c.drawString(20*mm, page_h - 38*mm, "Mr./Ms. ___________")
    c.drawString(20*mm, page_h - 44*mm, "ABC Corporation")
    c.drawString(20*mm, page_h - 50*mm, "Address: ___________________________")

    c.setFont(GO, 16)
    c.drawCentredString(page_w/2, page_h - 70*mm, "Letter of Appreciation")

    c.setFont(GO, 11)
    body_lines = [
        "Dear Mr./Ms. ___________,",
        "",
        "I am writing to express my sincere gratitude for your support",
        "of (project / meeting / occasion).",
        "Your professional advice and prompt cooperation have been",
        "invaluable to the successful completion of (specific work).",
        "",
        "I look forward to continuing our productive working",
        "relationship in the future.",
        "",
        "Please do not hesitate to contact me if you have any",
        "questions or require further information.",
        "",
        "Sincerely yours,",
        "",
        "[Your Name]",
        "[Your Title], [Your Company]",
        "Email: ____________  /  Tel: ____________",
    ]
    y = page_h - 85*mm
    for line in body_lines:
        c.drawString(25*mm, y, line); y -= 6*mm

    add_footer(c, page_w, example); c.showPage(); c.save()


def pdf_oreijo_ochugen(filename, example=False):
    """お礼状 お中元・お歳暮"""
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "令和 7 年 7 月 10 日")
        c.drawString(20*mm, page_h - 38*mm, "株式会社サンプル商事")
        c.drawString(20*mm, page_h - 44*mm, "営業部　佐藤 次郎　様")
        c.drawRightString(page_w - 20*mm, page_h - 56*mm, "株式会社サンプル工業")
        c.drawRightString(page_w - 20*mm, page_h - 62*mm, "営業部　山田 太郎")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "令和　年　月　日")
        c.drawString(20*mm, page_h - 38*mm, "○○株式会社")
        c.drawString(20*mm, page_h - 44*mm, "○○部　○○　○○　様")
        c.drawRightString(page_w - 20*mm, page_h - 56*mm, "○○株式会社")
        c.drawRightString(page_w - 20*mm, page_h - 62*mm, "○○部　○○　○○")

    c.setFont(GO, 16)
    c.drawCentredString(page_w/2, page_h - 80*mm, "お中元（お歳暮）御礼状")

    c.setFont(GO, 11)
    body_lines = [
        "拝啓　盛夏（または歳末）の候、貴社ますますご清栄のこととお慶び申し上げます。",
        "平素は格別のご高配を賜り、厚く御礼申し上げます。",
        "",
        "さて、このたびはご丁寧にお中元（お歳暮）の品をお送りいただき、",
        "誠にありがとうございました。",
        "結構なお品物をお贈りいただき、社員一同心より感謝申し上げます。",
        "",
        "本来であれば直接お伺いしてお礼を申し上げるべきところ、",
        "書中をもちまして失礼ながらご挨拶とさせていただきます。",
        "",
        "今後とも変わらぬお引き立てを賜りますようお願い申し上げます。",
        "末筆ながら、貴社のますますのご発展と皆様のご健勝を",
        "心よりお祈り申し上げます。",
    ]
    y = page_h - 95*mm
    for line in body_lines:
        c.drawString(25*mm, y, line); y -= 6*mm
    c.drawRightString(page_w - 25*mm, y - 4*mm, "敬具")

    add_footer(c, page_w, example); c.showPage(); c.save()


def pdf_shanai_tsutatsu(filename, example=False):
    """社内通達"""
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 10)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "通達番号： 2026-031")
        c.drawRightString(page_w - 20*mm, page_h - 31*mm, "発行日： 令和 7 年 5 月 5 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "通達番号： 　　-　　")
        c.drawRightString(page_w - 20*mm, page_h - 31*mm, "発行日： 令和　年　月　日")

    c.setFont(GO, 20)
    c.drawCentredString(page_w/2, page_h - 50*mm, "社 内 通 達")

    c.setFont(GO, 11)
    if example:
        c.drawString(20*mm, page_h - 70*mm, "【宛先】 営業部 全員")
        c.drawRightString(page_w - 20*mm, page_h - 70*mm, "発信者： 人事部 山田 花子")
    else:
        c.drawString(20*mm, page_h - 70*mm, "各位")
        c.drawRightString(page_w - 20*mm, page_h - 70*mm, "発信者： ○○部　○○　○○")

    sections = [
        ("【件名】", "（例：人事異動／システム障害対応／福利厚生制度改定）" if not example else "夏期休業期間のお知らせ"),
        ("【概要】", "本件の要点を3行以内で記載" if not example else "2026年8月10日(月)〜8月14日(金)を夏期休業とします。前後の業務調整をお願いします。"),
        ("【適用日】", "令和　年　月　日 より" if not example else "令和 7 年 8 月 10 日 より"),
        ("【対象者】", "（部署・役職・全社員）" if not example else "全社員（営業部・管理部・開発部 全員）"),
        ("【詳細】",
         "1. 変更点・実施事項を箇条書きで具体的に\n2. 関連するルール・規程の参照先\n3. 必要な手続きや対応期日" if not example else
         "1. 休業期間：8月10日(月)〜8月14日(金)\n2. 取引先への事前連絡（8月7日までに完了）\n3. 緊急連絡先：代表 03-1234-5678（休業中も応答可）"),
        ("【お問い合わせ】",
         "○○部　○○ ○○\n内線：　　　／メール：　　　@　　　" if not example else
         "人事部 山田 花子\n内線：120 ／メール：yamada@example.co.jp"),
    ]

    y = page_h - 90*mm
    for title, body in sections:
        c.setFont(GO, 10)
        c.drawString(20*mm, y, title); y -= 5*mm
        c.setFont(GO, 9)
        for line in body.split('\n'):
            wrapped, current = [], ""
            for ch in line:
                current += ch
                if len(current) >= 50:
                    wrapped.append(current); current = ""
            if current: wrapped.append(current)
            for w in wrapped:
                c.drawString(22*mm, y, w); y -= 4.5*mm
        y -= 3*mm
        if y < 30*mm:
            add_footer(c, page_w, example); c.showPage(); y = page_h - 25*mm

    add_footer(c, page_w, example); c.showPage(); c.save()


def pdf_ryoshusho_soejou(filename, example=False):
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "令和 7 年 5 月 5 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "令和　年　月　日")

    if example:
        c.drawString(20*mm, page_h - 38*mm, "株式会社サンプル商事")
        c.drawString(20*mm, page_h - 44*mm, "経理部　佐藤 次郎　様")
    else:
        c.drawString(20*mm, page_h - 38*mm, "○○株式会社")
        c.drawString(20*mm, page_h - 44*mm, "○○部　○○　○○　様")

    if example:
        c.drawRightString(page_w - 20*mm, page_h - 56*mm, "株式会社サンプル工業")
        c.drawRightString(page_w - 20*mm, page_h - 62*mm, "営業部　山田 太郎")
        c.drawRightString(page_w - 20*mm, page_h - 68*mm, "TEL: 03-1234-5678")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 56*mm, "○○株式会社")
        c.drawRightString(page_w - 20*mm, page_h - 62*mm, "○○部　○○　○○")
        c.drawRightString(page_w - 20*mm, page_h - 68*mm, "TEL: 　　-　　-　　")

    c.setFont(GO, 16)
    c.drawCentredString(page_w/2, page_h - 85*mm, "領収書送付のご案内")

    c.setFont(GO, 11)
    body_lines = [
        "拝啓　時下ますますご清栄のこととお慶び申し上げます。",
        "平素は格別のご高配を賜り、厚く御礼申し上げます。",
        "",
        "さて、ご請求金額につきまして、お振込みを確認させていただきました。",
        "つきましては、下記のとおり領収書を同封させていただきましたので、",
        "ご査収のほどよろしくお願い申し上げます。",
        "",
        "今後とも変わらぬお引き立てを賜りますようお願い申し上げます。",
    ]
    y = page_h - 100*mm
    for line in body_lines:
        c.drawString(25*mm, y, line); y -= 6*mm

    c.drawRightString(page_w - 25*mm, y - 4*mm, "敬具")

    c.setFont(GO, 12)
    c.drawCentredString(page_w/2, y - 18*mm, "記")

    c.setFont(GO, 11)
    if example:
        items = [
            "・領収書（No.0001 ／ 金額：￥50,000-）　　1通",
            "・支払明細書　　　　　　　　　　　　　　　1通",
        ]
    else:
        items = [
            "・領収書（No.　　　　／ 金額：￥　　　-）　　1通",
            "・その他添付書類（必要に応じて記載）　　　　1通",
        ]
    y = y - 28*mm
    for it in items:
        c.drawString(30*mm, y, it); y -= 6*mm

    c.drawRightString(page_w - 25*mm, y - 4*mm, "以上")

    add_footer(c, page_w, example); c.showPage(); c.save()


def pdf_ryoshusho(filename, example=False):
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    # タイトル
    c.setFont(GO, 24)
    c.drawCentredString(page_w/2, page_h - 30*mm, "領 収 書")

    # No. 発行日
    c.setFont(GO, 10)
    if example:
        c.drawString(20*mm, page_h - 50*mm, "No. 0001")
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "発行日： 令和 7 年 5 月 5 日")
    else:
        c.drawString(20*mm, page_h - 50*mm, "No.　　　　　")
        c.drawRightString(page_w - 20*mm, page_h - 50*mm, "発行日： 令和　年　月　日")

    # 宛名
    c.setFont(GO, 14)
    if example:
        c.drawString(20*mm, page_h - 65*mm, "山田 太郎 様")
    else:
        c.drawString(20*mm, page_h - 65*mm, "○○ 様")

    # 金額
    c.setFont(GO, 22)
    if example:
        c.drawCentredString(page_w/2, page_h - 90*mm, "金額：￥ 50,000 -")
    else:
        c.drawCentredString(page_w/2, page_h - 90*mm, "金額：￥　　　　　　　-")

    # 但し書き
    c.setFont(GO, 11)
    if example:
        c.drawString(20*mm, page_h - 110*mm, "但し　 業務委託料 5月分 として")
    else:
        c.drawString(20*mm, page_h - 110*mm, "但し　（商品/サービス内容を記載）として")
    c.drawString(20*mm, page_h - 118*mm, "上記正に領収いたしました。")

    # インボイス情報
    c.setFont(GO, 10)
    if example:
        c.drawString(20*mm, page_h - 135*mm, "登録番号： T1234567890123（適格請求書発行事業者）")
        c.drawString(20*mm, page_h - 143*mm, "内訳：10%対象 ￥45,455（消費税 ￥4,545）／ 8%対象 ￥0")
    else:
        c.drawString(20*mm, page_h - 135*mm, "登録番号： T1234567890123（適格請求書発行事業者）")
        c.drawString(20*mm, page_h - 143*mm, "内訳：10%対象 ￥　　／ 8%対象 ￥　　")

    # 発行者
    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 165*mm, "発行者： 株式会社サンプル商事")
        c.drawRightString(page_w - 20*mm, page_h - 173*mm, "所在地： 東京都新宿区サンプル町1-2-3")
        c.drawRightString(page_w - 20*mm, page_h - 181*mm, "代表者： 代表取締役 山田 太郎  印")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 165*mm, "発行者： ○○商店")
        c.drawRightString(page_w - 20*mm, page_h - 173*mm, "所在地： 東京都○○区○○ 1-2-3")
        c.drawRightString(page_w - 20*mm, page_h - 181*mm, "代表者： ○○ ○○  印")

    add_footer(c, page_w, example); c.showPage(); c.save()


def pdf_nensho_kojin(filename, example=False):
    addressee = "山田　太郎　殿" if example else "○○　○○　殿"
    clauses = [
        ("第1条（誓約事項）",
         "私（以下「乙」という）は、貴殿（以下「甲」という）に対し、下記の事項を約束いたします。\n（1）禁止行為：（例：浮気・金銭の無断引出し・暴言暴力 等を具体的に）\n（2）履行事項：（例：金銭の返済・養育費・慰謝料 等を具体的に）" if not example else
         "私 佐藤花子（以下「乙」という）は、夫 佐藤次郎（以下「甲」という）に対し、下記の事項を約束いたします。\n（1）禁止行為： 第三者との男女関係を一切持たない\n（2）履行事項： 過去の関係に対する慰謝料 100万円の支払い"),
        ("第2条（履行内容・期限）",
         "・履行内容： 金 　万円の支払い（または行為の停止）\n・履行期限： 令和　年　月　日\n・履行方法： 甲指定の銀行口座への振込（または直接交付）" if not example else
         "・履行内容： 金 100万円の支払い\n・履行期限： 令和 7 年 12 月 31 日\n・履行方法： 甲指定の銀行口座への振込（毎月 10万円・10回分割）"),
        ("第3条（違反時の措置）",
         "上記の禁止事項を破り、または履行を怠った場合、下記の措置を受けることに同意します。\n（1）違約金 金 　万円を直ちに支払うこと\n（2）甲が本念書を証拠として、損害賠償請求・離婚調停・刑事告訴等の法的措置を執ること"),
        ("第4条（家族関係への配慮）",
         "本件が家族関係に与える影響を考慮し、両者は誠実に協議のうえ、家庭の平穏維持に努めることを確認します。"),
        ("第5条（公正証書化への協力）",
         "甲が必要と認めた場合は、本念書を公正証書として作成することに協力します。"),
        ("第6条（守秘）",
         "本念書の存在および内容を、両者は第三者に開示しないものとします（ただし、専門家への相談・法的手続きを除く）。"),
    ]
    _pdf_doc_with_clauses(filename, "念　書（個人間）", addressee, clauses, example=example, sign_label="氏名")


def pdf_tenmatsusho(filename, example=False):
    addressee = "○○株式会社　代表取締役　○○　○○　殿" if not example else "株式会社サンプル商事　代表取締役　山田 太郎　殿"
    clauses = [
        ("■ 件名",
         "（例：商品納品ミスに関する顛末書、業務上トラブル発生に関する顛末書 等）" if not example else
         "B 社向け納品 5月3日分 における数量違算に関する顛末書"),
        ("■ 発生日時",
         "令和　年　月　日　午前／午後　時　分頃" if not example else "令和 7 年 5 月 3 日　午後 14 時 30 分頃"),
        ("■ 発生場所",
         "（営業先・社内・倉庫・現場 等を具体的に）" if not example else "弊社 横浜倉庫 出荷場"),
        ("■ 関係者",
         "（自社：氏名・役職／取引先：会社名・氏名）" if not example else "自社： 営業部 佐藤 次郎、出荷課 田中 三郎／取引先： B社 購買部 鈴木 花子 様"),
        ("■ 経緯（時系列）",
         "1. 発生前の状況：\n2. 発生時の状況：\n3. 発生後の対応：\n4. 現時点の状況：" if not example else
         "1. 5/3 13:00 出荷指示書を受領（発注数量 1,000個）\n2. 5/3 14:30 ピッキング完了 → 検品未実施のまま出荷（実数量 800個）\n3. 5/4 10:00 B社より不足の指摘 → 即時 200個追加出荷\n4. 5/5 09:00 B社購買部に謝罪訪問・受領確認"),
        ("■ 原因（直接原因・根本原因）",
         "・直接原因： （現象として何が起きたか）\n・根本原因： （なぜ発生したか・5なぜ分析）" if not example else
         "・直接原因： 検品工程をスキップしたため、ピッキング時の数量誤り（180個欠品）が発覚しなかった\n・根本原因： 5月連休前で人手不足、検品工程の責任者が不在、ダブルチェック体制が機能していなかった"),
        ("■ 影響範囲",
         "・お客様への影響：\n・社内への影響：\n・金銭的損失（試算）：" if not example else
         "・お客様への影響： B社製造ラインで2時間の生産遅延、信頼関係の毀損リスク\n・社内への影響： 緊急対応で営業3名・出荷2名の残業が発生\n・金銭的損失（試算）： 緊急配送費 4万円、人件費 6万円、計 10万円"),
        ("■ 再発防止策",
         "1. \n2. \n3. " if not example else
         "1. 検品工程の必須化（出荷前の数量・品質チェック表を導入し、責任者の押印必須）\n2. ダブルチェック体制（ピッカー＋検品担当者の2名制を5月中に運用開始）\n3. 連休前後の応援体制（事前に応援要員を配置・週次の出荷予定数の見える化）"),
        ("■ 結語",
         "今後はこのような事態を繰り返さぬよう、再発防止策を遵守し、業務にあたります。この度は誠に申し訳ございませんでした。"),
    ]
    _pdf_doc_with_clauses(filename, "顛 末 書", addressee, clauses, example=example, sign_label="氏名")


def pdf_oreijo(filename, example=False):
    out = OUT_DIR / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    page_w, page_h = A4

    c.setFont(GO, 11)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "令和 7 年 5 月 5 日")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 25*mm, "令和　年　月　日")

    if example:
        c.drawString(20*mm, page_h - 38*mm, "株式会社サンプル商事")
        c.drawString(20*mm, page_h - 44*mm, "営業部　佐藤 次郎　様")
    else:
        c.drawString(20*mm, page_h - 38*mm, "○○株式会社")
        c.drawString(20*mm, page_h - 44*mm, "○○部　○○　○○　様")

    if example:
        c.drawRightString(page_w - 20*mm, page_h - 56*mm, "株式会社サンプル工業")
        c.drawRightString(page_w - 20*mm, page_h - 62*mm, "営業部　山田 太郎")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 56*mm, "○○株式会社")
        c.drawRightString(page_w - 20*mm, page_h - 62*mm, "○○部　○○　○○")

    c.setFont(GO, 18)
    c.drawCentredString(page_w/2, page_h - 80*mm, "お礼状")

    c.setFont(GO, 11)
    if example:
        body = [
            "拝啓　時下ますますご清栄のこととお慶び申し上げます。",
            "平素は格別のご高配を賜り、厚く御礼申し上げます。",
            "",
            "さて、このたびは弊社 新製品 開発プロジェクトに際し、",
            "貴社のご協力により、当初予定の 1ヶ月前に納品を完了することができました。",
            "誠にありがとうございました。",
            "",
            "つきましては、書面にて略儀ながら御礼申し上げます。",
            "今後とも変わらぬお引き立てを賜りますようお願い申し上げます。",
            "",
            "末筆ながら、貴社のますますのご発展と皆様のご健勝を",
            "心よりお祈り申し上げます。",
        ]
    else:
        body = [
            "拝啓　時下ますますご清栄のこととお慶び申し上げます。",
            "平素は格別のご高配を賜り、厚く御礼申し上げます。",
            "",
            "さて、このたびは（用件・受領内容を具体的に）にあたり、",
            "格別のご配慮を賜り誠にありがとうございました。",
            "おかげさまをもちまして滞りなく完了することができ、",
            "心より感謝申し上げます。",
            "",
            "つきましては、書面にて略儀ながら御礼申し上げます。",
            "今後とも変わらぬお引き立てを賜りますようお願い申し上げます。",
            "",
            "末筆ながら、貴社のますますのご発展と皆様のご健勝を",
            "心よりお祈り申し上げます。",
        ]
    y = page_h - 95*mm
    for line in body:
        c.drawString(25*mm, y, line)
        y -= 6*mm

    c.drawRightString(page_w - 25*mm, y - 5*mm, "敬具")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


# ==========================================================
# T028: 見積依頼書（RFQ）PDF
# ==========================================================
def pdf_mitsumori_iraisho(filename, example=False):
    page_w, page_h = A4
    c = canvas.Canvas(str(OUT_DIR / filename), pagesize=A4)

    c.setFont(GO, 22)
    c.drawCentredString(page_w/2, page_h - 25*mm, "見積依頼書")

    c.setFont(GO, 10)
    if example:
        c.drawRightString(page_w - 20*mm, page_h - 42*mm, "依頼日： 令和 7 年 5 月 12 日")
        c.drawString(20*mm, page_h - 50*mm, "株式会社○○製作所 御中")
    else:
        c.drawRightString(page_w - 20*mm, page_h - 42*mm, "依頼日： 令和　年　月　日")
        c.drawString(20*mm, page_h - 50*mm, "　　　　　御中")

    c.setFont(GO, 9)
    c.drawString(20*mm, page_h - 62*mm, "拝啓  時下ますますご清栄のこととお慶び申し上げます。")
    c.drawString(20*mm, page_h - 67*mm, "下記の通り見積をご依頼申し上げます。よろしくお願い申し上げます。")

    if example:
        items = [
            ("件名", "新規Webサイト制作"),
            ("依頼内容", "コーポレートサイトのリニューアル"),
            ("仕様・条件", "レスポンシブ対応・WordPress 構築・ページ数 約20"),
            ("数量", "1 式"),
            ("納期", "令和 7 年 8 月 31 日"),
            ("納入場所", "弊社サーバー（後日アクセス情報を提供）"),
            ("見積回答期限", "令和 7 年 5 月 30 日"),
            ("支払条件", "納品後 30 日以内・銀行振込"),
            ("その他", "プロトタイプ提示後に正式契約の流れ"),
        ]
    else:
        items = [
            ("件名", ""),
            ("依頼内容", ""),
            ("仕様・条件", ""),
            ("数量", ""),
            ("納期", "令和　年　月　日"),
            ("納入場所", ""),
            ("見積回答期限", "令和　年　月　日"),
            ("支払条件", ""),
            ("その他", ""),
        ]

    table_top = page_h - 80*mm
    row_h = 9*mm
    label_w = 35*mm
    value_w = 135*mm
    for i, (k, v) in enumerate(items):
        y = table_top - (i+1)*row_h
        _draw_table_row(c, 20*mm, y, k, v, label_w, value_w, row_h, GO, 9)

    info_y = table_top - len(items)*row_h - 12*mm
    c.setFont(GO, 9)
    if example:
        c.drawRightString(page_w - 20*mm, info_y,         "【依頼者】")
        c.drawRightString(page_w - 20*mm, info_y - 5*mm,  "会社名： 株式会社サンプル商事")
        c.drawRightString(page_w - 20*mm, info_y - 10*mm, "所属： 営業部第一課")
        c.drawRightString(page_w - 20*mm, info_y - 15*mm, "担当者： 山田 太郎")
        c.drawRightString(page_w - 20*mm, info_y - 20*mm, "電話： 03-1234-5678")
        c.drawRightString(page_w - 20*mm, info_y - 25*mm, "メール： yamada@sample.co.jp")
    else:
        c.drawRightString(page_w - 20*mm, info_y,         "【依頼者】")
        c.drawRightString(page_w - 20*mm, info_y - 5*mm,  "会社名：")
        c.drawRightString(page_w - 20*mm, info_y - 10*mm, "所属：")
        c.drawRightString(page_w - 20*mm, info_y - 15*mm, "担当者：")
        c.drawRightString(page_w - 20*mm, info_y - 20*mm, "電話：")
        c.drawRightString(page_w - 20*mm, info_y - 25*mm, "メール：")

    add_footer(c, page_w, example)
    c.showPage()
    c.save()


if __name__ == "__main__":
    print("Generating PDFs...")

    # T001: 退職届 (空欄 + 記入例)
    pdf_taishokutodoke_a4_tategaki("taishokutodoke_a4_tategaki.pdf");          print("  [ok] taishokutodoke_a4_tategaki.pdf")
    pdf_taishokutodoke_a4_yokogaki("taishokutodoke_a4_yokogaki.pdf");          print("  [ok] taishokutodoke_a4_yokogaki.pdf")
    pdf_taishokutodoke_b5_tategaki("taishokutodoke_b5_tategaki.pdf");          print("  [ok] taishokutodoke_b5_tategaki.pdf")
    pdf_taishokutodoke_a4_yokogaki("taishokutodoke_a4_yokogaki_example.pdf", example=True)
    print("  [ok] taishokutodoke_a4_yokogaki_example.pdf")

    # T011: 労働条件通知書 (空欄 + 記入例)
    pdf_roudoujouken_seishain("roudoujouken-tsuuchisho_seishain.pdf");         print("  [ok] roudoujouken-tsuuchisho_seishain.pdf")
    pdf_roudoujouken_keiyaku("roudoujouken-tsuuchisho_keiyaku.pdf");           print("  [ok] roudoujouken-tsuuchisho_keiyaku.pdf")
    pdf_roudoujouken_arbeit("roudoujouken-tsuuchisho_arbeit.pdf");             print("  [ok] roudoujouken-tsuuchisho_arbeit.pdf")
    pdf_roudoujouken_seishain("roudoujouken-tsuuchisho_seishain_example.pdf", example=True)
    print("  [ok] roudoujouken-tsuuchisho_seishain_example.pdf")

    # T016: 業務委託契約書 (空欄 + 記入例)
    pdf_gyoumu_itaku("gyoumu-itaku_general.pdf", "一般委託");                  print("  [ok] gyoumu-itaku_general.pdf")
    pdf_gyoumu_itaku("gyoumu-itaku_junin.pdf", "準委任");                      print("  [ok] gyoumu-itaku_junin.pdf")
    pdf_gyoumu_itaku("gyoumu-itaku_ukeoi.pdf", "請負");                        print("  [ok] gyoumu-itaku_ukeoi.pdf")
    pdf_gyoumu_itaku("gyoumu-itaku_general_example.pdf", "一般委託", example=True)
    print("  [ok] gyoumu-itaku_general_example.pdf")

    # T002: 退職届 無料特化（T001 派生）
    pdf_taishokutodoke_muryou_a4("taishokutodoke-muryou_a4.pdf");               print("  [ok] taishokutodoke-muryou_a4.pdf")
    pdf_taishokutodoke_muryou_a4_tategaki("taishokutodoke-muryou_a4_tategaki.pdf"); print("  [ok] taishokutodoke-muryou_a4_tategaki.pdf")
    pdf_taishokutodoke_muryou_a4("taishokutodoke-muryou_example.pdf", example=True); print("  [ok] taishokutodoke-muryou_example.pdf")

    # T007/T009: 始末書（汎用 / 遅刻 / 記入例 各種）
    pdf_shimatsusho_general("shimatsusho_general.pdf");                         print("  [ok] shimatsusho_general.pdf")
    pdf_shimatsusho_chikoku("shimatsusho_chikoku.pdf");                         print("  [ok] shimatsusho_chikoku.pdf")
    pdf_shimatsusho_general("shimatsusho_general_example.pdf", example=True);   print("  [ok] shimatsusho_general_example.pdf")
    pdf_shimatsusho_chikoku("shimatsusho_chikoku_example.pdf", example=True);   print("  [ok] shimatsusho_chikoku_example.pdf")

    # T012: 雇用契約書（正社員 / 契約 / アルバイト / 記入例）
    pdf_koyou_keiyakusho_seishain("koyou-keiyakusho_seishain.pdf");             print("  [ok] koyou-keiyakusho_seishain.pdf")
    pdf_koyou_keiyakusho_keiyaku("koyou-keiyakusho_keiyaku.pdf");               print("  [ok] koyou-keiyakusho_keiyaku.pdf")
    pdf_koyou_keiyakusho_arbeit("koyou-keiyakusho_arbeit.pdf");                 print("  [ok] koyou-keiyakusho_arbeit.pdf")
    pdf_koyou_keiyakusho_seishain("koyou-keiyakusho_seishain_example.pdf", example=True)
    print("  [ok] koyou-keiyakusho_seishain_example.pdf")

    # T023: 請求書 個人事業主
    pdf_seikyu_kojin("seikyu-kojin-jigyonushi.pdf");                            print("  [ok] seikyu-kojin-jigyonushi.pdf")
    pdf_seikyu_kojin("seikyu-kojin-jigyonushi_example.pdf", example=True);     print("  [ok] seikyu-kojin-jigyonushi_example.pdf")

    # T029: 見積書 登録不要
    pdf_mitsumori("mitsumori-tourokufuyou.pdf");                                print("  [ok] mitsumori-tourokufuyou.pdf")
    pdf_mitsumori("mitsumori-tourokufuyou_example.pdf", example=True);          print("  [ok] mitsumori-tourokufuyou_example.pdf")

    # T035: 議事録
    pdf_gijiroku_standard("gijiroku_standard.pdf");                             print("  [ok] gijiroku_standard.pdf")
    pdf_gijiroku_1on1("gijiroku_1on1.pdf");                                     print("  [ok] gijiroku_1on1.pdf")
    pdf_gijiroku_standard("gijiroku_standard_example.pdf", example=True);       print("  [ok] gijiroku_standard_example.pdf")

    # T020: 秘密保持誓約書
    pdf_himitsuhoji_nyusha("himitsuhoji-seiyakusho_nyusha.pdf");                print("  [ok] himitsuhoji-seiyakusho_nyusha.pdf")
    pdf_himitsuhoji_taisha("himitsuhoji-seiyakusho_taisha.pdf");                print("  [ok] himitsuhoji-seiyakusho_taisha.pdf")
    pdf_himitsuhoji_nyusha("himitsuhoji-seiyakusho_nyusha_example.pdf", example=True)
    print("  [ok] himitsuhoji-seiyakusho_nyusha_example.pdf")

    # T019: 秘密保持契約書（NDA）— 取引先間
    pdf_nda_souhou("nda_souhou.pdf");                                           print("  [ok] nda_souhou.pdf")
    pdf_nda_henmu("nda_henmu.pdf");                                             print("  [ok] nda_henmu.pdf")
    pdf_nda_souhou("nda_souhou_example.pdf", example=True);                     print("  [ok] nda_souhou_example.pdf")

    # T028: 見積依頼書
    pdf_mitsumori_iraisho("mitsumori-iraisho.pdf");                             print("  [ok] mitsumori-iraisho.pdf")
    pdf_mitsumori_iraisho("mitsumori-iraisho_example.pdf", example=True);       print("  [ok] mitsumori-iraisho_example.pdf")

    # Vol.2 サイクル1: T041 念書 / T054 日報 / T057 お礼状
    pdf_nensho("nensho_general.pdf");                                           print("  [ok] nensho_general.pdf")
    pdf_nensho("nensho_general_example.pdf", example=True);                     print("  [ok] nensho_general_example.pdf")
    pdf_nippo("nippo_standard.pdf");                                            print("  [ok] nippo_standard.pdf")
    pdf_nippo("nippo_standard_example.pdf", example=True);                      print("  [ok] nippo_standard_example.pdf")
    pdf_oreijo("oreijo_general.pdf");                                           print("  [ok] oreijo_general.pdf")
    pdf_oreijo("oreijo_general_example.pdf", example=True);                     print("  [ok] oreijo_general_example.pdf")

    # Vol.2 サイクル2: T042 支払い念書 / T043 金銭念書 / T060 顛末書
    pdf_nensho_shiharai("nensho_shiharai.pdf");                                 print("  [ok] nensho_shiharai.pdf")
    pdf_nensho_shiharai("nensho_shiharai_example.pdf", example=True);           print("  [ok] nensho_shiharai_example.pdf")
    pdf_nensho_kinsen("nensho_kinsen.pdf");                                     print("  [ok] nensho_kinsen.pdf")
    pdf_nensho_kinsen("nensho_kinsen_example.pdf", example=True);               print("  [ok] nensho_kinsen_example.pdf")
    pdf_tenmatsusho("tenmatsusho_general.pdf");                                 print("  [ok] tenmatsusho_general.pdf")
    pdf_tenmatsusho("tenmatsusho_general_example.pdf", example=True);           print("  [ok] tenmatsusho_general_example.pdf")

    # Vol.2 サイクル3: T044 念書個人 PDF（T045 PDF特化は同ファイル流用）
    pdf_nensho_kojin("nensho_kojin.pdf");                                       print("  [ok] nensho_kojin.pdf")
    pdf_nensho_kojin("nensho_kojin_example.pdf", example=True);                 print("  [ok] nensho_kojin_example.pdf")

    # Vol.2 サイクル4: T047 委任状総会 / T048 委任状銀行 / T049 委任状汎用
    pdf_ininjo_sokai("ininjo_sokai.pdf");                                       print("  [ok] ininjo_sokai.pdf")
    pdf_ininjo_sokai("ininjo_sokai_example.pdf", example=True);                 print("  [ok] ininjo_sokai_example.pdf")
    pdf_ininjo_ginko("ininjo_ginko.pdf");                                       print("  [ok] ininjo_ginko.pdf")
    pdf_ininjo_ginko("ininjo_ginko_example.pdf", example=True);                 print("  [ok] ininjo_ginko_example.pdf")
    pdf_ininjo_general("ininjo_general.pdf");                                   print("  [ok] ininjo_general.pdf")
    pdf_ininjo_general("ininjo_general_example.pdf", example=True);             print("  [ok] ininjo_general_example.pdf")

    # Vol.2 サイクル5: T050/T051/T052 領収書サブ
    pdf_ryoshusho("ryoshusho.pdf");                                             print("  [ok] ryoshusho.pdf")
    pdf_ryoshusho("ryoshusho_example.pdf", example=True);                       print("  [ok] ryoshusho_example.pdf")

    # Vol.2 サイクル6: T053 領収書添え状（T055/T056 は既存ファイル流用）
    pdf_ryoshusho_soejou("ryoshusho_soejou.pdf");                               print("  [ok] ryoshusho_soejou.pdf")
    pdf_ryoshusho_soejou("ryoshusho_soejou_example.pdf", example=True);         print("  [ok] ryoshusho_soejou_example.pdf")

    # Vol.2 サイクル7: T058/T059/T061
    pdf_oreijo_english("oreijo_english.pdf");                                   print("  [ok] oreijo_english.pdf")
    pdf_oreijo_ochugen("oreijo_ochugen.pdf");                                   print("  [ok] oreijo_ochugen.pdf")
    pdf_oreijo_ochugen("oreijo_ochugen_example.pdf", example=True);             print("  [ok] oreijo_ochugen_example.pdf")
    pdf_shanai_tsutatsu("shanai_tsutatsu.pdf");                                 print("  [ok] shanai_tsutatsu.pdf")
    pdf_shanai_tsutatsu("shanai_tsutatsu_example.pdf", example=True);           print("  [ok] shanai_tsutatsu_example.pdf")

    # Vol.3: 法律深堀7本（メイン+派生）
    pdf_simple("naiyo_shomei_general.pdf",       "通　知　書",        "Word原本をそのまま PDF 化したものです。詳細は Word 版をご覧ください。")
    pdf_simple("naiyo_shomei_general_example.pdf","通　知　書（記入例）","記入例 PDF。実際の内容はご自身の状況に合わせて記入してください。", example=True)
    pdf_simple("shakuyosho_general.pdf",         "借　用　書",        "Word原本をそのまま PDF 化したものです。")
    pdf_simple("shakuyosho_general_example.pdf", "借用書（記入例）",  "記入例 PDF。実際の内容はご自身の状況に合わせて記入してください。", example=True)
    pdf_simple("kaiko_tsuchisho_general.pdf",    "解 雇 通 知 書",    "Word原本をそのまま PDF 化したものです。")
    pdf_simple("kaiko_tsuchisho_general_example.pdf","解雇通知書（記入例）","記入例 PDF。", example=True)
    pdf_simple("taishoku_shomeisho_general.pdf", "退 職 証 明 書",    "Word原本をそのまま PDF 化したものです。労基法第22条準拠。")
    pdf_simple("taishoku_shomeisho_general_example.pdf","退職証明書（記入例）","記入例 PDF。", example=True)
    pdf_simple("jidan_sho_general.pdf",          "示　談　書",        "Word原本をそのまま PDF 化したものです。")
    pdf_simple("jidan_sho_general_example.pdf",  "示談書（記入例）",  "記入例 PDF。", example=True)
    pdf_simple("yuigon_sho.pdf",                 "遺　言　書",        "民法第968条準拠の自筆証書遺言テンプレート。")
    pdf_simple("yuigon_sho_example.pdf",         "遺言書（記入例）",  "記入例 PDF。", example=True)
    pdf_simple("rikon_kyogisho.pdf",             "離 婚 協 議 書",    "Word原本をそのまま PDF 化したものです。")
    pdf_simple("rikon_kyogisho_example.pdf",     "離婚協議書（記入例）","記入例 PDF。", example=True)

    print(f"\nAll PDFs generated to: {OUT_DIR}")
