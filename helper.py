### CONSTS
NUMBER_OF_PLANTING_POINTS = 500 # THE NUMBER OF PLANTING POINTS IN EACH GREENHOUSE

### FUNCTIONS THAT USEFULL IN OTHER CLASSES
def checkDate(date:str):
    if type(date) != str or len(date.split("/")) != 3:
        raise ValueError("ERROR -> DATE SHOULD BE STRING, EXAMPLE: 01/01/2022")
    day, month, year = date.split("/")
    if len(day) != 2 or len(month) != 2 or len(year) != 4:
        raise ValueError("ERROR -> DATE SHOULD BE STRING, EXAMPLE: 01/01/2022")
    if not day.isdigit() or not month.isdigit() or not year.isdigit():
        raise ValueError("ERROR -> DATE SHOULD BE STRING, EXAMPLE: 01/01/2022")  

  