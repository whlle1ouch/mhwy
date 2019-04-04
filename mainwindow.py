# -*- coding: utf-8 -*-
from ui.wx import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QListWidgetItem,QApplication,QListWidget,QMessageBox,qApp
from PyQt5.QtCore import QThread,pyqtSignal,Qt
import wxpy,win32timezone,datetime
from senddialog import SendDialog
from autoreplywindow import AutoReplyWindow

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
        self.sendDialog = SendDialog(self)
        self.autoReplyWindow = AutoReplyWindow(self)

        #显示列表
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setFixedSize(self.listWidget.width(),self.listWidget.height())
        self.listWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.listWidget.setStyleSheet('background-color:white;border-bottom:0.5px;border-color:grey')

        #定义微信bot线程
        self.wx = WxThread(self)

        #定义事件和信号
        self.setEvent()

        #其他参数
        self.listMaxCount = 30
        self.listCount = 0
        self.senderList = list()

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
            self.bot = wxpy.Bot(cache_path='data/cache',login_callback=self.loginMessage)
            self.openButton()
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
                if not self.bot.is_listening:
                    self.bot.start()
                self.wxTriggerSingal.emit(True)
                self.pushButton_2.setText('停止自动回复')

                qApp.processEvents()
        elif self.pushButton_2.text() == '停止自动回复':
            self.pushButton_2.setText('开启自动回复')
            self.wxTriggerSingal.emit(False)

    def on_clicked_pushButton(self):
        self.autoReplyWindow.showNormal()

    def on_clicked_listWdigetItem(self, item):
        """
        聊天信息列表弹出消息框发送消息
        :param item:
        :return:
        """

        index = self.listWidget.row(item)
        sender = self.senderList[index]
        self.sendDialog.changeSender(sender)
        self.sendDialog.showNormal()





    def listwidget_addItem(self, msg_str,sep='{msg_separator}'):
        """
        增加消息条目
        :param msg_str: 微信自动监听的字符串，分隔符sep
        :return:
        """
        msg_list = msg_str.split(sep)
        sender = msg_list[0]
        time = msg_list[1]
        content = msg_list[2]
        self.listCount += 1
        msg = sender + '  ' + '('+ time +')' + ':\n' + content
        listItem = QListWidgetItem()
        listItem.setText(msg)
        listItem.setTextAlignment(Qt.AlignLeft)
        listItem.setTextAlignment(Qt.AlignTop)

        if self.listCount > self.listMaxCount:
            self.listWidget.takeItem(self.listMaxCount-1)
            self.senderList.pop(-1)
            qApp.processEvents()
        self.listWidget.insertItem(0,listItem)
        self.senderList.insert(0,sender)
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
        self.is_replying = False


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
                receive_time = datetime.datetime.strftime(msg.receive_time, '%Y-%m-%d %H:%M')
                msg_content = msg.text
                record = sender_name + '   '+'(' + receive_time + ' )' +'  :\n' + msg_content+'\n'
                with open('data/record.txt','a',encoding='utf-8') as f:
                    f.write(record)
                if self.is_replying:
                    sep = '{msg_separator}'
                    msg_str = sender_name + sep  + receive_time + sep + msg_content
                    self.sleep(1)
                    self.wxSignal.emit(msg_str)
                else:
                    self.window.bot.messages.clear()  ####如果上传消息，就清空历史消息
                # else:
                #     self.window.bot.stop()

            self.window.bot.join()


    def stopEmit(self, flag):
        """
        组织消息发送
        :return:
        """
        self.is_replying = flag









