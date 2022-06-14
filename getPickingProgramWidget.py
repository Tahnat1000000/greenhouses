from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, 
QScrollArea, QSpacerItem, QSizePolicy, QGroupBox, QComboBox, QLineEdit )
from PyQt5.QtCore import Qt, QSize
from greenhouses import Greenhouses

class GetPickingProgramWidget(QWidget):
    def __init__(self, parent=None):
        super(GetPickingProgramWidget, self).__init__(parent)

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
        title = QLabel("PICKING PROGRAM                    ") # TITLE - LABEL
        font.setPointSize(20)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        topBarLayout.addWidget(self.menuButton)
        topBarLayout.addWidget(title, 1)
        topBarLayout.setAlignment(Qt.AlignLeft)
        centerLayout.addLayout(topBarLayout)

        # ADD SEEDLINGS BY PROGRAM LAYOUT
        getPickingProgramLayout = QHBoxLayout()
        getPickingProgramLayout.setContentsMargins(50, 0, 50, 0)
        dateLabel = QLabel("Date: ")
        font = dateLabel.font()
        font.setBold(True)
        self.dateInputForPickingProgram = QLineEdit()
        self.dateInputForPickingProgram.setAlignment(Qt.AlignCenter)
        self.dateInputForPickingProgram.setFixedHeight(25)
        self.dateInputForPickingProgram.setPlaceholderText("01/01/2022")
        self.showProgramButton = QPushButton("GET PROGRAM")
        self.showProgramButton.setFont(font)
        self.showProgramButton.setFixedSize(QSize(200,25))
        self.showProgramButton.setStyleSheet("background-color:#3A6B35 ; border-radius:3")
        self.showProgramButton.clicked.connect(self.showProgram)
        getPickingProgramLayout.addWidget(dateLabel)
        getPickingProgramLayout.addWidget(self.dateInputForPickingProgram)
        getPickingProgramLayout.addWidget(self.showProgramButton)
        centerLayout.addLayout(getPickingProgramLayout)  

        # SCROLL AREA TITLE LAYOUT
        scrollAreaTitles = QHBoxLayout()
        scrollAreaTitles.setContentsMargins(30, 0, 30, 0)
        titles = [QLabel("            Greenhouse Id"), QLabel("          Planting Point Id       "), QLabel("-         Planting Point Id    ")]
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

        # HARVEST BUTTON
        self.harvestSeedlings = QPushButton("HARVEST SEEDLINGS")
        self.harvestSeedlings.setFont(font)
        self.harvestSeedlings.setFixedHeight(30)
        self.harvestSeedlings.setStyleSheet("background-color:#3A6B35 ; border-radius:3")
        self.harvestSeedlings.clicked.connect(self.harvestButton)
        self.harvestSeedlings.setEnabled(False)
        centerLayout.addWidget(self.harvestSeedlings)
        self.greenhouses = Greenhouses()
        self.greenhouses.initByFiles()
        self.program = None

        # MESSAGE LABEL
        self.messageLabel = QLabel("SEEDLING WAS HARVESTED SUCCESSFULLY")
        self.messageLabel.setAlignment(Qt.AlignCenter)
        centerLayout.addWidget(self.messageLabel)

    def showProgram(self):
        self.greenhouses.initByFiles()
        date = self.dateInputForPickingProgram.text()
        if type(date) != str or len(date.split("/")) != 3:
            return
        day, month, year = date.split("/")
        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            return
        if int(day) < 1 or int(day) > 31 and int(month) < 1 or int(month) > 12:
            return
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return

        self.messageLabel.hide()
        self.program = self.greenhouses.getAndPrintPickingProgram(date)
        print(self.program)

        # LIST OF DATA FOR SCROLL AREA
        if self.scrollAreaWidgetLayout.count() != 1:
            item = self.scrollAreaWidgetLayout.itemAt(self.scrollAreaWidgetLayout.count()-2)
            widget = item.widget()
            self.scrollAreaWidgetLayout.removeItem(item)
            widget.deleteLater()

        dataListOfQLabels = []
        for index, data in enumerate(self.program):
            id, startPlantPointId, endPlantPointId = data[0], str(data[1]), str(data[2])
            # if int(seedlingsCanBePlant) == 0:
            #     continue
            idLabel, startPlantPointIdLabel, endPlantPointIdLabel = QLabel(id), QLabel(startPlantPointId), QLabel(endPlantPointId)
            labels = [idLabel, startPlantPointIdLabel, endPlantPointIdLabel]
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
        for i, offer in enumerate(dataListOfQLabels):
            for j, detail in enumerate(offer):
                tableLayout.addWidget(detail, i, j) 

        if len(self.program) > 0:
            self.harvestSeedlings.setEnabled(True)

    def harvestButton(self):
        if len(self.program) > 0:
            self.greenhouses.harvestSeedlingsByPickingProgram(self.program)
            for programLine in self.program:
                    self.greenhouses.GREENHOUSES[int(programLine[0])-1].saveDataInFile()
        
        item = self.scrollAreaWidgetLayout.itemAt(self.scrollAreaWidgetLayout.count()-2)
        widget = item.widget()
        self.scrollAreaWidgetLayout.removeItem(item)
        widget.deleteLater()

        self.dateInputForPickingProgram.setText("")
        self.harvestSeedlings.setEnabled(False)

        self.messageLabel.show()


    
