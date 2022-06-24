from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLabel
from utils.font_utils import get_font


class TeamNameLabel(QLabel):
    def __init__(self, text):
        super(TeamNameLabel, self).__init__()
        self.setText(text)
        self.set_style()

    def set_style(self):
        self.setStyleSheet("QLabel { background-color : #38003c; color : #ffffff; }")
        self.setFixedHeight(40)
        self.setFixedWidth(300)
        team_name_font = get_font(bold=True, pointSize=18)
        self.setFont(team_name_font)
        self.setAlignment(Qt.AlignCenter)

    def set_content(self, text):
        self.setText(text)