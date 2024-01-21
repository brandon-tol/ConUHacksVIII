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

def getNodeDistance(a: Entry, b: Entry):
    dayWeight = 1
    timeWeight = 0
    partyWeight = 1
    mmrWeight = 1
    roleWeight = 1000

    if a.matchmakingOutcome is not Entry.MatchmakingOutcome.SUCCESS or b.matchmakingOutcome is not Entry.MatchmakingOutcome.SUCCESS or a.server is not b.server:
        return math.inf
    return getDistance(dayWeight * circularCompare(a.dayOfWeek.value, b.dayOfWeek.value, 8), timeWeight * circularCompare(a.startTime, b.startTime, 86400), partyWeight * abs(a.partySize - b.partySize), mmrWeight * abs(a.mmr - b.mmr), roleWeight * abs(a.role - b.role))