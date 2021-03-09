# coding:utf-8

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QLabel
import sys
import qtawesome
import csv
import requests
import re
from PIL import Image, ImageTk
import tkinter as tk
from PIL.ImageTk import PhotoImage

# 预测包导入
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from pandas import read_csv
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARMA
# 时间增加
from datetime import datetime


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 在左侧菜单模块中，继续使用网格对部件进行布局。
        # 在左侧菜单的布局中添加按钮部件QPushButton()左侧菜单的按钮、菜单列提示和整个窗口的最小化和关闭按钮。
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(self.closeButtonClick)  # 绑定按键点击事件

        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(self.minButtonClick)  # 绑定按键点击事件minButtonClick

        self.left_label_1 = QtWidgets.QPushButton("价格预测")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("销量预测")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        # 此处功能是调用prediction显示图像
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.music', color='white'), "预测5个时间点")
        self.left_button_1.clicked.connect(self.showfiveprice)
        self.left_button_1.setObjectName('left_button')

        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color='white'), "预测24个时间点")
        self.left_button_2.clicked.connect(self.show24price)
        self.left_button_2.setObjectName('left_button')

        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='white'), "预测72个时间点")
        self.left_button_3.clicked.connect(self.show72price)
        self.left_button_3.setObjectName('left_button')

        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "预测5个时间点")
        self.left_button_4.clicked.connect(self.showfivenumber)
        self.left_button_4.setObjectName('left_button')

        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "预测24个时间点")
        self.left_button_5.clicked.connect(self.show24number)
        self.left_button_5.setObjectName('left_button')

        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "预测72个时间点")
        self.left_button_6.clicked.connect(self.show72number)
        self.left_button_6.setObjectName('left_button')

        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_7.clicked.connect(self.returnidea)
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.clicked.connect(self.trytoconnect)
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.clicked.connect(self.meetproblem)
        self.left_button_9.setObjectName('left_button')
        self.left_xxx = QtWidgets.QPushButton(" ")
        # 使用qtawesome这个第三方库来实现按钮中的Font Awesome字体图标的显示。然后将创建的按钮添加到左侧部件的网格布局层中：
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)

        # 搜索模块中，有一个文本和一个搜索框，我们通过QLable()部件和QLineEdit()部件来实现，
        # 这两个部件同时包裹在一个网格布局的QWidget()部件，分列第一列和第二列
        # 添加系统标题
        self.title = QtWidgets.QLabel('STEAM游戏价格销量预测系统')
        self.title.setAlignment(QtCore.Qt.AlignCenter);
        self.title.setFont(qtawesome.font('fa', 30))
        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索 ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入想要查询的商品的网页URL，回车进行搜索")
        self.right_bar_widget_search_input.returnPressed.connect(self.pc)  # 回车搜索

        self.right_bar_layout.addWidget(self.title, 0, 0, 1, 8)
        self.right_bar_layout.addWidget(self.search_icon, 1, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 1, 1, 1, 8)

        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)
        # 推荐音乐模块，在推荐音乐模块中，有一个推荐的标题，和一个横向排列的音乐封面列表，在这里：
        #
        # 推荐标题使用QLable()来实现；
        #
        # 音乐封面列表由多个QToolButton()组成，其继续由一个布局为QGridLayout()的QWidget()部件所包含
        self.right_recommend_label = QtWidgets.QLabel("结果查询")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("价格数据")  # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon('./r1.jpg'))  # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(100, 100))  # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.recommend_button_1.clicked.connect(self.image)
        # self.recommend_button_1.clicked.connect(self.show_img)

        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("价格预测")
        self.recommend_button_2.setIcon(QtGui.QIcon('./r2.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("销量数据")
        self.recommend_button_3.setIcon(QtGui.QIcon('./r3.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_4.setText("销量预测")
        self.recommend_button_4.setIcon(QtGui.QIcon('./r4.jpg'))
        self.recommend_button_4.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_5 = QtWidgets.QToolButton()
        self.recommend_button_5.setText("一键查询")
        self.recommend_button_5.setIcon(QtGui.QIcon('./r5.jpg'))
        self.recommend_button_5.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.right_recommend_layout.addWidget(self.recommend_button_1, 0, 0)
        self.right_recommend_layout.addWidget(self.recommend_button_2, 0, 1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 0, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_5, 0, 4)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)

        # 创建音乐列表模块和音乐歌单模块。音乐列表模块和音乐歌单模块都有一个标题和一个小部件来容纳具体的内容。
        #
        # 其中标题我们都使用QLabel()
        # 部件来实现，而音乐列表我们使用网格布局的QWidget()
        # 部件下包裹着数个QPushButton()
        # 按钮部件来实现，音乐歌单列表则使用网格布局的QWidget()
        # 部件下包裹着数个QToolButton()
        # 工具按钮部件来实现。
        # 音乐列表
        # self.right_newsong_lable = QtWidgets.QLabel("最新歌曲")
        # self.right_newsong_lable.setObjectName('right_lable')
        #
        # self.right_playlist_lable = QtWidgets.QLabel("热门歌单")
        # self.right_playlist_lable.setObjectName('right_lable')
        #
        # self.right_newsong_widget = QtWidgets.QWidget() # 最新歌曲部件
        # self.right_newsong_layout = QtWidgets.QGridLayout() # 最新歌曲部件网格布局
        # self.right_newsong_widget.setLayout(self.right_newsong_layout)
        #
        # self.newsong_button_1 = QtWidgets.QPushButton("夜机   陈慧娴   永远的朋友   03::29")
        # self.newsong_button_2 = QtWidgets.QPushButton("夜机   陈慧娴   永远的朋友   03::29")
        # self.newsong_button_3 = QtWidgets.QPushButton("夜机   陈慧娴   永远的朋友   03::29")
        # self.newsong_button_4 = QtWidgets.QPushButton("夜机   陈慧娴   永远的朋友   03::29")
        # self.newsong_button_5 = QtWidgets.QPushButton("夜机   陈慧娴   永远的朋友   03::29")
        # self.newsong_button_6 = QtWidgets.QPushButton("夜机   陈慧娴   永远的朋友   03::29")
        # self.right_newsong_layout.addWidget(self.newsong_button_1,0,1,)
        # self.right_newsong_layout.addWidget(self.newsong_button_2, 1, 1, )
        # self.right_newsong_layout.addWidget(self.newsong_button_3, 2, 1, )
        # self.right_newsong_layout.addWidget(self.newsong_button_4, 3, 1, )
        # self.right_newsong_layout.addWidget(self.newsong_button_5, 4, 1, )
        # self.right_newsong_layout.addWidget(self.newsong_button_6, 5, 1, )
        # # 音乐歌单
        # self.right_playlist_widget = QtWidgets.QWidget()  # 播放歌单部件
        # self.right_playlist_layout = QtWidgets.QGridLayout()  # 播放歌单网格布局
        # self.right_playlist_widget.setLayout(self.right_playlist_layout)
        #
        # self.playlist_button_1 = QtWidgets.QToolButton()
        # self.playlist_button_1.setText("无法释怀的整天循环音乐…")
        # self.playlist_button_1.setIcon(QtGui.QIcon('./p1.jpg'))
        # self.playlist_button_1.setIconSize(QtCore.QSize(100, 100))
        # self.playlist_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #
        # self.playlist_button_2 = QtWidgets.QToolButton()
        # self.playlist_button_2.setText("不需要歌词,也可以打动你的心")
        # self.playlist_button_2.setIcon(QtGui.QIcon('./p2.jpg'))
        # self.playlist_button_2.setIconSize(QtCore.QSize(100, 100))
        # self.playlist_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #
        # self.playlist_button_3 = QtWidgets.QToolButton()
        # self.playlist_button_3.setText("那些你熟悉又不知道名字…")
        # self.playlist_button_3.setIcon(QtGui.QIcon('./p3.jpg'))
        # self.playlist_button_3.setIconSize(QtCore.QSize(100, 100))
        # self.playlist_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #
        # self.playlist_button_4 = QtWidgets.QToolButton()
        # self.playlist_button_4.setText("那些只听前奏就中毒的英文歌")
        # self.playlist_button_4.setIcon(QtGui.QIcon('./p4.jpg'))
        # self.playlist_button_4.setIconSize(QtCore.QSize(100, 100))
        # self.playlist_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #
        # self.right_playlist_layout.addWidget(self.playlist_button_1, 0, 0)
        # self.right_playlist_layout.addWidget(self.playlist_button_2, 0, 1)
        # self.right_playlist_layout.addWidget(self.playlist_button_3, 1, 0)
        # self.right_playlist_layout.addWidget(self.playlist_button_4, 1, 1)
        # # 添加到右侧布局层中
        # self.right_layout.addWidget(self.right_newsong_lable, 4, 0, 1, 5)
        # self.right_layout.addWidget(self.right_playlist_lable, 4, 5, 1, 4)
        # self.right_layout.addWidget(self.right_newsong_widget, 5, 0, 1, 5)
        # self.right_layout.addWidget(self.right_playlist_widget, 5, 5, 1, 4)
        #
        #
        # # 音乐播放进度条我们使用QProgressBar()进度条部件来实现，
        # # 音乐播放控制按钮组则使用一个QWidget()部件下包裹着三个QPushButton()按钮部件来实现。
        # self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        # self.right_process_bar.setValue(49)
        # self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
        # self.right_process_bar.setTextVisible(False)  # 不显示进度条文字
        #
        # self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        # self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        # self.right_playconsole_widget.setLayout(self.right_playconsole_layout)
        #
        # self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#F76677'), "")
        # self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#F76677'), "")
        # self.console_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.pause', color='#F76677', font=18), "")
        # self.console_button_3.setIconSize(QtCore.QSize(30, 30))
        #
        # self.right_playconsole_layout.addWidget(self.console_button_1, 0, 0)
        # self.right_playconsole_layout.addWidget(self.console_button_2, 0, 2)
        # self.right_playconsole_layout.addWidget(self.console_button_3, 0, 1)
        # self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示
        #
        # self.right_layout.addWidget(self.right_process_bar, 9, 0, 1, 9)
        # self.right_layout.addWidget(self.right_playconsole_widget, 10, 0, 1, 9)

        # QSS部件美化
        # 左侧的最顶端是三个窗口控制按钮，我们需要将其设置为小圆点的形式。首先，我们使用QPushButton()
        # 的setFixedSize()
        # 方法，设置按钮的大小：

        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        # 通过setStyleSheet()方法，设置按钮部件的QSS样式，在这里，左侧按钮默认为淡绿色，鼠标悬浮时为深绿色；
        # 中间按钮默认为淡黄色，鼠标悬浮时为深黄色；右侧按钮默认为浅红色，鼠标悬浮时为红色。所以它们的QSS样式设置如下所示：

        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        # 左侧的部件背景是灰色的，所以我们需要将左侧菜单中的按钮和文字颜色设置为白色，并且将按钮的边框去掉，
        # 在left_widget中设置qss样式为：
        self.left_widget.setStyleSheet('''
          QPushButton{border:none;color:white;}
          QPushButton#left_label{
            border:none;
            border-bottom:1px solid white;
            font-size:18px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
          }
          QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')

        # 右侧的内容部件进行处理，首先是顶部的搜索框，因为搜索框使用的是QLineEdit()
        # 部件，默认情况下棱角分明很是不好看，我们对其进行圆角处理：
        self.right_bar_widget_search_input.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
            }''')

        # 图形界面是会呈现出无边框的圆角形式，所以右侧的部件的右上角和右下角需要先行处理为圆角的，
        # 同时背景设置为白色。对推荐模块、音乐列表模块和音乐歌单模块的标题我们也需要对其字体进行放大处理，
        self.right_widget.setStyleSheet('''
          QWidget#right_widget{
            color:#232C51;
            background:white;
            border-top:1px solid darkGray;
            border-bottom:1px solid darkGray;
            border-right:1px solid darkGray;
            border-top-right-radius:10px;
            border-bottom-right-radius:10px;
          }
          QLabel#right_lable{
            border:none;
            font-size:16px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
          }
        ''')

        # 推荐模块和歌单模块中使用的都是QToolButton()部件
        self.right_recommend_widget.setStyleSheet(
            '''
              QToolButton{border:none;}
              QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')
        # self.right_playlist_widget.setStyleSheet(
        #     '''
        #       QToolButton{border:none;}
        #       QToolButton:hover{border-bottom:2px solid #F76677;}
        #     ''')

        # 音乐列表使用的是QPushButton()按钮部件，我们需要对其去除边框，修改字体和颜色等，所以其样式为
        # self.right_newsong_widget.setStyleSheet('''
        #   QPushButton{
        #     border:none;
        #     color:gray;
        #     font-size:12px;
        #     height:40px;
        #     padding-left:5px;
        #     padding-right:10px;
        #     text-align:left;
        #   }
        #   QPushButton:hover{
        #     color:black;
        #     border:1px solid #F3F3F5;
        #     border-radius:10px;
        #     background:LightGray;
        #   }
        # ''')

        # 播放进度条和播放控制按钮组了，我们需要将播放进度条的样色设置为浅红色，然后去除播放控制按钮的边框，所以其QSS样式为：
        # self.right_process_bar.setStyleSheet('''
        #   QProgressBar::chunk {
        #     background-color: #F76677;
        #   }
        # ''')
        #
        # self.right_playconsole_widget.setStyleSheet('''
        #   QPushButton{
        #     border:none;
        #   }
        # ''')

        # 透明的窗口背景会让图形界面有现代感和时尚感，我们来讲图形界面的窗口背景设为透明：
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # 通过窗口的setWindowFlag()属性我们可以设置窗口的状态从而把边框给隐藏了
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # 为了避免隐藏窗口边框后，左侧部件没有背景颜色和边框显示，我们再对左侧部件添加QSS属性：
        self.main_widget.setStyleSheet('''
        QWidget#left_widget{
        background:gray;
        border-top:1px solid white;
        border-bottom:1px solid white;
        border-left:1px solid white;
        border-top-left-radius:10px;
        border-bottom-left-radius:10px;
        }
        ''')
        # 图形界面中左侧部件和右侧部件中有一条缝隙，我们通过设置布局内部件的间隙来把那条缝隙去除掉：
        self.main_layout.setSpacing(0)

    def closeButtonClick(self):

        # sender 是发送信号的对象，此处发送信号的对象是button1按钮

        sender = self.sender()

        # print(sender.text() + ' 被按下了')

        qApp = QApplication.instance()

        qApp.quit()  # 关闭窗口

    def minButtonClick(self):
        # qApp = QApplication.instance()
        #
        # qApp.showMinimized()
        self.showMinimized()

    # def mousePressEvent(self, event):  # 鼠标拖拽窗口移动
    #     if event.button() == QtCore.Qt.LeftButton:
    #         self.m_flag = True
    #         self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
    #         event.accept()
    #         self.setCursor(QtCore.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标
    #
    # def mouseMoveEvent(self, QMouseEvent):  # 鼠标拖拽窗口移动
    #     if QtCore.Qt.LeftButton and self.m_flag:
    #         self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
    #         QMouseEvent.accept()
    #
    # def mouseReleaseEvent(self, QMouseEvent):  # 鼠标拖拽窗口移动
    #     self.m_flag = False
    #     self.setCursor(QtCore.QCursor(QtCore.Qt.ArrowCursor))

    def pc(self):
        # print(self.right_bar_widget_search_input.text())
        url = self.right_bar_widget_search_input.text()
        # headers = {'user-agent': 'user-agent'}
        # file = csv.writer(open('猫眼电影.csv', 'w'))
        # for i in range(0, 100, 10):
        #     new_url = url + '?offset=%d' % i
        #     print('在解析网址中：', new_url)
        #     req = requests.get(url=new_url, headers=headers)
        #     html = req.text
        #     doc = pq(html)
        #     items = doc('dl.board-wrapper dd').items()
        #     for each in items:
        #         title = each.find('a').text()
        #         # 添加数据
        #         text.insert(END, title)
        #         # 文本框向下滚动
        #         text.see(END)
        #         # 更新
        #         text.update()
        # print('已抓取完毕')
        # url = 'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20%28Field-Tested%29'
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
        }

        response = requests.get(url, headers=headers)

        result = re.search('<script.*?line1=(.*?);.*?</script>', response.text, re.S)
        name = re.findall('<span class="market_listing_item_name" style="">(.*?)</span>', response.text)
        print(name[0])

        txtpath = r'D:/文档/urp/data/' + name[0] + '.txt'
        txtpath = txtpath.replace(' | ', ' ')
        print(txtpath)

        with open(txtpath, 'w', encoding='utf-8') as f:
            f.write(result.group(1))

        file = open(txtpath)
        file_read = file.read()

        table = str.maketrans('', '', ':"+[]')  # 删除字符串中的“ ： + []
        file_translate = file_read.translate(table)

        lst = file_translate.split(',')  # 以逗号为分隔符，将字符串转换为列表

        list_time = []
        list_price = []
        list_num = []
        # 将时间、价格、数量三个信息分别存入三个list
        i = 0
        j = 0
        while i < len(lst):
            list_time.insert(j, lst[i])
            list_price.insert(j, lst[i + 1])
            list_num.insert(j, lst[i + 2])
            i = i + 3
            j = j + 1
        # 创建csv文件，并将数据写入
        csvpath = r'D:/文档/urp/data/' + name[0] + '.csv'
        csvpath = csvpath.replace(' | ', ' ')
        with open(csvpath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['time', 'price', 'number'])
            for i in range(len(list_time)):
                writer.writerow([list_time[i], list_price[i], list_num[i]])

    def image(self):
        QMessageBox.information(self, '信息提示对话框', '前方右拐到达目的地', QMessageBox.Yes | QMessageBox.No)

    def airma_predict_number(self):
        # 借助AIC、BIC统计量自动确定
        def proper_model(data_ts, maxLag):
            init_bic = float("inf")  # 初始值为正无穷
            init_p = 0  # p代表周期、q代表噪音
            init_q = 0
            init_properModel = None
            for p in np.arange(maxLag):
                for q in np.arange(maxLag):
                    model = ARMA(data_ts, order=(p, q))
                    try:
                        result_ARMA = model.fit(disp=-1, method='css')
                    except:
                        continue
                    bic = result_ARMA.bic  # 确定贝叶斯信息量
                    if bic < init_bic:
                        init_p = p
                        init_q = q
                        init_properModel = result_ARMA
                        init_bic = bic
            return init_bic, init_p, init_q, init_properModel

        # 我们常用的是AIC准则，AIC鼓励数据拟合的优良性但是尽量避免出现过度拟合(Overfitting)的情况。所以优先考虑的模型应是AIC值最小的那一个模型。
        # 为了控制计算量，我们限制AR最大阶不超过5，MA最大阶不超过5。 但是这样带来的坏处是可能为局部最优。
        # timeseries是待输入的时间序列，是pandas.Series类型，max_ar、max_ma是p、q值的最大备选值。
        # order.bic_min_order返回以BIC准则确定的阶数，是一个tuple类型

        # 差分序列还原
        def predict_recover(ts):
            ts = np.exp(ts)
            return ts

        # 数据读取
        dateparse1 = lambda dates: datetime.strptime(dates, '%b %d %Y %H %M')
        # %Y/%m/%d %H:%M %b %d %Y %H %M
        series_new = read_csv('AK-47 Redline.csv', parse_dates=[0], index_col=0, usecols=['time', 'number'],
                              engine='python',
                              date_parser=dateparse1, dtype={'number': float})
        # 分割测试集和数据集

        train_data = series_new.values[:1500]
        test_data = series_new.values[1500:series_new.count() + 1]
        # 划分训练集和测试集
        init_bic, init_p, init_q, init_properModel = proper_model(train_data, 5)
        # 确定模型参数

        train_predict = init_properModel.predict()
        RMSE = np.sqrt(mean_squared_error(train_data[init_p:], train_predict))
        print(RMSE)
        # 评价线性回归模型效果的时候，使用RMSE均方根误差
        # plt.title("从商品上架到今天的价格折线图")
        # plt.plot(train_predict, 'r', train_data[init_p:], 'b')
        # plt.savefig("train.jpg")
        # plt.show()

        # AR模型，q=0
        # RSS是残差平方和
        # 循环建模单步预测，效率太低
        train_data = series_new.values[:series_new.count() + 1]
        # test_data = series_new.values[1500:series_new.count() + 1]
        # test_data = test_data.reshape(len(test_data))
        train_data = train_data.reshape(len(train_data))
        history = [x for x in train_data]
        global predictions1 # 保存销量数据
        predictions1 = list()
        # 列表形式构建预测集
        for t in range(72):
            # (len(test_data))
            init_bic, init_p, init_q, init_properModel = proper_model(history, 5)
            output = init_properModel.forecast()
            yhat = output[0]
            predictions1.append(yhat)
            # obs = np.array(test_data)[t]
            # history.append(obs)
            history.append(yhat)
            print('predicted=%f' % (yhat))
        print("预测结束")

        # 销量
        # 五小时预测图
        plt.figure().gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title("Prediction of 5 hours")
        plt.plot(predictions1[0:5], 'r')
        plt.xlabel('time')
        plt.ylabel('number')
        plt.savefig("npredict5.jpg")
        # plt.show()

        # 24小时预测图
        plt.figure().gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title("Prediction of 24 hours")
        plt.plot(predictions1[0:24], 'r')
        plt.xlabel('time')
        plt.ylabel('number')
        plt.savefig("npredict24.jpg")

        # 72小时预测图
        plt.figure().gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title("Prediction of 72 hours")
        plt.plot(predictions1[0:72], 'r')
        plt.xlabel('time')
        plt.ylabel('number')
        plt.savefig("npredict72.jpg")



        # rmse = np.sqrt(mean_squared_error(predictions, test_data[:10]))
        # print(rmse)
        QMessageBox.information(self, '信息提示对话框', '预测已完成可查看', QMessageBox.Yes | QMessageBox.No)

    def airma_predict_price(self): # 预测价格
        # 借助AIC、BIC统计量自动确定
        def proper_model(data_ts, maxLag):
            init_bic = float("inf")  # 初始值为正无穷
            init_p = 0  # p代表周期、q代表噪音
            init_q = 0
            init_properModel = None
            for p in np.arange(maxLag):
                for q in np.arange(maxLag):
                    model = ARMA(data_ts, order=(p, q))
                    try:
                        result_ARMA = model.fit(disp=-1, method='css')
                    except:
                        continue
                    bic = result_ARMA.bic  # 确定贝叶斯信息量
                    if bic < init_bic:
                        init_p = p
                        init_q = q
                        init_properModel = result_ARMA
                        init_bic = bic
            return init_bic, init_p, init_q, init_properModel

        # 我们常用的是AIC准则，AIC鼓励数据拟合的优良性但是尽量避免出现过度拟合(Overfitting)的情况。所以优先考虑的模型应是AIC值最小的那一个模型。
        # 为了控制计算量，我们限制AR最大阶不超过5，MA最大阶不超过5。 但是这样带来的坏处是可能为局部最优。
        # timeseries是待输入的时间序列，是pandas.Series类型，max_ar、max_ma是p、q值的最大备选值。
        # order.bic_min_order返回以BIC准则确定的阶数，是一个tuple类型

        # 差分序列还原
        def predict_recover(ts):
            ts = np.exp(ts)
            return ts

        # 数据读取
        dateparse1 = lambda dates: datetime.strptime(dates, '%b %d %Y %H %M')
        # %Y/%m/%d %H:%M %b %d %Y %H %M
        series_new = read_csv('AK-47 Redline.csv', parse_dates=[0], index_col=0, usecols=['time', 'price'],
                              engine='python',
                              date_parser=dateparse1)
        # 分割测试集和数据集

        train_data = series_new.values[:1500]
        test_data = series_new.values[1500:series_new.count() + 1]
        # 划分训练集和测试集
        init_bic, init_p, init_q, init_properModel = proper_model(train_data, 5)
        # 确定模型参数

        train_predict = init_properModel.predict()
        RMSE = np.sqrt(mean_squared_error(train_data[init_p:], train_predict))
        print(RMSE)
        # 评价线性回归模型效果的时候，使用RMSE均方根误差
        # plt.title("从商品上架到今天的价格折线图")
        # plt.plot(train_predict, 'r', train_data[init_p:], 'b')
        # plt.savefig("train.jpg")
        # plt.show()

        # AR模型，q=0
        # RSS是残差平方和
        # 循环建模单步预测，效率太低
        train_data = series_new.values[:series_new.count() + 1]
        # test_data = series_new.values[1500:series_new.count() + 1]
        # test_data = test_data.reshape(len(test_data))
        train_data = train_data.reshape(len(train_data))
        history = [x for x in train_data]
        global predictions2 # 保存销量数据
        predictions2 = list()
        # 列表形式构建预测集
        for t in range(72):
            # (len(test_data))
            init_bic, init_p, init_q, init_properModel = proper_model(history, 5)
            output = init_properModel.forecast()
            yhat = output[0]
            predictions2.append(yhat)
            # obs = np.array(test_data)[t]
            # history.append(obs)
            history.append(yhat)
            print('predicted=%f' % (yhat))
        print("预测结束")

        # 销量
        # 五小时预测图
        plt.figure().gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title("Prediction of 5 hours")
        plt.plot(predictions2[0:5], 'r')
        plt.xlabel('time')
        plt.ylabel('number')
        plt.savefig("npredict5.jpg")
        # plt.show()

        # 24小时预测图
        plt.figure().gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title("Prediction of 24 hours")
        plt.plot(predictions2[0:24], 'r')
        plt.xlabel('time')
        plt.ylabel('number')
        plt.savefig("npredict24.jpg")

        # 72小时预测图
        plt.figure().gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title("Prediction of 72 hours")
        plt.plot(predictions2[0:72], 'r')
        plt.xlabel('time')
        plt.ylabel('number')
        plt.savefig("npredict72.jpg")



        # rmse = np.sqrt(mean_squared_error(predictions, test_data[:10]))
        # print(rmse)
        QMessageBox.information(self, '信息提示对话框', '预测已完成可查看', QMessageBox.Yes | QMessageBox.No)

    def showfiveprice(self):
        # 调用图片
        pix = QPixmap('ppredict5.jpg')

        lb2 = QLabel(self)
        lb2.setGeometry(0, 250, 500, 210)
        lb2.setPixmap(pix)
        lb2.setScaledContents(True)  # 自适应QLabel大小

    def show24price(self):
        # 调用图片
        pix = QPixmap('ppredict24.jpg')

        lb2 = QLabel(self)
        lb2.setGeometry(0, 250, 500, 210)
        lb2.setPixmap(pix)
        lb2.setScaledContents(True)  # 自适应QLabel大小

    def show72price(self):
        # 调用图片
        pix = QPixmap('ppredict72.jpg')

        lb2 = QLabel(self)
        lb2.setGeometry(0, 250, 500, 210)
        lb2.setPixmap(pix)
        lb2.setScaledContents(True)  # 自适应QLabel大小

    def showfivenumber(self):
        # 调用图片
        pix = QPixmap('npredict5.jpg')

        lb2 = QLabel(self)
        lb2.setGeometry(0, 250, 500, 210)
        lb2.setPixmap(pix)
        lb2.setScaledContents(True)  # 自适应QLabel大小

    def show24number(self):
        # 调用图片
        pix = QPixmap('npredict24.jpg')

        lb2 = QLabel(self)
        lb2.setGeometry(0, 250, 500, 210)
        lb2.setPixmap(pix)
        lb2.setScaledContents(True)  # 自适应QLabel大小

    def show72number(self):
        # 调用图片
        pix = QPixmap('npredict72.jpg')

        lb2 = QLabel(self)
        lb2.setGeometry(0, 250, 500, 210)
        lb2.setPixmap(pix)
        lb2.setScaledContents(True)  # 自适应QLabel大小

    def showtablenumber(self):
        # self.airma_predict()
        global predictions2
        # predictions = list()
        # predictions.append(60)
        print("showtableprice")
        # print(predictions)
        for i in range(72):
            item1 = QTableWidgetItem('第'+str(i)+'个时间点')
            self.right_playlist_lable.setItem(i, 0, item1)
            item2 = QTableWidgetItem(str(predictions2[0][i]))
            self.right_playlist_lable.setItem(i, 1, item2)

    def showtableprice(self):
        # self.airma_predict()
        global predictions1
        # predictions = list()
        # predictions.append(60)
        print("showtableprice")
        # print(predictions)
        for i in range(72):
            item1 = QTableWidgetItem('第'+str(i)+'个时间点')
            self.right_playlist_lable.setItem(i, 0, item1)
            item2 = QTableWidgetItem(str(predictions1[0][i]))
            self.right_playlist_lable.setItem(i, 1, item2)

    def returnidea(self): # 反馈建议
        QMessageBox.information(self, '反馈建议', '联系方式QQ:503075401', QMessageBox.Yes | QMessageBox.No)

    def trytoconnect(self): # 关注我们
        QMessageBox.information(self, '关注我们', '公众号：没有回信', QMessageBox.Yes | QMessageBox.No)

    def meetproblem(self): # 遇到问题
        QMessageBox.information(self, '遇到问题', '可以通过反馈建议联系我们', QMessageBox.Yes | QMessageBox.No)

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
