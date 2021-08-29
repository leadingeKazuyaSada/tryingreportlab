from collections import namedtuple
import io

from reportlab.pdfgen import canvas
from playscript import PScLineType, PScLine

Size = namedtuple('Size' , 'w h')


class PageMan:
    def __init__(self, size, margin=None, upper_space=None,
                 font_name='HeiseiMin-W3', num_font_name='Times-Roman',
                 font_size=None, line_space=None,):
        """コンストラクタ

        Parameters
        ----------
        size : tuple
            ページのサイズ (ポイント)
        margin : tuple
            左右と上下のマージン (ポイント)
        upper_space : float
            上の余白 (ポイント)
        font_name : str
            本文のフォント
        num_font_name : str
            数字のフォント
        font_size : float
            本文のフォントサイズ (ポイント)
        line_space : float
            本文の行間 (ポイント)
        """

        # 属性の設定
        self.size = Size(*size)
        self.font_name = font_name
        self.num_font_name = num_font_name

        self.margin = Size(*margin) if margin else Size(2 * cm, 2 * cm)
        if upper_space is None:
            self.upper_space = self.size.h / 4
        else:
            self.upper_space = upper_space
        self.font_size = 10.0 if font_size is None else font_size
        self.line_space = self.font_size if line_space is None else line_space

        # 書き出しの準備
        self.pdf = io.BytesIO()
        self.canvas = canvas.Canvas(self.pdf, pagesize=self.size)
        self.init_page()

    def get_line_x(self, l_idx):
        x = self.size.w - self.margin.w - self.font_size / 2
        x = x - l_idx * (self.font_size + self.line_space)
        return x

    def get_line_y(self, indent):
        y = self.size.h - self.margin.h - self.upper_space - indent
        return y

    def max_line_count(self):
        area_w = self.size.w - 2 * self.margin.w + self.line_space
        count = area_w // (self.font_size + self.line_space)
        return int(count)

    def init_page(self):
        """新しいページのための前処理
        """
        # 横線を書き出す
        x1 = self.margin.w - self.line_space
        x2 = self.size.w - self.margin.w + self.line_space
        y = self.size.h - self.margin.h - self.upper_space
        self.canvas.setLineWidth(0.1)
        self.canvas.line(x1, y, x2, y)

        # フォントを設定する
        self.canvas.setFont(self.font_name, self.font_size)

    def commit_page(self):
        self.canvas.showPage()

    def save(self, file_name):
        """PDF をファイルに出力する

        Parameters
        ----------
        file_name : str
            出力先のファイル名
        """
        self.commit_page()
        self.canvas.save()
        self.pdf.seek(0)
        with open(file_name, 'wb') as f:
            f.write(self.pdf.read())

    def draw_line(self, l_idx, text, indent=None):
        """テキストを行末まで書き出して残りを返す
        """
        # インデントのデフォルトを1文字分とする
        if indent is None:
            indent = self.font_size

        x = self.get_line_x(l_idx)
        y = self.get_line_y(indent)

        height = self.size.h - 2 * self.margin.h - self.upper_space \
            - indent
        max_len = int(height // self.font_size)

        # 簡易的ぶら下げ処理
        if len(text) > max_len and text[max_len] in '、。」':
            max_len += 1
            if len(text) > max_len and text[max_len] == '」':
                max_len -= 2

        # テキストを書き出す
        self.canvas.drawString(x, y, text[:max_len])
        return text[max_len:]

    def draw_lines(self, l_idx, lines, indent=None, first_indent=None):
        """複数行に渡るテキストを書き出す
        """
        if not first_indent:
            first_indent = indent

        # 改行で分ける
        texts = lines.splitlines()
        first_line = True

        for text in texts:
            line = text
            while len(line) > 0:
                # l_idx をチェックして改ページ
                if l_idx >= self.max_line_count():
                    self.commit_page()
                    self.init_page()
                    l_idx = 0

                # 1行分だけ書き出す
                line_indent = first_indent if first_line else indent
                line = self.draw_line(l_idx, line, indent=line_indent)
                first_line = False
                l_idx += 1
        return l_idx

    def draw_single_line(self, l_idx, line, indent=None):
        """1行に収まるテキストを書き出す
        """
        # l_idx をチェックして改ページ
        if l_idx >= self.max_line_count():
            self.commit_page()
            self.init_page()
            l_idx = 0

        # テキストを書き出す
        _ = self.draw_line(l_idx, line, indent=indent)
        return l_idx + 1

    def draw_line_bottom(self, l_idx, line):
        """テキストを下寄せで書き出す
        """
        # インデント (1文字分)
        indent = self.font_size

        # 1行に収まる文字数にする
        height = self.size.h - 2 * self.margin.h - self.upper_space \
            - indent
        max_len = int(height // self.font_size)
        line = line[:max_len]

        # 下端につくようにインデントを増やす
        indent += (max_len - len(line)) * self.font_size

        # テキストを1行として書き出す
        l_idx = self.draw_single_line(l_idx, line, indent=indent)
        return l_idx

    def draw_title(self, l_idx, ttl_line):
        """題名を書き出す
        """
        indent = self.font_size * 7
        l_idx = self.draw_lines(l_idx, ttl_line.text, indent=indent)
        return l_idx

    def draw_author(self, l_idx, athr_line):
        """著者名を書き出す
        """
        self.draw_line_bottom(l_idx, athr_line.text)
        return l_idx + 1

    def draw_charsheadline(self, l_idx, chead_line):
        """登場人物見出し行を書き出す
        """
        # インデント (8文字分)
        indent = self.font_size * 8

        # テキストを1行として書き出す
        l_idx = self.draw_single_line(l_idx, chead_line.text, indent=indent)
        return l_idx

    def draw_character(self, l_idx, char_line):
        """登場人物行を書き出す
        """
        name = char_line.name
        text = char_line.text if hasattr(char_line, 'text') else ''

        # 名前に説明をつけて一個の文字列にする
        if text:
            # 名前が2文字未満の場合は空白を足してから説明をつける
            if len(name) < 2:
                name += '　'
            text = name + '　' + text
        else:
            text = name

        # インデント (7文字分 -> 10文字分)
        first_indent = self.font_size * 7
        indent = self.font_size * 10

        # テキストを書き出す
        l_idx = self.draw_lines(
            l_idx, text, indent=indent, first_indent=first_indent)
        return l_idx

    def draw_slugline(self, l_idx, hx_line, number=None, border=False):
        """柱を書き出す
        """
        # テキストを1行として書き出す
        l_idx = self.draw_single_line(l_idx, hx_line.text)

        # 囲み線
        if border:
            x = self.get_line_x(l_idx - 1)
            x1 = x + self.font_size / 2 + self.line_space * 0.8
            x2 = x - self.font_size / 2 - self.line_space * 0.8
            y1 = self.get_line_y(-(self.font_size * 3))
            y2 = self.margin.h - self.font_size

            self.canvas.setLineWidth(0.1)
            self.canvas.line(x1, y1, x1, y2)
            self.canvas.line(x1, y1, x2, y1)
            self.canvas.line(x2, y1, x2, y2)

        # 数字
        if number is not None:
            num_str = str(number)
            w = self.canvas.stringWidth(
                num_str, self.num_font_name, self.font_size)
            x = self.get_line_x(l_idx - 1) - w / 2
            y = self.get_line_y(-self.font_size)

            # 数字を書き出す
            self.canvas.setFont(self.num_font_name, self.font_size)
            self.canvas.drawString(x, y, num_str)

            # フォントを元に戻す
            self.canvas.setFont(self.font_name, self.font_size)

        return l_idx

    def draw_direction(self, l_idx, drct_line):
        """ト書き行を書き出す
        """
        indent = self.font_size * 7
        l_idx = self.draw_lines(l_idx, drct_line.text, indent=indent)
        return l_idx

    def draw_dialogue(self, l_idx, dlg_line):
        """セリフ行を書き出す
        """
        name = dlg_line.name
        text = dlg_line.text

        # 名前にセリフをつけて一個の文字列にする
        if len(name) == 1:
            name = ' ' + name + ' '
        elif len(name) == 2:
            name = name[0] + ' ' + name[1]
        text = name + '「' + text + '」'

        # インデント (1文字分 -> 5文字分)
        first_indent = self.font_size * 1
        indent = self.font_size * 5

        # テキストを書き出す
        l_idx = self.draw_lines(
            l_idx, text, indent=indent, first_indent=first_indent)
        return l_idx

    def draw_endmark(self, l_idx, endmk_line):
        """エンドマークを書き出す
        """
        self.draw_line_bottom(l_idx, endmk_line.text)
        return l_idx + 1

    def draw_comment(self, l_idx, cmmt_line):
        """コメント行を書き出す
        """
        indent = self.font_size * 7
        l_idx = self.draw_lines(l_idx, cmmt_line.text, indent=indent)
        return l_idx

    def draw_empty(self, l_idx, empty_line):
        """空行を書き出す
        """
        # 空文字列を1行として書き出す
        l_idx = self.draw_single_line(l_idx, '')
        return l_idx
