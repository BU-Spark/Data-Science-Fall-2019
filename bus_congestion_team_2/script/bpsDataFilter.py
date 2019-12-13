import csv
import json

from interval import Interval

def getSchoolTime():
    pathTime = '../csv/schools_hr_fixed.csv'
    with open(pathTime, 'r', encoding='UTF-8') as f:
        csvData = csv.reader(f)
        i = 0
        beginHours, endHours = [], []
        for line in csvData:
            if i == 0:
                i += 1
                continue
            beginHours.append(int(line[2].split(' a.m. - ')[0].strip().split(':')[0]))
            endHours.append(int(line[2].split(' a.m. - ')[-1].replace(' p.m.', '').strip().split(':')[0])+12)
            i += 1
            if i == 127:
                break
    return (min(beginHours), max(beginHours), min(endHours), max(endHours))

def bpsFilter(beginHourA, beginHourB, endHourA, endHourB, interval):
    startInterval = Interval(beginHourA-interval, beginHourB+interval)
    endInterval = Interval(endHourA - interval, endHourB + interval)
    pathBPS = '../rawData/bps.csv'
    with open(pathBPS, 'r', encoding='UTF-8') as f:
        csvData = csv.reader(f)
        i = 0
        data = {}
        for line in csvData:
            if i == 0:
                i += 1
                continue
            time = line[0].split()[-1]
            timeHour = int(time.split(':')[0])
            # print(timeHour)
            if timeHour in startInterval or timeHour in endInterval:
                [logtime,latitude,longitude,heading,speed,vendorhardwareid] = line
                if vendorhardwareid not in data.keys():
                    data[vendorhardwareid] = {}
                data[vendorhardwareid][logtime] = {}
                data[vendorhardwareid][logtime]['latitude'] = latitude
                data[vendorhardwareid][logtime]['longitude'] = longitude
                data[vendorhardwareid][logtime]['speed'] = speed
            i += 1
            if i == 30000:
                dataJs = json.dumps(data)
                with open('../csv/bpfFiltedData.txt', 'a') as f:
                    f.write(dataJs)
                data = {}
            if i == 300000:
                break



    with open('../csv/bpfFiltedData.txt', 'r') as f:
        js = f.read()
        dic = json.loads(js)
        print(dic['MS146'])

a, b, c, d = getSchoolTime()
data = bpsFilter(a, b, c, d, 1)