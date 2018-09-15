import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAction, qApp, QInputDialog, QFileDialog, QMenu, QActionGroup, QFileDialog
import webbrowser
from feedback import feedbackDialog
from aboutme import aboutDialog
from meituMain import mainWindow

class rootWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.root = os.getcwd()
        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.createToolBars()
        self.move(500, 400)
        self.setFixedSize(650, 210)
        self.setWindowTitle('美图下载器')
        self.setWindowIcon(QIcon('icon/download.ico'))
        self.setCentralWidget(mainWindow(self))

    def createActions(self):
        self.setpathAct = QAction(QIcon('icon/open.ico'), "保存路径", self, statusTip="设置保存路径，当前@ %s"%self.root, triggered=self.selectPath)
        self.debug=QAction('开发者模式',self,statusTip='本功能为开发者调试功能，用户请勿使用！',checkable=True,enabled=False)
        self.user=QAction('用户模式',self,statusTip='目前为用户模式！',checkable=True)
        self.aboutappAct = QAction(QIcon('icon/app.ico'), "关于应用",self,triggered=self.aboutapp, statusTip="关于应用的信息")
        self.aboutmeAct = QAction(QIcon('icon/avatar.ico'), "关于作者", self, triggered=self.aboutme, statusTip="关于作者信息")
        self.aboutQtAct = QAction(QIcon('icon/qt.ico'), "关于Qt", self, triggered=QApplication.instance().aboutQt, statusTip="关于GUI界面")
        self.feedbackAct = QAction(QIcon('icon/feedback.ico'), '反馈', self, triggered=self.feedback, statusTip="报错或反馈")
        self.helpAct = QAction(QIcon("icon/help.ico"), "使用指南", self, triggered=self.help, statusTip = "使用指南")
        self.openWebAct = QAction(QIcon("icon/shoe.ico"), "打开网站", self, statusTip="打开 美图 网站", triggered=self.openmeitu)
        self.githubAct = QAction(QIcon("icon/github.ico"), "查看源码or更新", self, statusTip="打开github查看源码or更新动态，欢迎star", triggered=self.opengithub)
        self.user.setChecked(True)

    def createMenus(self):
        modemenu = QMenu('模式切换',self)
        modemenu.addAction(self.user)
        modemenu.addAction(self.debug)

        settingMenu = self.menuBar().addMenu('设置(&S)')
        settingMenu.addAction(self.setpathAct)
        settingMenu.addSeparator()
        settingMenu.addMenu(modemenu)

        feedbackMenu = self.menuBar().addMenu('反馈(&B)')
        feedbackMenu.addAction(self.feedbackAct)

        aboutMenu=self.menuBar().addMenu("关于(&A)")
        aboutMenu.addAction(self.aboutappAct)
        aboutMenu.addAction(self.aboutmeAct)
        aboutMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(settingMenu)
        self.menuBar().addMenu(feedbackMenu)
        self.menuBar().addMenu(aboutMenu)

    def createToolBars(self):
        self.toolbar=self.addToolBar('Help')
        self.toolbar.addAction(self.helpAct)
        self.toolbar.addAction(self.githubAct)
        self.toolbar.addAction(self.openWebAct)

    def createStatusBar(self,words='使用前，先点击帮助，了解更多'):
        self.statusBar().showMessage(words)

    def selectPath(self):    
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,"QFileDialog.getExistingDirectory()", options=options)
        if directory is not None:
            self.root = directory
        else:
            self.root = os.getcwd()
        self.setpathAct.setStatusTip("设置保存路径，当前@ %s"%self.root)

    def aboutapp(self):
        QMessageBox.about(self, "关于 美图下载器","<p>应用 <b>美图下载器</b> 可以用于下载美女套图。</p>" 
                          "<p>本应用仅作为交流学习使用，请勿用于商业用途，否则后果自负。</p>" 
                          "<p>本应用中的所有图片版权归出版商所有。</p>"
                          "<p>当前版本号： <i>V0.1 Alpha<i> </p>"
                          "<p>多说一句：你现在使用的版本是免费的，如果是从第三方购买所得，意味着你被骗了。</p>")

    def aboutme(self):
        abm=aboutDialog()
        r=abm.exec_()

    def feedback(self):
        fbd=feedbackDialog()
        r=fbd.exec_()

    def help(self):
        webbrowser.open("https://github.com/crj1998/meitu")

    def openmeitu(self):
        webbrowser.open("https://www.meituri.com/")

    def opengithub(self):
        webbrowser.open("https://github.com/crj1998")


if __name__ == '__main__':
    import sys
    app=QApplication(sys.argv)
    win=rootWindow()
    win.show()
    sys.exit(app.exec_())