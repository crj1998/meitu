#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/22 20:57
#!Author: Renjie Chen
#!Function: 反馈界面

from PyQt5.QtWidgets import QPushButton,QApplication,QTextEdit,QLabel,QLineEdit,QGridLayout,QComboBox,QMessageBox,QDialog, QCompleter, QCheckBox
from PyQt5.QtGui import QStandardItemModel, QRegExpValidator, QIcon
from PyQt5.QtCore import QRegExp
from sendEmail import sEmail
import os

class feedbackDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createGridLayout()
        self.setGeometry(300,300,450,500)
        self.setWindowTitle('用户反馈')
        self.setWindowIcon(QIcon('icon/feedback.ico'))
    def sendLogging(self):
        if self.cb.isChecked():
            return ["logging.txt"]
        else:
            return []
    def emailSubmit(self):
        if self.contactEdit.text()=='' or self.contentEdit.toPlainText()=='':
            self.warningMessage()
        elif sEmail(self.combo.currentText(),self.contactEdit.text()+'\n'+self.contentEdit.toPlainText(),self.sendLogging()):
            self.successMessage()
        else:
            self.failureMessage()
    def createWidgets(self):
        self.title=QLabel('反馈类型：')
        self.contact=QLabel('邮箱地址：')
        self.content=QLabel('具体内容：')
        self.submit=QPushButton('提交')
        self.submit.clicked.connect(self.emailSubmit)
        self.combo=QComboBox()
        self.combo.addItem('意见反馈')
        self.combo.addItem('问题反馈')
        self.combo.addItem('联系作者')
        self.contactEdit=QLineEdit()
        self.contentEdit=QTextEdit()
        self.contentEdit.setText('具体描述需要反馈的内容')
        self.contentEdit.selectAll()
        self.contentEdit.setFocus(True)
        self.cb = QCheckBox("上传日志", self)
        self.cb.setChecked(True)

        self.model = QStandardItemModel(0, 1, self)
        completer = QCompleter(self.model, self)
        self.contactEdit.setCompleter(completer)
        completer.activated[str].connect(self.contactEdit.setText)
        self.contactEdit.textEdited[str].connect(self.autocomplete)

        regx = QRegExp("^[0-9A-Za-z_.-]{3,16}@[0-9A-Za-z-]{1,10}(\.[a-zA-Z0-9-]{0,10}){0,2}\.[a-zA-Z0-9]{2,6}$")
        validator = QRegExpValidator(regx, self.contactEdit)
        self.contactEdit.setValidator(validator)

    def createGridLayout(self):
        #新建表格排列对象，并设置间距为10
        grid=QGridLayout()
        grid.setSpacing(10)
        #表格布局
        grid.addWidget(self.title,1,0)
        grid.addWidget(self.combo,1,1)
        grid.addWidget(self.contact,2,0)
        grid.addWidget(self.contactEdit,2,1)
        grid.addWidget(self.content,3,0)
        grid.addWidget(self.contentEdit,3,1,5,1)
        grid.addWidget(self.submit,9,0,1,2)
        grid.addWidget(self.cb, 7, 0, 1, 1)
        #使能表格布局
        self.setLayout(grid)
    def warningMessage(self):
        MESSAGE="<p>联系邮箱和具体内容为必填项。</p><p>点击OK返回反馈界面。</p>"
        warning=QMessageBox.information(self,'注意',MESSAGE)
    def successMessage(self):
        MESSAGE="<p>你的反馈我们已经收到，我们会尽快给您回馈，感谢您的支持。</p><p>点击OK退出反馈界面。</p>"
        success=QMessageBox.information(self,'反馈成功',MESSAGE)
        self.close()

    def failureMessage(self):
        MESSAGE="<p>由于某些原因，您没有反馈成功。<p>是否重新尝试一次？"
        failure=QMessageBox(QMessageBox.Warning,'反馈失败',MESSAGE,QMessageBox.NoButton,self)
        failure.addButton('是',QMessageBox.AcceptRole)
        failure.addButton("否",QMessageBox.RejectRole)
        if failure.exec_()==QMessageBox.AcceptRole:
            pass
        else:
            self.close()

    def autocomplete(self, text):
        if '@' in self.contactEdit.text():
            return
        emaillist = ["@live.com", "@139.com", "@126.com", "@163.com", "@gmail.com", "@qq.com"]
        self.model.removeRows(0, self.model.rowCount())
        for i in range(0, len(emaillist)):
            self.model.insertRow(0)
            self.model.setData(self.model.index(0, 0), text + emaillist[i])


if __name__ == '__main__':
    import sys
    app=QApplication(sys.argv)
    interface=feedbackDialog()
    interface.show()
    sys.exit(app.exec_())