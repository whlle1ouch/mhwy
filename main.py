# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from PyQt5.QtNetwork import QLocalSocket,QLocalServer
import sys
from loading import LoadingWindow

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        serverName = 'MhProcess'
        socket = QLocalSocket()
        socket.connectToServer(serverName)
        if socket.waitForConnected(500):
            app.quit()
        else:
            localServer = QLocalServer()
            localServer.listen(serverName)
            LoadingWindow()
            w = MainWindow()

        sys.exit(app.exec_())
    except Exception as e:
        print(e.args)



