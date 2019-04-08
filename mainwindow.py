# -*- coding: utf-8 -*-
from ui.wx import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QListWidgetItem,QListWidget,QMessageBox,qApp
from PyQt5.QtCore import QThread,pyqtSignal,Qt,QPropertyAnimation
from PyQt5.QtGui import QColor
import wxpy,win32timezone,datetime
from senddialog import SendDialog
from chatwindow import ChatWindow
from autoreplywindow import AutoReplyWindow
from utility.msg import *

class MainWindow(QMainWindow,Ui_MainWindow):
    wxTriggerSingal = pyqtSignal(bool)   #定义信号关闭QThread中的进程


    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.bot = None
        self.closeButton()
        #主窗体
        self.setFixedSize(self.width(), self.height())   ##固定窗口大小
        self.setWindowTitle('Magic&House SoftWare')

        #副窗体
        self.friendsWindowDict = dict()
        self.autoReplyWindow = AutoReplyWindow(self)

        #显示列表
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setFixedSize(self.listWidget.width(),self.listWidget.height())
        self.listWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.listWidget.setStyleSheet('background-color:white;border-bottom:1px;border-color:grey')


        #定义微信bot线程
        self.wx = WxThread(self)

        # 其他参数
        self.autoReply = False
        self.senderList = list()

        #定义事件和信号
        self.setEvent()



        self.show()

    def setEvent(self):
        #事件
        self.pushButton_5.clicked.connect(self.on_clicked_pushButton_5)  #登录微信按钮
        self.pushButton_4.clicked.connect(self.on_clicked_pushButton_4)  #退出登录
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)  #开启自动回复按钮
        self.listWidget.itemDoubleClicked.connect(self.on_clicked_listWdigetItem)   #列表双击事件
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        #信号
        self.wx.wxSignal.connect(self.listwidget_addItem)
        self.wxTriggerSingal.connect(self.wx.stopEmit)


    def on_clicked_pushButton_5(self):
        """
        微信登录按钮
        :return:
        """
        if (not self.bot) or (not self.bot.is_listening):
            qApp.processEvents()
            self.bot = wxpy.Bot(cache_path='data/mhwx.cache',login_callback=self.loginMessage)
            self.openButton()
            puid_path = 'data/' + self.bot.self.name+'_puid.pkl'
            print(puid_path)
            self.bot.enable_puid(path=puid_path)
            self.wx.start()
    def on_clicked_pushButton_4(self):
        """
        微信登出按钮
        :return:
        """
        if self.bot:
            self.bot.logout()
        self.bot = None
        self.closeButton()
        self.logoutMessage()

    def on_clicked_pushButton_2(self):
        """
        开启自动回复按钮 和切换
        :return:
        """
        if self.pushButton_2.text() == '开启自动回复':
            if self.bot:
                self.autoReply = True
                self.pushButton_2.setText('停止自动回复')

                qApp.processEvents()
        elif self.pushButton_2.text() == '停止自动回复':
            self.pushButton_2.setText('开启自动回复')
            self.autoReply = False


    def on_clicked_pushButton(self):
        self.autoReplyWindow.showNormal()

    def on_clicked_listWdigetItem(self, item):
        """
        聊天信息列表弹出消息框发送消息
        :param item:
        :return:
        """
        index = self.listWidget.row(item)
        sender_puid = self.senderList[index]
        chat = self.friendsWindowDict.get(sender_puid,None)
        if chat:
            chatWindow = chat.get('window')
            chatWindow.showNormal()



    def listwidget_addItem(self, msg_str):
        """
        增加消息条目
        :param msg_str: 微信自动监听的字符串，分隔符sep
        :return:
        """

        sender_puid,time,msg_content = dePackMsg(msg_str)
        sender = wxpy.ensure_one(self.bot.friends().search(puid=sender_puid))

        sender_name = sender.name
        msg = parseMsg(sender_name, time, msg_content)

        chat = self.friendsWindowDict.get(sender_puid,None)
        if not chat:
            chatWindow = ChatWindow( friend = sender , mainwindow=self)
            print(2)
            self.friendsWindowDict[sender_puid] = dict()
            self.friendsWindowDict[sender_puid]['window'] = chatWindow
            listItem = QListWidgetItem()
            listItem.setText(msg)
            listItem.setTextAlignment(Qt.AlignLeft)
            listItem.setTextAlignment(Qt.AlignTop)
            self.listWidget.insertItem(0, listItem)
            qApp.processEvents()
            self.senderList.insert(0, sender_puid)
            self.friendsWindowDict[sender_puid]['row'] = listItem

            self.bot.puid_map.dump()

        elif chat.get('row'):
            chatWindow = chat.get('window')
            listItem = chat.get('row')
            listItem.setText(msg)
        else:
            chatWindow = chat.get('window')
            listItem = QListWidgetItem()
            listItem.setText(msg)
            listItem.setTextAlignment(Qt.AlignLeft)
            listItem.setTextAlignment(Qt.AlignTop)
            self.listWidget.insertItem(0, listItem)
            qApp.processEvents()
            self.senderList.insert(0, sender_puid)
            chat['row'] = listItem



        # anime = QPropertyAnimation(listItem, b'color')
        # anime.setDuration(1000)
        # anime.setEndValue(QColor(0, 0, 0, 0))  # 米黄
        # anime.setKeyValueAt(0.5, QColor(255, 0, 0, 250))  # 红色
        # anime.setEndValue(QColor(0, 0, 0, 0))  # 米黄
        # anime.start()
        chatWindow.addMsgToList(sender_name,time,msg_content)
        qApp.processEvents()

    def loginMessage(self):
        """
        登录消息提示
        :return:
        """
        qApp.processEvents()
        QMessageBox.information(self.centralwidget,'提示！','微信已登录！')

    def logoutMessage(self):
        """
        登出消息提示
        :return:
        """
        qApp.processEvents()
        QMessageBox.information(self.centralwidget,'提示！','微信已登出！')



    def openButton(self):
        """
        登录状态下按钮切换状态
        :return:
        """
        self.pushButton_5.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def closeButton(self):
        """
        登出状态下按钮切换状态
        """
        self.pushButton_5.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)



class WxThread(QThread):
    """
    定义微信自动监听线程
    监听微信的好友（没有群和公众号）消息
    """
    wxSignal = pyqtSignal(str)

    def __init__(self,window):
        super().__init__()
        self.work = True
        self.window = window
        self.is_listening = True


    def __del__(self):
        self.work = False
        self.wait()

    def run(self):
        if self.window.bot:
            my_friends = self.window.bot.friends()
            @wxpy.dont_raise_response_error
            @self.window.bot.register(chats=my_friends,msg_types=wxpy.TEXT)
            def add_newItem_to_list(msg):
                """
                注册微信自动监听程序
                注册的监听程序在另一个线程中挂起，监听一旦开始，无法停止，直到程序退出
                 self.stop()函数可以设置是否将监听的消息发送给主界面
                :param msg:
                :return:
                """
                sender_name = msg.sender.name
                sender_puid = msg.sender.puid
                receive_time = datetime.datetime.strftime(msg.receive_time, '%Y-%m-%d %H:%M')
                msg_content = msg.text
                record = packMsg(sender=sender_name,time=receive_time,message=msg_content)
                filename = 'data/'+ sender_puid+ '.dat'
                with open(filename,'a',encoding='utf-8') as f:
                    f.write(record)
                if self.is_listening:
                    msg_str = packMsg(sender=sender_puid,time=receive_time,message=msg_content,seq_msg="")
                    self.sleep(1)
                    self.wxSignal.emit(msg_str)


            self.window.bot.join()


    def stopEmit(self, flag):
        """
        组织消息发送
        :return:
        """
        self.is_listening = flag












