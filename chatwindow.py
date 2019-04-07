from PyQt5.QtWidgets import QWidget,QTextEdit,QListWidgetItem
from ui.chat import Ui_Form
from PyQt5.QtCore import Qt
from datetime import datetime
import wxpy


class ChatWindow(QWidget,Ui_Form):
    def __init__(self, friend=None, mainwindow=None,parent=None):
        super().__init__(parent)
        self.mainWindow = mainwindow
        self.friend = friend or ""
        self.setupUi(self)
        self.textEdit = MessageEdit(self)
        self.gridLayout.addWidget(self.textEdit)

        self.setWindowTitle(self.friend)


        self.setEvent()

    def setEvent(self):
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)

    def on_clicked_pushButton(self):
        if self.textEdit.toPlainText() != "":
            msg_text = self.textEdit.toPlainText()
            bot = self.mainWindow.bot
            if bot and bot.is_listening:
                receiver = wxpy.ensure_one(bot.friends().search(self.friend))
                receiver.send(msg_text)
                self.addMsgToList(msg_text)

            self.textEdit.setText("")
        self.hide()

    def on_clicked_pushButton_2(self):
        self.hide()

    def loadHistory(self):
        if self.friend:
            file = 'data/'+self.friend+'.dat'
            with open(file,'r',encoding='utf-8') as f:
                history = f.read()
            if history:
                history_List = history.split()

    def addMsgToList(self, message , time=None , sender=None):
        if not time:
            time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
        if not sender:
            sender = ""
        msg = sender + "   " + "(" + time + ")" + ":\n" + message + "\n"
        item = QListWidgetItem()
        item.setText(msg)
        if sender:
            item.setTextAlignment(Qt.AlignLeft)
        else:
            item.setTextAlignment(Qt.AlignRight)
        # item.setTextAlignment(Qt.AlignTop)
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