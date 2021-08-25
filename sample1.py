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
    line_space = 9.5
    pm = PageMan(
        size, margin=margin, font_size=font_size, line_space=line_space)

    pm.new_page()

    line_idx = 0

    text = '私はいかにしてパッケージを作ったか'
    ttl_line = PScLine(PScLineType.TITLE, text=text)
    line_idx = pm.draw_direction(line_idx, ttl_line)

    text = 'アラン・スミシ'
    athr_line = PScLine(PScLineType.AUTHOR, text=text)
    line_idx = pm.draw_author(line_idx, athr_line)

    # 空行をはさむ
    line_idx += 1

    text = '登場人物'
    chead_line = PScLine(PScLineType.CHARSHEADLINE, text=text)
    line_idx = pm.draw_charsheadline(line_idx, chead_line)

    # 空行をはさむ
    line_idx += 1

    name = '太郎'
    text = '主人公。'
    char_line = PScLine(PScLineType.CHARACTER, name=name, text=text)
    line_idx = pm.draw_character(line_idx, char_line)

    name = '光'
    text = '正体不明の人物。' * 5
    char_line = PScLine(PScLineType.CHARACTER, name=name, text=text)
    line_idx = pm.draw_character(line_idx, char_line)

    name = 'ジョージ・クルーニー'
    text = '濃い外人。' * 5 + '\n' + '濃い外人。' * 3
    char_line = PScLine(PScLineType.CHARACTER, name=name, text=text)
    line_idx = pm.draw_character(line_idx, char_line)

    # 空行をはさむ
    line_idx += 1

    text = '太郎、登場する。' * 5
    drct_line = PScLine(PScLineType.DIRECTION, text=text)
    line_idx = pm.draw_direction(line_idx, drct_line)

    # 空行をはさむ
    line_idx += 1

    name = '太郎'
    text = 'あいうえおかきくけこ' * 5 + '\n' + 'あいうえおかきくけこ' * 5
    dlg_line = PScLine(PScLineType.DIALOGUE, name=name, text=text)
    line_idx = pm.draw_dialogue(line_idx, dlg_line)

    # 空行をはさむ
    line_idx += 1

    text = '光、登場する。' * 5 + '\n' + '光、登場する。' * 5
    drct_line = PScLine(PScLineType.DIRECTION, text=text)
    line_idx = pm.draw_direction(line_idx, drct_line)

    # 空行をはさむ
    line_idx += 1

    name = '光'
    text = 'こっそりぴょん' * 5 + '\n' + 'こっそりぴょん' * 5
    dlg_line = PScLine(PScLineType.DIALOGUE, name=name, text=text)
    line_idx = pm.draw_dialogue(line_idx, dlg_line)

    name = 'ジョージ・クルーニー'
    text = 'あいうえおかきくけこさしすせそたちつてと' * 10
    dlg_line = PScLine(PScLineType.DIALOGUE, name=name, text=text)
    line_idx = pm.draw_dialogue(line_idx, dlg_line)

    # ページを確定する
    pm.close_page()

    # ファイルに出力する
    pm.save('out.pdf')


if __name__ == '__main__':
    main()
