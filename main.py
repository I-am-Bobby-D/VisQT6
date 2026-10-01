from window import MainWindow

#app obj declaration, window obj declaration, event loop
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
