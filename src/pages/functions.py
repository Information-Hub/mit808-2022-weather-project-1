import requests
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from pyproj import Transformer
import requests
import pickle


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def read_from_drive(url):
    url = "https://drive.google.com/uc?id=" + url.split("/")[-2]
    df = pd.read_csv(url)
    return df


def getStations(pestLocation, stations, tmonth, value, weatherStationsAll):
    pestLoc = np.array([[pestLocation[0], pestLocation[1]]])
    pestStations = []
    stationValues = []
    distanceValues = []

    stationsInMonth = stations[stations["month"] == tmonth].set_index("Id")
    stationsInMonth = stationsInMonth.join(weatherStationsAll)

    for tyear in range(1950, 2020):
        try:
            activeStations = stationsInMonth[
                stationsInMonth["year"] == tyear
            ].reset_index()
            activeStationLoc = np.array(activeStations[["x_m", "y_m"]])
            distance = distance_matrix(pestLoc, activeStationLoc, p=2)
            closestStationIndex = np.where(distance[0] == np.amin(distance[0]))[0][0]

            pestStations.append(activeStations["Id"].iloc[closestStationIndex])
            stationValues.append(activeStations[value].iloc[closestStationIndex])
            distanceValues.append(round(distance[0][closestStationIndex] / 1000, 3))
        except:
            pestStations.append(-99)
            stationValues.append(-99.9)
            distanceValues.append(-99.9)
    return pestStations, stationValues, distanceValues


def feature_engineering(month, rainInput, maxTempInput, minTempInput, gpsLat, gpsLon):
    # Transform gps coords
    TRAN_4326_TO_3857 = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    location = TRAN_4326_TO_3857.transform(gpsLon, gpsLat)

    # Fetch active weather stations
    rainPerMonth = pd.read_csv("data/processed/rainfallAtActiveStations.csv")
    maxTempPerMonth = pd.read_csv("data/processed/temperature_maxAtActiveStations.csv")
    minTempPerMonth = pd.read_csv("data/processed/temperature_minAtActiveStations.csv")

    # Get stations
    weatherStationsAll = pd.read_csv(
        "data/processed/WeatherStationsClean_R04.csv"
    ).set_index("Id")

    rainStations, rainValues, rainDist = getStations(
        location, rainPerMonth, month, "rainfall", weatherStationsAll
    )
    tempMaxStations, tempMaxValues, maxDist = getStations(
        location, maxTempPerMonth, month, "temperature_max", weatherStationsAll
    )
    tempMinStations, tempMinValues, minDist = getStations(
        location, minTempPerMonth, month, "temperature_min", weatherStationsAll
    )

    # Prepare data for station distance vs time graph
    stationsComb = list(
        zip(
            range(1950, 2020),
            [str(x) for x in rainStations],
            [str(x) for x in tempMaxStations],
            [str(x) for x in tempMinStations],
            rainDist,
            maxDist,
            minDist,
        )
    )
    stationsComb = pd.DataFrame(
        stationsComb,
        columns=[
            "year",
            "rainStations",
            "tempMaxStations",
            "tempMinStations",
            "rainDist",
            "tempMaxDist",
            "tempMinDist",
        ],
    )
    stationsComb = stationsComb.replace("-99", None)
    stationsComb = stationsComb.replace(-99.9, None)

    # Prepare data for station map plot
    stationLoc = []
    stationLocYears = range(1950, 2020)
    for i in range(0, len(stationLocYears)):
        stationLoc.append([rainStations[i], stationLocYears[i], rainDist[i]])
        stationLoc.append([tempMaxStations[i], stationLocYears[i], maxDist[i]])
        stationLoc.append([tempMinStations[i], stationLocYears[i], minDist[i]])

    stationLoc = pd.DataFrame(
        stationLoc,
        columns=[
            "StationId",
            "year",
            "Distance",
        ],
    )
    stationLoc = stationLoc.replace(-99, None)
    stationLoc = stationLoc.replace(-99.9, None)
    stationLoc = stationLoc.set_index("StationId").join(weatherStationsAll)
    stationLoc = stationLoc.reset_index().drop_duplicates()
    stationLoc = stationLoc.rename(columns={"index": "StationId"})

    groups = stationLoc.groupby(["StationId", "x_m", "y_m"])
    minStations = groups.min().index.tolist()
    minYears = groups.min()["year"].values.tolist()
    minDist = groups.min()["Distance"].values.tolist()

    stationLoc = list(
        zip(
            [i[0] for i in minStations],
            [i[1] for i in minStations],
            [i[2] for i in minStations],
            minYears,
            minDist,
        )
    )
    stationLoc = pd.DataFrame(
        stationLoc, columns=["StationId", "x_m", "y_m", "year", "Distance"]
    )
    stationLoc = stationLoc.drop_duplicates(subset=["year", "StationId"])
    TRAN_4326_TO_3857Rev = Transformer.from_crs(
        "EPSG:3857", "EPSG:4326", always_xy=True
    )
    stationLoc["lon"] = TRAN_4326_TO_3857Rev.transform(
        stationLoc["x_m"], stationLoc["y_m"]
    )[0]
    stationLoc["lat"] = TRAN_4326_TO_3857Rev.transform(
        stationLoc["x_m"], stationLoc["y_m"]
    )[1]

    stationLoc = stationLoc.drop(columns=["x_m", "y_m"])

    # Get data for rainfall and temp graphs
    valuesComb = list(
        zip(
            range(1950, 2020),
            rainValues,
            tempMaxValues,
            tempMinValues,
        )
    )
    valuesComb = pd.DataFrame(
        valuesComb,
        columns=[
            "year",
            "rainValues",
            "tempMaxValues",
            "tempMinValues",
        ],
    )
    valuesComb = valuesComb.replace(-99.9, None)

    # Get parameters
    averages = valuesComb.mean()
    rainfalldiff = rainInput - averages["rainValues"]
    rainfall = rainInput
    rainfallavg = averages["rainValues"]
    temperature_maxdiff = maxTempInput - averages["tempMaxValues"]
    temperature_max = maxTempInput
    temperature_maxavg = averages["tempMaxValues"]
    temperature_mindiff = minTempInput - averages["tempMinValues"]
    temperature_min = minTempInput
    temperature_minavg = averages["tempMinValues"]
    temperature_diffdiff = temperature_maxdiff - temperature_mindiff
    temperature_diff = temperature_max - temperature_min
    temperature_diffavg = temperature_maxavg - temperature_minavg

    parameters = [
        rainfalldiff,
        rainfall,
        rainfallavg,
        temperature_maxdiff,
        temperature_max,
        temperature_maxavg,
        temperature_mindiff,
        temperature_min,
        temperature_minavg,
        temperature_diffdiff,
        temperature_diff,
        temperature_diffavg,
    ]

    return parameters, stationsComb, valuesComb, stationLoc


def getMap(monthValue, timeframeValue, rainInput, maxTempInput, minTempInput):
    monthAvgs = pd.read_csv("data/processed/featuresDf_all.csv")
    monthAvgsForMonth = monthAvgs[monthAvgs["month"] == monthValue]

    timeframeList = []
    for i in range(0, len(monthAvgsForMonth)):
        timeframeList.append(timeframeValue)

    # Get parameters
    parameters = pd.DataFrame()
    parameters["id"] = monthAvgsForMonth["id"]
    parameters["timeframe"] = timeframeList
    parameters["rainfalldiff"] = rainInput - monthAvgsForMonth["rainfallavg"]
    parameters["rainfall"] = rainInput
    parameters["rainfallavg"] = monthAvgsForMonth["rainfallavg"]
    parameters["temperature_maxdiff"] = (
        maxTempInput - monthAvgsForMonth["temperature_maxavg"]
    )
    parameters["temperature_max"] = maxTempInput
    parameters["temperature_maxavg"] = monthAvgsForMonth["temperature_maxavg"]
    parameters["temperature_mindiff"] = (
        minTempInput - monthAvgsForMonth["temperature_minavg"]
    )
    parameters["temperature_min"] = minTempInput
    parameters["temperature_minavg"] = monthAvgsForMonth["temperature_minavg"]
    parameters["temperature_diffdiff"] = (
        maxTempInput - minTempInput
    ) - monthAvgsForMonth["temperature_diffavg"]
    parameters["temperature_diff"] = maxTempInput - minTempInput
    parameters["temperature_diffavg"] = monthAvgsForMonth["temperature_diffavg"]

    return parameters


def getModelResults(parameters, model):
    exportDf = pd.DataFrame()
    exportDf["id"] = parameters["id"]

    # lepto
    Lxg = pickle.load(open("models/lepto_xgb2.pickle", "rb"))
    Lsvm = pickle.load(open("models/lepto_svm2.pickle", "rb"))
    Lscaler = pickle.load(open("models/lepto_scaler.pickle", "rb"))

    # df = parameters
    df = parameters.drop(columns=["id"])
    dfList = df.values.tolist()
    # Standardizing variables
    Lsc = Lscaler
    leptoSVM_prob = []
    leptoXG_prob = []

    if model == "Support Vector Machine":
        for i in range(0, len(dfList)):
            # Convert to 1d list
            XPre = []
            for j in range(0, len(dfList[i])):
                XPre.append(dfList[i][j])

            # Transform this list
            X = Lsc.transform([XPre])

            # Perform predictions
            lsvmp = Lsvm.predict_proba(X)
            lsvm_pred = Lsvm.predict(X)

            if lsvm_pred[0] == 1:
                prob = max(lsvmp[0])
            else:
                prob = 1 - max(lsvmp[0])
            leptoSVM_prob.append(prob)

        exportDf["lepto_prob"] = leptoSVM_prob

    else:
        for i in range(0, len(dfList)):
            XPre = []
            for j in range(0, len(dfList[i])):
                XPre.append(dfList[i][j])
            X = Lsc.transform([XPre])

            lxgp = Lxg.predict_proba(X)
            lxg_pred = Lxg.predict(X)

            if lxg_pred[0] == 1:
                prob = max(lxgp[0])
            else:
                prob = 1 - max(lxgp[0])
            leptoXG_prob.append(prob)

        exportDf["lepto_prob"] = leptoXG_prob

    # Sirex
    Sxg = pickle.load(open("models/sirex_xgb2.pickle", "rb"))
    Ssvm = pickle.load(open("models/sirex_svm2.pickle", "rb"))
    Sscaler = pickle.load(open("models/sirex_scaler.pickle", "rb"))

    # df = parameters
    df2 = parameters.drop(columns=["id"])
    df2List = df2.values.tolist()
    # Standardizing variables
    Ssc = Sscaler
    sirexSVM_prob = []
    sirexXG_prob = []

    if model == "Support Vector Machine":
        for i in range(0, len(df2List)):
            # Convert to 1d list
            XPre = []
            for j in range(0, len(df2List[i])):
                XPre.append(df2List[i][j])

            # Transform this list
            X = Ssc.transform([XPre])

            # Perform predictions
            ssvmp = Ssvm.predict_proba(X)
            ssvm_pred = Ssvm.predict(X)

            if ssvm_pred[0] == 1:
                prob = max(ssvmp[0])
            else:
                prob = 1 - max(ssvmp[0])
            sirexSVM_prob.append(prob)

        exportDf["sirex_prob"] = sirexSVM_prob

    else:
        for i in range(0, len(df2List)):
            XPre = []
            for j in range(0, len(df2List[i])):
                XPre.append(df2List[i][j])
            X = Ssc.transform([XPre])

            sxgp = Sxg.predict_proba(X)
            sxg_pred = Sxg.predict(X)

            if sxg_pred[0] == 1:
                prob = max(sxgp[0])
            else:
                prob = 1 - max(sxgp[0])
            sirexXG_prob.append(prob)

        exportDf["sirex_prob"] = sirexXG_prob

    return exportDf
