import matplotlib.pyplot as plt
import os

def plotScooterBatteryLevels(id):
    filename = f'Bird {id}.txt'
    file = open(f'BirdIDData/{filename}', 'r')

    battery_levels = [] #y axis
    times = [] #x axis
    for line in file.readlines():
        pieces = line.split(', ')
        date_pieces = pieces[0].split()
        date, time = date_pieces[0], date_pieces[1]
        time_no_seconds = time[:5]
        times.append(str(time_no_seconds))
        battery_levels.append(int(pieces[1].strip()))

    plt.plot(times, battery_levels)
    plt.ylabel('Battery Level (%)')
    plt.xlabel('Time')
    plt.title(f'Bird Scooter {id} Battery Data\n{date}')
    plt.show()

entry_ex = '2019-07-25 15:53:52, 47'

def getTimeRange(time, radius):
    time_range = []

    pieces = time.split(':')
    #print(pieces)
    seconds = int(pieces[2])

    addendum = 1 if seconds >= 30 else 0
    minutes = int(pieces[1]) + addendum

    addenduh = 1 if minutes == 60 else 0
    hours = int(pieces[0]) + addenduh

    zero_pad_hours = ''
    for i in range(-radius, radius+1):
        if minutes + i == 60:
            hours += 1
            minutes = -i
        zero_pad_minutes = ''
        if len(str(minutes+i)) == 1:
            zero_pad_minutes = '0'
        if hours == 24:
            hours = 0
        if len(str(hours)) == 1:
            zero_pad_hours = '0'
        time_range.append(f'{zero_pad_hours}{hours}:{zero_pad_minutes}{minutes+i}')
    return time_range


def plotBatteryBinsAtTime(desired_date, desired_time, desired_range):
    """
    desired_date MUST be in yyyy-mm-dd

    """
    bins = [20, 40, 60, 80, 100] # x axis
    numberInBins = [0 for _ in range(5)] # y axis
    for filename in os.listdir('BirdIDData'):
        file = open(f'BirdIDData/{filename}', 'r', errors='replace')
        for line in file.readlines():
            pieces = line.strip('\n').split(', ')
            if len(pieces) == 1:
                continue
            date_time = pieces[0].split()
            time = date_time[1]
            time_range = getTimeRange(time, desired_range)
            #print(time_range)
            desired_time_no_seconds = f'{desired_time.split(":")[0]}:{desired_time.split(":")[1]}'
            if desired_time_no_seconds in time_range:
                for b in range(len(bins)):
                    int(pieces[1])
                    if int(pieces[1]) <= bins[b]:
                        numberInBins[b] += 1
                        break
    plt.bar(bins, numberInBins)
    plt.ylabel('Number of Scooters')
    plt.xlabel('Time Bins')
    plt.title(f'Bird Scooter data at {desired_time} on {desired_date}')
    plt.show()
    return numberInBins

def determineStationChargedScooters():
    total, grido_charged = 0, 0
    for filename in os.listdir('BirdIDData'):
    total += 1
        with open(f'BirdIDData/{filename}', 'r') as file:
            


desired_id = '0df5e637-6de0-4d4d-b839-cade559f188b'

if __name__ == '__main__':
    #print(getTimeRange('23:58:29', 5))
    #print(plotBatteryBinsAtTime('', '15:53:52', 5))
    plotScooterBatteryLevels(desired_id)
