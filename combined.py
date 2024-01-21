from enum import Enum
import math
import pandas as pd

class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    def toStr(day):
        if day == Day.MONDAY:
            return "Monday"
        elif day == Day.TUESDAY:
            return "Tuesday"
        elif day == Day.WEDNESDAY:
            return "Wednesday"
        elif day == Day.THURSDAY:
            return "Thursday"
        elif day == Day.FRIDAY:
            return "Friday"
        elif day == Day.SATURDAY:
            return "Saturday"
        elif day == Day.SUNDAY:
            return "Sunday"
        else:
            return "Invalid Day"

    def fromStr(day_str: str):
        capitalized_str = day_str.upper()

        if capitalized_str == "MONDAY":
            return Day.MONDAY
        elif capitalized_str == "TUESDAY":
            return Day.TUESDAY
        elif capitalized_str == "WEDNESDAY":
            return Day.WEDNESDAY
        elif capitalized_str == "THURSDAY":
            return Day.THURSDAY
        elif capitalized_str == "FRIDAY":
            return Day.FRIDAY
        elif capitalized_str == "SATURDAY":
            return Day.SATURDAY
        elif capitalized_str == "SUNDAY":
            return Day.SUNDAY
        else:
            raise ValueError(f"Invalid day string: {day_str}")


class Server(Enum):
    AP_SOUTHEAST_1 = "AP-SOUTHEAST-1"
    AP_SOUTHEAST_2 = "AP-SOUTHEAST-2"
    US_WEST_1 = "US-WEST-1"
    US_WEST_2 = "US-WEST-2"
    EU_CENTRAL_1 = "EU-CENTRAL-1"
    EU_CENTRAL_2 = "EU-CENTRAL-2"
    US_EAST_1 = "US-EAST-1"
    US_EAST_2 = "US-EAST-2"

class Platform(Enum):
    STEAM = "STEAM"
    XSX = "XSX"
    PS5 = "PS5"
    CGS = "CGS"

class MatchmakingOutcome(Enum):
    SUCCESS = "SUCCESS"
    PLAYED_CANCELLED = "PLAYED_CANCELLED"

class Entry:
    matchId: str
    startTime: int
    dayOfWeek: Day
    role: int
    partySize: int
    server: Server
    platform: Platform
    queueDuration: int
    matchmakingOutcome: MatchmakingOutcome
    mmr: int
    charName: str

    def __init__(self, matchId, startTime, dayOfWeek, role, partySize, server, platform, queueDuration, matchmakingOutcome, mmr, charName):
        self.matchId = matchId
        self.startTime = startTime
        self.dayOfWeek = dayOfWeek
        self.role = role
        self.partySize = partySize
        self.server = server
        self.platform = platform
        self.queueDuration = queueDuration
        self.matchmakingOutcome = matchmakingOutcome
        self.mmr = mmr
        self.charName = charName

def parse(filename: str):
    entrylist = list()
    with open(filename, 'r') as file:
        next(file) # TODO: skip the first line for now
        for line in file:
            arr = line.upper().split(',')
            time = arr[1].split(':')
            entrylist.append(Entry(arr[0], int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2]), Day.fromStr(arr[2]), 1 if arr[3] == "KILLER" else 0, int(arr[4]), Server(arr[5]), Platform(arr[6]), int(arr[7]), MatchmakingOutcome(arr[8]), int(arr[9]), arr[10]))
    
    return entrylist

def getDistance(*args):
    x = 0
    for arg in args:
        x += math.pow(arg, 2)
    return math.sqrt(x)

def circularCompare(a, b, size):
    x = abs(a - b)
    y = size - x
    return x if x < y else y

def getFunction(dayWeight: float, timeWeight: float, partyWeight: float, mmrWeight: float, roleWeight: float):
    return lambda a, b: getNodeDistance(dayWeight, timeWeight, partyWeight, mmrWeight, roleWeight, a, b)

def getNodeDistance(dayWeight: float, timeWeight: float, partyWeight: float, mmrWeight: float, roleWeight: float, a: Entry, b: Entry):
    print(f"Debug: a.server={a.server}, b.server={b.server}")

    if a.matchmakingOutcome != MatchmakingOutcome.SUCCESS or b.matchmakingOutcome != MatchmakingOutcome.SUCCESS or a.server != b.server:
        print("Debug: Returning math.inf")
        return math.inf

    result = getDistance(dayWeight/8 * circularCompare(a.dayOfWeek.value, b.dayOfWeek.value, 8),
                         timeWeight/86400 * circularCompare(a.startTime, b.startTime, 86400),
                         partyWeight/5 * abs(a.partySize - b.partySize),
                         mmrWeight/20 * abs(a.mmr - b.mmr),
                         roleWeight * abs(a.role - b.role))

    print(f"Debug: Returning result={result}")
    return result


def get_absolute_correlations(file_path, dependent_variable):
    # Read data from the CSV file
    df = pd.read_csv(file_path, encoding='utf-8')

    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    # Identify the variables with the highest correlations to the dependent variable
    strong_correlations = correlation_matrix[dependent_variable].abs()

    # Take the absolute value of the correlations and convert them to float
    absolute_correlations = strong_correlations.abs().astype(float)

    # Extract the first five absolute correlations and create a tuple
    top_5_absolute_correlations = tuple(absolute_correlations.head(6))[1:]

    return top_5_absolute_correlations

def intToTime(time: int):
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60
    return f"{hours}:{minutes}:{seconds}"

def timeToInt(str: str):
    x = str.split(":")
    return x[0] * 3600 + x[1] * 60 + x[2]

def calculate_wait_time(time: int, day: Day, killer: bool, partySize: int, server: Server, platform: Platform, matchmakingOutcome: MatchmakingOutcome, mmr: int, charName: str):
    entryList = parse("test_data.csv")
    with open('parsed_data.csv', 'w') as file:
        file.write("Role,TimeofDay,DayofWeek,MMR,PartySize,QueueDuration\n")
        for entry in entryList:
            file.write(f"{entry.role}, {entry.startTime/86400}, {entry.dayOfWeek.value/8}, {entry.mmr/20}, {entry.partySize/5}, {entry.queueDuration}\n")

    weight_tuple = get_absolute_correlations('parsed_data.csv', 'QueueDuration')
    current = Entry(None, 10800, Day.SATURDAY, 0, 2, Server.EU_CENTRAL_2, Platform.STEAM, None, MatchmakingOutcome.SUCCESS, 8, None)
    sortingKey = lambda element: getNodeDistance(*weight_tuple, current, element)
    
    closestNeighbour = None
    maxDistance = math.inf
    for node in entryList:
        x = sortingKey(node)
        if x < maxDistance:
            closestNeighbour = node
            maxDistance = x

    return (closestNeighbour.queueDuration)

if __name__ == "__main__":
    print(calculate_wait_time(10800, Day.SATURDAY, False, 2, Server.EU_CENTRAL_2, Platform.STEAM, MatchmakingOutcome.SUCCESS, 8, None))