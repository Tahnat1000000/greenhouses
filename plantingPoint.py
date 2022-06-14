import helper

class PlantingPoint:
    idNumber = 1
    # CONSTRUCTOR
    def __init__(self, date:str="00/00/0000", name:str="-", occupied:bool=False):
        self.__id = str(PlantingPoint.idNumber)
        if date == "00/00/0000" and name == "-":
            self.__seedingDate = date
            self.__name = name
            self.__occupied = occupied
        else:
            self.__setSeedingDate(date)
            self.__setName(name)
            self.__setOccupied(occupied)

        PlantingPoint.idNumber += 1
        if(PlantingPoint.idNumber == 5001):
            PlantingPoint.idNumber = 0


    # GETTERS AND SETTERS
    def __getId(self) -> str:
        return self.__id
    
    def __getSeedingDate(self) -> str:
        return self.__seedingDate

    def __setSeedingDate(self, date:str):
        helper.checkDate(date)
        self.__seedingDate = date

    def __getName(self) -> str:
        return self.__name

    def __setName(self, name:str):
        if type(name) != str:
            raise ValueError("ERROR -> SEEDLING NAME SHOULD BE STRING")
        self.__name = name

    def __isOccupied(self) -> bool:
        return self.__occupied

    def __setOccupied(self, occupied:bool):
        if type(occupied) != bool:
            raise ValueError("ERROR -> OCCUPIED MUST BE BOOLEAN, TRUE OR FALSE")
        self.__occupied = occupied

    ID = property(__getId)
    SEEDING_DATE = property(__getSeedingDate, __setSeedingDate)
    NAME = property(__getName, __setName)
    OCCUPIED = property(__isOccupied, __setOccupied)


    # CLASS METHODS
    def addSeeding(self, date:str, name:str):
        self.__setSeedingDate(date)
        self.__setName(name)
        self.__setOccupied(True)

    def harvestSeedling(self):
        self.__setSeedingDate("00/00/0000")
        self.__setName("-")
        self.__setOccupied(False)

    def getPlantingPointStringList(self) -> list:
        return [self.ID, self.SEEDING_DATE, self.NAME, self.OCCUPIED]
        
    def getDict(self) -> dict:
        return {"ID":self.ID, "DATE":self.SEEDING_DATE, "NAME":self.NAME, "OCCUPIED":self.OCCUPIED}
        
    # SPECIAL CLASS METHODS
    def __str__(self):
        return f"PLANTING POINT: Id {self.__id}, Seeding date: {self.__seedingDate}, Name: {self.__name}, Occupied: {self.__occupied}"
