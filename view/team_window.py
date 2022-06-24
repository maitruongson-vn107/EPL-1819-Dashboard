from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout)

from controllers.team_controller import getTeamInfo
from data_loaders.utils import getTeamLogo
from utils.font_utils import get_font
from view.team_window_components.team_info_tab import TeamInfoTab


class TeamNameHeader(QLabel):
    def __init__(self, team_name):
        super(TeamNameHeader, self).__init__()
        self.load_data(team_name)
        self.set_style()

    def load_data(self, team_name):
        self.setText(team_name)

    def set_style(self):
        font = get_font(bold=True, pointSize=30)
        self.setFont(font)
        self.setStyleSheet("QLabel { background-color : #38003c; color : #00ff85; }")
        self.setAlignment(Qt.AlignCenter)


class TeamWindow(QWidget):
    def __init__(self, team_name):
        super(TeamWindow, self).__init__()
        self.team_data = getTeamInfo(team_name)
        self.layout = QGridLayout()
        self.initUI()
        self.load_data(self.team_data)

    def initUI(self):
        self.setLayout(self.layout)
        self.setGeometry(100, 100, 800, 700)

    def load_data(self, team_data):
        # LOGO
        team_logo_widget = getTeamLogo(team_data["common_name"], size=80)
        team_logo_widget.setFixedWidth(120)
        self.layout.addWidget(team_logo_widget, 0, 0, 1, 1)

        # TEAM NAME
        team_name_label = TeamNameHeader(team_data["team_name"])
        self.layout.addWidget(team_name_label, 0, 1, 1, 7)

        # GENERAL INFO
        self.load_general_info(team_data)

        # TEAM INFO TABS
        self.load_team_tabs(team_data)

    def load_general_info(self, team_data):
        general_info_label = QLabel()
        general_info_label.setText(f"Country: {team_data['country']}"
                                   f"\nHome Stadium: {team_data['stadium_name']}"
                                   f"\nAverage Attendance: {team_data['average_attendance_overall']}")
        general_info_label.setStyleSheet("QLabel { background-color : #38003c; color : #ffffff; }")
        general_info_label.setFixedHeight(60)
        general_info_label.setMargin(5)
        self.layout.addWidget(general_info_label, 1, 0, 1, 8)

    def load_team_tabs(self, team_data):
        team_info_tabs = TeamInfoTab(team_data)
        self.layout.addWidget(team_info_tabs, 2, 0, 4, 8)