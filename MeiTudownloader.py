import logging
from PyQt5.QtWidgets import QApplication
from meituGUI import rootWindow
from PyQt5 import sip
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%m-%d %H:%M:%S %p", filename='logging.txt')

if __name__ == '__main__':
    import sys
    app=QApplication(sys.argv)
    win=rootWindow()
    win.show()
    sys.exit(app.exec_())