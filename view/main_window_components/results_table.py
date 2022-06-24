from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from controllers.match_controller import getFixtures
from view.match_window import MatchWindow
from utils.font_utils import get_font
from view.team_window import TeamWindow


class BoldItem(QTableWidgetItem):
    def __init__(self, text):
        super(BoldItem, self).__init__()
        self.set_content(text)
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)

    def set_content(self, text):
        self.setText(text)
        font = get_font(bold=True)
        self.setFont(font)
        self.setTextAlignment(Qt.AlignCenter)


class ResultsTable(QTableWidget):
    def __init__(self, game_week: str):
        super(ResultsTable, self).__init__()
        self.team_window = None
        self.match_window = None
        self.set_col_row(game_week)
        self.load_data(game_week)
        self.set_style()
        self.itemDoubleClicked.connect(self.clickingHandler)

    def set_col_row(self, game_week):
        if game_week == "All GWs":
            self.setRowCount(380 + 38)
        else:
            self.setRowCount(11)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(("Time", "Home", "FT", "Away", "Stadium"))

    def load_data(self, game_week):
        self.clearSpans()
        fixtures_data = getFixtures(game_week)
        if game_week == "All GWs":
            gw_list = [i for i in range(1, 39)]
        else:
            gw_list = [int(game_week)]

        for i in range(len(gw_list)):
            gw = int(gw_list[i])
            base_row = i*11
            game_week_row = BoldItem(f"GAME WEEK {gw}")
            game_week_row.setBackground(QColor(233, 0, 82))
            game_week_row.setForeground(QColor(255, 255, 255))
            game_week_row.setTextAlignment(Qt.AlignCenter)

            self.setItem(base_row, 0, game_week_row)
            self.setSpan(base_row, 0, 1, 5)

            gw_matches = fixtures_data[i*11: i*11 + 10]
            for j in range(len(gw_matches)):
                match = gw_matches[j]
                date_time = match["m.date_GMT"]
                stadium_name = match["m.stadium_name"].split("(")[0].strip()
                home_team = match["m.home_team_name"]
                away_team = match["m.away_team_name"]
                home_team_score = int(float(match["h.home_team_goal_count"]))
                away_team_score = int(float(match["a.away_team_goal_count"]))
                ft_score = QTableWidgetItem(str(home_team_score) + " - " + str(away_team_score))
                ft_score.setTextAlignment(Qt.AlignCenter)
                ft_score.setFlags(ft_score.flags() ^ Qt.ItemIsEditable)

                self.setItem(base_row + j + 1, 0, QTableWidgetItem(date_time))
                self.setItem(base_row + j + 1, 1, BoldItem(home_team))
                self.setItem(base_row + j + 1, 2, ft_score)
                self.setItem(base_row + j + 1, 3, BoldItem(away_team))
                self.setItem(base_row + j + 1, 4, QTableWidgetItem(stadium_name))

    def set_style(self):
        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()

    def clickingHandler(self, item: QTableWidgetItem):
        item_col = item.column()
        item_row = item.row()
        if item_col == 2:
            # MATCH INFO
            home_team = self.item(item_row, item_col - 1).text()
            away_team = self.item(item_row, item_col + 1).text()
            self.match_window = MatchWindow(home_team, away_team)
            self.match_window.show()
        if item_col == 1 or item_col == 3:
            team_name = item.text()
            self.team_window = TeamWindow(team_name)
            self.team_window.show()



