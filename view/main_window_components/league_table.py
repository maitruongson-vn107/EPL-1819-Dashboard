from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from controllers.team_controller import getTeamsData
from data_loaders.utils import getTeamLogo
from utils.font_utils import get_font
from view.team_window import TeamWindow


class LeagueTable(QTableWidget):
    def __init__(self, opt="All Matches"):
        super().__init__()
        self.team_window = None
        self.setRowCount(20)
        self.setColumnCount(10)
        columns = ("", "Club Name", "Played", "W", "D", "L", "GF", "GA", "GD", "Points")
        self.setHorizontalHeaderLabels(columns)
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 250)
        self.load_data(opt)
        self.set_style()
        self.itemDoubleClicked.connect(self.click_handler)

    def set_style(self):
        for col in range(1, self.columnCount()):
            self.item(0, col).setBackground(QtGui.QColor(238, 206, 0))
        for row in range(1, 4):
            for col in range(1, self.columnCount()):
                self.item(row, col).setBackground(QtGui.QColor(153, 204, 255))
        for row in range(4, 6):
            for col in range(1, self.columnCount()):
                self.item(row, col).setBackground(QtGui.QColor(255, 204, 153))
        for row in range(17, 20):
            for col in range(1, self.columnCount()):
                self.item(row, col).setBackground(QtGui.QColor(255, 153, 153))

    def load_data(self, opt):
        cols = ["league_position", "wins", "draws", "losses",
                "goals_scored", "goals_conceded", "goal_difference", "points"]
        matches_played = "38"

        if opt == "Home Only":
            cols = [col + "_home" for col in cols]
            matches_played = "19"
        if opt == "Away Only":
            cols = [col + "_away" for col in cols]
            matches_played = "19"

        teams_data = getTeamsData()
        for team in teams_data:
            row = int(team[cols[0]]) - 1    # league_position
            logo_widget = getTeamLogo(team["common_name"])
            logo_widget.setAlignment(Qt.AlignHCenter)
            self.setCellWidget(row, 0, logo_widget)
            self.setItem(row, 1, QTableWidgetItem(team["common_name"]))
            self.setItem(row, 2, QTableWidgetItem(matches_played))
            self.setItem(row, 3, QTableWidgetItem(team[cols[1]]))   # wins
            self.setItem(row, 4, QTableWidgetItem(team[cols[2]]))   # draws
            self.setItem(row, 5, QTableWidgetItem(team[cols[3]]))   # losses
            self.setItem(row, 6, QTableWidgetItem(team[cols[4]]))   # goals scored
            self.setItem(row, 7, QTableWidgetItem(team[cols[5]]))   # goals conceded
            self.setItem(row, 8, QTableWidgetItem(team[cols[6]]))   # goals difference
            font = get_font(bold=True)
            point_item = QTableWidgetItem(str(team["points"]))
            point_item.setFont(font)
            self.setItem(row, 9, point_item)

    def click_handler(self, item: QTableWidgetItem):
        if item.column() == 0 or item.column() == 1:
            team_common_name = self.item(item.row(), 1).text()
            self.team_window = TeamWindow(team_common_name)
            self.team_window.show()