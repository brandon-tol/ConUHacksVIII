import CSVParser
import Entry
from NodeDistance import getFunction

def testWeights(a, b, c, d, e):
    return getFunction(0.2, 0.2, 0.2, 0.2, 0.2)

def sortingKey(element):
    getNodeDistance = testWeights(0.2, 0.2, 0.2, 0.2, 0.2)
    return getNodeDistance(Entry.Entry(None, 0, Entry.Day.MONDAY, 1, 1, Entry.Server.US_EAST_1, Entry.Platform.STEAM, None, Entry.MatchmakingOutcome.SUCCESS, 7, None), element)


if __name__ == "__main__":
    entryList = CSVParser.parse("test_data.csv")

    sortedList = sorted(entryList, key=sortingKey)
    print(sortedList[0].matchId)