import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QGridLayout
from scene import GLWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Coordinate System")
        self.setMinimumSize(600, 400)



        #
        #.addLayout(<layout>) to nest layouts
        grid_widget = QWidget()
        main_layout = QGridLayout()
        grid_widget.setLayout(main_layout)

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)
        main_layout.setRowStretch(2, 1)

        self.setCentralWidget(grid_widget)

        #input box
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter function here...")

        main_layout.addWidget(self.input_box, 0, 0, 1, 1)


        #context menu switch
        self.toggle_button = QPushButton("Show Context Menu")
        self.toggle_button.clicked.connect(self.toggle_context_menu)

        main_layout.addWidget(self.toggle_button, 0, 1)

        self.context_menu = QWidget()
        context_menu_layout = QGridLayout()
        self.context_menu.setLayout(context_menu_layout)
        self.context_menu.setVisible(False)

        #special character button declarations
        integral_button = QPushButton("∫")  # Integral symbol
        derivative_button = QPushButton("d/dx")  # Derivative symbol
        plus_button = QPushButton("+")
        minus_button = QPushButton("-")
        mul_button = QPushButton("⋅")
        div_button = QPushButton("/")

        #add to context menu
        context_menu_layout.addWidget(integral_button, 0, 3)
        context_menu_layout.addWidget(derivative_button, 0, 2)
        context_menu_layout.addWidget(plus_button, 1, 2)
        context_menu_layout.addWidget(minus_button, 1, 3)
        context_menu_layout.addWidget(mul_button, 2, 2)
        context_menu_layout.addWidget(div_button, 2, 3)

        main_layout.addWidget(self.context_menu, 0, 2)


        # Toggle axes button
        self.toggle_axes_button = QPushButton("Toggle Axes")
        self.toggle_axes_button.clicked.connect(self.toggle_axes)
        main_layout.addWidget(self.toggle_axes_button, 2, 2)

        # OpenGL rendering widget
        self.gl_widget = GLWidget()
        main_layout.addWidget(self.gl_widget, 2, 0, 3, 3)

    def toggle_axes(self):
        self.gl_widget.show_axes = not self.gl_widget.show_axes
        self.gl_widget.update()

    def toggle_context_menu(self):
        is_visible = self.context_menu.isVisible()
        self.context_menu.setVisible(not is_visible)
        # Update button text based on context menu visibility
        self.toggle_button.setText("Hide Context Menu" if not is_visible else "Show Context Menu")
