from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, QLabel, QButtonGroup


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._count_cells = 9
        self._count_colors = 7
        self._count_balls_line = 5
        self.label1 = QLabel()
        self.label1.setText("Size of Area")
        self.label2 = QLabel()
        self.label2.setText("Count of colors")
        self.label3 = QLabel()
        self.label3.setText("Count of balls in line")
        self.setGeometry(0, 0, 400, 200)
        self.setWindowTitle("Settings")
        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.label1, 0, 0)
        chooseSize1 = QRadioButton("9 X 9")
        chooseSize1.area = 9
        chooseSize1.setChecked(True)
        layout.addWidget(chooseSize1, 1, 0)

        chooseSize2 = QRadioButton("11 X 11")
        chooseSize2.area = 11
        layout.addWidget(chooseSize2, 1, 1)

        chooseSize3 = QRadioButton("13 X 13")
        chooseSize3.area = 13
        layout.addWidget(chooseSize3, 1, 2)

        self.button_group = QButtonGroup()
        self.button_group.addButton(chooseSize1)
        self.button_group.addButton(chooseSize2)
        self.button_group.addButton(chooseSize3)
        self.button_group.buttonClicked.connect(self.on_clicked1)
        layout.addWidget(self.label2, 2, 0)

        chooseColors1 = QRadioButton("7")
        chooseColors1.count = 7
        layout.addWidget(chooseColors1, 3, 0)
        chooseColors1.setChecked(True)

        chooseColors2 = QRadioButton("6")
        chooseColors2.count = 6
        layout.addWidget(chooseColors2, 3, 1)

        chooseColors3 = QRadioButton("5")
        chooseColors3.count = 5
        layout.addWidget(chooseColors3, 3, 2)

        self.button_group1 = QButtonGroup()
        self.button_group1.addButton(chooseColors1)
        self.button_group1.addButton(chooseColors2)
        self.button_group1.addButton(chooseColors3)
        self.button_group1.buttonClicked.connect(self.on_clicked2)

        layout.addWidget(self.label3, 4, 0)
        countBalls1 = QRadioButton("4")
        countBalls1.count = 4
        layout.addWidget(countBalls1, 5, 0)

        countBalls2 = QRadioButton("5")
        countBalls2.count = 5
        layout.addWidget(countBalls2, 5, 1)
        countBalls2.setChecked(True)

        countBalls3 = QRadioButton("6")
        countBalls3.count = 6
        layout.addWidget(countBalls3, 5, 2)

        self.button_group2 = QButtonGroup()
        self.button_group2.addButton(countBalls1)
        self.button_group2.addButton(countBalls2)
        self.button_group2.addButton(countBalls3)
        self.button_group2.buttonClicked.connect(self.on_clicked3)

    def on_clicked1(self, button):
        self._count_cells = button.area

    def on_clicked2(self, button):
        self._count_colors = button.count

    def on_clicked3(self, button):
        self._count_balls_line = button.count

    @property
    def count_cells(self):
        return self._count_cells

    @property
    def count_colors(self):
        return self._count_colors

    @property
    def count_balls_line(self):
        return self._count_balls_line
