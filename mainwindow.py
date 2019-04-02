# -*- coding: utf-8 -*-
from ui.wx import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QListWidgetItem
import wxpy,win32timezone

class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.bot = None
        self.closeButton()
        self.listWidget.setAcceptDrops(True)

        self.setEvent()
        self.show()

    def setEvent(self):
        self.pushButton_5.clicked.connect(self.on_clicked_pushButton_5)
        self.pushButton_4.clicked.connect(self.on_clicked_pushButton_4)
        # self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)


    def on_clicked_pushButton_5(self):
        if not self.bot:
            self.bot = wxpy.Bot(cache_path='data/cache.txt',login_callback=self.openButton,logout_callback=self.closeButton)

    def on_clicked_pushButton_4(self):
        if self.bot:
            self.bot.logout()
        self.bot = None
        self.closeButton()

    # def on_clicked_pushButton_2(self):
    #     if self.bot:
    #         my_friends = self.bot.friends()
    #         @self.bot.register([my_friends], TEXT)
    #         def add_newItem_to_list(msg):
    #             # 打印消息
    #             item = QListWidgetItem(self.centralwidget)
    #             item.setText(msg)
    #             self.listWidget.addItem(item)





    def openButton(self):
        self.pushButton_5.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def closeButton(self):
        self.pushButton_5.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)