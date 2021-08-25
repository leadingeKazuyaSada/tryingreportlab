from collections import namedtuple
import io

from reportlab.pdfgen import canvas
from playscript import PScLineType, PScLine

Size = namedtuple('Size' , 'w h')
Point = namedtuple('Point' , 'x y')


class PageMan:
    def __init__(self, size, margin=None, upper_space=None,
                 font_name=None, font_size=None, line_space=None):
        """コンストラクタ

        Parameters
        ----------
        size : tuple
        margin : tuple
        upper_space : float
        font_name : str
        font_size : float
        line_space : float
        """

        self.size = Size(*size)
        self.margin = Size(*margin) if margin else Size(2 * cm, 2 * cm)
        if upper_space is None:
            self.upper_space = self.size.h / 4
        else:
            self.upper_space = upper_space

        self.font_name = 'HeiseiMin-W3' if font_name is None else font_name
        self.font_size = 10.0 if font_size is None else font_size
        self.line_space = self.font_size if line_space is None else line_space

        self.pdf = io.BytesIO()
        self.canvas = canvas.Canvas(self.pdf, pagesize=self.size)

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

    def new_page(self):
        # 横線
        x1 = self.margin.w - self.line_space
        x2 = self.size.w - self.margin.w + self.line_space
        y = self.size.h - self.margin.h - self.upper_space
        self.canvas.setLineWidth(0.1)
        self.canvas.line(x1, y, x2, y)

        # フォントを再セット
        self.canvas.setFont(self.font_name, self.font_size)

    def close_page(self):
        self.canvas.showPage()

    def save(self, file_name):
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

        # 書き出す
        self.canvas.drawString(x, y, text[:max_len])
        return text[max_len:]

    def draw_line_bottom(self, l_idx, text):
        """テキストを下寄せで書き出す
        """
        # インデントを1文字分とする
        indent = self.font_size

        x = self.get_line_x(l_idx)
        y = self.get_line_y(indent)

        height = self.size.h - 2 * self.margin.h - self.upper_space \
            - indent
        max_len = int(height // self.font_size)

        # 一行に収まる長さにする
        text = text[:max_len]

        # 下端につくように y を減らす
        y -= (max_len - len(text)) * self.font_size

        # 書き出す
        self.canvas.drawString(x, y, text)

    def draw_title(self, l_idx, ttl_line):
        """題名を書き出す
        """
        # ト書きの書き出しと同じ処理
        return self.draw_direction(l_idx, ttl_line)

    def draw_author(self, l_idx, athr_line):
        """著者名を書き出す
        """
        self.draw_line_bottom(l_idx, athr_line.text)
        return l_idx + 1

    def draw_direction(self, l_idx, drct_line):
        """ト書き行を書き出す
        """
        # 改行で分ける
        texts = drct_line.text.splitlines()
        # インデントは7文字分
        indent = self.font_size * 7

        for text in texts:
            line = text
            while len(line) > 0:
                # l_idx をチェックして改ページ
                if l_idx >= self.max_line_count():
                    self.canvas.showPage()
                    self.new_page()
                    l_idx = 0

                line = self.draw_line(l_idx, line, indent=indent)
                first_line = False
                l_idx += 1

        return l_idx

    def draw_dialogue(self, l_idx, dlg_line):
        """セリフ行を書き出す
        """
        name = dlg_line.name
        text = dlg_line.text

        # 名前をつけて一個の文字列にする
        if len(name) == 1:
            name = ' ' + name + ' '
        elif len(name) == 2:
            name = name[0] + ' ' + name[1]
        text = name + '「' + text + '」'

        # 改行で分ける
        texts = text.splitlines()
        first_line = True
        for text in texts:
            line = text
            while len(line) > 0:
                # l_idx をチェックして改ページ
                if l_idx >= self.max_line_count():
                    self.canvas.showPage()
                    self.new_page()
                    l_idx = 0

                indent = self.font_size * (1 if first_line else 5)
                line = self.draw_line(l_idx, line, indent=indent)
                first_line = False
                l_idx += 1

        return l_idx
