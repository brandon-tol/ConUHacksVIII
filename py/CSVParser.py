from enum import Enum

class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

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
        
    def compare(self, other):
        return self - other


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