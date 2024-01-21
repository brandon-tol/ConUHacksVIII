import Entry

def parse(filename: str):
    entrylist = list()
    with open(filename, 'r') as file:
        next(file) # TODO: skip the first line for now
        for line in file:
            arr = line.upper().split(',')
            time = arr[1].split(':')
            entrylist.append(Entry.Entry(arr[0], int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2]), Entry.Day.fromStr(arr[2]), 1 if arr[3] == "KILLER" else 0, int(arr[4]), Entry.Server(arr[5]), Entry.Platform(arr[6]), int(arr[7]), Entry.MatchmakingOutcome(arr[8]), int(arr[9]), arr[10]))
    
    return entrylist