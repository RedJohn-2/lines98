from PyQt5.QtWidgets import QApplication
from GUI.GameWindow import GameWindow
from GUI.SettingsWindow import SettingsWindow


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w1 = SettingsWindow()
    w1.show()
    w = GameWindow(w1)
    w.show()
    sys.exit(app.exec_())
