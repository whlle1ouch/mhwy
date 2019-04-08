from PyQt5.QtWidgets import QWidget,QTextEdit,QListWidgetItem
from ui.chat import Ui_Form
from PyQt5.QtCore import Qt
from datetime import datetime
import wxpy
from utility.msg import packMsg,dePackMsgList,dePackMsg,parseMsg
import os

class ChatWindow(QWidget,Ui_Form):
    def __init__(self , friend , mainwindow=None,parent=None):
        super().__init__(parent)

        self.mainWindow = mainwindow
        self.friend = friend
        self.autoReply = True
        self.setupUi(self)
        self.textEdit = MessageEdit(self)
        # self.loadHistory()
        self.gridLayout.addWidget(self.textEdit)
        if self.friend:
            self.setWindowTitle(self.user.name)
        self.setEvent()

    def setEvent(self):
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)

    def on_clicked_pushButton(self):
        if self.textEdit.toPlainText() != "":
            msg_text = self.textEdit.toPlainText()
            bot = self.mainWindow.bot
            if bot and bot.is_listening:
                self.friend.send(msg_text)
                self.addMsgToList(msg_text)

            self.textEdit.setText("")


    def on_clicked_pushButton_2(self):
        self.hide()

    def loadHistory(self):
        puid = self.friend.puid
        file = 'data/'+ puid +'.dat'
        if os.path.exists(file):
            print(1)
            with open(file,'r',encoding='utf-8') as f:
                history = f.read()
            if history:
                history_List = dePackMsgList(history)
            if not isinstance(history_List,list) or len(history_List)==0:
                return
            for msgHistory in history_List:
                sender,time,message = parseMsg(msgHistory)
                self.addMsgToList(sender,time,message)


    def addMsgToList(self, sender , time , message):
        if not time:
            time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
        msg = sender + "   " + "(" + time + ")" + ":\n" + message + "\n"
        item = QListWidgetItem()
        item.setText(msg)
        item.setTextAlignment(Qt.AlignTop)
        if sender:
            item.setTextAlignment(Qt.AlignLeft)
        else:
            item.setTextAlignment(Qt.AlignRight)
        self.listWidget.addItem(item)












class MessageEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWidget = parent

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()==Qt.Key_Return:
            return self.mainWidget.on_clicked_pushButton()
        elif QKeyEvent.key() ==  Qt.Key_Escape:
            self.mainWidget.hide()

        else:
            return super().keyPressEvent(QKeyEvent)