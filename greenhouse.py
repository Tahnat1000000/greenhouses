from plantingPoint import PlantingPoint
from helper import NUMBER_OF_PLANTING_POINTS, checkDate
import os, json

class Greenhouse:
    # CONSTRUCTOR
    def __init__(self, id:str, avarageTemperature:float, plantingPoints:list=[PlantingPoint() for i in range(NUMBER_OF_PLANTING_POINTS)]):
        self.__id = id
        self.__setAvarageTemperature(avarageTemperature)
        self.__plantingPoints = plantingPoints
        self.__emptyPlantingPoints = len([plantingPoint for plantingPoint in self.__plantingPoints if plantingPoint.OCCUPIED == False])


    # GETTERS AND SETTERS
    def __getId(self) -> str:
        return self.__id

    def __getAvarageTemperature(self) -> float:
        return self.__avarageTemperature

    def __setAvarageTemperature(self, temperature):
        if type(temperature) != float and type(temperature) != int:
            raise ValueError("ERROR -> TEMPERATURE MUST BE NUMBER")
        self.__avarageTemperature = temperature

    def __getPlantingPoints(self) -> list:
        return self.__plantingPoints

    def __setPlantingPoints(self, plantingPointList):
        if type(plantingPointList) != list:
            raise ValueError("ERROR -> PLANTING POINTS MUST BE LIST")
        self.__plantingPoints = plantingPointList

    def __getAmountOfEmptyPlantingPoints(self) -> int:
        return self.__emptyPlantingPoints
    
    def updateAmountOfEmptyPlantingPoints(self):
        self.__emptyPlantingPoints = len([plantingPoint for plantingPoint in self.__plantingPoints if plantingPoint.OCCUPIED == False])

        
    ID = property(__getId)
    AVARAGE_TEMPERATURE = property(__getAvarageTemperature, __setAvarageTemperature)
    PLANTING_POINTS = property(__getPlantingPoints, __setPlantingPoints)
    AMOUNT_OF_EMPTY_PLANTING_POINTS = property(__getAmountOfEmptyPlantingPoints)


    # CLASS METHODS
    def getPlatingPoint(self, index:int) -> PlantingPoint:
        if type(index) != int or index < 1 or index > NUMBER_OF_PLANTING_POINTS:
            raise ValueError("ERROR -> getPlantingPoint SHOULD GET INDEX (1-500)")
        return self.__plantingPoints[index-1]

    def getFirstEmptyPlantingPointId(self) -> int:
        occupiedList = [plantingPoint.OCCUPIED for plantingPoint in self.__plantingPoints]
        index = occupiedList.index(False)
        return int(self.__plantingPoints[index].ID)
        

    def addSeedlingInPlantingPoint(self, date:str, name:str):
        checkDate(date)
        if len([plantingPoint.OCCUPIED for plantingPoint in self.__plantingPoints if plantingPoint.OCCUPIED == False]) > 0:
            index = [plantingPoint.OCCUPIED for plantingPoint in self.__plantingPoints].index(False)
            self.__plantingPoints[index].addSeeding(date, name)
            self.__emptyPlantingPoints -= 1
        
    def occupiedLen(self) -> int:
        return len([plantingPoint.OCCUPIED for plantingPoint in self.__plantingPoints if plantingPoint.OCCUPIED == True])
   
    def saveDataInFile(self):
        data = []
        data.append({"TEMPERATURE": self.AVARAGE_TEMPERATURE})
        for plantingPoint in self.__plantingPoints:
            data.append(plantingPoint.getDict())
        jsonData = json.dumps(data, indent = 4)
        with open(f"files/greenhouses/{self.ID}.json", "w") as f:
            f.write(jsonData)

    # SPECIAL CLASS METHODS
    def __str__(self):
        plantingPointsOccupied = self.occupiedLen()
        return f"GREENHOUSE: Id: {self.__id}, avarage temperature: {self.__avarageTemperature}, planting points occupied: {plantingPointsOccupied}/{NUMBER_OF_PLANTING_POINTS}"