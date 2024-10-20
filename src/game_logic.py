import random
from threading import Thread

from PySide6.QtCore import Signal, QObject, QTimer

from . import config
from .particle_manager import ParticleManager


class SignalEmitter(QObject):
    move_received = Signal(tuple)
    game_ended = Signal(tuple)


class GameLogic:
    def __init__(self, network_thread, field, is_my_turn):
        self.signal_emitter = SignalEmitter()
        self.particle_manager = ParticleManager()
        self.network_thread = network_thread

        self.field = field
        self.is_my_turn = is_my_turn

        self.empty_cells_left = config.FIELD_SIZE ** 2 - config.NUM_MINES
        self.mine_cells_left = config.NUM_MINES
        self.my_score = 0
        self.opponent_score = 0

        self.delayTimer = QTimer()
        self.delayTimer.setSingleShot(True)

    def make_move(self, button, x, y):
        if not self.is_my_turn or button.is_flagged:
            return
        self.is_my_turn = False
        cell = self.field[x][y]
        self.my_score += config.SCORE_MINE if cell == 9 else config.SCORE_EMPTY

        Thread(target=self.network_thread.send_move, args=(x, y), daemon=True).start()
        self.open_cells_recursively(x, y) if cell == 0 else self.open_cell(x, y)
        if cell != 9:
            self.particle_manager.emit_particle(button.parentWidget(), button.geometry().topLeft())
        self.wait_for_opponent_move()
        self.delayTimer.start(config.TURN_DELAY_MS)

    def open_cell(self, x, y):
        self.update_game_state(x, y, self.field[x][y])
        self.field[x][y] = -1

    def open_cells_recursively(self, x, y):
        if self.field[x][y] not in (-1, 0):
            return

        for i in range(max(0, x - 1), min(config.FIELD_SIZE, x + 2)):
            for j in range(max(0, y - 1), min(config.FIELD_SIZE, y + 2)):
                if self.field[i][j] == -1:
                    continue
                cell = self.field[i][j]
                self.open_cell(i, j)
                if cell == 0:
                    self.open_cells_recursively(i, j)

    def update_game_state(self, x, y, item):
        self.empty_cells_left -= (item != 9)
        self.mine_cells_left -= (item == 9)
        content = ('empty', *range(1, 9), 'mine')[item]
        self.signal_emitter.move_received.emit((x, y, content))
        if self.mine_cells_left <= 0 or self.empty_cells_left <= 0:
            self.end_game()

    def wait_for_opponent_move(self):
        Thread(target=self.network_thread.listen_move, daemon=True).start()

    def receive_opponent_move(self, data):
        x, y = data
        cell = self.field[x][y]
        self.opponent_score += config.SCORE_MINE if cell == 9 else config.SCORE_EMPTY
        self.is_my_turn = True
        self.open_cells_recursively(x, y) if cell == 0 else self.open_cell(x, y)
        self.delayTimer.start(config.TURN_DELAY_MS)

    def end_game(self):
        result = 2 if self.my_score == self.opponent_score else 1 if self.my_score < self.opponent_score else 0
        game_status = ("Мин не осталось! ", "Все клетки без мин открыты! ")[
            self.empty_cells_left < self.mine_cells_left]
        winner_status = ("Вы выиграли!", "Вы проиграли!", "Ничья!")[result]
        self.signal_emitter.game_ended.emit((game_status, winner_status))

    @staticmethod
    def generate_field():
        size = config.FIELD_SIZE
        positions = [(i, j) for i in range(size) for j in range(size)]
        random.shuffle(positions)

        field = [[0 for _ in range(size)] for _ in range(size)]

        for i, j in positions[:config.NUM_MINES]:
            field[i][j] = 9

        for i in range(size):
            for j in range(size):
                if field[i][j] == 9:
                    continue
                field[i][j] = sum(
                    1 for ni in range(max(0, i - 1), min(size, i + 2))
                    for nj in range(max(0, j - 1), min(size, j + 2))
                    if field[ni][nj] == 9
                )
        return field
