
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QPushButton, QItemDelegate, QHBoxLayout
from PyQt5.QtCore import Qt, QModelIndex, QUrl
#from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser

from picclassify import DataManagement

class MyButtonDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def createButtons(self):
        self.viewBtn = QPushButton(self.tr("预览"), self.parent(), clicked = self.parent().viewBtnClicked)
        self.viewBtn.setStyleSheet('''
            QPushButton{
                height:30px;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                background-color: NavajoWhite}
            QPushButton:hover {
                background-color: NavajoWhite;
                color:white;
                border-style: inset;}
            QPushButton:pressed {
                background: transparent;
                border-style: inset;}''')

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            self.createButtons()
            self.viewBtn.index = [index.row(), index.column()]
            hLayout = QHBoxLayout()
            hLayout.addWidget(self.viewBtn)
            #hLayout.setContentsMargins(5,2,5,2)
            hLayout.setContentsMargins(0, 0, 0, 0)
            hLayout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(hLayout)
            self.parent().setIndexWidget(index, widget)


class tableItem(QTableWidgetItem):
    def __init__(self, text):
        super(tableItem, self).__init__()
        self.setText(text)
        self.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)    

class ClassTable(QTableWidget):

    def __init__(self, filename="class01.dat"):
        super().__init__()
        self.filename = filename
        self.style_init()
        
        
    def style_init(self):
        self.setGeometry(50,50,1200,400)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["操作", "分类名称", "详细信息", "url"])
        self.setSortingEnabled(True)
        self.setItemDelegateForColumn(0, MyButtonDelegate(self))

        dm = DataManagement(self.filename)
        data = dm.load_data()

        for line,info in enumerate(data):
            self.insertLine(line, info)

        #self.resizeColumnsToContents()
        #self.resizeRowsToContents()
        self.setColumnWidth(0,60)
        self.setColumnWidth(1,200)
        self.setColumnWidth(2,700)
        self.setColumnWidth(3,300)
        #self.setWordWrap(True)
        #self.hideColumn(4)

    def insertLine(self, line, info):
        self.insertRow(line)
        name_item = tableItem(info[1])
        detail_item = tableItem(info[2])
        url_item = tableItem(info[0])


        self.setItem(line, 1, name_item)
        self.setItem(line, 2, detail_item)
        self.setItem(line, 3, url_item)

    def viewBtnClicked(self):
        row = self.sender().index[0]
        url = self.item(row, 3).text()
        webbrowser.open(url)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = ClassTable("class02.dat")
    win.show()
    sys.exit(app.exec_())