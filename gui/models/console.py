# -*- coding: utf-8 -*-
# Name:         console.py
# Author:       小菜
# Date:         2024/1/10 17:08
# Description:
import inspect
import re
from collections import defaultdict

from rich.console import Console
from rich.style import Style

from gui.views import TextInputDialog
from src.custom import (
    PROMPT,
    WARNING,
    MASTER,
    DISCLAIMER_TEXT
)


def text_to_colored_html(text, style=PROMPT):
    # 使用正则匹配 文本是否带颜色
    color_pattern = re.compile(r'\[.*?]')
    matches = color_pattern.findall(text)
    if matches:
        text = text.replace(matches[0], '').replace(matches[1], '')
        style = matches[0][1:-1]
    #
    style = Style.parse(style)  # 解析 rich 格式的颜色
    text = text.replace("\n", "<br>")
    colors = str()
    if style.color:
        color = style.color.get_truecolor()  # 获取真实颜色
        colors = f"color: rgb({color.red}, {color.green}, {color.blue})"
    return f'<span style="{colors}">{text}</span>'


def live_special_extract_info(data: list):
    show_text = str()
    _map = defaultdict(list)
    for item in data:
        show_text += '直播标题: ' + item['title'] + '\n'
        show_text += '主播昵称: ' + item['nickname'] + '\n'
        show_text += '在线观众: ' + item['user_count_str'] + '\n'
        show_text += '观看次数: ' + item['total_user_str'] + '\n\n'
        show_text += "FLV 推流地址: " + '\n'
        for k, v in item['flv_pull_url'].items():
            show_text += '&nbsp;&nbsp;&nbsp;&nbsp;' + ': ' + k + '\n'
            _map[k].append(v)
        show_text += '\n' + "M3U8 推流地址: " + '\n'
        for k, v in item["hls_pull_url_map"].items():
            show_text += '&nbsp;&nbsp;&nbsp;&nbsp;' + ': ' + k + '\n'
            _map[k].append(v)
        show_text += "\n请选择下载清晰度(选择对应序号，不选代表不下载): "
    return _map, show_text


class ColorfulConsole(Console):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = signal

    def print(self, *args, style=PROMPT, highlight=False, **kwargs):
        with self.capture() as capture:
            super().print(*args, style=style, highlight=highlight, **kwargs, end="")
        res = text_to_colored_html(capture.get(), style)
        self.signal.emit(res)

    def input(self, prompt_="", *args, **kwargs):
        style = WARNING
        # 这个特别一些，因为文本太长
        if inspect.currentframe().f_back.f_code.co_name == 'disclaimer':
            prompt_ = "\n".join(DISCLAIMER_TEXT) + '\n\n' + prompt_
            style = MASTER
        # 直播输入的, 也比较特别
        if inspect.currentframe().f_back.f_code.co_name == 'special_live_mode':
            _map, _prompt = live_special_extract_info(prompt_)
            dialog = TextInputDialog(
                text_to_colored_html(_prompt, style=style), add_radio_btn=True, radio_btn_list=_map.keys()
            )
            if dialog.exec():
                selected_radio = dialog.get_selected_radio_button()
                return _map.get(selected_radio, list())
            return list()
        # 一般的弹框
        dialog = TextInputDialog(text_to_colored_html(prompt_, style=style))
        res = dialog.exec()
        return 'yes' if res else 'no'
