from PyQt5.QtWidgets import QLabel


class MatchGeneralInfo(QLabel):
    def __init__(self, match_data):
        super(MatchGeneralInfo, self).__init__()
        self.load_data(match_data)
        self.set_style()

    def load_data(self, match_data):
        self.setText(
            f"Kick-off Time: {match_data['date_GMT']}"
            f"\nReferee: {match_data['referee']}"
            f"\nStadium: {match_data['stadium_name']}"
            f"\nAttendance: {match_data['attendance']}"
        )

    def set_style(self):
        self.setStyleSheet("QLabel { background-color : #38003c; color : #ffffff; }")
        self.setFixedHeight(100)
        self.setMargin(10)