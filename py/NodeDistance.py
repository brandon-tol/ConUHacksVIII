import Entry
import math

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

    if a.matchmakingOutcome is not Entry.MatchmakingOutcome.SUCCESS or b.matchmakingOutcome is not Entry.MatchmakingOutcome.SUCCESS or a.server is not b.server:
        return math.inf
    return getDistance(dayWeight/8 * circularCompare(a.dayOfWeek.value, b.dayOfWeek.value, 8), timeWeight/86400 * circularCompare(a.startTime, b.startTime, 86400), partyWeight/5 * abs(a.partySize - b.partySize), mmrWeight/20 * abs(a.mmr - b.mmr), roleWeight * abs(a.role - b.role))