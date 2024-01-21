import random


def randomStartTime():
    hour = random.randint(0, 23)
    min = random.randint(0, 59)
    sec = random.randint(0, 59)
    return f'{hour}:{min}:{sec}'


def randDayOfWeek():
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return random.choice(days_of_week)


def randomServer():
    regions = ['ap-southeast-1', 'ap-southeast-2', 'us-west-1', 'us-west-2', 'eu-central-1', 'eu-central-2', 'us-east-1', 'us-east-2']

    return random.choice(regions)


def randomPlatform():
    options = ["xsx", "cgs", "ps5", "steam"]
    return random.choice(options)


def randomRole():
    num = random.randint(0, 100)

    if num <= 20:
        return "killer"
    else:
        return "survivor"


def randomMatchmakingOutcome():
    num = random.randint(0, 100)

    # under 2% chance of cancelling
    if num <= 2:
        return "played_cancelled"
    else:
        return "success"


def randomName():
    name = ["Killer", "Survivor"]
    return f'{random.choice(name)} {random.randint(0, 50)}'


class Row:
    counter = 1

    def __init__(self):
        self.MATCH_ID = Row.counter
        Row.counter += 1

        self.MATCHMAKING_ATTEMPT_START_TIME_UTC = randomStartTime()
        self.MATCHMAKING_DAY_OF_WEEK = randDayOfWeek()
        self.PLAYER_ROLE = randomRole()
        self.PARTY_SIZE = self.randomPartySize()
        self.SERVER_NAME = randomServer()
        self.PLATFORM = randomPlatform()
        self.MATCHMAKING_OUTCOME = randomMatchmakingOutcome()
        self.MMR_GROUP_DECILE = random.randint(1, 20)
        self.CHARACTER_NAME = randomName()

        self.QUEUE_DURATION_IN_SECS = None
        self.generateQueueTime()

    def increment(self):
        Row.counter += 1

    def randomPartySize(self):
        if self.PLAYER_ROLE == "killer":
            return 1
        else:
            return random.randint(1, 4)

    def generateQueueTime(self):

        queueTime = random.choice(queueTimeSample)
        queueTimeSample.remove(queueTime)

        # if between 6pm and 12 am, decrease
        is_evening = 18 <= int(self.MATCHMAKING_ATTEMPT_START_TIME_UTC.split(":")[0]) < 24

        # if day falls on weekend
        is_weekend = self.MATCHMAKING_DAY_OF_WEEK in ["Saturday", "Sunday"]

        # during evenings time gets reduced by 25%
        if is_evening:
            queueTime *= (1 - .25)

        # during weekends queue is reduced by 20%
        if is_weekend:
            queueTime *= (1 - 0.20)

        self.QUEUE_DURATION_IN_SECS = int(queueTime)

    def __str__(self):
        return f"{self.MATCH_ID},{self.MATCHMAKING_ATTEMPT_START_TIME_UTC},{self.MATCHMAKING_DAY_OF_WEEK}," \
               f"{self.PLAYER_ROLE},{self.PARTY_SIZE},{self.SERVER_NAME},{self.PLATFORM}," \
               f"{self.QUEUE_DURATION_IN_SECS},{self.MATCHMAKING_OUTCOME},{self.MMR_GROUP_DECILE}," \
               f"{self.CHARACTER_NAME},"


import numpy as np


def generate_lognormal_samples(mean: float, std_dev: float, num_samples: int) -> np.ndarray:
    """
    Generate random samples from a log-normal distribution.

    Parameters:
    mean (float): Mean of the log-normal distribution.
    std_dev (float): Standard deviation of the log-normal distribution.
    num_samples (int): Number of samples to generate.

    Returns:
    np.ndarray: Array of generated samples.
    """

    if std_dev <= 0:
        raise ValueError("Standard deviation must be greater than zero.")

    # Generate random samples from a normal distribution
    normal_samples = np.random.normal(mean, std_dev, num_samples)

    # Transform them to follow a log-normal distribution
    lognormal_samples = np.exp(normal_samples)

    return list(lognormal_samples)


import matplotlib.pyplot as plt

numberOfRows = 100000

queueTimeSample = generate_lognormal_samples(4, 0.65, numberOfRows)

# # Plotting the data
# plt.hist(queueTimeSample, bins=50)
#
# # Adding labels and title
# plt.xlabel('Queue Time')
# plt.ylabel('Count')
# plt.title('Simple Line Plot')
#
# # Display the plot
# plt.show()

rows = list()
output_file = "data.csv"

for _ in range(0, numberOfRows):
    rows.append(Row())

with open(output_file, 'w') as file:
    # Write header if needed
    file.write("MATCH_ID,MATCHMAKING_ATTEMPT_START_TIME_UTC,MATCHMAKING_DAY_OF_WEEK,"
               "PLAYER_ROLE,PARTY_SIZE,SERVER_NAME,PLATFORM,QUEUE_DURATION_IN_SECS,"
               "MATCHMAKING_OUTCOME,MMR_GROUP_DECILE,CHARACTER_NAME,\n")

    # Write each Row object to the file
    for row in rows:
        file.write(str(row) + '\n')

print(f"Data has been written to {output_file}")



