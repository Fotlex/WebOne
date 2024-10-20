from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout


class StatsWidget(QWidget):
    def __init__(self, game_logic, result):
        super().__init__()
        self.game_logic = game_logic
        self.result = result

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        font = QFont('Comic Sans MS', 14, QFont.Weight.Bold)

        self.status_label = QLabel()
        self.my_score_label = QLabel()
        self.opponent_score_label = QLabel()
        self.update_stats()

        for label in [self.status_label, self.my_score_label, self.opponent_score_label]:
            label.setFont(font)
            layout.addWidget(label)

    def update_stats(self):
        self.status_label.setText(f"Статус: {self.result}")
        self.my_score_label.setText(f"Ваши очки: {self.game_logic.my_score}")
        self.opponent_score_label.setText(f"Очки оппонента: {self.game_logic.opponent_score}")


class EndGameDialog(QDialog):
    def __init__(self, parent, game_logic, game_status, winner_status):
        super().__init__(parent)
        self.setStyleSheet("""
            QDialog { background-color: rgb(53, 53, 53); }
            QLabel { color: white; }
            QPushButton { 
                background-color: rgb(80, 80, 80);
                color: white; 
                border-radius: 10px; 
                padding: 10px;
            }
            QPushButton:hover { background-color: rgb(100, 100, 100); }
        """)
        self.game_logic = game_logic
        self.parent_window = parent

        self.setMinimumSize(450, 200)
        self.setWindowTitle("WebOne")
        grid_layout = QGridLayout(self)

        font = QFont('Comic Sans MS', 15, QFont.Weight.Bold)

        self.title = QLabel("Игра завершена! " + game_status, self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(font)
        grid_layout.addWidget(self.title, 0, 0)

        self.stats_widget = StatsWidget(game_logic, winner_status)
        grid_layout.addWidget(self.stats_widget, 1, 0)

        self.ok_button = QPushButton("ОК", self)
        self.ok_button.setFont(font)
        self.ok_button.clicked.connect(self.accept)
        grid_layout.addWidget(self.ok_button, 2, 0)

        self.setLayout(grid_layout)
        self.finished.connect(self.on_finished)

    def on_finished(self):
        if self.parent_window and hasattr(self.parent_window, 'parent') and self.parent_window.parent():
            self.parent_window.parent().close()
