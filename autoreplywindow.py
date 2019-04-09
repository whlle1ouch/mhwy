# -*- coding: utf-8 -*-

from ui.autoreply import Ui_Form
from PyQt5.QtWidgets import QWidget,QTableWidgetItem,QMessageBox,QApplication,\
    QMenu,QHeaderView,QTableWidgetItem,QRadioButton,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.Qt import QCursor
import json



class AutoReplyWindow(QWidget,Ui_Form):



    def __init__(self, parent=None):
        QWidget.__init__(self,None)
        self.mainWindow = parent
        self.setupUi(self)
        self.setWindowTitle('设置自动回复')

        self.pushButton_2.setEnabled(False)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  ###设置手动调整列宽

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QHeaderView.Interactive)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu) # 右键菜单，如果不设为CustomContextMenu,无法使用customContextMenuRequested
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.loadReply()
        self.setEvent()

    def setEvent(self):
        self.pushButton_4.clicked.connect(self.on_clicked_pushButton_4)  #返回
        self.pushButton.clicked.connect(self.on_clicked_pushButton)    #修改
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)   #提交
        self.tableWidget.customContextMenuRequested.connect(self.addMenu)



    def on_clicked_pushButton(self):
        if self.pushButton.text()== '修改':
            self.tableWidget.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton.setText('取消')
        elif self.pushButton.text()=='取消':
            self.tableWidget.setEnabled(False)
            self.pushButton.setText('修改')
            self.pushButton_2.setEnabled(False)
            self.refreshTable()

    def on_clicked_pushButton_2(self):
        answer = QMessageBox.warning(self,'警告！','是否确认提交修改？\n  提交后将覆盖本地数据.',
                                     QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if answer ==QMessageBox.Yes:
            self.tableTextChange()
            self.refreshTable()
            if self.pushButton.text()=='取消':
                self.pushButton.setText('修改')
            self.tableWidget.setEnabled(False)



    def on_clicked_pushButton_4(self):
        self.hide()

    def loadReply(self):
        with open('data/reply.json','r',encoding='utf-8') as f:
            self.replyList = json.loads(f.read())
        if self.replyList:
            self.addTable(self.replyList)


    def save_to_local(self):
        with open('data/reply.json','w',encoding='utf-8') as f:
            replyJson = json.dumps(self.replyList)
            f.write(replyJson)

    def addMenu(self,pos):
        self.tableMenu = QMenu(self)
        item1 = self.tableMenu.addAction('增加行')
        item2 = self.tableMenu.addAction('删除行')
        rowNumber = self.tableWidget.rowAt(pos.y())   #获取右键点击的行号
        item1.triggered.connect(lambda: self.addRow(rowNumber))
        item2.triggered.connect(lambda: self.deleteRow(rowNumber))
        self.tableMenu.popup(QCursor.pos())


    def addRow(self, rowNum):
        if rowNum == -1:
            rowNum=0
        print(rowNum)
        self.tableWidget.insertRow(rowNum)
        checkBox = QRadioButton()
        checkBox.setChecked(False)
        self.tableWidget.setCellWidget(rowNum,3,checkBox)
        self.tableWidget.cellWidget(rowNum,3).setStyleSheet("margin-left:auto;margin-right:auto;")


    def deleteRow(self, rowNum):
        self.tableWidget.removeRow(rowNum)





    def addTable(self, value):
        if not isinstance(value,list):
            return
        row = len(value)
        col = len(value[0])
        table = self.tableWidget
        table.setRowCount(row)
        table.setColumnCount(col)
        # table.setEnabled(False)
        for i, row in enumerate(value):
            for j, cell in enumerate(row):
                if j!=3:
                    newItem = QTableWidgetItem(str(cell))
                    newItem.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, j, newItem)
                else:
                    newCheck = QRadioButton()
                    newCheck.setChecked(bool(cell))

                    table.setCellWidget(i,j,newCheck)
                    table.cellWidget(i,j).setStyleSheet("margin-left:auto;")
                QApplication.processEvents()
        self.tableWidget.setEnabled(False)


    def refreshTable(self):
        row = self.tableWidget.rowCount()
        if row == 0:
            return
        for i in range(row):
            self.tableWidget.removeRow(i)
            QApplication.processEvents()
        self.addTable(self.replyList)

    def tableTextChange(self):
        row = self.tableWidget.rowCount()
        column = self.tableWidget.columnCount()
        newList = list()
        for i in range(row):
            row = list()
            for j in range(column):
                if self.tableWidget.item(i,j):
                    row.append(self.tableWidget.item(i,j).text())
                elif self.tableWidget.cellWidget(i,j):
                    checkState = self.tableWidget.cellWidget(i,j).isChecked()
                    if checkState:
                        row.append(1)
                    else:
                        row.append(0)
                else:
                    row.append("")
            newList.append(row)
        self.replyList = newList
        self.save_to_local()

    def showMsg(self , title , msg):
        return QMessageBox.information(self,title,msg)








