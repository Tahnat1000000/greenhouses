from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, 
QScrollArea, QSpacerItem, QSizePolicy, QGroupBox )
from PyQt5.QtCore import Qt, QSize
from greenhouses import Greenhouses

class GreenhousesWidget(QWidget):
    def __init__(self, parent=None):
        super(GreenhousesWidget, self).__init__(parent)

        # LAYOUTS
        centerLayout = QVBoxLayout()
        self.setLayout(centerLayout)

        # TOP BAR LAYOUT
        topBarLayout = QHBoxLayout()
        font = QLabel().font()
        font.setBold(True)
        self.menuButton = QPushButton("MENU") # BACK TO MENU -  BUTTON
        self.menuButton.setFont(font)
        self.menuButton.setFixedSize(QSize(75,30))
        self.menuButton.setStyleSheet("background-color:#CBD18F ; border-radius:5")
        title = QLabel("GREENHOUSES                    ") # TITLE - LABEL
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
        titles = [QLabel("                 ID"), QLabel("    TEMPERATURE"), QLabel("       OCCUPIED"), QLabel("              SIZE")]
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

    def setDataInTable(self):
        # LIST OF DATA FOR SCROLL AREA
        if self.scrollAreaWidgetLayout.count() != 1:
            item = self.scrollAreaWidgetLayout.itemAt(self.scrollAreaWidgetLayout.count()-2)
            widget = item.widget()
            self.scrollAreaWidgetLayout.removeItem(item)
            widget.deleteLater()

        dataListOfQLabels = []
        greenhouses = Greenhouses()
        greenhouses.initByFiles()
        greenhousesData = greenhouses.getGreenhousesStringList()
        for index, data in enumerate(greenhousesData):
            id, avgTemp, occupiedLen, totalLen = data[0], str(data[1]), str(data[2]) , str(data[3])
            idLabel, avgTempLabel, occupiedLenLabel, totalLenLabel = QLabel(id), QLabel(avgTemp), QLabel(occupiedLen), QLabel(totalLen)
            labels = [idLabel, avgTempLabel, occupiedLenLabel, totalLenLabel]
            font = QLabel().font()
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
        for i, greenhouse in enumerate(dataListOfQLabels):
            for j, detail in enumerate(greenhouse):
                tableLayout.addWidget(detail, i, j)