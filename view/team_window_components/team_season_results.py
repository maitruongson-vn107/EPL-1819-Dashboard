from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from controllers.match_controller import getAllMatchesByTeam
from utils.font_utils import get_font
from view.match_window import MatchWindow


class TeamSeasonResults(QTableWidget):
    def __init__(self, team_common_name):
        super(TeamSeasonResults, self).__init__()
        self.team_window = None
        self.match_window = None
        self.all_matches = getAllMatchesByTeam(team_common_name)
        self.set_col_row()
        self.load_data(self.all_matches, team_common_name)
        self.itemDoubleClicked.connect(self.clickingHandler)

    def set_col_row(self):
        self.setColumnCount(6)
        self.setRowCount(38)
        self.setHorizontalHeaderLabels(("GW", "DATE", "HOME", "FT", "AWAY", "STADIUM"))
        self.setColumnWidth(0, 30)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(4, 200)
        self.horizontalHeader().setStretchLastSection(QHeaderView.Stretch)
        self.verticalHeader().hide()

    def load_data(self, all_matches, team_common_name):
        for match in all_matches:
            self.load_one_row(match, team_common_name)

    def load_one_row(self, one_match: dict, team_common_name: str):
        row = int(one_match["m.game_week"]) - 1
        # Game Week
        gw = QTableWidgetItem(one_match["m.game_week"])
        gw.setTextAlignment(Qt.AlignCenter)
        gw.setForeground(QColor(56, 0, 60))
        gw.setBackground(QColor(0, 255, 133))
        gw.setFont(get_font(bold=True, pointSize=13))

        # Date
        date = QTableWidgetItem(one_match["m.date_GMT"].split("-")[0].strip())
        date.setTextAlignment(Qt.AlignCenter)

        # Home - Away Team
        home_name = QTableWidgetItem(one_match["m.home_team_name"])
        home_name.setTextAlignment(Qt.AlignCenter)
        away_name = QTableWidgetItem(one_match["m.away_team_name"])
        away_name.setTextAlignment(Qt.AlignCenter)
        stadium = QTableWidgetItem(one_match["m.stadium_name"].split("(")[0].strip())
        if one_match["m.home_team_name"] == team_common_name:
            home_name.setFont(get_font(bold=True, pointSize=13))
            home_name.setForeground(QColor(233, 0, 82))
        else:
            away_name.setFont(get_font(bold=True, pointSize=13))
            away_name.setForeground(QColor(233, 0, 82))

        # FT Score
        home_team_score = int(float(one_match["h.home_team_goal_count"]))
        away_team_score = int(float(one_match["a.away_team_goal_count"]))
        ft_score = QTableWidgetItem(str(home_team_score) + " - " + str(away_team_score))
        ft_score.setTextAlignment(Qt.AlignCenter)
        ft_score.setFlags(ft_score.flags() ^ Qt.ItemIsEditable)
        ft_score.setForeground(QColor(255, 255, 255))
        ft_score.setBackground(QColor(233, 0, 82))

        self.setItem(row, 0, gw)
        self.setItem(row, 1, date)
        self.setItem(row, 2, home_name)
        self.setItem(row, 3, ft_score)
        self.setItem(row, 4, away_name)
        self.setItem(row, 5, stadium)

    def clickingHandler(self, item: QTableWidgetItem):
        item_col = item.column()
        item_row = item.row()
        if item_col == 3:
            # MATCH INFO
            home_team = self.item(item_row, item_col - 1).text()
            away_team = self.item(item_row, item_col + 1).text()
            self.match_window = MatchWindow(home_team, away_team)
            self.match_window.show()
