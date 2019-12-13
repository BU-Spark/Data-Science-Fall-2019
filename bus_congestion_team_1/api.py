"""
@author: Zachary Hyman
"""
import requests
import pandas as pd
import os
import json
import math
import time

APIKEY = ''

class roadLabel:
    '''RoadLabel object used for classification in callAPI'''
    def __init__(self, lat, lon, roadname, speedlimit):
        self.lat = lat
        self.lon = lon
        self.roadname = roadname
        self.speedlimit = speedlimit

def create_dataframe(directory_path, filename):
    '''Creates and returns a dataframe with given filename and files directory path'''
    data = pd.read_csv(directory_path + '/' + filename)
    return data

def callAPI(points):
    '''Calls external Bing API with given batch of points passed to it, returns a list of label objects'''

    url = "https://dev.virtualearth.net/REST/v1/Routes/SnapToRoad"
    querystring = {
        "points": points,
        "IncludeSpeedLimit": "true",
        "speedUnit": "MPH",
        "travelMode": "driving",
        "interpolate": "false",
        #KEY FOR API ASSIGNED AT TOP OF FILE
        "key": APIKEY
    }
    #Send request to API
    response = requests.request("GET", url, params=querystring)
    #Return error in all cases except success
    if response.status_code != 200:
        return ("ERROR")



    jsonData = json.loads(response.text)

    roadPoints = []

    #IF errors field present API encountered internal error
    if 'errors' in jsonData:
        if len(jsonData['errors']) > 0:
            return ("ERROR")
    #Log size of list of points returned
    label_list = jsonData["resourceSets"][0]["resources"][0]['snappedPoints']
    print("Return size of " + str(len(label_list)) + " points")
    #Turn all complete labels into label objects to and add to array to be returned
    for item in label_list:
        if item['coordinate']['latitude'] == '' or item['coordinate']['longitude'] == '' or item['name'] == '' or item['speedLimit'] == '':
            continue
        roadPoint = roadLabel(
            item['coordinate']['latitude'],
            item['coordinate']['longitude'],
            item['name'],
            item['speedLimit']
        )
        roadPoints.append(roadPoint)
    return roadPoints


def calculateDistance(x1, y1, x2, y2):
    '''Calculates and returns the distance between two sets of coordinates'''
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def processBus(df, busID):
    '''Function to call API and does error checking on API return'''

    #IF a given bus contains very few points this will throw an error in the API
    #and if it contains so little data it most likely never left the bus lot
    if df.shape[0] < 15:
        print("Bus " + busID + " encountered an API/GPS Error")
        df_empty = pd.DataFrame({'A': []})
        #Return empty dataframe and avoid API call that would lead to error
        return df_empty


    #Collection of points, used to accumulate up to 50 points to be sent to the API in one call
    batch = []
    #Collection of road label objects to be used later in labeling
    All_Road_labels = []

    #Loop through all entries for a given bus
    for ind in df.index:
        point = str(df['latitude'][ind]) + ',' + str(df['longitude'][ind])
        #IF batch at max size or there are no points left in bus route, call API
        if len(batch) % 50 == 0 and len(batch) != 0 or ind == df.shape[0]-1:  # 99
            batch.append(point)
            print("API CALLED: ", end = ' ')
            #Call API with given batch of points
            #API can handle max of approximately 50 points at once
            batch_road_Labels = callAPI("".join(batch))

            #IF error then return empty dataframe
            if batch_road_Labels == "ERROR":
                print("Bus " + busID + " encountered an API/GPS Error")
                df_empty = pd.DataFrame({'A': []})
                return df_empty
            else:
                #Else add labels to collection of labels
                All_Road_labels.extend(batch_road_Labels)
            batch = []
        else:
            batch.append(point + ';')
            continue

    #Arrays to hold road names and speedlabels to later be columns appended to dataframe
    roadNames = []
    speedLabels = []

    #If no labels encountered return error df
    if len(All_Road_labels) < 1:
        print("Bus " + busID + " encountered an API/GPS Error")
        df_empty = pd.DataFrame({'A': []})
        return df_empty


    #For entries in dataframe for given bus
    for ind in df.index:
        minDist = 10000000000000
        nearestPoint = None
        #Loop through all labels and identify closest label to self
        for roadLabelObj in All_Road_labels:
            dist = calculateDistance(float(df['latitude'][ind]),
                                     float(df['longitude'][ind]),
                                     roadLabelObj.lat,
                                     roadLabelObj.lon)
            if dist < minDist:
                minDist = dist
                nearestPoint = roadLabelObj
        if nearestPoint == None:
            return
        #Add values of closest label to arrays with index matching own to be paired later
        roadNames.append(nearestPoint.roadname)
        speedLabels.append(nearestPoint.speedlimit)

    #Append arrays of labels as columns to dataframes and return labeled dataframe
    df["road_name"] = roadNames
    df["speedlimit"] = speedLabels
    return df

def implement(directory_path,date):
    '''Creates a series of dataframes with labeled road names and street limits
    which are saved under a given date named directory in a new directory called
    Street_labeled_data. Takes a selected date for bus selection as input'''

    #Loops through all buses found in our previous data directory
    for file in os.listdir(directory_path):
        filename = os.fsdecode(file)
        # print(filename)
        #Only reads .csv files
        if filename.endswith(".csv"):
            #Select bus files containing the selected date in name
            if date in filename:
                # print(filename)
                #Extract given busID from file name
                busID = filename[:-28]
                #Create dataframe with given bus
                df = create_dataframe(directory_path, filename)

                #TESTING BLOCK: Uncomment and comment chunk below to run. Used to isolate specific bus with an ID matching
                # if busID == "HS421":
                #     print(df.shape)
                #     print(df)
                #     print("Processing " + busID)
                #     start_time = time.time()
                #     labeled_df = processBus(df, busID)
                #     print("--- Bus %s Complete in %s seconds ---" % (busID,(time.time() - start_time)))
                # else:
                #     continue


                print("Processing " + busID)
                start_time = time.time()
                #Send bus df to be processed and labeled
                labeled_df = processBus(df, busID)
                print("--- Bus %s Complete in %s seconds ---" % (busID,(time.time() - start_time)))

                #Empty df returned in case of error for given bus, logged in previous function
                if labeled_df.empty:
                    continue
                else:
                    #Create and fill directory with new .csv containing labeled data
                    outname = busID + '.csv'
                    outdir = './Street_labeled_data/' + date
                    if not os.path.exists(outdir):
                        os.mkdir(outdir)

                    fullname = os.path.join(outdir, outname)

                    labeled_df.to_csv(fullname,index=False)

##################################################################################################################
start_time = time.time()
implement("/Users/Zachary/Desktop/CS506/Bus_Project/Cleaned_data/cleanedData", date = "2018-04-02")
print("--- Day Complete in %s seconds ---" % (time.time() - start_time))
