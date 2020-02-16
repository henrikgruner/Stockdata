import requests
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib import rcParams
import constants


def fetchMarketData():

    url = constants.URLGETSUMMARY

    querystring = {"region": "NO", "lang": "en"}
    headers = {
        'x-rapidapi-host': constants.APIHOST,
        'x-rapidapi-key': constants.APIKEY
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    if(response.status_code == 200):
        return response.json()
    else:
        print("helvete")
        return None


def getMarkedSummary(inputdata):

    closingPrice = []

    for i in range(len(inputdata['marketSummaryResponse']['result'])):
        closingPrice.append(
            inputdata['marketSummaryResponse']['result'][i]['regularMarketPrice']['fmt'])
    return closingPrice


def getTime(inputdata):
    time = []
    calendertime = []
    for i in range(len(inputdata['marketSummaryResponse']['result'])):
        time.append(inputdata['marketSummaryResponse']
                    ['result'][i]['regularMarketTime']['raw'])
    for ts in time:
        dt = datetime.fromtimestamp(ts)
        calendertime.append(dt.strftime("%H:%M - %d/%m/%Y"))
    return calendertime


def getIndexName(inputdata):
    indexName = []
    for i in range(len(inputdata['marketSummaryResponse']['result'])):
        try:
            indexName.append(
                inputdata['marketSummaryResponse']['result'][i]['shortName'])
        except Exception:
            indexName.append(
                inputdata['marketSummaryResponse']['result'][i]['symbol'])

    return indexName


def getSummary(summary, indexes, time):
    for i in range(0, len(summary)):
        print(indexes[i], ':', summary[i], 'Date: ', time[i], '\n')


marketdata = fetchMarketData()
summary = getMarkedSummary(marketdata)
indexes = getIndexName(marketdata)
time = getTime(marketdata)
getSummary(summary, indexes, time)
# timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
# timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"
