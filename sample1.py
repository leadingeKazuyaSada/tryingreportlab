from reportlab.lib.pagesizes import portrait, A5
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont

from playscript import PScLineType, PScLine

from conv.pdf import PageMan


def main():

    # フォントの設定
    font_name = 'HeiseiMin-W3'
    # font_name = 'HeiseiKakuGo-W5'
    pdfmetrics.registerFont(UnicodeCIDFont(font_name, isVertical=True))

    # ページの設定
    size = portrait(A5)
    margin = (2.0 * cm, 2.0 * cm)
    font_size = 10.0
    pm = PageMan(size, margin=margin, font_size=font_size)

    pm.new_page()

    line_idx = 0
    name = '太郎'
    text = 'あいうえおかきくけこさしすせそたちつてと' * 10
    dlg_line = PScLine(PScLineType.DIALOGUE, name, text)
    line_idx = pm.draw_dialogue(line_idx, dlg_line)

    name = '光'
    text = 'こっそりぴょんぴょん' * 10
    dlg_line = PScLine(PScLineType.DIALOGUE, name, text)
    line_idx = pm.draw_dialogue(line_idx, dlg_line)

    name = 'ジョージ'
    text = 'あいうえおかきくけこさしすせそたちつてと' * 10
    dlg_line = PScLine(PScLineType.DIALOGUE, name, text)
    line_idx = pm.draw_dialogue(line_idx, dlg_line)

    # ページを確定する
    pm.close_page()

    # ファイルに出力する
    pm.save('out.pdf')


if __name__ == '__main__':
    main()
