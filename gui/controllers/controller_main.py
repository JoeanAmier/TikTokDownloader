# -*- coding: utf-8 -*-
# @Author : Frica01
# @Time   : 2023-12-28 23:25
# @Name   : controller_main.py

import os
import sys
from datetime import time
from types import SimpleNamespace

from PySide6.QtCore import (QObject, Signal, Slot, QTimer)
from PySide6.QtGui import QTextCursor

from gui.models import (ColorfulConsole, ModelMain)
from gui.views import ViewMain
from src.DataAcquirer import (Live, Comment)
from src.application import TikTokDownloader
from src.application.main_api_server import APIServer
from src.application.main_complete import TikTok
from src.application.main_server import Server
from src.application.main_web_UI import WebUI
from src.custom import (failure_handling, suspend, WARNING, SERVER_HOST, PROJECT_ROOT)
from src.tools import TikTokAccount


class ControllerMain(QObject):
    signal_text_edit = Signal(str)

    def __init__(self):
        super().__init__()
        # 信号, 用于传输到text_edit
        self.signal_text_edit.connect(self.append_text)
        #
        self.view = ViewMain()
        self.model = ModelMain()
        self.model.signal_initial.connect(self.run_mode)
        self.model.signal_live.connect(self.special_live_mode)
        #
        cc = ColorfulConsole(self.signal_text_edit)
        self.ttk = TikTokDownloader()
        self.ttk.console = cc
        self.ttk.settings.console = cc
        self.ttk.cookie.console = cc
        self.ttk.register.console = cc
        self.initial_update_setting()
        #
        self.event_connect()
        #
        self.frame_show_flag = False
        self.run_mode_type = str()
        self.run_mode_map = dict()
        #
        QTimer.singleShot(1000, self.first_use_tip)

    def event_connect(self):
        # 运行模式
        self.view.btn_run_local.clicked.connect(self.start_run_mode)
        self.view.btn_run_api.clicked.connect(self.start_run_mode)
        self.view.btn_run_web_ui.clicked.connect(self.start_run_mode)
        self.view.btn_run_server_deploy.clicked.connect(self.start_run_mode)
        # cookie
        self.view.btn_paste_set_cookie.clicked.connect(self.view.setting_toggle)
        self.view.btn_scan_set_cookie.clicked.connect(self.scan_cookie)
        self.view.btn_check_cookie.clicked.connect(self.write_cookie)
        #
        self.view.btn_download.clicked.connect(self.run_local)
        self.view.radio_btn_1.clicked.connect(self.change_radio)
        self.view.radio_btn_2.clicked.connect(self.change_radio)
        self.view.radio_btn_3.clicked.connect(self.change_radio)
        self.view.radio_btn_4.clicked.connect(self.change_radio)
        self.view.radio_btn_5.clicked.connect(self.change_radio)
        self.view.radio_btn_6.clicked.connect(self.change_radio)
        self.view.radio_btn_7.clicked.connect(self.change_radio)
        self.view.radio_btn_8.clicked.connect(self.change_radio)
        self.view.radio_btn_9.clicked.connect(self.change_radio)
        self.view.radio_btn_10.clicked.connect(self.change_radio)
        # 互斥 radio
        self.view.group_radio_btn(self)
        # 绑定配置
        self.view.check_box_enable_check_update.clicked.connect(self.manual_update_setting)
        self.view.check_box_enable_download_record.clicked.connect(self.manual_update_setting)
        self.view.check_box_enable_log.clicked.connect(self.manual_update_setting)
        #
        self.view.closeAppBtn.clicked.connect(self.close)

    def start_run_mode(self):
        self.run_mode_type = self.sender().objectName()  # 获取发送信号的按钮
        # 任务初始化
        if self.run_mode_type == 'btn_run_local':
            self.view.btn_result.click()
        QTimer.singleShot(500, self._init)

    def _init(self):
        if not self.run_mode_map.get(self.run_mode_type):
            func_list = [
                self.ttk.check_config,
                self.ttk.version,
                self.ttk.check_update,
            ]
            self.model.initial(func_list)
            self.run_mode_map[self.run_mode_type] = True

    def first_use_tip(self):
        FIRST_USE = {"path": PROJECT_ROOT.joinpath("./src/config/First_Use")}
        # 如果文件存在, 则跳过
        if FIRST_USE['path'].exists():
            return
        # 弹窗提示
        self.ttk.console.input(
            "初次使用，点击左下角查看详细说明文档！\n 大致操作过程如下：\n&nbsp;&nbsp;&nbsp;&nbsp;1. 在设置界面选择一个运行模式\n&nbsp;&nbsp;&nbsp;&nbsp;2. 设置Cookie\n&nbsp;&nbsp;&nbsp;&nbsp;3. 看图界面就行"
        )
        self.ttk.change_config(FIRST_USE['path'])

    def write_cookie(self):
        cookie = self.view.line_edit_cookie.text()
        if not cookie or cookie.__len__() < 100:
            self.view.show_msg_box("请输入正确的 Cookie")
            return
        self.ttk.cookie.extract(cookie)
        self.ttk.check_settings()
        self.ttk.parameter.update_cookie()

    def scan_cookie(self):
        self.model.run_task(self.ttk.auto_cookie, thread_name='auto_cookie')

    def initial_update_setting(self):
        """初始化时候更新配置勾选"""
        self.view.check_box_enable_check_update.setChecked(True) if not self.ttk.UPDATE['path'].exists() else None
        self.view.check_box_enable_download_record.setChecked(True) if not self.ttk.RECORD['path'].exists() else None
        self.view.check_box_enable_log.setChecked(True) if self.ttk.LOGGING['path'].exists() else None

    def manual_update_setting(self):
        """手动更新基础设置"""
        check_name = self.sender().objectName()
        print(check_name)
        if check_name == 'check_box_enable_check_update':
            self.ttk.change_config(self.ttk.UPDATE['path'])
        elif check_name == 'check_box_enable_download_record':
            self.ttk.change_config(self.ttk.RECORD['path'])
        elif check_name == 'check_box_enable_log':
            self.ttk.change_config(self.ttk.LOGGING['path'])

    def change_radio(self):
        """切换 radio_btn 时候的操作."""
        self.view.radio_btn_hidden.setChecked(True)  # 点击隐藏按钮
        self.view.line_edit_url.clear()  # 清空 内容
        radio_btn_name = self.get_selected_radio_button()
        if radio_btn_name == 'radio_btn_1':
            self.view.line_edit_url.setPlaceholderText('')
        elif radio_btn_name == 'radio_btn_2':
            self.view.radio_btn_recommend.setText('使用 accounts_urls 参数(推荐)')
            self.view.line_edit_url.setPlaceholderText('在此输入抖音主页链接!')
        elif radio_btn_name == 'radio_btn_3':
            self.view.line_edit_url.setPlaceholderText('在此输入抖音视频链接!')
        elif radio_btn_name == 'radio_btn_4':
            self.view.line_edit_url.setPlaceholderText('在此输入抖音直播链接!')
        elif radio_btn_name == 'radio_btn_5':
            self.view.line_edit_url.setPlaceholderText('在此输入抖音视频链接!')
        elif radio_btn_name == 'radio_btn_6':
            self.view.radio_btn_recommend.setText('使用 mix_urls 参数的合集链接(推荐)')
            self.view.line_edit_url.setPlaceholderText('在此输入抖音合集链接!')
        elif radio_btn_name == 'radio_btn_7':
            self.view.radio_btn_recommend.setText('使用 accounts_urls 参数(推荐)')
            self.view.line_edit_url.setPlaceholderText('在此输入抖音账号链接!')
        elif radio_btn_name == 'radio_btn_8':
            self.view.line_edit_url.setPlaceholderText('在此输入：关键词 搜索类型 页数 排序规则 时间筛选 等!')
        elif radio_btn_name == 'radio_btn_9':
            self.view.line_edit_url.setPlaceholderText('该模式不用输入!')
        elif radio_btn_name == 'radio_btn_10':
            self.view.line_edit_url.setPlaceholderText('该模式不用输入!')

        # 如果选中了对应的模式
        if any([
            self.view.radio_btn_2.isChecked(),
            self.view.radio_btn_6.isChecked(),
            self.view.radio_btn_7.isChecked()
        ]):
            self.view.radio_btn_recommend.show()
            self.view.radio_btn_manual.show()
            self.view.label_manual.hide()
        else:
            self.view.radio_btn_recommend.hide()
            self.view.radio_btn_manual.hide()
            self.view.label_manual.show()
        # 设置不可输入
        if radio_btn_name in ['radio_btn_9', 'radio_btn_10']:
            self.view.line_edit_url.setEnabled(False)
        else:
            self.view.line_edit_url.setEnabled(True)
        # 只有在第一次切换时候展示
        if not self.frame_show_flag:
            self.frame_show_flag = True
            self.view.frame_input.show()
            self.view.frame_input_label.show()

    def get_selected_radio_button(self):
        """获取当前选择的 radio_button """
        radio_buttons = [
            self.view.radio_btn_1,
            self.view.radio_btn_2,
            self.view.radio_btn_3,
            self.view.radio_btn_4,
            self.view.radio_btn_5,
            self.view.radio_btn_6,
            self.view.radio_btn_7,
            self.view.radio_btn_8,
            self.view.radio_btn_9,
            self.view.radio_btn_10
        ]

        for radio_button in radio_buttons:
            if radio_button.isChecked():
                return radio_button.objectName()
        return None

    def get_line_edit_text(self) -> str | None:
        if text := self.view.line_edit_url.text():
            return text
        return None

    def run_mode(self):  #
        """运行对应模式"""
        run_mode_map = {
            'btn_run_local': '本地运行',
            'btn_run_api': 'Web API 接口',
            'btn_run_web_ui': 'Web UI 交互',
            'btn_run_server_deploy': '服务器部署'
        }
        self.ttk.check_settings()
        if not self.ttk.disclaimer():
            sys.exit(1)
        #
        # 提醒设置 cookie
        if not self.ttk.parameter.cookie:
            if self.ttk.console.input("Cookie 为空，不更新程序将无法预期运行，是否更新 Cookie？") == 'yes':
                self.view.btn_setting.click()
        # 更新 cookie
        self.model.run_task(self.ttk.periodic_update_cookie, thread_name='update_cookie')
        #
        self.view.show_msg_box("初始化完成!")
        self.view.btn_download.setEnabled(True)
        # 运行
        if self.run_mode_type == 'btn_run_local':
            return
        # 同时只能启动一个 web 端的任务
        elif self.run_mode_type == 'btn_run_api':
            self.model.run_task(self.ttk.server, APIServer, SERVER_HOST, thread_name='web')
        elif self.run_mode_type == 'btn_run_web_ui':
            self.model.run_task(self.ttk.server, WebUI, token=False, thread_name='web')
        elif self.run_mode_type == 'btn_run_server_deploy':
            self.model.run_task(self.ttk.server, Server, thread_name='web')

    def run_local(self):
        radio_btn_obj_name = self.get_selected_radio_button()
        if not radio_btn_obj_name:
            self.view.show_msg_box("未选中下载模式")
            return
        # 输入框
        line_edit_text = self.get_line_edit_text()
        # 如果没有存在就添加, 避免每次点击下载都添加
        if not hasattr(self, 'tk'):
            self.tk = TikTok(self.ttk.parameter)
        if radio_btn_obj_name == 'radio_btn_1':
            if not line_edit_text:
                self.view.show_msg_box("链接为空")
                return
            self.model.run_task(self.mode_1, line_edit_text)
        elif radio_btn_obj_name == 'radio_btn_2':
            if not line_edit_text and (not self.view.radio_btn_recommend.isChecked()):
                self.view.show_msg_box("链接为空")
                return
            self.model.run_task(self.mode_2, thread_name='mode_2')
        elif radio_btn_obj_name == 'radio_btn_3':
            if not line_edit_text:
                self.view.show_msg_box("链接为空")
                return
            self.model.run_task(self.mode_3, line_edit_text, thread_name='mode_3')
        elif radio_btn_obj_name == 'radio_btn_4':
            if not line_edit_text:
                self.view.show_msg_box("链接为空")
                return
            params = self.tk._generate_live_params(*self.tk.links.live(line_edit_text))
            if not params:
                self.tk.logger.warning(f"{line_edit_text} 提取直播 ID 失败")
                return
            self.model.run_live(Live, self.tk.parameter, params=params)
        elif radio_btn_obj_name == 'radio_btn_5':
            if not line_edit_text:
                self.view.show_msg_box("链接为空")
                return
            self.model.run_task(self.mode_5, line_edit_text, thread_name='mode_5')
        elif radio_btn_obj_name == 'radio_btn_6':
            if not line_edit_text and (not self.view.radio_btn_recommend.isChecked()):
                self.view.show_msg_box("链接为空")
                return
            self.model.run_task(self.mode_6, line_edit_text, thread_name='mode_6')
        elif radio_btn_obj_name == 'radio_btn_7':
            if not line_edit_text and (not self.view.radio_btn_recommend.isChecked()):
                self.view.show_msg_box("链接为空")
                return
            self.model.run_task(self.mode_7, line_edit_text, thread_name='mode_7')
        elif radio_btn_obj_name == 'radio_btn_8':
            self.model.run_task(self.mode_8, line_edit_text, thread_name='mode_8')
        elif radio_btn_obj_name == 'radio_btn_9':
            self.model.run_task(self.mode_9, thread_name='mode_9')
        elif radio_btn_obj_name == 'radio_btn_10':
            self.model.run_task(self.mode_10, thread_name='mode_10')

    def special_live_mode(self, live_data: list):
        if not [i for i in live_data if i]:
            self.tk.logger.warning("获取直播数据失败")
            return
        live_data = self.tk.extractor.run(live_data, None, "live")
        download_tasks = [(*self.ttk.console.input(live_data),)]
        if not download_tasks:
            self.ttk.console.print("没有选中下载!", style=WARNING)
            return
        download_tasks = [(_, *item) for _, item in zip(live_data, download_tasks)]
        self.model.run_task(self.mode_4, download_tasks, thread_name='special')

    def mode_1(self, path):
        self.tk.logger.info("账号作品正在下载...")
        root, params, logger = self.tk.record.run(self.ttk.parameter)
        items = TikTokAccount(path).run()
        if not items:
            self.tk.logger.warning(f"{path} 读取 HTML 文件失败")
            return
        #
        # count = SimpleNamespace(time=time(), success=0, failed=0)
        for index, (uid, nickname, item) in enumerate(items, start=1):
            if not self.tk._deal_account_works_tiktok(index, uid, nickname, item, root, params, logger):
                # count.failed += 1
                if index != len(items) and failure_handling():
                    continue
                break
            # count.success += 1
        # self.tk.logger.info("已退出批量下载账号作品(TikTok)模式")

    def mode_2(self):
        self.tk.logger.info("账号作品正在下载...")
        root, params, logger = self.tk.record.run(self.ttk.parameter)
        if self.view.radio_btn_recommend.isChecked():
            self.tk.account_works_batch(root, params, logger)
        elif self.view.radio_btn_manual.isChecked():
            url = self.get_line_edit_text()
            if not url:
                return
            links = self.tk.links.user(url)
            if not links:
                self.tk.logger.warning(f"{url} 提取账号 sec_user_id 失败")
                return
            count = SimpleNamespace(time=time(), success=0, failed=0)
            for index, sec in enumerate(links, start=1):
                if not self.tk.deal_account_works(index, sec_user_id=sec, root=root, params=params, logger=logger):
                    count.failed += 1
                    if index != len(links) and failure_handling():
                        continue
                    break
                count.success += 1
        # self.tk.logger.info("已退出批量下载合集作品模式")

    def mode_3(self, url):
        self.tk.logger.info("链接作品正在下载...")
        root, params, logger = self.tk.record.run(self.ttk.parameter)
        with logger(root, **params) as record:
            tiktok, ids = self.tk.links.works(url)
            if not any(ids):
                self.tk.logger.warning(f"{url} 提取作品 ID 失败")
                return
            self.tk.input_links_acquisition(tiktok, ids, record)
        # self.tk.logger.info("已退出批量下载链接作品模式")

    def mode_4(self, download_tasks):
        self.tk.logger.info("直播推流正在下载...")
        self.tk.downloader.run_live(download_tasks)
        # self.tk.logger.info("已退出获取直播推流地址模式")

    def mode_5(self, url):
        self.tk.logger.info("作品评论正在下载...")
        root, params, logger = self.tk.record.run(self.ttk.parameter, type_="comment")
        tiktok, ids = self.tk.links.works(url)
        if not any(ids):
            self.tk.logger.warning(f"{url} 提取作品 ID 失败")
            return
        elif tiktok:
            self.tk.console.print("目前项目暂不支持采集 TikTok 作品评论数据！", style=WARNING)
            return
        for i in ids:
            name = f"作品{i}_评论数据"
            with logger(root, name=name, **params) as record:
                if Comment(self.tk.parameter, i).run(self.tk.extractor, record):
                    self.tk.logger.info(f"作品评论数据已储存至 {name}")
                else:
                    self.tk.logger.warning("采集评论数据失败")
        # self.tk.logger.info("已退出采集作品评论数据模式")

    def mode_6(self, url):
        self.tk.logger.info("合集作品正在下载...")
        root, params, logger = self.tk.record.run(self.ttk.parameter, type_='mix')
        if self.view.radio_btn_recommend.isChecked():
            self.tk.mix_batch(root, params, logger)
        elif self.view.radio_btn_manual.isChecked():
            mix_id, ids = self.tk.links.mix(url)
            if not ids:
                self.tk.logger.warning(f"{url} 获取作品 ID 或合集 ID 失败")
                return
            count = SimpleNamespace(time=time(), success=0, failed=0)
            for index, i in enumerate(ids, start=1):
                if not self.tk._deal_mix_works(root, params, logger, mix_id, i):
                    count.failed += 1
                    if index != len(ids) and failure_handling():
                        continue
                    break
                count.success += 1
                if index != len(ids):
                    suspend(index, self.tk.console.print)
        # self.tk.logger.info("已退出批量下载合集作品模式")

    def mode_7(self, url):
        self.tk.logger.info("账号数据正在下载...")
        if self.view.radio_btn_recommend.isChecked():
            self.tk.user_batch()
        elif self.view.radio_btn_manual.isChecked():
            root, params, logger = self.tk.record.run(self.tk.parameter, type_="user")
            sec_user_ids = self.tk.links.user(url)
            if not sec_user_ids:
                self.tk.logger.warning(f"{url} 提取账号 sec_user_id 失败")
                return
            users = [self.tk._get_user_data(i) for i in sec_user_ids]
            self.tk._deal_user_data(root, params, logger, [i for i in users if i])
        # self.tk.logger.info("已退出批量采集账号数据模式")

    def mode_8(self, text):

        text = text.split()
        while 0 < len(text) < 5:
            text.append("0")
        if isinstance(c := self.tk._verify_search_criteria(*text), tuple):
            self.tk.logger.info("搜索结果数据正在下载...")
            self.tk._deal_search_data(*c)
        else:
            self.tk.console.print("搜索条件输入格式错误，详细说明请查阅文档！", style=WARNING)
            return
        # self.tk.logger.info("已退出采集搜索结果数据模式")

    def mode_9(self):
        self.tk.logger.info("热榜数据正在下载...")
        self.tk._deal_hot_data()
        # self.tk.logger.info("已退出采集抖音热榜数据模式")

    def mode_10(self):
        self.tk.logger.info("收藏作品正在下载...")
        self.tk.collection_interactive()
        # self.tk.logger.info("已退出批量下载收藏作品模式")

    @Slot(str)
    def append_text(self, text):
        # 在主线程中更新 text_edit
        self.view.text_edit_run_log.append(text)
        self.view.text_edit_run_log.moveCursor(QTextCursor.End)  # 再次确保光标在末尾

    def close(self):
        self.ttk.delete_temp()
        self.ttk.event.set()
        self.ttk.blacklist.close()
        self.ttk.parameter.logger.info("程序结束运行")
        os._exit(0)