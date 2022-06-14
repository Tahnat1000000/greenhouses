class SeedlingType:
    # CONSTRUCTOR
    def __init__(self, name:str, growTime:int, temperatureRange:tuple):
        self.__setName(name)
        self.__setGrowTime(growTime)
        self.__setTemperatureRange(temperatureRange)
    

    # GETTERS AND SETTERS
    def __getName(self) -> str:
        return self.__name

    def __setName(self, name:str):
        if type(name) != str:
            raise ValueError("ERROR -> SEEDLING NAME SHOULD BE STRING")
        self.__name = name

    def __getGrowTime(self) -> int:
        return self.__growTime

    def __setGrowTime(self, growTime:int):
        if type(growTime) != int:
            raise ValueError("ERROR -> SEEDLING GROW TIME SHOULD BE INTEGER")
        self.__growTime = growTime

    def __getTemperatureRange(self) -> tuple:
        return self.__temperatureRange

    def __setTemperatureRange(self, temperatureRange:tuple):
        if type(temperatureRange) != tuple or len(temperatureRange) != 2:
            raise ValueError("ERROR -> SEEDLING TEMPERATURE RANGE SHOULD BE TUPLE WITH 2 ITEMS - MIN TEMP AND MAX TEMP")
        for value in temperatureRange:
            if type(value) != int and type(value) != float:
                raise ValueError("ERROR -> SEEDLING TEMPERATURE RANGE SHOULD BE TUPLE WITH 2 ITEMS - MIN TEMP AND MAX TEMP")
        self.__temperatureRange = temperatureRange

    NAME = property(__getName, __setName)
    GROW_TIME = property(__getGrowTime, __setGrowTime)
    TEMPERATURE_RANGE = property(__getTemperatureRange, __setTemperatureRange)


    # SPECIAL CLASS METHODS
    def __str__(self) -> str:
        return f"SEEDLING TYPE: Name: {self.__name}, Grow time in days: {self.__growTime}, Temperature range: {self.__temperatureRange[0]} - {self.__temperatureRange[1]}"


