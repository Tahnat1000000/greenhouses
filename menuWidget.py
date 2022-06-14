from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QWidget)
from PyQt5.QtCore import Qt, QSize

class MenuWidget(QWidget):
    def __init__(self, parent=None):
        super(MenuWidget, self).__init__(parent)

        # LAYOUTS
        centerLayout = QVBoxLayout()
        buttonsLayout = QVBoxLayout()
        buttonsLayout.setSpacing(10)

        # FONT SETTINGS
        font = QLabel().font()
        font.setBold(True)
        font.setPointSize(30)

        # TITLE
        title = QLabel("GREENHOUSES\nMANAGMENT")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(font)

        # BUTTONS
        font.setPointSize(15)
        self.seedlingTypesButton = QPushButton("SEEDLINGS TYPES")
        self.greenhousesButton = QPushButton("GREENHOUSES")
        self.getPlantingProgramButton = QPushButton("GET PLANTING PROGRAM")
        self.getPickingProgramButton = QPushButton("GET PICKING PROGRAM")
        buttonsList = [self.seedlingTypesButton, self.greenhousesButton, self.getPlantingProgramButton, self.getPickingProgramButton]
        for button in buttonsList:
            button.setFixedHeight(50)
            button.setStyleSheet("background-color:#E3B448 ; border-radius:5")
            button.setFont(font)

        buttonsLayout.addWidget(self.seedlingTypesButton)
        buttonsLayout.addWidget(self.greenhousesButton)
        buttonsLayout.addWidget(self.getPlantingProgramButton)
        buttonsLayout.addWidget(self.getPickingProgramButton)
        centerLayout.addWidget(title)
        centerLayout.addLayout(buttonsLayout)

        self.setLayout(centerLayout)