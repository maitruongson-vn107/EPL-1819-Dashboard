import sys

import PyQt5.QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QApplication, QHBoxLayout, QComboBox, QVBoxLayout,
                             QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView)

from utils.font_utils import get_font


def get_stats_items(home_stat: str, away_stat: str, is_float=False):
    if is_float:
        home_stat = float(home_stat)
        away_stat = float(away_stat)
    else:
        home_stat = int(float(home_stat))
        away_stat = int(float(away_stat))
    home_stat_item = QTableWidgetItem(str(home_stat))
    home_stat_item.setTextAlignment(Qt.AlignCenter)

    away_stat_item = QTableWidgetItem(str(away_stat))
    away_stat_item.setTextAlignment(Qt.AlignCenter)

    font = get_font(bold=True)
    home_stat_item.setFont(font)
    away_stat_item.setFont(font)

    if home_stat > away_stat:
        home_stat_item.setForeground(QColor(233, 0, 82))
    if home_stat < away_stat:
        away_stat_item.setForeground(QColor(233, 0, 82))

    return home_stat_item, away_stat_item


class MatchStatsTable(QTableWidget):
    def __init__(self, match_data):
        super(MatchStatsTable, self).__init__()
        self.set_col_row()
        self.load_data(match_data)
        self.set_style()

    def set_col_row(self):
        self.setColumnCount(3)
        self.setRowCount(9)

    def load_data(self, match_data):
        # Haft-time score
        home_ht_score = match_data["home_team_goal_count_half_time"]
        away_ht_score = match_data["away_team_goal_count_half_time"]
        home_ht_item, away_ht_item = get_stats_items(home_ht_score, away_ht_score)
        self.load_row(0, home_ht_item, away_ht_item, "HT Goals")

        # Possession
        home_possession = match_data["home_team_possession"]
        away_possession = match_data["away_team_possession"]
        home_possession_item, away_possession_item = get_stats_items(home_possession, away_possession, is_float=True)
        self.load_row(1, home_possession_item, away_possession_item, "Possession %")

        # Shots
        home_shots = match_data["home_team_shots"]
        away_shots = match_data["away_team_shots"]
        home_shots_item, away_shots_item = get_stats_items(home_shots, away_shots)
        self.load_row(2, home_shots_item, away_shots_item, "Shots")

        # Shots on Target
        home_shots_target = match_data["home_team_shots_on_target"]
        away_shots_target = match_data["away_team_shots_on_target"]
        home_shots_target_item, away_shots_target_item = get_stats_items(home_shots_target, away_shots_target)
        self.load_row(3, home_shots_target_item, away_shots_target_item, "Shots on target")

        # Corners
        home_corners = match_data["home_team_corner_count"]
        away_corners = match_data["away_team_corner_count"]
        home_corners_item, away_corners_item = get_stats_items(home_corners, away_corners)
        self.load_row(4, home_corners_item, away_corners_item, "Corners")

        # Fouls
        home_fouls = match_data["home_team_fouls"]
        away_fouls = match_data["away_team_fouls"]
        home_fouls_item, away_fouls_item = get_stats_items(home_fouls, away_fouls)
        self.load_row(5, home_fouls_item, away_fouls_item, "Fouls")

        # Yellow Cards
        home_yellow_cards = match_data["home_team_yellow_cards"]
        away_yellow_cards = match_data["away_team_yellow_cards"]
        home_yellow_cards_item, away_yellow_cards_item = get_stats_items(home_yellow_cards, away_yellow_cards)
        self.load_row(6, home_yellow_cards_item, away_yellow_cards_item, "Yellow cards")

        # Red Cards
        home_red_cards = match_data["home_team_red_cards"]
        away_red_cards = match_data["away_team_red_cards"]
        home_red_cards_item, away_red_cards_item = get_stats_items(home_red_cards, away_red_cards)
        self.load_row(7, home_red_cards_item, away_red_cards_item, "Red cards")

        # XG
        home_xg = match_data["team_a_xg"]
        away_xg = match_data["team_b_xg"]
        home_xg_item, away_xg_item = get_stats_items(home_xg, away_xg, is_float=True)
        self.load_row(8, home_xg_item, away_xg_item, "XG")

    def load_row(self, row: int,
                 home_stat_item: QTableWidgetItem,
                 away_stat_item: QTableWidgetItem,
                 row_name: str):
        row_name_item = QTableWidgetItem(row_name)
        row_name_item.setTextAlignment(Qt.AlignCenter)

        self.setItem(row, 0, home_stat_item)
        self.setItem(row, 1, row_name_item)
        self.setItem(row, 2, away_stat_item)

    def set_style(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
