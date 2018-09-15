from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QLabel, QPushButton, QMessageBox, QCheckBox, QGridLayout, QCompleter, QLayout, QWidget, QProgressBar
from PyQt5.QtCore import Qt, QEvent, QRegExp, QObject, QTimer
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator, QFont, QPixmap, QStandardItemModel, QIcon
import requests
import re
import os
from meituCore import meituInfoThread, meituDownThread

class mainWindow(QWidget):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.createWidgets()
        self.createTimer()
        self.createGridLayout()
        self.setFixedSize(650, 110)
        self.setWindowTitle("美图下载器")

    def createWidgets(self):
        self.lb1 = QLabel("输入链接：", self)
        self.lb1.setFixedSize(80,30)
        self.lb2 = QLabel("下载进度：", self)
        self.lb2.setFixedSize(80,30)

        self.edit = QLineEdit(self)
        self.edit.setFixedSize(400,25)
        self.edit.setPlaceholderText("请注意链接格式")
        self.edit.setClearButtonEnabled(True)
        regx = QRegExp("https://www.meituri.com/a/[0-9]{1,7}/?$")
        validator = QRegExpValidator(regx, self.edit)
        self.edit.setValidator(validator)
        self.r1 = re.compile('https://www.meituri.com/a/[0-9]{1,7}/?')

        self.btn = QPushButton("下载", self)
        self.btn.setFixedSize(130,30)
        self.btn.setEnabled(False)
        self.btn.setStyleSheet('''
            QPushButton{
                height:30px;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                background-color: deepskyblue}
            QPushButton:hover {
                background-color: #0078d7;
                color:white;
                border-style: inset;}
            QPushButton:!enabled{
                color:grey;
                border-color:red;
                background-color: #F5F5F5}
            QPushButton:pressed {
                background: transparent;
                border-style: inset;}''')
        self.btn.clicked.connect(self.do)

        self.pb = QProgressBar(self)
        self.pb.setFixedSize(530, 20)
        self.pb.setMinimum(0)
        #self.pb.setMaximum(0)
        self.pb.setOrientation(Qt.Horizontal)


    def createTimer(self):
        self.time_100ms = QTimer(self)
        self.time_100ms.setInterval(100)
        self.time_100ms.timeout.connect(self.Refresh_100ms)
        self.time_100ms.start()

        self.count = 14
        self.time_1000ms = QTimer(self)
        self.time_1000ms.setInterval(1000)
        self.time_1000ms.timeout.connect(self.Refresh_1000ms)

    def createGridLayout(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.lb1, 0, 0, 1, 1)
        grid.addWidget(self.edit, 0, 1, 1, 3)
        grid.addWidget(self.btn, 0, 5, 1, 1)
        grid.addWidget(self.lb2, 1, 0, 1, 1)
        grid.addWidget(self.pb, 1, 1, 1, 3)
        self.setLayout(grid)

    def Refresh_100ms(self):
        url = self.edit.text()
        if url != "":
            m = re.match(self.r1, url)
            if m is not None:
                self.btn.setEnabled(True)
            else:
                self.btn.setEnabled(False)


    def Refresh_1000ms(self):
        if self.count > 0:
            self.btn.setText(str(self.count) + '秒后下载')
            self.count -= 1
        else:
            self.time_100ms.start()
            self.time_1000ms.stop()
            self.btn.setText("下载")
            self.btn.setEnabled(True)
            self.edit.setEnabled(True)
            self.count = 14

    def do(self):
        self.url = self.edit.text()
        self.time_100ms.stop()
        self.btn.setEnabled(False)
        self.edit.setEnabled(False)
        self.pb.setMaximum(0)
        self.father.createStatusBar("正在获取图集@ %s 信息..." %self.url)
        self.downloadThread = meituInfoThread(self.url)
        self.downloadThread.download_info_signal[str].connect(self.showInfo)
        self.downloadThread.download_error_signal[int].connect(self.showError)
        self.downloadThread.start()

    def showInfo(self, info):
        i = info.split(",")
        self.pb.setMaximum(int(i[1]))
        reply = QMessageBox.question(self, "下载提醒", "图集名称: %s\n图片数量: %sP \n是否下载？"%(i[0],i[1]), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            data = self.downloadThread.getData()
            root = self.father.root
            self.savepicThread = meituDownThread(root, data)
            self.savepicThread.download_process_signal[int].connect(self.changepb)
            self.savepicThread.finished.connect(self.time_1000ms.start)
            self.savepicThread.start()
        else:
            self.time_100ms.start()
            self.btn.setEnabled(True)
            self.edit.setEnabled(True)

    def showError(self, error_num):
        self.pb.setMaximum(100)
        reply = QMessageBox.warning(self, "警告", "图集URL: %s无效。\n请重新填写"%self.url, QMessageBox.Yes)
        self.father.createStatusBar("无效的URL @ %s"%self.url)
        self.edit.clear()
        self.time_100ms.start()
        self.btn.setEnabled(True)
        self.edit.setEnabled(True)

    def changepb(self, process):
        self.father.createStatusBar("已保存第 %d 张图片"%process)
        self.pb.setValue(process)



if __name__ == '__main__':
    #"https://www.meituri.com/a/10068/"
    import sys
    app = QApplication(sys.argv)
    wim = mainWindow()
    wim.show()
    sys.exit(app.exec_())