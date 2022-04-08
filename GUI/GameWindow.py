from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor
from PyQt5.QtCore import Qt

from Ball import Ball
from Game import Game
from GameService import GameService
from Size import Size

from GUI.SettingsWindow import SettingsWindow


class GameWindow(QMainWindow):
    def __init__(self, w: SettingsWindow):
        super().__init__()
        self.w = w
        self.game = None
        uic.loadUi('untitled.ui', self)
        self.setWindowTitle("Lines 98")
        self.pushButton.setFixedSize(100, 100)
        self.pushButton.clicked.connect(self.start_game)
        self.label = QLabel()
        self.points = QLabel()
        canvas = QPixmap(720, 720)
        self.label.setPixmap(canvas)
        layout = QGridLayout(self.centralwidget)
        layout.addWidget(self.pushButton, 0, 0, alignment=Qt.AlignCenter)
        layout.addWidget(self.points, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.label, 1, 0)

    def start_game(self):
        self.game = Game(self.w.count_cells, self.w.count_colors, self.w.count_balls_line)
        GameService.start_game(self.game)
        self.draw_game()
        self.pushButton.setText("Restart")
        self.points.setText(str(self.game.points))

    def draw_cells(self):
        size = 720 / self.game.size
        painter = QPainter(self.label.pixmap())
        pen = QPen()
        painter.setBrush(QColor(153, 154, 153))
        painter.drawRect(0, 0, 720, 720)
        if self.game.choosing_cell is not None:
            painter.setBrush(QColor(45, 45, 45))
            painter.drawRect(self.game.choosing_cell[1] * size, self.game.choosing_cell[0] * size, size, size)
        pen.setWidth(3)
        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)
        for i in range(1, self.game.size):
            painter.drawLine(i * size, 0, i * size, 720)
            painter.drawLine(0, i * size, 720, i * size)

        painter.end()
        self.update()

    def draw_game(self):
        self.draw_cells()
        self.draw_balls()

    def draw_balls(self):
        size = 720 / self.game.size
        painter = QPainter(self.label.pixmap())
        for key in self.game.area.keys():
            if isinstance(self.game.area.get(key), Ball):
                ball = self.game.area.get(key)
                painter.setBrush(QColor(ball.color.value[0], ball.color.value[1], ball.color.value[2]))
                if ball.size == Size.big:
                    painter.drawEllipse(key[1] * size, key[0] * size, size, size)
                else:
                    painter.drawEllipse(key[1] * size + size / 4, key[0] * size + size / 4, size / 2, size / 2)

    def mousePressEvent(self, event):
        if self.game is not None:
            size = 720 / self.game.size
            GameService.move(self.game, (int(event.y() - self.label.y()) // size, int(event.x() - self.label.x()) // size))
            self.draw_game()
            self.points.setText(str(self.game.points))
            if GameService.is_game_over(self.game):
                self.points.setText("You lose: " + str(self.game.points))
                self.game = None
