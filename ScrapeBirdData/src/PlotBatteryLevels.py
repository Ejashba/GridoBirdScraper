import matplotlib.pyplot as plt
import os
#from datetimerange import DateTimeRange
from collections import OrderedDict
import numpy as np
from datetime import datetime
from time import sleep

class GraphPlotter:

    def plotGraph(self, xseries, yseries, xlabel, ylabel, title, plotfunc=plt.plot):
        plotfunc(xseries, yseries)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.show()

    def plotScooterBatteryLevels(self, id, path):
        filename = f'Bird {id}.txt'
        file = open(f'{path}{filename}', 'r')

        battery_levels = [] #y axis
        times = [] #x axis
        for line in file.readlines():
            pieces = line.split(', ')
            date_pieces = pieces[0].split()
            date, time = date_pieces[0], date_pieces[1]
            time_no_seconds = time[:5]
            times.append(str(time_no_seconds))
            battery_levels.append(int(pieces[1].strip()))

        self.plotGraph(times, battery_levels, 'Time', 'Battery Level (%)', f'Bird Scooter {id} Battery Data\n{date}')
        #plt.show()

    def getTimeRange(self, time, radius):
        time_range = []
        pieces = time.split(':')
        #print(pieces)
        seconds = int(pieces[2])

        addendum = 1 if seconds >= 30 else 0
        minutes = int(pieces[1]) + addendum

        addenduh = 0
        if minutes == 60:
            addenduh = 1
            minutes = 0
        hours = int(pieces[0]) + addenduh

        #print(hours, minutes)
        zero_pad_hours = ''
        for i in range(-radius, radius+1):
            currMin = minutes + i
            currHour = hours
            if minutes + i == 60:
                currHour = hours + 1
                currMin = 0
            elif minutes + i > 60:
                currHour = hours + 1
                currMin = minutes + i - 60
            elif minutes + i < 0:
                currMin = 60 + i
                currHour = hours - 1

            if currHour < 0:
                currHour = 23 + hours

            zero_pad_minutes = ''
            if len(str(currMin)) == 1:
                zero_pad_minutes = '0'
            if currHour == 24:
                currHour = 0
            if len(str(currHour)) == 1:
                zero_pad_hours = '0'
            time_range.append(f'{zero_pad_hours}{currHour}:{zero_pad_minutes}{currMin}')
        return time_range

    def removeSeconds(self, t):
        return t[:5]

    def plotBatteryBinsAtTime(self, desired_date, desired_time, cities, foldername='IDData'):
        """
        desired_date MUST be in yyyy-mm-dd

        """
        eg = 'MEX, 8a9b2676-4e2d-4d91-b22f-e8ffeb9bffbd, 97, 13588, 9g3qx2kprhhj'

        desired_time = self.removeSeconds(desired_time)
        percent_counts = [0 for i in range(101)]
        bins_axis = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100'] #x-axis
        #assert len(bins_markers) == len(bins_axis)
        numberInBins = [0 for _ in range(len(bins_axis))] # y axis
        numBelow40 = 0
        total_files = 0
        for filename in os.listdir(foldername):

            time_in_filename = filename.split('.')[0].split()[2] #Feb 2021: decremented by 1
            date_in_filename = filename.split('.')[0].split()[1] #Feb 2021: decremented by 1

            if time_in_filename == desired_time and date_in_filename == desired_date:
                with open(f'{foldername}/{filename}', 'r') as file:
                    for line in file.readlines():
                        pieces = line.strip('\n').split(', ')
                        city = pieces[0]
                        if city in cities:
                            charge = int(pieces[2])
                            percent_counts[charge] += 1
                break

        numberInBins = [sum(percent_counts[10*i:10*(i+1)]) for i in range(len(bins_axis))]
        print(numberInBins)
        assert sum(percent_counts) == sum(numberInBins)
        numBelow40 = sum(numberInBins[:4])
        #print(f'total files: {total_files}')
        print(numberInBins)
        print(percent_counts)
        print(f'scooters gathered: {sum(percent_counts)}')
        print(f'# Below 40%: {numBelow40}')
        title = f'Bird Scooter data at {desired_time} on {desired_date} for {", ".join([c for c in cities])}'
        self.plotGraph(bins_axis, numberInBins, 'Percent Charge', 'Number of Scooters', title, plt.bar)

    def determineStationChargedScooters(self, desired_date): #TODO implement checking for a single day ONLY
        total, grido_charged = 0, 0
        for filename in os.listdir('BirdIDData'):
            total += 1
            currCharge = -1
            currDay = ''
            with open(f'BirdIDData/{filename}', 'r') as file:
                for line in file.readlines():
                    pieces = line.strip('\n').split(', ')
                    date_time = pieces[0].split(' ')
                    date = date_time[0]
                    time = date_time[1]
                    charge = int(pieces[1])
                    datePieces = date.split('-')
                    year = int(datePieces[0])
                    month = int(datePieces[1])
                    day = int(datePieces[2])
                    if currCharge == -1:
                        currCharge = charge
                    if currDate == '':
                        currDay = day
                    if charge > currCharge and ():
                        pass

    eg = 'Bird, MEX, 2f0764ee-4fa3-4adb-9344-301b113add55, 96, 13430, No update data, 9g3qx2st0ygu, (scrape datetime to go here)'

    def avgConsumed(self, foldername, cityCode, scooterBrand):
        scooter_list = {} #keys: id, values: list of charges
        times = []  # x-axis

        # compile list of charges
        filenames = sorted(os.listdir(foldername))
        for filename in filenames:
            fname_date = filename.split('.')[0].split()[0]
            fname_time = filename.split('.')[0].split()[1]
            fname_datetime = f'{fname_date} {fname_time}'
            times.append(fname_datetime)
            with open(f'{foldername}/{filename}', 'r') as f:
                for line in f.readlines():
                    pieces = line.split(', ')
                    if not pieces[3].isdigit(): #ignore all Lime scooters for now, no way of telling their battery charge
                        continue
                    charge = int(pieces[3])
                    id = pieces[2]
                    if id not in scooter_list:
                        scooter_list[id] = [charge]
                    else:
                        scooter_list[id] += [charge]
        times.sort()
        #Scooter_list is a list of id's with charges

        #compile diffs list
        diffs = {} #{id: {time: charge, time: charge, ...}, id: {...}
        for id in scooter_list:
            if id not in diffs:
                diffs[id] = {}
            for i in range(1, len(scooter_list[id])):
                #print(times) #some IndexError is happening with times[i] no clue why
                diffs[id].update({times[i]: scooter_list[id][i] - scooter_list[id][i-1]})
        #print(diffs)

        #print(diffs['a2551d9a-1e52-49fd-8f45-43a645c2c964'])
        consumed = OrderedDict() #
        consumed = {t: [] for t in times}  # y-axis
        for id in diffs:
            for t in diffs[id]:
                consumed[t].append(diffs[id][t])
        #print(consumed)

        num_scooters_at_time = {t: len(consumed[t]) for t in times}
        #print(num_scooters_at_time)

        avgs_consumed = OrderedDict()
        for t in consumed:
            if len(consumed[t]) == 0:
                avgs_consumed[t] = 0 #MAKE SURE THIS IS ONLY THE FIRST ONE
                continue
            avgs_consumed[t] = sum(consumed[t])/len(consumed[t])
        #print(avgs_consumed)

        #BEGIN 2021 CUMULATIVE MODIFICATION

        running_total = 0
        for datetime in avgs_consumed:
            running_total += avgs_consumed[datetime]
            avgs_consumed[datetime] = running_total
        print(avgs_consumed)
        #END 2021 CUMULATIVE MODIFICATION

        interval = 1
        #print(sum(list(avgs_consumed.values())))
        self.plotGraph([elem.split()[1] for elem in avgs_consumed.keys()], list(avgs_consumed.values()), 'Time', 'Charge Consumed (%)', f'Bird Data on {fname_date}')

    eg = 'Bird, MEX, 2f0764ee-4fa3-4adb-9344-301b113add55, 96, 13430, No update data, 9g3qx2st0ygu, (scrape datetime to go here)'

    def getTimestampScooterIDDict(self, foldername, city_codes):
        """
        creates {timestamp: [id, id, id, ...], timestamp: [id, id, ...], ...}

        """
        times = [] # x-axis
        scooters_by_timestamp = {}
        net_changes = []
        all_scooters_seen = set()

        new_scooters_list = []
        exited_scooters_list = []

        pings_since_seen = {}

        #compile scooter ids into dictionary (scooters_by_timestamp)
        for filename in sorted(os.listdir(foldername)): #MUST BE sorted otherwise will read file in random order
            timestamp = filename.split('.')[0]
            time = timestamp.split()[1]
            scooters_by_timestamp.update({timestamp: []})
            times.append(time)
            with open(f'{foldername}/{filename}', 'r') as file:
                for line in file.readlines():
                    line = line.strip('\n')
                    pieces = line.split(', ')
                    id = pieces[2]
                    city = pieces[1]
                    charge = pieces[3]
                    geohash = pieces[6]
                    scooter_brand = pieces[0]
                    if city in city_codes:
                        scooters_by_timestamp[timestamp].append(id)
        return scooters_by_timestamp


    # timestamp: {id: 0/1, id: 0/1, ...}, timestamp: {...}
    def trackScooterAbsencesInPings(self, cities, foldername='IDData'):
        scooters_by_timestamp = self.getTimestampScooterIDDict(foldername, cities)
        for timestamp in scooters_by_timestamp:
            scooters_by_timestamp[timestamp].sort()

        all_ids_seen = set()
        for timestamp in scooters_by_timestamp: #elem[0] is id in list [id, charge, geohash]
            all_ids_seen.update(set(scooters_by_timestamp[timestamp]))

        all_ids_ordered = sorted(list(all_ids_seen))

        for timestamp in scooters_by_timestamp:
            for id_index in range(len(scooters_by_timestamp[timestamp])):
                if all_ids_ordered.index(id_index):
                    pass


        print('############'+str(len(all_ids_seen))+'##############')
        sleep(10)
        ids_seen_at_timestamp = {}
        prev_timestamp_ids = {}
        for timestamp in scooters_by_timestamp:
            ids_seen_at_timestamp.update({timestamp: {}})
            for id in all_ids_seen:
                if id not in scooters_by_timestamp[timestamp]:
                    ids_seen_at_timestamp[timestamp].update({id: 0})
                elif id in scooters_by_timestamp[timestamp]:
                    ids_seen_at_timestamp[timestamp].update({id: 1})

        for id in all_ids_seen:
            for timestamp in ids_seen_at_timestamp:
                pass


        print(ids_seen_at_timestamp)


    def trackNewScootersInCity(self, foldername): #TODO write function for tracking scooters entering and exiting city
        scooters_by_timestamp = self.getTimestampScooterIDDict(foldername, ['MEX'])

        #for timestamp in scooters_by_timestamp:


        #calculate new scooters at timestamp and
        iteration_count = 0
        prev_seen = set()
        new_scooter_count = 0
        curr_seen = set()
        all_scooters_seen = set()

        pings_absent = {} #{timestamp: {id: pingsabsent(int), id: pingsabsent}}

        #scooters re-entering should have battery level above 90
        total_scooters = []
        new_scooters_list = []
        exited_scooters_list = []
        net_changes = []
        for timestamp in scooters_by_timestamp:
            curr_seen = set()
            if iteration_count == 0:
                prev_seen = set(scooters_by_timestamp[timestamp])
                pings_absent = {id: 0 for id in scooters_by_timestamp[timestamp]}
                iteration_count += 1
                continue
            for scooter_id in scooters_by_timestamp[timestamp]:
                curr_seen.add(scooter_id)
                all_scooters_seen.add(scooter_id)


            new_scooter_set = curr_seen - prev_seen
            #print(new_scooter_set)
            new_scooters_list.append(new_scooter_set)

            scooters_left_set = prev_seen - curr_seen
            #print(scooters_left_set)
            exited_scooters_list.append(scooters_left_set)

            left_and_entered_list = list(new_scooter_set) + list(scooters_left_set)
            uniques = set(left_and_entered_list)
            print(f'##########{len(uniques)}#########\n')

            net_change = len(new_scooter_set) - len(scooters_left_set)
            net_changes.append(net_change)

            total_scooters.append(len(curr_seen))

            #reset prev_seen set
            prev_seen = set()
            for elem in curr_seen:
                prev_seen.add(elem)

            iteration_count += 1

        exited_scooters_counts = [len(s) for s in exited_scooters_list]
        new_scooters_counts = [len(s) for s in new_scooters_list]
        #print(total_scooters)
        #plt.plot(times, total_scooters)
        #plt.xlabel('Time')
        #plt.ylabel('Total Scooters')
        #plt.title(f'Total scooters on {str(datetime.now())}')

        #print(net_changes)
        #print(new_scooters_counts)
        neg_exited_scooters_counts = []
        for n in exited_scooters_counts:
            assert n >= 0
            neg_exited_scooters_counts.append(-n)
        #print(exited_scooters_counts)


        #print([list(s)[:3] for s in new_scooters_list])
        #print([list(s)[:3] for s in exited_scooters_list])
        #if scooter hasn't been present for
        interval = 1

        net_change_series = plt.plot(times[::interval], net_changes[::interval], 'o', label='Net Change')
        entered_series = plt.plot(times[::interval], new_scooters_counts[::interval], 'o', label='Entered')
        exited_series = plt.plot(times[::interval], neg_exited_scooters_counts[::interval], 'o', label='Exited')
        zero_series = plt.plot(times[::interval], [0 for t in times[::interval]])
        plt.legend(['Net', 'Entered', 'Exited']) #'Entered', 'Exited'])
        plt.xlabel('Time')
        plt.ylabel('# of Scooters')
        plt.title(f'Bird Data on {str(datetime.now())}')

    #def convToMXTime(timeUTCFormat):

    desired_id = '0df5e637-6de0-4d4d-b839-cade559f188b'

    def padZero(self, n):
        if len(str(n)) == 1:
            return f'0{n}'
        return str(n)

    def plotBatteryBinsSpecificDate2021(self, foldername, date, time, cityCode):
        #plots based on format:
        #ScooterBrand, CityCode, ScooterID, BatteryCharge, EstimatedRange, UpdateTime, Geohash

        #date MUST be in format: yyyy-mm-dd
        foldername = 'IDData08-08'
        #bin_ranges = [range(i*10, (i+1)*10) for i in range(10)] + [[100]] #create graphing bins
        bins = [0]*10
        for filename in os.listdir(foldername):
            filename_without_ext = filename.split('.')[0] #remove .txt extension
            date_in_file = filename_without_ext.split()[0]
            time_in_file = filename_without_ext.split()[1]
            if date == date_in_file and time == time_in_file:
                with open(f'{foldername}/{filename}', 'r') as file:
                    for line in file.readlines():
                        pieces = line.strip('\n').split(', ')
                        city = pieces[1]
                        charge = int(pieces[3])
                        if cityCode == city:
                            bins[min(charge//10, 9)] += 1 #min accounts for charge=100 edge case
        bins_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-100'] #x-axis
        title = f'Distribution of scooters in {cityCode} on {date} at {time}'
        print(bins)
        self.plotGraph(bins_labels, bins, 'Percent Charge', 'Number of Scooters', title, plt.bar)
        #plt.show()

    def plotBatteryBinsOverTime2021(self, foldername, date, threshold, cityCode, above=True):
        #comparisonDir is 'above' or 
        #starting with charges above threshold parameter
        #plots based on format:
        #ScooterBrand, CityCode, ScooterID, BatteryCharge, EstimatedRange, UpdateTime, Geohash

        #date MUST be in format: yyyy-mm-dd
        foldername = 'IDData08-08'
        #bin_ranges = [range(i*10, (i+1)*10) for i in range(10)] + [[100]] #create graphing bins
        bins = [] #list of numbers of scooters with charge above threshold
        bin_labels = [] #list of times
        sorted_file_list = sorted(os.listdir(foldername))
        for filename in sorted_file_list:
            filename_without_ext = filename.split('.')[0] #remove .txt extension
            date_in_file = filename_without_ext.split()[0]
            time_in_file = filename_without_ext.split()[1]
            if date == date_in_file:
                with open(f'{foldername}/{filename}', 'r') as file:
                    bins.append(0)
                    bin_labels.append(time_in_file)
                    for line in file.readlines():
                        pieces = line.strip('\n').split(', ')
                        city = pieces[1]
                        charge = int(pieces[3])
                        if cityCode == city:
                            if above and charge >= threshold:
                                bins[-1] += 1
                            elif not above and charge <= threshold:
                                bins[-1] += 1

        #bins_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100'] #x-axis
        title = f"Timeline of scooters with charge {'over' if above else 'under'} {threshold} inclusive in {cityCode} on {date}"
        #title = f"Total scooters in {cityCode} on {date}"
        print(bins)
        self.plotGraph(bin_labels, bins, 'Time', 'Number of Scooters', title)
        #plt.show()   

    #2021 addition
    def plotSingleScooterCharge(self, foldername, scooterID):
        charges = []
        times = []
        IDdict = {}
        for filename in sorted(os.listdir(foldername)):
            filename_without_ext = filename.split('.')[0]
            filename_pieces = filename_without_ext.split()
            date = filename_pieces[0]
            time = filename_pieces[1]
            times.append(time)
            sanity = 0 #sanity check for more than one ID found in a single file
            with open(f'{foldername}/{filename}', 'r') as file:
                for line in file.readlines():
                    charge = -1
                    pieces = line.strip('\n').split(', ')
                    id = pieces[2]
                    if id == scooterID:
                        #print('found it')
                        sanity += 1
                        if sanity == 2:
                            raise Exception(f'Duplicate ID {id} found in {filename}')
                        if not pieces[3].isdigit():
                            continue
                        charge = int(pieces[3])
                        break
                charges.append(charge)
        self.plotGraph(times, charges, 'Time', 'Charge', f'Charges for {scooterID}')

                
gp = GraphPlotter()

if __name__ == '__main__':
    
    #gp.plotBatteryBinsSpecificDate2021(foldername='IDData08-08', date='2019-08-08', time='19:47', cityCode='MEX')

    #gp.plotBatteryBinsOverTime2021(foldername='IDData08-08', date='2019-08-08', threshold=39, cityCode='MEX', above=False)

    #gp.avgConsumed('IDData08-08')

    gp.plotSingleScooterCharge('IDData08-08', '55f3a73e-4df5-470a-8786-dddf62210cf7')

    #desired_date, desired_time, cities, foldername='IDData')
    #
    #time_ranges = [f'{gp.padZero(i)}:00:00' for i in range(6, 19)]
    #fig, axs = plt.subplots(13)
    #for rang in time_ranges:
    #    gp.plotBatteryBinsAtTime('2019-07-27', rang, ['MEX'], 'BirdIDData')#'BirdDataJuly29-31')
    #    print(f'{rang} plotted')
    #    plt.show()

    #time_ranges = [f'{padZero(i)}:00:00' for i in range(6, 19)]
    #fig, axs = plt.subplots(13)
    #for rang in time_ranges:
    #    plotBatteryBinsAtTime('2019-07-27', rang, 5, ['MEX'], 'BirdDataJuly29-31')#'BirdDataJuly29-31')
    #    print(f'{rang} plotted')
    #    plt.show()
    #desired_cities = ['MEX']
    #plotBatteryBinsAtTime('2019-08-01', '18:57:00', desired_cities)
    #plt.show()
    #print(getTimeRange('00:00:30', 5))
    #print(plotBatteryBinsAtTime('', '15:53:52', 5))
    #plotBatteryBinsAtTime('2019-07-26', '18:00:00', 10)
