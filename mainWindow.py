from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QDesktopWidget)
from PyQt5.QtCore import Qt, QSize
from importsPackage import (MenuWidget, SeedlingsWidget, GreenhousesWidget, 
                            GetPlantingProgramWidget, GetPickingProgramWidget)
from greenhouses import Greenhouses
                            
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # WINDOW SETTINGS
        self.setWindowTitle("GREENHOUSES APPLICATION")
        self.setFixedSize(QSize(300,350))

        # CREATE MAIN WIDGET - STACKED WIDGET
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        # CREATE MENU WIDGET AND ENTER TO MAIN STACK WIDGET
        self.menuWidget = MenuWidget(self)
        self.centralWidget.addWidget(self.menuWidget)

        # CREATE SEEDLINGS WIDGET AND ENTER TO MAIN STACK WIDGET
        self.seedlingsWidget = SeedlingsWidget(self)
        self.centralWidget.addWidget(self.seedlingsWidget)

        # CREATE GREENHOUSE WIDGET AND ENTER TO MAIN STACK WIDGET
        self.greenhousesWidget = GreenhousesWidget(self)
        self.centralWidget.addWidget(self.greenhousesWidget)

        # CREATE GET PLANTING PROGRAM WIDGET AND ENTER TO MAIN STACK WIDGET
        self.getPlantingProgramWidget = GetPlantingProgramWidget(self)
        self.centralWidget.addWidget(self.getPlantingProgramWidget)

        # CREATE GET PICKING PROGRAM WIDGET AND ENTER TO MAIN STACK WIDGET
        self.getPickingProgramWidget = GetPickingProgramWidget(self)
        self.centralWidget.addWidget(self.getPickingProgramWidget)


        self.menuWidget.seedlingTypesButton.clicked.connect(self.openSeedlingsWindow)
        self.menuWidget.greenhousesButton.clicked.connect(self.openGreenhousesWindow)
        self.menuWidget.getPlantingProgramButton.clicked.connect(self.openGetPlantingProgramWindow)
        self.menuWidget.getPickingProgramButton.clicked.connect(self.openGetPickingProgramWindow)
        self.seedlingsWidget.menuButton.clicked.connect(self.openMenuWindow)
        self.greenhousesWidget.menuButton.clicked.connect(self.openMenuWindow)
        self.getPlantingProgramWidget.menuButton.clicked.connect(self.openMenuWindow)
        self.getPickingProgramWidget.menuButton.clicked.connect(self.openMenuWindow)
        
        
    # MENU BUTTONS FUNCTIONS
    def openMenuWindow(self):
        self.centralWidget.setCurrentWidget(self.menuWidget)
        self.setFixedSize(QSize(300,350))
        self.center()
    def openSeedlingsWindow(self):
        self.centralWidget.setCurrentWidget(self.seedlingsWidget)
        self.setFixedSize(QSize(700,500))
        self.center()
    def openGreenhousesWindow(self):
        self.centralWidget.setCurrentWidget(self.greenhousesWidget)
        self.setFixedSize(QSize(700,500))
        self.greenhousesWidget.setDataInTable()
        self.center()
    def openGetPlantingProgramWindow(self):
        self.centralWidget.setCurrentWidget(self.getPlantingProgramWidget)
        self.getPlantingProgramWidget.messageLabel.hide()
        self.setFixedSize(QSize(700,500))
        self.center()
    def openGetPickingProgramWindow(self):
        self.centralWidget.setCurrentWidget(self.getPickingProgramWidget)
        self.getPickingProgramWidget.messageLabel.hide()
        self.setFixedSize(QSize(700,500))
        self.center()

    def center(self):
        windowDetails = self.frameGeometry()
        centerPosition = QDesktopWidget().availableGeometry().center()
        windowDetails.moveCenter(centerPosition)
        self.move(windowDetails.topLeft())

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
