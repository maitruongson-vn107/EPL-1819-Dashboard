from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QComboBox, QVBoxLayout,
                             QTableWidget, QTableWidgetItem)

from controllers.player_controller import getTeamAllPlayers
from utils.font_utils import get_font

position_dict = {
    "Defender": "DF",
    "Midfielder": "MF",
    "Forward": "FW",
    "Goalkeeper": "GK"
}


class TeamPlayersTable(QTableWidget):
    def __init__(self, team_common_name, sort_by="Full Name", opt="Overall"):
        super(TeamPlayersTable, self).__init__()
        self.players_list = getTeamAllPlayers(team_common_name)
        self.set_col_row(self.players_list)
        self.load_data(self.players_list, sort_by, opt)
        self.set_style()

    def set_col_row(self, players_list):
        self.setColumnCount(10)
        self.setRowCount(len(players_list))
        self.setHorizontalHeaderLabels(
            ("NAME", "D.O.B", "POS", "NATIONALITY", "APP", "MINS", "G", "A", "", ""))
        yellow_header = QTableWidgetItem('')
        yellow_header.setBackground(QColor(253, 218, 13))
        self.setHorizontalHeaderItem(8, yellow_header)

        red_header = QTableWidgetItem('')
        red_header.setBackground(QColor(210, 43, 43))
        self.setHorizontalHeaderItem(9, red_header)

    def load_data(self, players_list, sort_by, opt, desc=True):
        opt = opt.lower()
        # Sort and Filter Players List
        sorted_players_list = []
        if sort_by in ["Appearances", "Minutes Played", "Goals", "Assists"]:
            sort_by = sort_by.lower().replace(" ", "_")
            sort_by += "_" + opt
            sorted_players_list = sorted(players_list, key=lambda p: int(p[sort_by]), reverse=desc)
        if sort_by in ["Full Name", "Position", "Nationality"]:
            sort_by = sort_by.lower().replace(" ", "_")
            sorted_players_list = sorted(players_list, key=lambda p: p[sort_by], reverse=desc)
        if sort_by in ["Yellow Cards", "Red Cards"]:
            sort_by = sort_by.lower().replace(" ", "_") + "_overall"
            sorted_players_list = sorted(players_list, key=lambda p: int(p[sort_by]), reverse=desc)
        if sort_by == "D.O.B":
            sort_by = "birthday_GMT"
            sorted_players_list = sorted(players_list, key=lambda p: p[sort_by], reverse=desc)

        if sort_by == "Position":
            if desc:
                sorted_players_list = [p for p in players_list if p["position"] == "Forward"]
                sorted_players_list += [p for p in players_list if p["position"] == "Midfielder"]
                sorted_players_list += [p for p in players_list if p["position"] == "Defender"]
                sorted_players_list += [p for p in players_list if p["position"] == "Goalkeeper"]
            else:
                sorted_players_list = [p for p in players_list if p["position"] == "Goalkeeper"]
                sorted_players_list += [p for p in players_list if p["position"] == "Defender"]
                sorted_players_list += [p for p in players_list if p["position"] == "Midfielder"]
                sorted_players_list += [p for p in players_list if p["position"] == "Forward"]

        # Load player list
        for i in range(len(sorted_players_list)):
            player = sorted_players_list[i]
            self.load_one_row(player, i, opt)

    def load_one_row(self, one_player: dict, row: int, opt: str):
        # Full Name
        full_name = QTableWidgetItem(one_player["full_name"])
        full_name.setFont(get_font(bold=True, pointSize=13))

        # DOB
        dob = QTableWidgetItem(one_player["birthday_GMT"])

        # Position
        position = QTableWidgetItem(position_dict[one_player["position"]])
        position.setTextAlignment(Qt.AlignCenter)

        nationality = QTableWidgetItem(one_player["nationality"])

        # Appearances
        appearances = QTableWidgetItem(str(int(float(one_player["appearances_" + opt]))))
        appearances.setTextAlignment(Qt.AlignCenter)

        # Minutes Played
        minutes_played = QTableWidgetItem(str(int(float(one_player["minutes_played_" + opt]))))
        minutes_played.setTextAlignment(Qt.AlignCenter)

        # Goals
        goals = QTableWidgetItem(str(int(float(one_player["goals_" + opt]))))
        goals.setTextAlignment(Qt.AlignCenter)

        # Assists
        assists = QTableWidgetItem(str(int(float(one_player["assists_" + opt]))))
        assists.setTextAlignment(Qt.AlignCenter)

        # Yellow Cards
        yellow_cards = QTableWidgetItem(str(int(float(one_player["yellow_cards_overall"]))))
        yellow_cards.setTextAlignment(Qt.AlignCenter)

        # Red Cards
        red_cards = QTableWidgetItem(str(int(float(one_player["red_cards_overall"]))))
        red_cards.setTextAlignment(Qt.AlignCenter)

        self.setItem(row, 0, full_name)
        self.setItem(row, 1, dob)
        self.setItem(row, 2, position)
        self.setItem(row, 3, nationality)
        self.setItem(row, 4, appearances)
        self.setItem(row, 5, minutes_played)
        self.setItem(row, 6, goals)
        self.setItem(row, 7, assists)
        self.setItem(row, 8, yellow_cards)
        self.setItem(row, 9, red_cards)

    def set_style(self):
        self.setColumnWidth(0, 250)
        for col in range(2, 10):
            if col != 3:
                self.setColumnWidth(col, 60)


class TeamPlayersListTab(QWidget):
    def __init__(self, team_common_name):
        super(TeamPlayersListTab, self).__init__()
        self.team_common_name = team_common_name
        self.player_list_table = None
        self.opt = "Overall"
        self.sort_by = "Full Name"
        self.hbox = QHBoxLayout()
        self.home_away_filter = QComboBox()
        self.sort_by_filter = QComboBox()
        self.sort_order_filter = QComboBox()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.load_data(team_common_name)

    def load_data(self, team_common_name):
        # Load Filters
        self.load_filters()

        # Load Table
        self.player_list_table = TeamPlayersTable(team_common_name)
        self.layout.addWidget(self.player_list_table)

    def load_filters(self):
        # Home - Away Filter
        self.home_away_filter.setFixedWidth(200)
        self.home_away_filter.addItems(["Overall", "Home", "Away"])
        self.home_away_filter.setStyleSheet("QComboBox QAbstractItemView { "
                                            "border: 1px solid grey; "
                                            "background: white; "
                                            "selection-background-color: #e90052;}")
        self.home_away_filter.currentIndexChanged.connect(self.home_away_filter_handler)

        home_away_filter_label = QLabel("Filter by:")
        home_away_filter_label.setAlignment(Qt.AlignRight)
        self.hbox.addWidget(home_away_filter_label)
        self.hbox.addWidget(self.home_away_filter)

        # Sort by
        self.sort_by_filter.setFixedWidth(200)
        self.sort_by_filter.addItems(["Full Name", "D.O.B", "Position", "Nationality", "Appearances",
                                      "Minutes Played", "Goals", "Assists", "Yellow Cards", "Red Cards"])
        self.sort_by_filter.setStyleSheet("QComboBox QAbstractItemView { "
                                          "border: 1px solid grey; "
                                          "background: white; "
                                          "selection-background-color: #e90052;}")
        self.sort_by_filter.currentIndexChanged.connect(self.sort_by_filter_handler)

        sort_by_filter_label = QLabel("Sort by:")
        sort_by_filter_label.setAlignment(Qt.AlignRight)

        self.sort_order_filter.setFixedWidth(80)
        self.sort_order_filter.addItems(["A-Z", "Z-A"])
        self.sort_order_filter.setStyleSheet("QComboBox QAbstractItemView { "
                                             "border: 1px solid grey; "
                                             "background: white; "
                                             "selection-background-color: #e90052;}")
        self.sort_order_filter.currentIndexChanged.connect(self.sort_order_filter_handler)

        self.hbox.addWidget(sort_by_filter_label)
        self.hbox.addWidget(self.sort_by_filter)
        self.hbox.addWidget(self.sort_order_filter)
        self.layout.addLayout(self.hbox)

    def home_away_filter_handler(self):
        self.opt = self.home_away_filter.currentText()
        self.sort_by = self.sort_by_filter.currentText()
        sort_order = self.sort_order_filter.currentText()
        if sort_order == "A-Z":
            desc = False
        else:
            desc = True
        player_list = getTeamAllPlayers(self.team_common_name)
        self.player_list_table.load_data(player_list, self.sort_by, self.opt, desc)

    def sort_by_filter_handler(self):
        self.opt = self.home_away_filter.currentText()
        self.sort_by = self.sort_by_filter.currentText()
        sort_order = self.sort_order_filter.currentText()
        if sort_order == "A-Z":
            desc = False
        else:
            desc = True
        player_list = getTeamAllPlayers(self.team_common_name)
        self.player_list_table.load_data(player_list, self.sort_by, self.opt, desc)

    def sort_order_filter_handler(self):
        self.opt = self.home_away_filter.currentText()
        self.sort_by = self.sort_by_filter.currentText()
        sort_order = self.sort_order_filter.currentText()
        if sort_order == "A-Z":
            desc = False
        else:
            desc = True
        player_list = getTeamAllPlayers(self.team_common_name)
        self.player_list_table.load_data(player_list, self.sort_by, self.opt, desc)
