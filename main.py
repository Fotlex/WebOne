import sys

from PySide6.QtWidgets import QApplication

from src.game_window import GameWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
