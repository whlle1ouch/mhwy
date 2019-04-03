# -*- coding: utf-8 -*-
from ui.wx import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QListWidgetItem,QApplication,QListWidget
from PyQt5.QtCore import QThread,pyqtSignal,Qt
import wxpy,win32timezone,datetime
from senddialog import SendDialog

class MainWindow(QMainWindow,Ui_MainWindow):
    wxStopSingal = pyqtSignal()   #定义信号关闭QThread中的进程

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

        #显示列表
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setFixedSize(self.listWidget.width(),self.listWidget.height())
        self.listWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.listWidget.setStyleSheet('background-color:grey;border-bottom:0.5px')

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
        self.pushButton_5.clicked.connect(self.on_clicked_pushButton_5)
        self.pushButton_4.clicked.connect(self.on_clicked_pushButton_4)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)
        self.listWidget.itemClicked.connect(self.on_clicked_listWdigetItem)

        self.wx.wxSignal.connect(self.listwidget_addItem)
        self.wxStopSingal.connect(self.wx.stop)




    def on_clicked_pushButton_5(self):
        if not self.bot:
            self.bot = wxpy.Bot(cache_path='data/cache',login_callback=self.openButton,logout_callback=self.closeButton)

    def on_clicked_pushButton_4(self):
        if self.bot:
            self.bot.logout()
        self.bot = None
        self.closeButton()

    def on_clicked_pushButton_2(self):
        if self.pushButton_2.text() == '开启自动回复':
            if self.bot:
                self.pushButton_2.setText('停止自动回复')
                self.wx.start()

                QApplication.processEvents()
        elif self.pushButton_2.text() == '停止自动回复':
            self.pushButton_2.setText('开启自动回复')
            self.wxStopSingal.emit()

    def on_clicked_listWdigetItem(self,item):
        index = self.listWidget.row(item)
        sender = self.senderList[index]
        print(sender)
        self.sendDialog.changeSender(sender)
        self.sendDialog.show()





    def listwidget_addItem(self, msg_str):
        msg_list = msg_str.split('{msg_separator}')
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
            QApplication.processEvents()
        self.listWidget.insertItem(0,listItem)
        self.senderList.insert(0,sender)
        QApplication.processEvents()
















    def openButton(self):
        self.pushButton_5.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def closeButton(self):
        self.pushButton_5.setEnabled(True)
        # self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)



class WxThread(QThread):
    wxSignal = pyqtSignal(str)

    def __init__(self,window):
        super().__init__()
        self.work = True
        self.window = window
        self.listen = False


    def __del__(self):
        self.work = False
        self.wait()

    def run(self):
        self.listen = True
        if self.window.bot:
            my_friends = self.window.bot.friends()
            @self.window.bot.register(chats=my_friends,msg_types=wxpy.TEXT)
            def add_newItem_to_list(msg):
                print(msg)
                if self.listen:
                    sender_name = msg.sender.name
                    receive_time = datetime.datetime.strftime(msg.receive_time,'%Y-%m-%d %H:%M')
                    msg_content = msg.text
                    sep = '{msg_separator}'
                    msg_str = sender_name + sep  + receive_time + sep + msg_content
                    self.wxSignal.emit(msg_str)

            self.window.bot.join()


    def stop(self):
        self.listen = False









