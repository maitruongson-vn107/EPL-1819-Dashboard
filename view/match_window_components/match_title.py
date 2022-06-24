from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QLabel, QGridLayout)

from data_loaders.utils import getTeamLogo
from utils.font_utils import get_font
from view.match_window_components.team_name import TeamNameLabel


class MatchTitle(QGridLayout):
    def __init__(self, match_data):
        super(MatchTitle, self).__init__()
        self.load_data(match_data)
        self.set_style()

    def load_data(self, match_data):
        home_team_name = match_data["home_team_name"]
        away_team_name = match_data["away_team_name"]

        # get teams' logos
        home_logo = getTeamLogo(home_team_name, 80)
        home_logo.setFixedWidth(80)
        away_logo = getTeamLogo(away_team_name, 80)
        away_logo.setFixedWidth(80)

        # teams' names label
        home_team_name_label = TeamNameLabel(home_team_name)
        away_team_name_label = TeamNameLabel(away_team_name)

        # ft score
        ft_score_str = str(int(float(match_data["home_team_goal_count"]))) \
                       + " - " + \
                       str(int(float(match_data["away_team_goal_count"])))
        ft_score_label = QLabel(ft_score_str)
        ft_score_label.setAlignment(Qt.AlignCenter)
        ft_score_label.setStyleSheet("QLabel { background-color : #e90052; color : #ffffff; }")
        ft_score_label.setFixedHeight(40)
        ft_score_label.setFixedWidth(100)
        ft_score_font = get_font(bold=True, pointSize=20)
        ft_score_label.setFont(ft_score_font)

        # ht score
        ht_score_str = "HT: " \
                       + str(int(float(match_data["home_team_goal_count_half_time"]))) \
                       + " - " \
                       + str(int(float(match_data["away_team_goal_count_half_time"])))
        ht_score_label = QLabel(ht_score_str)
        ht_score_label.setAlignment(Qt.AlignCenter)
        ht_score_label.setStyleSheet("QLabel { background-color : #e90052; color : #ffffff; }")
        ht_score_label.setFixedHeight(30)
        ht_score_label.setFixedWidth(100)
        ht_score_font = get_font(bold=False, pointSize=13)
        ht_score_label.setFont(ht_score_font)

        self.addWidget(home_logo, 0, 0)
        self.addWidget(home_team_name_label, 0, 1)
        self.addWidget(ft_score_label, 0, 2)
        self.addWidget(away_team_name_label, 0, 3)
        self.addWidget(away_logo, 0, 4)
        self.addWidget(ht_score_label, 1, 2)

    def set_style(self):
        pass