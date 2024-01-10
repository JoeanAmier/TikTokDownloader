# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainDJAYEB.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QStackedWidget,
    QTextEdit, QVBoxLayout, QWidget)

from . resources_rc import *



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 635)
        MainWindow.setMinimumSize(QSize(1080, 600))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, "
                        "147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#btn_menu {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#btn_menu:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#btn_menu:pressed {\n"
"	background-color: rgb(189, 147, 249);"
                        "\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid"
                        " rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; bord"
                        "er-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255)"
                        ";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	font: 12pt \"Microsoft YaHei UI\";\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	font: 16pt \"Microsoft YaHei UI\";\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
""
                        "{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	se"
                        "lection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontro"
                        "l-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-righ"
                        "t-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb"
                        "(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"\n"
"	 background: 3px solid rgba(255, 121, 198, 255);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
""
                        "}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
" "
                        "   background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////"
                        "////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	/*background-color: rgb(35, 69, 104);*/\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"\n"
"#extraLeftBox QPushBu"
                        "tton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	/*background-color: rgb(35, 69, 104);*/\n"
"}\n"
"#extraLeftBox QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#extraLeftBox QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(60, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        self.titleLeftDescription.setFont(font)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(60, 5, 101, 21))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setMinimumSize(QSize(400, 0))
        self.leftMenuFrame.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btn_menu = QPushButton(self.toggleBox)
        self.btn_menu.setObjectName(u"btn_menu")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu.sizePolicy().hasHeightForWidth())
        self.btn_menu.setSizePolicy(sizePolicy)
        self.btn_menu.setMinimumSize(QSize(0, 45))
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei UI"])
        font2.setPointSize(12)
        font2.setBold(False)
        font2.setItalic(False)
        self.btn_menu.setFont(font2)
        self.btn_menu.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_menu.setLayoutDirection(Qt.LeftToRight)
        self.btn_menu.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.btn_menu)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setMinimumSize(QSize(0, 0))
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font2)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_run = QPushButton(self.topMenu)
        self.btn_run.setObjectName(u"btn_run")
        sizePolicy.setHeightForWidth(self.btn_run.sizePolicy().hasHeightForWidth())
        self.btn_run.setSizePolicy(sizePolicy)
        self.btn_run.setMinimumSize(QSize(0, 45))
        self.btn_run.setFont(font2)
        self.btn_run.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_run.setLayoutDirection(Qt.LeftToRight)
        self.btn_run.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-settings.png);")

        self.verticalLayout_8.addWidget(self.btn_run)

        self.btn_result = QPushButton(self.topMenu)
        self.btn_result.setObjectName(u"btn_result")
        sizePolicy.setHeightForWidth(self.btn_result.sizePolicy().hasHeightForWidth())
        self.btn_result.setSizePolicy(sizePolicy)
        self.btn_result.setMinimumSize(QSize(0, 45))
        self.btn_result.setFont(font2)
        self.btn_result.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_result.setLayoutDirection(Qt.LeftToRight)
        self.btn_result.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-data-transfer-down.png);")

        self.verticalLayout_8.addWidget(self.btn_result)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.btn_setting = QPushButton(self.bottomMenu)
        self.btn_setting.setObjectName(u"btn_setting")
        sizePolicy.setHeightForWidth(self.btn_setting.sizePolicy().hasHeightForWidth())
        self.btn_setting.setSizePolicy(sizePolicy)
        self.btn_setting.setMinimumSize(QSize(0, 45))
        self.btn_setting.setFont(font2)
        self.btn_setting.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_setting.setLayoutDirection(Qt.LeftToRight)
        self.btn_setting.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_9.addWidget(self.btn_setting)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_insert = QFrame(self.extraContent)
        self.frame_insert.setObjectName(u"frame_insert")
        self.frame_insert.setMinimumSize(QSize(0, 100))
        self.frame_insert.setStyleSheet(u"")
        self.frame_insert.setFrameShape(QFrame.StyledPanel)
        self.frame_insert.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_insert)
        self.verticalLayout_21.setSpacing(6)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(8, 0, 0, 0)
        self.frame_11 = QFrame(self.frame_insert)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 100))
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_11)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_11)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 0, 0)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(95, 0))
        font3 = QFont()
        font3.setFamilies([u"Microsoft YaHei UI"])
        font3.setPointSize(12)
        font3.setBold(True)
        font3.setItalic(False)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"font: 700 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_10.addWidget(self.label_4)


        self.verticalLayout_7.addWidget(self.frame_2, 0, Qt.AlignLeft)

        self.frame = QFrame(self.frame_11)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.line_edit_cookie = QLineEdit(self.frame)
        self.line_edit_cookie.setObjectName(u"line_edit_cookie")
        self.line_edit_cookie.setMinimumSize(QSize(260, 40))
        self.line_edit_cookie.setMaximumSize(QSize(16777215, 16777215))
        self.line_edit_cookie.setCursor(QCursor(Qt.IBeamCursor))
        self.line_edit_cookie.setStyleSheet(u"font:  600 11pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_6.addWidget(self.line_edit_cookie)


        self.verticalLayout_7.addWidget(self.frame)


        self.verticalLayout_21.addWidget(self.frame_11)

        self.frame_3 = QFrame(self.frame_insert)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"\n"
"QPushButton{	\n"
"	background-color: rgb(40, 50, 80);\n"
"	font: 550 22px\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(98, 114, 164);\n"
"}\n"
"\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"};\n"
"\n"
"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_3)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.btn_check_cookie = QPushButton(self.frame_3)
        self.btn_check_cookie.setObjectName(u"btn_check_cookie")
        sizePolicy.setHeightForWidth(self.btn_check_cookie.sizePolicy().hasHeightForWidth())
        self.btn_check_cookie.setSizePolicy(sizePolicy)
        self.btn_check_cookie.setMinimumSize(QSize(0, 40))
        self.btn_check_cookie.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_check_cookie.setLayoutDirection(Qt.LeftToRight)
        self.btn_check_cookie.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_check_cookie.setIcon(icon1)

        self.verticalLayout_16.addWidget(self.btn_check_cookie, 0, Qt.AlignHCenter)


        self.verticalLayout_21.addWidget(self.frame_3)


        self.verticalLayout_12.addWidget(self.frame_insert)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.viewport().setProperty("cursor", QCursor(Qt.OpenHandCursor))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.titleRightInfo.setFont(font4)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        font5.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font5)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.pagesContainer)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(6, 3, -1, -1)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMaximumSize(QSize(16777215, 16777215))
        self.stackedWidget.setStyleSheet(u"\n"
"\n"
"QComboBox{\n"
"	font: 18pt \"Microsoft YaHei UI\";\n"
"}\n"
"\n"
"QLabel { \n"
"	font:  22px \"Microsoft YaHei UI\";\n"
"	color: rgb(255, 255, 255); \n"
"	padding-left: 10px; \n"
"	padding-right: 10px; \n"
"	padding-bottom: 2px; \n"
"}\n"
"\n"
"QLabel#label_big_thumb_up, QLabel#label_big_coming, QLabel#label_watch { \n"
"	font:  25pt \"Microsoft YaHei UI\";\n"
"	color: rgb(255, 255, 255); \n"
"	padding-left: 10px; \n"
"	padding-right: 10px; \n"
"	padding-bottom: 2px; \n"
"}\n"
"\n"
"\n"
"QPushButton{	\n"
"	background-color: rgb(40, 50, 80);\n"
"	/*background-color:transparent;*/\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border-left: 1px solid transparent;\n"
"	text-align: left;\n"
"	padding-left: 1px;\n"
"	font: 550 22px \"Microsoft YaHei UI\";\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(98, 114, 164);\n"
"}\n"
"\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"};\n"
"\n"
"\n"
"\n"
"\n"
"backgr"
                        "ound: transparent;\n"
"\n"
"\n"
"")
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setStyleSheet(u"\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"background-image: url(:/images/images/images/TikTokDownloader.png);")
        self.stackedWidget.addWidget(self.page_home)
        self.page_run = QWidget()
        self.page_run.setObjectName(u"page_run")
        self.horizontalLayout_8 = QHBoxLayout(self.page_run)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_run_content = QFrame(self.page_run)
        self.frame_run_content.setObjectName(u"frame_run_content")
        self.frame_run_content.setFrameShape(QFrame.StyledPanel)
        self.frame_run_content.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_run_content)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_4 = QFrame(self.frame_run_content)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_4)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_9 = QFrame(self.frame_4)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setStyleSheet(u"font: 700 18pt \"Microsoft YaHei UI\";\n"
"color: rgb(85, 255, 255);")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_9)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"font: 700 14pt \"Microsoft YaHei UI\";")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.btn_run_local = QPushButton(self.frame_10)
        self.btn_run_local.setObjectName(u"btn_run_local")
        self.btn_run_local.setMinimumSize(QSize(0, 40))
        self.btn_run_local.setMaximumSize(QSize(110, 16777215))
        self.btn_run_local.setCursor(QCursor(Qt.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/cil-location-pin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_run_local.setIcon(icon4)

        self.horizontalLayout_12.addWidget(self.btn_run_local)

        self.btn_run_api = QPushButton(self.frame_10)
        self.btn_run_api.setObjectName(u"btn_run_api")
        self.btn_run_api.setMinimumSize(QSize(0, 40))
        self.btn_run_api.setMaximumSize(QSize(160, 16777215))
        self.btn_run_api.setCursor(QCursor(Qt.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/cil-cloudy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_run_api.setIcon(icon5)

        self.horizontalLayout_12.addWidget(self.btn_run_api)

        self.btn_run_web_ui = QPushButton(self.frame_10)
        self.btn_run_web_ui.setObjectName(u"btn_run_web_ui")
        self.btn_run_web_ui.setMinimumSize(QSize(0, 40))
        self.btn_run_web_ui.setMaximumSize(QSize(150, 16777215))
        self.btn_run_web_ui.setCursor(QCursor(Qt.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/icons/cil-cloud-upload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_run_web_ui.setIcon(icon6)

        self.horizontalLayout_12.addWidget(self.btn_run_web_ui)

        self.btn_run_server_deploy = QPushButton(self.frame_10)
        self.btn_run_server_deploy.setObjectName(u"btn_run_server_deploy")
        self.btn_run_server_deploy.setMinimumSize(QSize(0, 40))
        self.btn_run_server_deploy.setMaximumSize(QSize(125, 16777215))
        self.btn_run_server_deploy.setCursor(QCursor(Qt.PointingHandCursor))
        icon7 = QIcon()
        icon7.addFile(u":/icons/images/icons/cil-terminal.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_run_server_deploy.setIcon(icon7)

        self.horizontalLayout_12.addWidget(self.btn_run_server_deploy)


        self.gridLayout_2.addWidget(self.frame_10, 1, 0, 1, 1)


        self.verticalLayout_14.addWidget(self.frame_9)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_6 = QFrame(self.frame_run_content)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_6)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, -1)
        self.frame_13 = QFrame(self.frame_6)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setStyleSheet(u"font: 700 18pt \"Microsoft YaHei UI\";\n"
"color: rgb(85, 255, 255);")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_13)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_13)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.frame_12 = QFrame(self.frame_13)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setStyleSheet(u"font: 700 14pt \"Microsoft YaHei UI\";")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.frame_12)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_14)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.btn_paste_set_cookie = QPushButton(self.frame_14)
        self.btn_paste_set_cookie.setObjectName(u"btn_paste_set_cookie")
        self.btn_paste_set_cookie.setMinimumSize(QSize(0, 40))
        self.btn_paste_set_cookie.setCursor(QCursor(Qt.PointingHandCursor))
        icon8 = QIcon()
        icon8.addFile(u":/icons/images/icons/cil-pencil.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_paste_set_cookie.setIcon(icon8)

        self.gridLayout_4.addWidget(self.btn_paste_set_cookie, 0, 0, 1, 1)


        self.horizontalLayout_13.addWidget(self.frame_14, 0, Qt.AlignHCenter)

        self.frame_15 = QFrame(self.frame_12)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_15)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.btn_scan_set_cookie = QPushButton(self.frame_15)
        self.btn_scan_set_cookie.setObjectName(u"btn_scan_set_cookie")
        self.btn_scan_set_cookie.setMinimumSize(QSize(0, 40))
        self.btn_scan_set_cookie.setCursor(QCursor(Qt.PointingHandCursor))
        icon9 = QIcon()
        icon9.addFile(u":/icons/images/icons/cil-camera.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_scan_set_cookie.setIcon(icon9)

        self.gridLayout_5.addWidget(self.btn_scan_set_cookie, 0, 0, 1, 1)


        self.horizontalLayout_13.addWidget(self.frame_15, 0, Qt.AlignHCenter)


        self.gridLayout_3.addWidget(self.frame_12, 1, 0, 1, 1)


        self.verticalLayout_13.addWidget(self.frame_13)


        self.verticalLayout.addWidget(self.frame_6)

        self.frame_5 = QFrame(self.frame_run_content)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_5)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setStyleSheet(u"font: 700 18pt \"Microsoft YaHei UI\";\n"
"color: rgb(85, 255, 255);")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_7)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_7)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.verticalLayout_11.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.frame_5)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setCursor(QCursor(Qt.PointingHandCursor))
        self.frame_8.setStyleSheet(u"font: 700 14pt \"Microsoft YaHei UI\";")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.check_box_enable_check_update = QCheckBox(self.frame_8)
        self.check_box_enable_check_update.setObjectName(u"check_box_enable_check_update")

        self.horizontalLayout_7.addWidget(self.check_box_enable_check_update, 0, Qt.AlignHCenter)

        self.check_box_enable_download_record = QCheckBox(self.frame_8)
        self.check_box_enable_download_record.setObjectName(u"check_box_enable_download_record")

        self.horizontalLayout_7.addWidget(self.check_box_enable_download_record, 0, Qt.AlignHCenter)

        self.check_box_enable_log = QCheckBox(self.frame_8)
        self.check_box_enable_log.setObjectName(u"check_box_enable_log")

        self.horizontalLayout_7.addWidget(self.check_box_enable_log, 0, Qt.AlignHCenter)


        self.verticalLayout_11.addWidget(self.frame_8, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.frame_5)


        self.horizontalLayout_8.addWidget(self.frame_run_content)

        self.stackedWidget.addWidget(self.page_run)
        self.page_result = QWidget()
        self.page_result.setObjectName(u"page_result")
        self.horizontalLayout_9 = QHBoxLayout(self.page_result)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_result_content = QFrame(self.page_result)
        self.frame_result_content.setObjectName(u"frame_result_content")
        self.frame_result_content.setFrameShape(QFrame.StyledPanel)
        self.frame_result_content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_result_content)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_16 = QFrame(self.frame_result_content)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 0))
        self.frame_16.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_16)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_19 = QFrame(self.frame_16)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMaximumSize(QSize(16777215, 45))
        self.frame_19.setStyleSheet(u"font: 700 18pt \"Microsoft YaHei UI\";\n"
"color: rgb(85, 255, 255);")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_19)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_19)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 45))
        self.label_5.setMaximumSize(QSize(16777215, 45))

        self.gridLayout_6.addWidget(self.label_5, 0, 0, 1, 1, Qt.AlignLeft)


        self.verticalLayout_15.addWidget(self.frame_19, 0, Qt.AlignLeft)

        self.frame_18 = QFrame(self.frame_16)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setCursor(QCursor(Qt.PointingHandCursor))
        self.frame_18.setStyleSheet(u"font: 700 13pt \"Microsoft YaHei UI\";")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_18)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.radio_btn_1 = QRadioButton(self.frame_18)
        self.radio_btn_1.setObjectName(u"radio_btn_1")

        self.verticalLayout_17.addWidget(self.radio_btn_1)

        self.radio_btn_2 = QRadioButton(self.frame_18)
        self.radio_btn_2.setObjectName(u"radio_btn_2")

        self.verticalLayout_17.addWidget(self.radio_btn_2)

        self.radio_btn_3 = QRadioButton(self.frame_18)
        self.radio_btn_3.setObjectName(u"radio_btn_3")

        self.verticalLayout_17.addWidget(self.radio_btn_3)

        self.radio_btn_4 = QRadioButton(self.frame_18)
        self.radio_btn_4.setObjectName(u"radio_btn_4")

        self.verticalLayout_17.addWidget(self.radio_btn_4)

        self.radio_btn_5 = QRadioButton(self.frame_18)
        self.radio_btn_5.setObjectName(u"radio_btn_5")

        self.verticalLayout_17.addWidget(self.radio_btn_5)

        self.radio_btn_6 = QRadioButton(self.frame_18)
        self.radio_btn_6.setObjectName(u"radio_btn_6")

        self.verticalLayout_17.addWidget(self.radio_btn_6)

        self.radio_btn_7 = QRadioButton(self.frame_18)
        self.radio_btn_7.setObjectName(u"radio_btn_7")

        self.verticalLayout_17.addWidget(self.radio_btn_7)

        self.radio_btn_8 = QRadioButton(self.frame_18)
        self.radio_btn_8.setObjectName(u"radio_btn_8")

        self.verticalLayout_17.addWidget(self.radio_btn_8)

        self.radio_btn_9 = QRadioButton(self.frame_18)
        self.radio_btn_9.setObjectName(u"radio_btn_9")

        self.verticalLayout_17.addWidget(self.radio_btn_9)

        self.radio_btn_10 = QRadioButton(self.frame_18)
        self.radio_btn_10.setObjectName(u"radio_btn_10")

        self.verticalLayout_17.addWidget(self.radio_btn_10)


        self.verticalLayout_15.addWidget(self.frame_18)


        self.horizontalLayout_11.addWidget(self.frame_16)

        self.frame_17 = QFrame(self.frame_result_content)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_17)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_input_label = QFrame(self.frame_17)
        self.frame_input_label.setObjectName(u"frame_input_label")
        self.frame_input_label.setMaximumSize(QSize(16777215, 45))
        self.frame_input_label.setStyleSheet(u"font: 700 18pt \"Microsoft YaHei UI\";\n"
"color: rgb(85, 255, 255);")
        self.frame_input_label.setFrameShape(QFrame.StyledPanel)
        self.frame_input_label.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_input_label)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_input_label)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 45))
        self.label_6.setMaximumSize(QSize(16777215, 45))

        self.gridLayout_7.addWidget(self.label_6, 0, 0, 1, 1, Qt.AlignLeft)


        self.verticalLayout_18.addWidget(self.frame_input_label)

        self.frame_input = QFrame(self.frame_17)
        self.frame_input.setObjectName(u"frame_input")
        self.frame_input.setFrameShape(QFrame.StyledPanel)
        self.frame_input.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_input)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_21 = QFrame(self.frame_input)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_21)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(18, 0, 0, 0)
        self.frame_27 = QFrame(self.frame_21)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMaximumSize(QSize(16777215, 16777215))
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 5)
        self.radio_btn_recommend = QRadioButton(self.frame_27)
        self.radio_btn_recommend.setObjectName(u"radio_btn_recommend")
        self.radio_btn_recommend.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_btn_recommend.setStyleSheet(u"font: 700 14pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_14.addWidget(self.radio_btn_recommend)


        self.verticalLayout_19.addWidget(self.frame_27)

        self.frame_26 = QFrame(self.frame_21)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.radio_btn_manual = QRadioButton(self.frame_26)
        self.radio_btn_manual.setObjectName(u"radio_btn_manual")
        self.radio_btn_manual.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_btn_manual.setStyleSheet(u"font: 700 14pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_17.addWidget(self.radio_btn_manual)

        self.label_manual = QLabel(self.frame_26)
        self.label_manual.setObjectName(u"label_manual")
        self.label_manual.setStyleSheet(u"font: 700 14pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_17.addWidget(self.label_manual)

        self.line_edit_url = QLineEdit(self.frame_26)
        self.line_edit_url.setObjectName(u"line_edit_url")
        self.line_edit_url.setMinimumSize(QSize(260, 40))
        self.line_edit_url.setMaximumSize(QSize(16777215, 16777215))
        self.line_edit_url.setCursor(QCursor(Qt.IBeamCursor))
        self.line_edit_url.setStyleSheet(u"font:  600 11pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_17.addWidget(self.line_edit_url)


        self.verticalLayout_19.addWidget(self.frame_26)


        self.horizontalLayout_15.addWidget(self.frame_21)

        self.frame_24 = QFrame(self.frame_input)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_24)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(9, 0, 9, 0)
        self.btn_download = QPushButton(self.frame_24)
        self.btn_download.setObjectName(u"btn_download")
        self.btn_download.setMinimumSize(QSize(0, 40))
        self.btn_download.setCursor(QCursor(Qt.PointingHandCursor))
        icon10 = QIcon()
        icon10.addFile(u":/icons/images/icons/cil-media-play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_download.setIcon(icon10)

        self.gridLayout_8.addWidget(self.btn_download, 0, 0, 1, 1)


        self.horizontalLayout_15.addWidget(self.frame_24)


        self.verticalLayout_18.addWidget(self.frame_input)

        self.frame_23 = QFrame(self.frame_17)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_23)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.text_edit_run_log = QTextEdit(self.frame_23)
        self.text_edit_run_log.setObjectName(u"text_edit_run_log")
        self.text_edit_run_log.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.text_edit_run_log.setStyleSheet(u"\n"
"font: 13pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(33, 37, 43);")
        self.text_edit_run_log.setTabChangesFocus(True)
        self.text_edit_run_log.setReadOnly(True)

        self.gridLayout_9.addWidget(self.text_edit_run_log, 0, 0, 1, 1)


        self.verticalLayout_18.addWidget(self.frame_23)


        self.horizontalLayout_11.addWidget(self.frame_17)


        self.horizontalLayout_9.addWidget(self.frame_result_content)

        self.stackedWidget.addWidget(self.page_result)

        self.horizontalLayout_20.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font6 = QFont()
        font6.setFamilies([u"Segoe UI"])
        font6.setBold(False)
        font6.setItalic(False)
        self.creditsLabel.setFont(font6)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Modern Nice GUI", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"TikTok\u5c0f\u5de5\u5177", None))
        self.btn_menu.setText(QCoreApplication.translate("MainWindow", u"\u9690\u85cf", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u76ee\u5f55", None))
        self.btn_run.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u754c\u9762", None))
        self.btn_result.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u754c\u9762", None))
        self.btn_setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u680f", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Cookie \u8f93\u5165\u6846", None))
        self.line_edit_cookie.setText("")
        self.line_edit_cookie.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u5728\u6b64\u7c98\u8d34 Cookie", None))
        self.btn_check_cookie.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5Cookie\u8fde\u63a5", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:e"
                        "mpty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-weight:600; color:#ff79c6;\">PyDracula</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt; color:#ffffff;\">\u4f7f\u7528Python\u548cPyside6\u521b\u5efa\u7684\u4e00\u4e2a\u5e94\u7528\u7a0b\u5e8f(\u652f\u6301pyqt), \u5e03\u5c40\u57fa\u4e8ehttps://github.com/Wanderson-Magalhaes\u5f00\u6e90\u7684\u9879\u76ee\u3002</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt; color:#ffffff;\">MIT License</s"
                        "pan></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt; color:#bd93f9;\">Created by: frica01</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-weight:600; color:#ff79c6;\">\u5982\u4f55\u4f7f\u7528</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt; color:#ffffff;\">\u770b\u8bf4\u660e\u6587\u6863\uff08\u53cc\u51fb\u6253\u5f00\uff09</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-weight:600; color:#ff79c6;\">\u9047"
                        "\u5230\u95ee\u9898</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt; color:#ffffff;\">\u63d0\u4ea4issues</span></p></body></html>", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"TikTok\u89c6\u9891\u5c0f\u5de5\u5177 - \u57fa\u4e8ePython\u5f00\u53d1\u7684\u5c0f\u5de5\u5177.", None))
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u6a21\u5f0f", None))
        self.btn_run_local.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5730\u8fd0\u884c", None))
        self.btn_run_api.setText(QCoreApplication.translate("MainWindow", u"Web API \u63a5\u53e3", None))
        self.btn_run_web_ui.setText(QCoreApplication.translate("MainWindow", u"Web UI \u4ea4\u4e92", None))
        self.btn_run_server_deploy.setText(QCoreApplication.translate("MainWindow", u"\u670d\u52a1\u5668\u90e8\u7f72", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e Cookie \u65b9\u5f0f", None))
        self.btn_paste_set_cookie.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236\u7c98\u8d34\u5199\u5165", None))
        self.btn_scan_set_cookie.setText(QCoreApplication.translate("MainWindow", u"\u626b\u7801\u767b\u5f55\u5199\u5165", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5176\u5b83\u8bbe\u7f6e", None))
        self.check_box_enable_check_update.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u81ea\u52a8\u68c0\u67e5\u66f4\u65b0", None))
        self.check_box_enable_download_record.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u4f5c\u54c1\u4e0b\u8f7d\u8bb0\u5f55", None))
        self.check_box_enable_log.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u8fd0\u884c\u65e5\u5fd7\u8bb0\u5f55", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u91c7\u96c6\u529f\u80fd", None))
        self.radio_btn_1.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4e0b\u8f7d\u8d26\u53f7\u4f5c\u54c1(TikTok)", None))
        self.radio_btn_2.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4e0b\u8f7d\u8d26\u53f7\u4f5c\u54c1(\u6296\u97f3)", None))
        self.radio_btn_3.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4e0b\u8f7d\u94fe\u63a5\u4f5c\u54c1(\u901a\u7528)", None))
        self.radio_btn_4.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u76f4\u64ad\u63a8\u6d41\u5730\u5740(\u6296\u97f3)", None))
        self.radio_btn_5.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u96c6\u4f5c\u54c1\u8bc4\u8bba\u6570\u636e(\u6296\u97f3)", None))
        self.radio_btn_6.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4e0b\u8f7d\u5408\u96c6\u4f5c\u54c1(\u6296\u97f3)", None))
        self.radio_btn_7.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u91c7\u96c6\u8d26\u53f7\u6570\u636e(\u6296\u97f3)", None))
        self.radio_btn_8.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u96c6\u641c\u7d22\u7ed3\u679c\u6570\u636e(\u6296\u97f3)", None))
        self.radio_btn_9.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u96c6\u6296\u97f3\u70ed\u699c\u6570\u636e(\u6296\u97f3)", None))
        self.radio_btn_10.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4e0b\u8f7d\u6536\u85cf\u4f5c\u54c1(\u6296\u97f3)", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6846", None))
        self.radio_btn_recommend.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528 accounts_urls (\u63a8\u8350)", None))
        self.radio_btn_manual.setText(QCoreApplication.translate("MainWindow", u"\u624b\u52a8\u8f93\u5165\uff1a", None))
        self.label_manual.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5185\u5bb9\uff1a", None))
        self.line_edit_url.setText(QCoreApplication.translate("MainWindow", u"456456", None))
        self.line_edit_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u4f5c\u54c1\u94fe\u63a5", None))
        self.btn_download.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u91c7\u96c6", None))
        self.text_edit_run_log.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: \u5c0f\u83dc.", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

