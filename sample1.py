from reportlab.lib.pagesizes import portrait, A5
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

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
    pm = PageMan(size, margin=margin)

    # print(pm.canvas.getAvailableFonts())

    line_idx = 0

    text = '私はいかにしてパッケージを作ったか'
    ttl_line = PScLine(PScLineType.TITLE, text=text)
    line_idx = pm.draw_title(line_idx, ttl_line)

    text = 'アラン・スミシ'
    athr_line = PScLine(PScLineType.AUTHOR, text=text)
    line_idx = pm.draw_author(line_idx, athr_line)

    # 空行をはさむ
    line_idx += 1

    text = 'この台本に意味はありません。' * 5
    cmmt_line = PScLine(PScLineType.COMMENT, text=text)
    line_idx = pm.draw_comment(line_idx, cmmt_line)

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

    text = 'シーン１'
    h1_line = PScLine(PScLineType.H1, text=text)
    line_idx = pm.draw_slugline(line_idx, h1_line, number=1, border=True)

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

    # 空行をはさむ
    line_idx += 1

    text = 'その頃、ジョージは…'
    h1_line = PScLine(PScLineType.H1, text=text)
    line_idx = pm.draw_slugline(line_idx, h1_line, number='1A')

    # 空行をはさむ
    line_idx += 1

    name = 'ジョージ・クルーニー'
    text = 'あいうえおかきくけこさしすせそたちつてと' * 10
    dlg_line = PScLine(PScLineType.DIALOGUE, name=name, text=text)
    line_idx = pm.draw_dialogue(line_idx, dlg_line)

    # 空行をはさむ
    line_idx += 1

    text = 'ジョージ、退場。'
    drct_line = PScLine(PScLineType.DIRECTION, text=text)
    line_idx = pm.draw_direction(line_idx, drct_line)

    # 空行 x 2個
    empty_line = PScLine(PScLineType.EMPTY)
    line_idx = pm.draw_empty(line_idx, empty_line)
    line_idx = pm.draw_empty(line_idx, empty_line)

    text = '暗転。'
    drct_line = PScLine(PScLineType.DIRECTION, text=text)
    line_idx = pm.draw_direction(line_idx, drct_line)

    # 空行をはさむ
    line_idx += 1

    text = 'おわり'
    endmk_line = PScLine(PScLineType.ENDMARK, text=text)
    line_idx = pm.draw_endmark(line_idx, endmk_line)

    # ファイルに出力する
    pm.close()
    pm.save('out.pdf')


if __name__ == '__main__':
    main()
