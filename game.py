from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Поиск игры: ")
        self.layout.addWidget(self.label)

        self.setWindowTitle("Главное окно")
        self.setGeometry(100, 100, 1000, 1000)
