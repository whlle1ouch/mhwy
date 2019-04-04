# -*- coding: utf-8 -*-
from ui.send import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QTextEdit
from PyQt5.QtCore import Qt
import wxpy


class SendDialog(QDialog,Ui_Dialog):


    def  __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.mainWindow =parent
        self.setupUi(self)
        self.setWindowTitle('发送消息')
        self.setEvent()


    def setEvent(self):
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)
        self.textEdit.keyPressEvent = self.keyPressEvent


    def on_clicked_pushButton(self):
        if self.textEdit.toPlainText() != "":
            msg_text =self.textEdit.toPlainText()
            bot = self.mainWindow.bot
            if bot and bot.is_listening:
                receiver = wxpy.ensure_one(bot.friends().search(self.sender))
                print(receiver)
                receiver.send(msg_text)
            self.textEdit.setText("")
        self.hide()

    def keyPressEvent(self,e):
        if e.key()==Qt.Key_Enter:
            if self.textEdit.toPlainText() != "":
                return self.on_clicked_pushButton()
            else:
                return self.on_clicked_pushButton_2()
        else:
            return QTextEdit.keyPressEvent(e)



    def on_clicked_pushButton_2(self):
        self.hide()

    def changeSender(self,sender):
        if isinstance(sender,str):
            self.sender = sender
            self.label_2.setText(sender)



