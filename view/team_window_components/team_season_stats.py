from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QVBoxLayout, \
    QWidget

from controllers.match_controller import getTeamBiggestWin
from controllers.player_controller import getTeamTopScorers, getTeamTopAssists
from utils.font_utils import get_font
from view.match_window import MatchWindow


def insert_row(table: QTableWidget, row: int, match: dict, isHome: bool):
    date_time = match["m.date_GMT"].split("-")[0].strip()
    stadium_name = match["m.stadium_name"].split("(")[0].strip()
    home_team = QTableWidgetItem(match["m.home_team_name"])
    away_team = QTableWidgetItem(match["m.away_team_name"])

    bold = get_font(bold=True, pointSize=13)
    home_team.setFont(bold) if isHome else away_team.setFont(bold)

    home_team_score = int(float(match["h.home_team_goal_count"]))
    away_team_score = int(float(match["a.away_team_goal_count"]))
    ft_score = QTableWidgetItem(str(home_team_score) + " - " + str(away_team_score))
    ft_score.setTextAlignment(Qt.AlignCenter)
    ft_score.setFlags(ft_score.flags() ^ Qt.ItemIsEditable)
    ft_score.setBackground(QColor(233, 0, 82))
    ft_score.setForeground(QColor(255, 255, 255))

    table.setItem(row, 0, QTableWidgetItem(date_time))
    table.setItem(row, 1, home_team)
    table.setItem(row, 2, ft_score)
    table.setItem(row, 3, away_team)
    table.setItem(row, 4, QTableWidgetItem(stadium_name))


class TopPlayerTable(QTableWidget):
    def __init__(self, player_name: str, record: int):
        super(TopPlayerTable, self).__init__()
        self.set_style()
        self.load_data(player_name, record)

    def set_style(self):
        self.setColumnCount(2)
        self.setRowCount(1)
        self.setFixedHeight(50)

        self.horizontalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setColumnWidth(1, 80)
        self.verticalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def load_data(self, player_name, record):
        player_name = QTableWidgetItem(player_name)
        font = get_font(True, 14)
        player_name.setFont(font)
        player_name.setBackground(QColor(233, 0, 82))
        player_name.setForeground(QColor(255, 255, 255))
        player_name.setTextAlignment(Qt.AlignCenter)
        self.setItem(0, 0, player_name)

        record = QTableWidgetItem(str(record))
        record.setForeground(QColor(233, 0, 82))
        bold = get_font(True, 13)
        record.setFont(bold)
        record.setTextAlignment(Qt.AlignCenter)
        self.setItem(0, 1, record)


class ReportTableItem(QTableWidgetItem):
    def __init__(self, text: str, is_label: bool):
        super(ReportTableItem, self).__init__()
        self.load_data(text)
        self.set_style(is_label)

    def load_data(self, text):
        self.setText(text)

    def set_style(self, is_label):
        self.setTextAlignment(Qt.AlignCenter)
        if is_label:
            self.setBackground(QColor(233, 0, 82))
            self.setForeground(QColor(255, 255, 255))
        else:
            self.setForeground(QColor(233, 0, 82))
            font = get_font(True, 13)
            self.setFont(font)


class TeamWindowLabel(QLabel):
    def __init__(self, text):
        super(TeamWindowLabel, self).__init__()
        self.season_records_table = QTableWidget()
        self.load_data(text)
        self.set_style()

    def load_data(self, text):
        self.setText(text)

    def set_style(self):
        font = get_font(bold=True, pointSize=15)
        self.setFont(font)
        self.setStyleSheet("QLabel { background-color : #00ff85; color : #38003c; }")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(30)


class TeamSeasonStats(QWidget):
    def __init__(self, team_data):
        super(TeamSeasonStats, self).__init__()
        self.match_window = None
        self.season_records_table = QTableWidget()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.load_data(team_data)

    def load_data(self, team_data):
        self.load_season_stats(team_data)
        self.load_season_records(team_data)
        self.load_top_scorers(team_data['common_name'])
        self.load_top_assists(team_data['common_name'])

    def load_season_stats(self, team_data):
        # Set table size
        team_season_report = QTableWidget()
        team_season_report.setColumnCount(6)
        team_season_report.setRowCount(3)

        # League Position
        league_position_label = ReportTableItem("League Position", True)
        team_season_report.setItem(0, 0, league_position_label)
        team_season_report.setSpan(0, 0, 1, 3)

        league_position = ReportTableItem(team_data['league_position'], False)
        team_season_report.setItem(0, 3, league_position)
        team_season_report.setSpan(0, 3, 1, 3)

        # W-D-L
        win_label = ReportTableItem("W", True)
        team_season_report.setItem(1, 0, win_label)
        win_matches = ReportTableItem(team_data['wins'], False)
        team_season_report.setItem(1, 1, win_matches)

        draw_label = ReportTableItem("D", True)
        team_season_report.setItem(1, 2, draw_label)
        draw_matches = ReportTableItem(team_data['draws'], False)
        team_season_report.setItem(1, 3, draw_matches)

        loss_label = ReportTableItem("L", True)
        team_season_report.setItem(1, 4, loss_label)
        loss_matches = ReportTableItem(team_data['losses'], False)
        team_season_report.setItem(1, 5, loss_matches)

        # GS - GC
        goals_scored_label = ReportTableItem("Goals Scored", True)
        team_season_report.setItem(2, 0, goals_scored_label)
        team_season_report.setSpan(2, 0, 1, 2)
        goals_scored = ReportTableItem(team_data['goals_scored'], False)
        team_season_report.setItem(2, 2, goals_scored)

        goals_conceded_label = ReportTableItem("Goals Conceded", True)
        team_season_report.setItem(2, 3, goals_conceded_label)
        team_season_report.setSpan(2, 3, 1, 2)
        goals_conceded = ReportTableItem(team_data['goals_conceded'], False)
        team_season_report.setItem(2, 5, goals_conceded)

        team_season_report.setFixedHeight(100)
        team_season_report.horizontalHeader().hide()
        team_season_report.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        team_season_report.verticalHeader().hide()
        team_season_report.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(team_season_report)

    def load_season_records(self, team_data):
        self.season_records_table.setColumnCount(5)
        self.season_records_table.setRowCount(4)
        self.season_records_table.setFixedHeight(150)

        home_biggest_win, away_biggest_win = getTeamBiggestWin(team_data['common_name'])
        title_font = get_font(bold=True, pointSize=16)

        home_biggest_win_title = QTableWidgetItem("Home Biggest Win")
        home_biggest_win_title.setBackground(QColor(0, 255, 133))
        home_biggest_win_title.setForeground(QColor(56, 0, 60))
        home_biggest_win_title.setFont(title_font)
        home_biggest_win_title.setTextAlignment(Qt.AlignCenter)

        self.season_records_table.setItem(0, 0, home_biggest_win_title)
        self.season_records_table.setSpan(0, 0, 1, 5)
        insert_row(self.season_records_table, 1, home_biggest_win, isHome=True)

        away_biggest_win_title = QTableWidgetItem("Away Biggest Win")
        away_biggest_win_title.setBackground(QColor(0, 255, 133))
        away_biggest_win_title.setForeground(QColor(56, 0, 60))
        away_biggest_win_title.setFont(title_font)
        away_biggest_win_title.setTextAlignment(Qt.AlignCenter)

        self.season_records_table.setItem(2, 0, away_biggest_win_title)
        self.season_records_table.setSpan(2, 0, 1, 5)
        insert_row(self.season_records_table, 3, away_biggest_win, isHome=False)

        self.season_records_table.horizontalHeader().hide()
        self.season_records_table.verticalHeader().hide()
        self.season_records_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.season_records_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.season_records_table.doubleClicked.connect(self.clickHandling)

        self.layout.addWidget(self.season_records_table)

    def load_top_scorers(self, team_common_name):
        self.layout.addWidget(TeamWindowLabel("Top Score"))
        team_top_scorer = getTeamTopScorers(team_common_name)[0]
        team_top_scorer_table = TopPlayerTable(team_top_scorer[0], team_top_scorer[1])
        self.layout.addWidget(team_top_scorer_table)

    def load_top_assists(self, team_common_name):
        self.layout.addWidget(TeamWindowLabel("Top Assist"))
        team_top_assist = getTeamTopAssists(team_common_name)[0]
        team_top_assist_table = TopPlayerTable(team_top_assist[0], team_top_assist[1])
        self.layout.addWidget(team_top_assist_table)

    def clickHandling(self, item: QTableWidgetItem):
        item_row = item.row()
        item_col = item.column()
        if item.column() == 2:
            home_team = self.season_records_table.item(item_row, item_col - 1).text()
            away_team = self.season_records_table.item(item_row, item_col + 1).text()
            self.match_window = MatchWindow(home_team, away_team)
            self.match_window.show()
