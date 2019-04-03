# -*- coding: utf-8 -*-
from ui.send import Ui_Dialog
from PyQt5.QtWidgets import QDialog
import wxpy


class SendDialog(QDialog,Ui_Dialog):


    def  __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.mainwindow =parent
        self.setupUi(self)
        self.setEvent()


    def setEvent(self):
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)


    def on_clicked_pushButton(self):
        if self.textEdit.toPlainText() != "":
            msg_text =self.textEdit.toPlainText()
            bot = self.parent.bot
            # if bot:
            #     receiver = wxpy.ensure_one(bot.friends().search(self.sender))
            #     print(receiver)
                # receiver.send(msg_text)



    def on_clicked_pushButton_2(self):
        self.hide()

    def changeSender(self,sender):
        if isinstance(sender,str):
            self.sender = sender
            self.label_2.setText(sender)



