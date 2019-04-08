# -*- coding: utf-8 -*-
from ui.send import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QTextEdit
from PyQt5.QtCore import Qt
import wxpy


class SendDialog(QDialog,Ui_Dialog):


    def  __init__(self, friend , parent=None):
        QDialog.__init__(self,parent)
        self.mainWindow =parent

        self.friend = friend
        self.setupUi(self)
        self.setWindowTitle(friend)
        self.textEdit = MessageEdit(self)
        self.gridLayout.addWidget(self.textEdit)

        self.setEvent()


    def setEvent(self):
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)



    def on_clicked_pushButton(self):
        if self.textEdit.toPlainText() != "":
            msg_text =self.textEdit.toPlainText()
            bot = self.mainWindow.bot
            if bot and bot.is_listening:
                receiver = wxpy.ensure_one(bot.friends().search(self.sender))
                receiver.send(msg_text)
            self.textEdit.setText("")


    def on_clicked_pushButton_2(self):
        self.hide()

    def changeSender(self,sender):
        if isinstance(sender,str):
            self.sender = sender
            self.label_2.setText(sender)


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
