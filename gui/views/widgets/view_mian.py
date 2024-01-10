# -*- coding: utf-8 -*-
# @Author : Frica01
# @Time   : 2023-12-30 18:18
# @Name   : view_mian.py


from PySide6.QtCore import (Qt, QPoint, QTimer, QEvent, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, Slot,
                            QUrl, QRect)
from PySide6.QtGui import (QColor, QIcon, QDesktopServices, QFontMetrics, QFont)
from PySide6.QtWidgets import (QMainWindow, QGraphicsDropShadowEffect, QSizeGrip, QPushButton, QRadioButton,
                               QTableWidgetItem, QHeaderView, QCheckBox, QListWidget, QListWidgetItem,
                               QAbstractItemView, QTableWidget, QApplication, QMessageBox, QDialog, QTextEdit,
                               QDialogButtonBox, QVBoxLayout, QButtonGroup, QHBoxLayout)

from gui.views import (CustomGrip, Ui_MainWindow)


class TextInputDialog(QDialog):
    def __init__(self, prompt, parent=None, add_radio_btn=False, radio_btn_list=None):
        super().__init__(parent)
        self.setWindowTitle('超大号温馨提醒！')
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 设置为置顶窗口
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # 设置为只读
        # 调整对话框大小
        self.resize(650, 250)
        if prompt.__len__() >= 200:
            self.resize(800, 660)
        # 基础样式
        self.text_edit.setStyleSheet(
            """QTextEdit {
                line-height: 1.3; /* 设置行间距 */
                background-color: rgb(40, 44, 52);
                font: 12pt "Segoe UI"; /* 设置字体大小 */
            }
            """
        )
        self.text_edit.setText(prompt)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # 布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        # 如果需要添加 radio 按钮
        if add_radio_btn and radio_btn_list:
            self.radio_btns = list()  # 存储所有的RadioButton
            sub_layout = QHBoxLayout(self)
            for object_name in radio_btn_list:
                radio_btn = QRadioButton(object_name)
                self.radio_btns.append(radio_btn)
                radio_btn.setStyleSheet("""font: 700 15pt "Segoe UI";""")
                sub_layout.addWidget(radio_btn)
            layout.addLayout(sub_layout)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def get_selected_radio_button(self):
        # 遍历所有RadioButton，找到被选中的RadioButton并返回其文本
        for radio_btn in self.radio_btns:
            if radio_btn.isChecked():
                return radio_btn.text()
        return None  # 如果没有选中的RadioButton则返回None


class ViewMain(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("谱蓝直播水军小工具 - 小菜")
        # 变量初始
        self._move = False
        self.win_max_status = False
        self.move_position = QPoint(0, 0)
        #
        # 初始化
        self._init()
        self.timer = QTimer()
        self.msg_box = QMessageBox()

    def _init(self):
        # 设置标题的移动和双击全屏
        def move_window(event=None):
            if event.buttons() == Qt.LeftButton:
                self.move(event.globalPos() - self.move_position)
                event.accept()

        def double_click_restore(event=None):
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(200, self.maximize_restore)

        self.titleRightInfo.mouseMoveEvent = move_window
        self.titleRightInfo.mouseDoubleClickEvent = double_click_restore
        # 四周的可拖拽
        self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)
        # 隐藏边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(17)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.bgApp.setGraphicsEffect(shadow)
        # 调整窗口大小
        sizegrip = QSizeGrip(self.frame_size_grip)
        sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")
        # 最小化
        self.minimizeAppBtn.clicked.connect(self.showMinimized)
        # 最大化/恢复
        self.maximizeRestoreAppBtn.clicked.connect(self.maximize_restore)
        # 关闭应用
        self.closeAppBtn.clicked.connect(self.close)
        # setting面板
        self.btn_setting.setToolTip("设置")
        # 绑定点击打开 说明文档
        self.textEdit.mouseDoubleClickEvent = self.double_click_open_readme
        # 按钮绑定事件
        self.btn_menu.clicked.connect(self.menu_toggle)
        self.btn_home.clicked.connect(self.switch_page)

        self.btn_run.clicked.connect(self.switch_page)
        self.btn_result.clicked.connect(self.switch_page)

        self.btn_setting.clicked.connect(self.setting_toggle)
        self.extraCloseColumnBtn.clicked.connect(self.setting_toggle)
        # 隐藏输入 frame
        self.frame_input.hide()
        self.frame_input_label.hide()
        self.btn_download.setEnabled(False)

    def switch_page(self):
        """页面切换"""
        page_map = {
            'btn_home': 0,
            'btn_run': 1,
            'btn_result': 2,
        }
        btn = self.sender()
        btn_name = btn.objectName()
        idx = page_map[btn_name]
        if idx == self.stackedWidget.currentWidget():
            return
        QTimer.singleShot(150, lambda: self.stackedWidget.setCurrentIndex(idx))
        self.reset_style(btn_name)
        btn.setStyleSheet(self.select_menu(btn.styleSheet()))

    def menu_toggle(self):
        """设置 菜单 动画"""
        width = self.leftMenuBg.width()
        setting_width = self.extraLeftBox.width()
        self.group_animation(width, setting_width=setting_width, frame_name="menu")

    def setting_toggle(self):
        """设置 setting 动画"""
        width = self.extraLeftBox.width()
        menu_width = self.leftMenuBg.width()
        self.group_animation(menu_width, setting_width=width, frame_name="setting")

    def group_animation(self, menu_width, setting_width, frame_name) -> None:
        """
        菜单 + 设置 的组合动画.

        Args:
            menu_width(int): 菜单frame的宽度
            setting_width(int): 设置frame的宽度
            frame_name(str): 框架的objname

        Returns:

        """
        # get and set values
        end_menu_width = 160 if menu_width == 60 and frame_name == "menu" else 60
        # get and set values
        end_setting_width = 400 if setting_width == 0 and frame_name == "setting" else 0

        # ANIMATION MENU BOX
        self.menu_box = QPropertyAnimation(self.leftMenuBg, b"minimumWidth")
        self.menu_box.setDuration(750)
        self.menu_box.setStartValue(menu_width)
        self.menu_box.setEndValue(end_menu_width)
        self.menu_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION SETTING BOX
        self.setting_box = QPropertyAnimation(self.extraLeftBox, b"minimumWidth")
        self.setting_box.setDuration(750)
        self.setting_box.setStartValue(setting_width)
        self.setting_box.setEndValue(end_setting_width)
        self.setting_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        group = QParallelAnimationGroup(self)
        group.addAnimation(self.menu_box)
        group.addAnimation(self.setting_box)
        group.start()

    def group_radio_btn(self, parent=None):
        btn_group = QButtonGroup(parent)
        self.radio_btn_hidden = QRadioButton()
        btn_group.addButton(self.radio_btn_hidden)
        btn_group.addButton(self.radio_btn_recommend)
        btn_group.addButton(self.radio_btn_manual)
        btn_group.setExclusive(True)  # 设置按钮组为互斥模式

    def reset_style(self, btn_name: str):
        for w in self.topMenu.findChildren(QPushButton):
            if w.objectName() != btn_name:
                w.setStyleSheet(self.deselect_menu(w.styleSheet()))

    @staticmethod
    def select_menu(style):
        MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
        background-color: rgb(40, 44, 52);
        """
        return style + MENU_SELECTED_STYLESHEET

    @staticmethod
    def deselect_menu(get_style):
        MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
        background-color: rgb(40, 44, 52);
        """
        return get_style.replace(MENU_SELECTED_STYLESHEET, "")

    def maximize_restore(self):
        if not self.win_max_status:
            self.showMaximized()
            self.appMargins.setContentsMargins(0, 0, 0, 0)
            self.maximizeRestoreAppBtn.setToolTip("Restore")
            self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            self.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
            self.win_max_status = True
        else:
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.appMargins.setContentsMargins(10, 10, 10, 10)
            self.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            self.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()
            self.win_max_status = False

    @staticmethod
    def double_click_open_readme(event) -> None:
        import webbrowser
        webbrowser.open('https://github.com/JoeanAmier/TikTokDownloader/wiki/Documentation')

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._move = True
            self.move_position = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def resizeEvent(self, event) -> None:
        self.left_grip.setGeometry(0, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 10)
        self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    def show_msg_box(self, text: str = None):
        """
        显示消息弹框,

        Args:
            text (str): 弹窗的文本内容

        Returns:

        """
        self.msg_box.setText(text if text else '不知名提示')
        self.msg_box.setWindowTitle("提示")
        self.timer.singleShot(3000, self.msg_box.close)
        self.msg_box.exec_()
