from seedlingType import SeedlingType

class Seedlings:
    # CONSTRUCTOR
    def __init__(self):
        self.__seedlingsTypes = []
        self.addSeedlingsByFile()
    
    # GETTERS AND SETTERS
    def __getSeedlingsTypes(self) -> list:
        return self.__seedlingsTypes

    def __setSeedlingsTypes(self, seedlingsTypes):
        if type(seedlingsTypes) != list:
            raise ValueError(f"ERROR: SEEDLINGS MUST BE LIST OF SEEDLING TYPE CLASS")
        for type in seedlingsTypes:
            if not isinstance(type, SeedlingType):
                raise ValueError(f"ERROR: SEEDLINGS MUST BE LIST OF SEEDLING TYPE CLASS")
        self.__seedlingsTypes = seedlingsTypes

    SEEDLINGS_TYPES = property(__getSeedlingsTypes, __setSeedlingsTypes)


    # CLASS METHODS
    def addSeedlingType(self, seedlingType:SeedlingType):
        self.__seedlingsTypes.append(seedlingType)

    def getGrowTimeByName(self, name:str) -> str:
        seedlingsNames = [seedling.name for seedling in self.__seedlingsTypes]
        if not name in seedlingsNames:
            raise ValueError("ERROR: SEEDLING NAME NOT FOUND")
        return self.__seedlingsTypes[seedlingsNames.index(name)].GROW_TIME
    
    def getTemperatureRangeByName(self, name:str) -> tuple:
        seedlingsNames = [seedling.name for seedling in self.__seedlingsTypes]
        if not name in seedlingsNames:
            raise ValueError("ERROR: SEEDLING NAME NOT FOUND")
        return self.__seedlingsTypes[seedlingsNames.index(name)].TEMPERATURE_RANGE

    def addSeedlingsByFile(self):
        self.__seedlingsTypes = []
        seedlingsFile = open("./files/seedlings.txt", "rt")
        for index, line in enumerate(seedlingsFile):
            if index == 0 : continue
            name, growTime, minTemp, maxTemp = line.split(",")[0], int(line.split(",")[1]), int(line.split(",")[2]), int(line.split(",")[3])
            self.__seedlingsTypes.append(SeedlingType(name, growTime, (minTemp, maxTemp)))
        seedlingsFile.close()

    def getSeedlingsStringList(self) ->list:
        seedlingsList = []
        seedlingsFile = open("./files/seedlings.txt", "rt")
        for index, line in enumerate(seedlingsFile):
            if index == 0 : continue
            seedlingsList.append(line.split("\n")[0])
        seedlingsFile.close()
        return seedlingsList


    # SPECIAL CLASS METHODS
    def __str__(self):
        returnStr = "SEEDLINGS TYPES:\n"
        for index, seedling in enumerate(self.__seedlingsTypes):
            returnStr += f"{index+1}) " + seedling.__str__() + "\n"
        return returnStr
        