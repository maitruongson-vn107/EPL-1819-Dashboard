from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTabWidget, QHeaderView

from controllers.player_controller import getTopScorers, getTopAssists, getTopCleanSheets
from data_loaders.utils import getTeamLogo


class TopStatTableTab(QTableWidget):
    def __init__(self, data, rows: int, cols: int, labels: tuple):
        super(TopStatTableTab, self).__init__()
        self.team_window = None
        self.data = data
        self.set_col_row(rows, cols, labels)
        self.load_data(data, rows)
        self.set_style()

    def set_col_row(self, rows, cols, labels):
        self.setRowCount(rows)
        self.setColumnCount(cols)
        self.setHorizontalHeaderLabels(labels)

    def load_data(self, data, rows):
        for r in range(rows):
            self.setItem(r, 0, QTableWidgetItem(str(data[r][0])))   # player's name
            logo_widget = getTeamLogo(data[r][1], 35)
            logo_widget.setAlignment(Qt.AlignCenter)               # logo
            self.setCellWidget(r, 1, logo_widget)

            record_item = QTableWidgetItem(str(data[r][2]))         # record
            record_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(r, 2, record_item)

    def set_style(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnToContents(1)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


class TopStatsTab(QTabWidget):
    def __init__(self):
        super(TopStatsTab, self).__init__()
        self.top_clean_sheets_tab = None
        self.top_assists_tab = None
        self.top_scorers_tab = None
        self.load_data()
        self.set_style()

    def load_data(self):
        # TOP SCORERS TAB
        top_scorers_list = getTopScorers()
        top_scorers_labels = ("Player", "Club", "Goals")
        self.top_scorers_tab = TopStatTableTab(top_scorers_list,
                                               len(top_scorers_list),
                                               len(top_scorers_list[0]),
                                               top_scorers_labels)

        self.addTab(self.top_scorers_tab, "SCORERS")

        # TOP ASSISTS TAB
        top_assists_list = getTopAssists()
        top_assists_labels = ("Player", "Club", "Assists")
        self.top_assists_tab = TopStatTableTab(top_assists_list,
                                               len(top_scorers_list),
                                               len(top_scorers_list[0]),
                                               top_assists_labels)

        self.addTab(self.top_assists_tab, "ASSISTS")

        # TOP CLEAN SHEETS TAB
        top_clean_sheets_list = getTopCleanSheets()
        top_clean_sheets_labels = ("Player", "Club", "Clean Sheets")
        self.top_clean_sheets_tab = TopStatTableTab(top_clean_sheets_list,
                                                    len(top_clean_sheets_list),
                                                    len(top_clean_sheets_list[0]),
                                                    top_clean_sheets_labels)
        self.addTab(self.top_clean_sheets_tab, "CLEAN SHEETS")

    def set_style(self):
        self.setFixedWidth(300)
        stylesheet = "QTabBar::tab:selected {background: #e90052; color: #ffffff} "
        self.setStyleSheet(stylesheet)