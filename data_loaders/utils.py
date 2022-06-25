from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


def getTeamLogo(club_common_name, size=30):
    logo_path = "assets/png/" + club_common_name.lower().replace(" ", "") + ".png"
    logo = QPixmap(logo_path)
    logo_label = QLabel()
    logo_label.setPixmap(logo.scaled(size, size, aspectRatioMode=Qt.KeepAspectRatio))
    logo_label.setAlignment(Qt.AlignCenter)
    return logo_label

