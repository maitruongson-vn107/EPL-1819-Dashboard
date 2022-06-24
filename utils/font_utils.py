from PyQt5.QtGui import QFont


def get_font(bold: bool, pointSize=15):
    font = QFont()
    font.setBold(bold)
    font.setPointSize(pointSize)
    return font