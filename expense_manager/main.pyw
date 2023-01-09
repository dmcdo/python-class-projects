from PyQt5.QtWidgets import QApplication
import sys
from main_window import MainWindow

app = QApplication(sys.argv)

gui = MainWindow()
gui.show()
sys.exit(app.exec_())