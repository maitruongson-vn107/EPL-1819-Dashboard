from PyQt5.QtWidgets import QTabWidget

from view.team_window_components.team_player_list import TeamPlayersListTab
from view.team_window_components.team_season_results import TeamSeasonResults
from view.team_window_components.team_season_stats import TeamSeasonStats


class TeamInfoTab(QTabWidget):
    def __init__(self, team_data):
        super(TeamInfoTab, self).__init__()
        self.season_results = None
        self.season_stats_tab = None
        self.players_list_tab = None
        self.load_data(team_data)
        self.set_style()

    def load_data(self, team_data):
        self.season_stats_tab = TeamSeasonStats(team_data)
        self.addTab(self.season_stats_tab, "SEASON OVERVIEW")

        self.season_results = TeamSeasonResults(team_data["common_name"])
        self.addTab(self.season_results, "RESULTS")

        self.players_list_tab = TeamPlayersListTab(team_data["common_name"])
        self.addTab(self.players_list_tab, "PLAYERS")

    def set_style(self):
        stylesheet = "QTabBar::tab:selected {background: #00ff85; color: #38003c} "
        self.setStyleSheet(stylesheet)