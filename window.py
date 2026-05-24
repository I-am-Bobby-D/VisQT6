import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QGridLayout




#install dependencies in activated venv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grapher")
        self.setMinimumSize(600, 400)

#TOC: horizontal main layout
#     context menu layout
#

        #Configure horizontal layout for button menu and text box
        #.addLayout(<layout>) to nest layouts
        grid_widget = QWidget()
        main_layout = QGridLayout()
        grid_widget.setLayout(main_layout)
        self.setCentralWidget(grid_widget)

        #input box
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter function here...")

        main_layout.addWidget(self.input_box, 0, 0, 1, 2)


        #context menu switch
        self.toggle_button = QPushButton("Show Context Menu")
        self.toggle_button.clicked.connect(self.toggle_context_menu)

        main_layout.addWidget(self.toggle_button, 1, 0)

        self.context_menu = QWidget()
        context_menu_layout = QGridLayout()
        self.context_menu.setLayout(context_menu_layout)
        self.context_menu.setVisible(False)

         #special character button declarations
        integral_button = QPushButton("∫")  # Integral symbol
        derivative_button = QPushButton("d/dx")  # Derivative symbol
        plus_button = QPushButton("+")
        minus_button = QPushButton("-")

        #add to context menu
        context_menu_layout.addWidget(integral_button, 0, 0)
        context_menu_layout.addWidget(derivative_button, 1, 0)
        context_menu_layout.addWidget(plus_button, 0, 1)
        context_menu_layout.addWidget(minus_button, 1, 1)

        main_layout.addWidget(self.context_menu, 1, 1)


        # Placeholder for coordinate plane
        self.graph_placeholder = QFrame()
        self.graph_placeholder.setFrameShape(QFrame.Shape.Box)
        self.graph_placeholder.setFixedSize(400, 300)  # Adjust size as needed
        graph_placeholder_label = QLabel("Coordinate Plane (Future Widget)")
        graph_placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_placeholder_layout = QVBoxLayout(self.graph_placeholder)
        graph_placeholder_layout.addWidget(graph_placeholder_label)

        main_layout.addWidget(self.graph_placeholder, 2, 0, 1, 2)




    def toggle_context_menu(self):
        is_visible = self.context_menu.isVisible()
        self.context_menu.setVisible(not is_visible)
        # Update button text based on context menu visibility
        self.toggle_button.setText("Hide Context Menu" if not is_visible else "Show Context Menu")


        #widget positioning





#app object declaration
app = QApplication(sys.argv)


#widgets here
#window = window class, abstracts away from QMainWindow
window = MainWindow()
window.show()




#event loop
app.exec()
