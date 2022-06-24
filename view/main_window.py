import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QApplication, QHBoxLayout, QComboBox)

from view.main_window_components.main_window_banner import MainWindowBanner
from view.main_window_components.results_table import ResultsTable
from view.main_window_components.league_table import LeagueTable
from view.main_window_components.top_stats_tab import TopStatsTab


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.table_filter_label = QLabel()
        self.table_filter_layout = QHBoxLayout()
        self.table_filter = QComboBox()
        self.team_table = None

        self.results_filter_layout = QHBoxLayout()
        self.results_filter_label = QLabel()
        self.results_filter = QComboBox()
        self.results_table = None
        self.initUI()

    def table_filter_change(self):
        opt = self.table_filter.currentText()
        self.team_table.load_data(opt)
        self.team_table.set_style()

    def results_filter_change(self):
        game_week = self.results_filter.currentText().split(" ")[-1]
        if game_week == "GWs":
            game_week = "All GWs"
        self.results_table.set_col_row(game_week)
        self.results_table.load_data(game_week)

    def initUI(self):
        # MAIN LEAGUE TABLE
        # banner
        table_banner = MainWindowBanner("EPL TABLE 2018/19")

        # filter by home/away
        self.table_filter_layout = QHBoxLayout()

        self.table_filter_label = QLabel("Filters by: ")
        self.table_filter_label.setFixedWidth(200)

        self.table_filter.setFixedWidth(200)
        self.table_filter.addItems(["All Matches", "Home Only", "Away Only"])
        self.table_filter.currentIndexChanged.connect(self.table_filter_change)
        self.table_filter.setStyleSheet("QComboBox QAbstractItemView { "
                                        "border: 1px solid grey; "
                                        "background: white; "
                                        "selection-background-color: #e90052;}")

        self.table_filter_layout.addWidget(self.table_filter_label)
        self.table_filter_layout.addWidget(self.table_filter)

        # league table
        self.team_table = LeagueTable()

        # RESULTS
        # banner
        results_banner = MainWindowBanner("MATCH RESULTS")

        # filter by game week
        self.results_filter_label = QLabel("Choose GW: ")
        self.results_filter_label.setFixedWidth(200)

        self.results_filter.setFixedWidth(200)
        self.results_filter.addItem("All GWs")
        self.results_filter.addItems(["GW " + str(i) for i in range(1, 39)])
        self.results_filter.currentIndexChanged.connect(self.results_filter_change)
        self.results_filter.setStyleSheet("QComboBox QAbstractItemView { "
                                          "border: 1px solid grey; "
                                          "background: white; "
                                          "selection-background-color: #e90052;}")

        self.results_filter_layout.addWidget(self.results_filter_label)
        self.results_filter_layout.addWidget(self.results_filter)

        # results table

        self.results_table = ResultsTable(game_week='All GWs')

        # TOP STATS TAB

        top_scorers_banner = MainWindowBanner("TOP STATS")
        top_stats_tab = TopStatsTab()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(table_banner, 0, 0, 1, 4)
        grid.addLayout(self.table_filter_layout, 1, 0, 1, 1)
        grid.addWidget(self.team_table, 2, 0, 1, 1)
        grid.addWidget(results_banner, 3, 0, 1, 8)
        grid.addLayout(self.results_filter_layout, 4, 0, 1, 1)
        grid.addWidget(self.results_table, 5, 0, 2, 8)

        grid.addWidget(top_scorers_banner, 0, 4, 1, 4)
        grid.addWidget(top_stats_tab, 1, 4, 2, 4)

        self.setLayout(grid)

        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('EPL 18/19')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
