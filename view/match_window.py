from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout)

from controllers.match_controller import getOneMatchByTeamNames
from view.match_window_components.match_general_info import MatchGeneralInfo
from view.match_window_components.match_stats_table import MatchStatsTable
from utils.font_utils import get_font
from view.match_window_components.match_title import MatchTitle


class MatchWindow(QWidget):
    def __init__(self, home_team: str, away_team: str):
        super(MatchWindow, self).__init__()
        self.vbox = QVBoxLayout()
        self.initUI()
        self.load_data(home_team, away_team)

    def initUI(self):
        self.setLayout(self.vbox)
        self.setGeometry(100, 100, 800, 700)

    def load_data(self, home_team, away_team):
        match_data = getOneMatchByTeamNames(home_team, away_team)
        game_week_banner = QLabel("GAME WEEK: " + match_data["game_week"])
        game_week_banner.setStyleSheet("QLabel { background-color : #38003c; color : #00ff85; }")
        gw_font = get_font(True, 18)
        game_week_banner.setAlignment(Qt.AlignCenter)
        game_week_banner.setFixedHeight(30)
        game_week_banner.setFont(gw_font)
        self.vbox.addWidget(game_week_banner)
        # Match Title
        match_title_layout = MatchTitle(match_data)
        self.vbox.addLayout(match_title_layout)
        # General Info
        match_general_label = MatchGeneralInfo(match_data)
        self.vbox.addWidget(match_general_label)
        # Match Stats Table
        # banner
        match_stats_banner = QLabel("MATCH STATS")
        match_stats_banner.setStyleSheet("QLabel { background-color : #e90052; color : #ffffff; }")
        match_stats_banner.setAlignment(Qt.AlignCenter)
        match_stats_banner.setFixedHeight(50)
        font = get_font(bold=True, pointSize=18)
        match_stats_banner.setFont(font)
        self.vbox.addWidget(match_stats_banner)

        match_stats_table = MatchStatsTable(match_data)
        self.vbox.addWidget(match_stats_table)