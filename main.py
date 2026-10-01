import sys
from window import MainWindow
from PyQt6.QtWidgets import QApplication

#app obj declaration, window obj declaration, event loop
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
