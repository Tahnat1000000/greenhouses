from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, 
QScrollArea, QSpacerItem, QSizePolicy, QGroupBox, QComboBox, QLineEdit )
from PyQt5.QtCore import Qt, QSize
from greenhouses import Greenhouses

class GetPlantingProgramWidget(QWidget):
    def __init__(self, parent=None):
        super(GetPlantingProgramWidget, self).__init__(parent)

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
        title = QLabel("PLANTING PROGRAM                    ") # TITLE - LABEL
        font.setPointSize(20)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        topBarLayout.addWidget(self.menuButton)
        topBarLayout.addWidget(title, 1)
        topBarLayout.setAlignment(Qt.AlignLeft)
        centerLayout.addLayout(topBarLayout)

        # PLANTING DETAILS LAYOUT
        plantingDetailsLayout = QHBoxLayout()
        seedlingType = QLabel("Seedlings Type: ")
        self.seedlingsOptions = QComboBox()
        with open("files/seedlings.txt", "r") as f:
            self.seedlingsOptions.addItems([seedlingDetails.split(",")[0] for seedlingDetails in f.readlines()[1:]])
        amountOfSeedlingsTitle = QLabel("Amount Of Seedlings: ")
        font = amountOfSeedlingsTitle.font()
        font.setBold(True)
        self.amountOfSeedlingsInput = QLineEdit()
        self.amountOfSeedlingsInput.setAlignment(Qt.AlignCenter)
        self.amountOfSeedlingsInput.setFixedHeight(25)
        createProgramButton = QPushButton("CREATE PROGRAM")
        createProgramButton.setFont(font)
        createProgramButton.setFixedSize(QSize(140,25))
        createProgramButton.setStyleSheet("background-color:#3A6B35 ; border-radius:3")
        createProgramButton.clicked.connect(self.showProgram)
        plantingDetailsLayout.addWidget(seedlingType)
        plantingDetailsLayout.addWidget(self.seedlingsOptions)
        plantingDetailsLayout.addWidget(amountOfSeedlingsTitle)
        plantingDetailsLayout.addWidget(self.amountOfSeedlingsInput)
        plantingDetailsLayout.addWidget(createProgramButton)
        centerLayout.addLayout(plantingDetailsLayout)
        
        # SCROLL AREA TITLE LAYOUT
        scrollAreaTitles = QHBoxLayout()
        scrollAreaTitles.setContentsMargins(30, 0, 30, 0)
        titles = [QLabel("      GREENHOUSE ID"), QLabel("               AMOUNT"), QLabel("PLANTING POINTS IDS")]
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

        # ADD SEEDLINGS BY PROGRAM LAYOUT
        addSeedlingsByProgramLayout = QHBoxLayout()
        plantingDateTitle = QLabel("Date: ")
        font = plantingDateTitle.font()
        font.setBold(True)
        self.plantingDateInput = QLineEdit()
        self.plantingDateInput.setAlignment(Qt.AlignCenter)
        self.plantingDateInput.setFixedHeight(25)
        self.plantingDateInput.setEnabled(False)
        self.addSeedlingsButton = QPushButton("ADD SEDDLINGS TO PLANTING POINTS")
        self.addSeedlingsButton.setFont(font)
        self.addSeedlingsButton.setFixedSize(QSize(300,25))
        self.addSeedlingsButton.setStyleSheet("background-color:#3A6B35 ; border-radius:3")
        self.addSeedlingsButton.setEnabled(False)
        self.addSeedlingsButton.clicked.connect(self.addSeedlings)
        addSeedlingsByProgramLayout.addWidget(plantingDateTitle)
        addSeedlingsByProgramLayout.addWidget(self.plantingDateInput)
        addSeedlingsByProgramLayout.addWidget(self.addSeedlingsButton)
        centerLayout.addLayout(addSeedlingsByProgramLayout)  

        # MESSAGE LABEL
        self.messageLabel = QLabel("PLANTS WAS PLANTED SUCCESSFULLY")
        self.messageLabel.setAlignment(Qt.AlignCenter)
        centerLayout.addWidget(self.messageLabel)

        self.greenhouses = Greenhouses()
        self.greenhouses.initByFiles()
        self.program = None

    def showProgram(self):
        self.greenhouses.initByFiles()
        
        if self.amountOfSeedlingsInput.text().isdigit():
            seddlingsName, amount = self.seedlingsOptions.currentText(), int(self.amountOfSeedlingsInput.text())
            self.program = self.greenhouses.getAndPrintPlantingProgram(seddlingsName, amount)

            self.messageLabel.hide()

            # LIST OF DATA FOR SCROLL AREA
            if self.scrollAreaWidgetLayout.count() != 1:
                item = self.scrollAreaWidgetLayout.itemAt(self.scrollAreaWidgetLayout.count()-2)
                widget = item.widget()
                self.scrollAreaWidgetLayout.removeItem(item)
                widget.deleteLater()

            dataListOfQLabels = []
            for index, data in enumerate(self.program):
                id, seedlingsCanBePlant, startPlantPointId, endPlantPointId = data[0], str(data[1]), str(data[2]) , str(data[3])
                if int(seedlingsCanBePlant) == 0:
                    continue
                idLabel, seedlingsCanBePlantLabel, startEndPlantPointIdLabel = QLabel(id), QLabel(seedlingsCanBePlant), QLabel(startPlantPointId+" - "+endPlantPointId)
                labels = [idLabel, seedlingsCanBePlantLabel, startEndPlantPointIdLabel]
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
            
            if len(self.program)>0:
                self.plantingDateInput.setEnabled(True)
                self.plantingDateInput.setPlaceholderText("01/01/2022")
                self.addSeedlingsButton.setEnabled(True)
    
    def addSeedlings(self):
        date = self.plantingDateInput.text()
        if type(date) != str or len(date.split("/")) != 3:
            return
        day, month, year = date.split("/")
        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            return
        if int(day) < 1 or int(day) > 31 and int(month) < 1 or int(month) > 12:
            return
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return

        name = self.seedlingsOptions.currentText()
        self.greenhouses.addSeedlingsByPlantingProgram(date, name, self.program)
        for programLine in self.program:
            if programLine[1] > 0:
                greenhouses = self.greenhouses.GREENHOUSES
                greenhouses[int(programLine[0])-1].saveDataInFile()

        self.amountOfSeedlingsInput.setText("")        
        self.plantingDateInput.setText("")
        self.plantingDateInput.setEnabled(False)
        self.plantingDateInput.setPlaceholderText("")
        self.addSeedlingsButton.setEnabled(False)
        
        item = self.scrollAreaWidgetLayout.itemAt(self.scrollAreaWidgetLayout.count()-2)
        widget = item.widget()
        self.scrollAreaWidgetLayout.removeItem(item)
        widget.deleteLater()     

        self.messageLabel.show()

        
