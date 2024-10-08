import random
from threading import Thread

from PySide6.QtCore import Signal, QObject


class SignalEmitter(QObject):
    move_received = Signal(tuple)
    game_ended = Signal(str)


class GameLogic:
    def __init__(self, network_thread, is_my_turn):
        self.signal_emitter = SignalEmitter()
        self.network_thread = network_thread
        self.is_my_turn = is_my_turn
        self.buttons_left = 100
        self.my_score = 0
        self.opponent_score = 0

    def make_move(self, x, y):
        if not self.is_my_turn:
            return
        self.is_my_turn = False
        rnd = random.randint(0, 2)
        self.my_score += rnd - 1
        Thread(target=self.network_thread.send_move, args=(x, y, rnd), daemon=True).start()
        self.update_game_state(x, y, rnd)
        self.wait_for_opponent_move()

    def update_game_state(self, x, y, item):
        self.buttons_left -= 1
        content = ('mine', 'empty', 'cupcake')[item]
        self.signal_emitter.move_received.emit((x, y, content))
        if self.buttons_left <= 0:
            self.end_game()

    def wait_for_opponent_move(self):
        Thread(target=self.network_thread.listen_move, daemon=True).start()

    def receive_opponent_move(self, data):
        row, col, item = data
        self.opponent_score += item - 1
        self.is_my_turn = True
        self.update_game_state(row, col, item)

    def end_game(self):
        result = 2 if self.my_score == self.opponent_score else 1 if self.my_score < self.opponent_score else 0
        winner = ("Вы выиграли!", "Вы проиграли!", "Ничья!")[result]
        self.signal_emitter.game_ended.emit(winner)
