from fileinput import filename
import os, json
from greenhouse import Greenhouse
from seedlings import Seedlings
from plantingPoint import PlantingPoint
from datetime import date
from helper import checkDate, NUMBER_OF_PLANTING_POINTS

class Greenhouses:
    # CONSTRUCTOR
    def __init__(self):
        self.__greenhousesList = []
        seedlings = Seedlings()
        seedlings.addSeedlingsByFile()
        self.__seedlingsTypes = seedlings

    # GETTERS AND SETTERS
    def __getGreenhouses(self) -> list:
        return self.__greenhousesList
    
    GREENHOUSES = property(__getGreenhouses)


    # CLASS METHODS
    def addGreenhouse(self, greenhouse:Greenhouse):
        if not isinstance(greenhouse, Greenhouse):
            raise ValueError("ERROR -> addGreenhouse METHOD SHOULD GET GREENHOUSE OBJECT")
        self.__greenhousesList.append(greenhouse)

    def getGreenhouse(self, index) -> Greenhouse:
        if type(index) != int or index < 1 or index > len(self.__greenhousesList):
            raise ValueError(f"ERROR -> getGreenhouse SHOULD GET INDEX (1-{len(self.__greenhousesList)})")
        return self.__greenhousesList[index-1]

    def getAndPrintPlantingProgram(self, name:str, seedlingsAmount:int, greenhousesList:list=[]) -> list:
        if not name in [seedlingType.NAME for seedlingType in self.__seedlingsTypes.SEEDLINGS_TYPES]:
            raise ValueError("ERROR -> SEEDLING NAME NOT EXISTS IN SEEDLINGS LIST")
        if len(greenhousesList) == 0:
            greenhousesList = self.__greenhousesList
        temperatureRange = [seedlingType.TEMPERATURE_RANGE for seedlingType in self.__seedlingsTypes.SEEDLINGS_TYPES if seedlingType.NAME == name][0]
        greenhousesSuitable = [] # CONTAIN TUPLES OF (GREENHOUSE INDEX, NUMBER OF SEEDLINGS THAT CAN BE PLANT, FIRST PLANT POINT ID, LAST PLANT POINT ID)
        for greenhouse in greenhousesList:
            if greenhouse.AVARAGE_TEMPERATURE >= temperatureRange[0] and greenhouse.AVARAGE_TEMPERATURE <= temperatureRange[1]:
                if greenhouse.AMOUNT_OF_EMPTY_PLANTING_POINTS > 0:
                    firstSuitablePlatingPointId = greenhouse.getFirstEmptyPlantingPointId()
                    if greenhouse.AMOUNT_OF_EMPTY_PLANTING_POINTS - seedlingsAmount > 0:
                        lastSuitablePlantingPointId = greenhouse.getFirstEmptyPlantingPointId() + seedlingsAmount-1
                        greenhousesSuitable.append((greenhouse.ID, seedlingsAmount, firstSuitablePlatingPointId, lastSuitablePlantingPointId))
                        seedlingsAmount = 0
                        break
                    else:
                        lastSuitablePlantingPointId = greenhouse.getFirstEmptyPlantingPointId() + greenhouse.AMOUNT_OF_EMPTY_PLANTING_POINTS-1
                        greenhousesSuitable.append((greenhouse.ID, greenhouse.AMOUNT_OF_EMPTY_PLANTING_POINTS, firstSuitablePlatingPointId, lastSuitablePlantingPointId))
                        seedlingsAmount = -(greenhouse.AMOUNT_OF_EMPTY_PLANTING_POINTS - seedlingsAmount)
        print(f" -> PLANTING PROGRAM CHOOSED:")
        for suitable in greenhousesSuitable:
            print(f" ---> Greenhouse number: {suitable[0]}, seedlings can be plant: {suitable[1]}, planting points ids: {suitable[2]}-{suitable[3]}")
        if seedlingsAmount != 0:
            print(f" ---> BE NOTICE: There is {seedlingsAmount} more seedlings that dont have a plant points for them! ")
        return greenhousesSuitable

    def addSeedlingsByPlantingProgram(self, date:str, name:str, program:list):
        checkDate(date)
        if len(program) == 0 or type(program) != list:
            raise ValueError("ERROR -> PROGRAM SHOLUD BE LIST WITH PLANTING PROGRAM DETAILS")
        countSeedlings = 0
        for plantingDetails in program:
            greenhouseNumber, numberOfSeedlings = int(plantingDetails[0])-1, plantingDetails[1]
            countSeedlings += plantingDetails[1]
            for i in range(numberOfSeedlings):
                self.__greenhousesList[greenhouseNumber].addSeedlingInPlantingPoint(date, name)
        print(f" ---> {countSeedlings} seddlings was planted successfully!")

    def getDaysBetweenTwoDates(self, date1:str, date2:str) -> int:
        checkDate(date1)
        checkDate(date2)
        day1, month1, year1 = date1.split("/")
        day2, month2, year2 = date2.split("/")
        startDate, endDate = date(int(year1), int(month1), int(day1)), date(int(year2), int(month2), int(day2))
        delta = endDate - startDate
        return delta.days

    def getAndPrintPickingProgram(self, date:str, greenhousesList:list=[]) -> list:
        checkDate(date)
        pickingProgram = [] # CONTAIN TUPLES OF (GREENHOUSE INDEX, START PLANTING POINT ID, LAST PLANTING POINT ID)
        if len(greenhousesList) == 0:
            greenhousesList = self.__greenhousesList
        for greenhouse in greenhousesList:
            if greenhouse.AMOUNT_OF_EMPTY_PLANTING_POINTS == NUMBER_OF_PLANTING_POINTS:
                continue
            startPlantingPointId,  endPlantingPointId= "-", "-"
            for plantingPoint in greenhouse.PLANTING_POINTS:
                if startPlantingPointId != "-" and int(plantingPoint.ID)%NUMBER_OF_PLANTING_POINTS == 0:
                    endPlantingPointId = plantingPoint.ID
                    pickingProgram.append((greenhouse.ID, startPlantingPointId, endPlantingPointId))
                    startPlantingPointId,  endPlantingPointId= "-", "-"
                elif startPlantingPointId != "-" and plantingPoint.NAME == "-":
                    endPlantingPointId = plantingPoint.ID
                    pickingProgram.append((greenhouse.ID, startPlantingPointId, str(int(endPlantingPointId)-1)))
                    startPlantingPointId,  endPlantingPointId= "-", "-"
                    continue
                elif plantingPoint.NAME == "-":
                    continue
                seedlingGrowDay = [seedlingType.GROW_TIME for seedlingType in self.__seedlingsTypes.SEEDLINGS_TYPES if seedlingType.NAME == plantingPoint.NAME][0]
                days = self.getDaysBetweenTwoDates(plantingPoint.SEEDING_DATE, date)
                if startPlantingPointId == "-" and seedlingGrowDay-days <= 0:
                    startPlantingPointId = plantingPoint.ID
                if startPlantingPointId != "-" and seedlingGrowDay-days > 0:
                    endPlantingPointId = plantingPoint.ID
                    pickingProgram.append((greenhouse.ID, startPlantingPointId, endPlantingPointId))
                    startPlantingPointId,  endPlantingPointId= "-", "-"
        print(f" -> PICKING PROGRAM FOR DATE: {date}")
        for pickingDetails in pickingProgram:
            print(f" ---> Greenhouse number: {pickingDetails[0]}, planting points: {pickingDetails[1]}-{pickingDetails[2]} are ready for picking")
        return pickingProgram

    def harvestSeedlingsByPickingProgram(self, program:list):
        if len(program) == 0 or type(program) != list:
            raise ValueError("ERROR -> PROGRAM SHOLUD BE LIST WITH PLANTING PROGRAM DETAILS")
        countSeedlings = 0
        for pickingDetails in program:
            greenhouseIndex = int(pickingDetails[0])-1
            if int(pickingDetails[1])%500 == 0: 
                plantingPointIndex = 499
            else: 
                plantingPointIndex = int(pickingDetails[1])%500 - 1
            countSeedlings += int(pickingDetails[2])-int(pickingDetails[1])+1
            for i in range(int(pickingDetails[2])-int(pickingDetails[1])+1):
                self.__greenhousesList[greenhouseIndex].PLANTING_POINTS[plantingPointIndex].harvestSeedling()
                plantingPointIndex +=1
        print(f" ---> {countSeedlings} seddlings was harvested successfully!")

    def getGreenhousesStringList(self) -> list:
        greenhouseslist = []
        for greenhouse in self.__greenhousesList:
            greenhouseslist.append([greenhouse.ID, greenhouse.AVARAGE_TEMPERATURE, greenhouse.occupiedLen(), len(greenhouse.PLANTING_POINTS)])
        return greenhouseslist

    def initByFiles(self):
        self.__greenhousesList = []
        filesNames = os.listdir("files/greenhouses")
        filesNames = [int(fileName.split(".")[0]) for fileName in filesNames if fileName.split(".")[1] == "json"]
        filesNames.sort()
        filesNames = [str(fileName)+".json" for fileName in filesNames]
        PlantingPoint.idNumber = 1
        for fileName in filesNames:
            with open(f"files/greenhouses/{fileName}", "rt") as f:
                jsonFile = json.load(f)
                plantingPoints = [PlantingPoint(details["DATE"], details["NAME"], details["OCCUPIED"]) for details in jsonFile[1:]]
                greenhouse = Greenhouse(fileName.split(".")[0],jsonFile[0]["TEMPERATURE"], plantingPoints)
                greenhouse.updateAmountOfEmptyPlantingPoints()
                self.__greenhousesList.append(greenhouse)


    # SPECIAL CLASS METHODS
    def __str__(self) -> str:
        if len(self.__greenhousesList) == 0:
            return "Greenhouses:\nNone"
        returnStr = "Greenhouses:\n"
        for index, greenhouse in enumerate(self.__greenhousesList):
            returnStr += f"{str(index+1).ljust(2)}) " + greenhouse.__str__() + "\n"
        return returnStr