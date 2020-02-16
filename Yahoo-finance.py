import requests
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib import rcParams
import constants


def fetchStockData(symbol):

    import requests

    url = constants.URLCHARTS

    querystring = {"comparisons": "%5EGDAXI%2C%5EFCHI", "region": "US",
                   "lang": "en", "symbol": symbol, "interval": "1d", "range": "1y"}
    # Get your keys at yahoo finance api (rapidapi.com)
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


def parseTimestamp(inputdata):
    timestamplist = []
    calendertime = []
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])

    for ts in timestamplist:
        dt = datetime.fromtimestamp(ts)
        calendertime.append(dt.strftime("%m/%d/%Y"))

    return calendertime


def parseValues(inputdata):
    valueList = []
    valueList.extend(inputdata["chart"]["result"][0]
                     ["indicators"]["quote"][0]["open"])
    valueList.extend(inputdata["chart"]["result"][0]
                     ["indicators"]["quote"][0]["close"])
    return valueList


def attachEvents(inputdata):
    eventlist = []
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("open")
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")
    return eventlist


symbol_string = ""
inputdata = {}

symbol_string = "AAPL"

retdata = fetchStockData(symbol_string)


if (None != inputdata):
    inputdata["Timestamp"] = parseTimestamp(retdata)
    inputdata["Values"] = parseValues(retdata)
    inputdata["Events"] = attachEvents(retdata)
    df = pd.DataFrame(inputdata)

    sns.set(style="darkgrid")
    rcParams['figure.figsize'] = 13, 5
    rcParams['figure.subplot.bottom'] = 0.2

    ax = sns.lineplot(x="Timestamp", y="Values", hue="Events",
                      data=df, sort=False)

    ax.set_title('Symbol: ' + symbol_string)

    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='xx-small',

    )

    plt.show()
