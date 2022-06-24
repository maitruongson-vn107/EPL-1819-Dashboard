from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLabel

from utils.font_utils import get_font


class MainWindowBanner(QLabel):
    def __init__(self, text):
        super(MainWindowBanner, self).__init__()
        self.setGeometry(0, 0, 100, 100)
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        self.setStyleSheet("QLabel { background-color : #38003c; color : #ffffff; }")
        font = get_font(bold=True, pointSize=20)
        self.setFont(font)