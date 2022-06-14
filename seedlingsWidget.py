from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, 
QScrollArea, QSpacerItem, QSizePolicy, QGroupBox )
from PyQt5.QtCore import Qt, QSize
from seedlings import Seedlings

class SeedlingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SeedlingsWidget, self).__init__(parent)

        # CENTER LAYOUT
        centerLayout = QVBoxLayout()
        self.setLayout(centerLayout)

        # TOP BAR LAYOUT
        topBarLayout = QHBoxLayout()
        font = QLabel().font()
        font.setBold(True)
        self.menuButton = QPushButton("MENU") # BACK TO MENU -  BUTTON
        self.menuButton.setFont(font)
        self.menuButton.setFixedSize(QSize(75,30))
        self.menuButton.setStyleSheet("background-color:#CBD18F ; border-radius:3")
        title = QLabel("SEEDLINGS                    ") # TITLE - LABEL
        font.setPointSize(20)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        topBarLayout.addWidget(self.menuButton)
        topBarLayout.addWidget(title, 1)
        topBarLayout.setAlignment(Qt.AlignLeft)
        centerLayout.addLayout(topBarLayout)

        # SCROLL AREA TITLE LAYOUT
        scrollAreaTitles = QHBoxLayout()
        scrollAreaTitles.setContentsMargins(30, 0, 30, 0)
        titles = [QLabel("            index"), QLabel("              Name"), QLabel("         Grow Time"), QLabel("Temperature Range")]
        font.setPointSize(17)
        for title in titles:
            title.setFont(font)
            scrollAreaTitles.addWidget(title)
        centerLayout.addLayout(scrollAreaTitles)
        
        # SCROLL AREA
        self.scrollArea = QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidgetLayout = QVBoxLayout(self.scrollAreaWidget)
        self.scrollAreaWidgetLayout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.scrollArea.setWidget(self.scrollAreaWidget)
        centerLayout.addWidget(self.scrollArea)

        # LIST OF DATA FOR SCROLL AREA
        dataListOfQLabels = []
        seedlings = Seedlings()
        seedlingsData = seedlings.getSeedlingsStringList()
        for index, seedling in enumerate(seedlingsData):
            name, growTime, temperatureRange = seedling.split(",")[0], seedling.split(",")[1], seedling.split(",")[2] +" - "+ seedling.split(",")[3]
            indexLabel, nameLabel, growTimeLabel, tempRangeLabel = QLabel(str(index+1)), QLabel(name), QLabel(growTime), QLabel(temperatureRange)
            labels = [indexLabel, nameLabel, growTimeLabel, tempRangeLabel]
            font.setPointSize(15)
            for label in labels:
                if index%2 == 1:
                    label.setStyleSheet("background-color:#787878")
                label.setAlignment(Qt.AlignCenter)
                label.setFont(font)
                label.setFixedHeight(25)
            dataListOfQLabels.append(labels)

        groupBox = QGroupBox(self.scrollAreaWidget)
        groupBox.setFlat(True)
        self.scrollAreaWidgetLayout.insertWidget(self.scrollAreaWidgetLayout.count() - 1, groupBox)       
        
        tableLayout = QGridLayout(groupBox)
        tableLayout.setSpacing(0)
        for i, seedlingType in enumerate(dataListOfQLabels):
            for j, detail in enumerate(seedlingType):
                tableLayout.addWidget(detail, i, j)
        
