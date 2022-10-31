import streamlit as st
from PIL import Image
from datetime import datetime, date
import numpy as np
import pandas as pd
from pages.functions import feature_engineering, getMap, getModelResults
import pickle

Lxg = pickle.load(open("models/lepto_xgb2.pickle", "rb"))
Lsvm = pickle.load(open("models/lepto_svm2.pickle", "rb"))
Lscaler = pickle.load(open("models/lepto_scaler.pickle", "rb"))

Sxg = pickle.load(open("models/sirex_xgb2.pickle", "rb"))
Ssvm = pickle.load(open("models/sirex_svm2.pickle", "rb"))
Sscaler = pickle.load(open("models/sirex_scaler.pickle", "rb"))


def app():
    st.markdown("---")

    # Set defaults of session
    if "model_L" not in st.session_state:
        st.session_state["model_L"] = "Choose your model"
    if "month" not in st.session_state:
        st.session_state["month"] = 1
    if "Years" not in st.session_state:
        st.session_state["Years"] = 1
    if "rain" not in st.session_state:
        st.session_state["rain"] = 0
    if "maxTemp" not in st.session_state:
        st.session_state["maxTemp"] = 20
    if "minTemp" not in st.session_state:
        st.session_state["minTemp"] = 10
    if "lat" not in st.session_state:
        st.session_state["lat"] = -30.00
    if "lon" not in st.session_state:
        st.session_state["lon"] = 30.70
    if "getParameters" not in st.session_state:
        st.session_state["getParameters"] = None
    if "stationData" not in st.session_state:
        st.session_state["stationData"] = pd.DataFrame()
    if "valuesComb" not in st.session_state:
        st.session_state["valuesComb"] = pd.DataFrame()
    if "stationLoc" not in st.session_state:
        st.session_state["stationLoc"] = pd.DataFrame()
    if "mapPredictResults" not in st.session_state:
        st.session_state["mapPredictResults"] = pd.DataFrame()
    if "pred2L" not in st.session_state:
        st.session_state["pred2L"] = None
    if "probaL" not in st.session_state:
        st.session_state["probaL"] = None
    if "pred2S" not in st.session_state:
        st.session_state["pred2S"] = None
    if "probaS" not in st.session_state:
        st.session_state["probaS"] = None
    if "mapParameterInput" not in st.session_state:
        st.session_state["mapParameterInput"] = pd.DataFrame()

    topinput1, topinput2, topinput3 = st.columns((2, 0.5, 0.5))

    input1, space12, input2, space23, input3, space34, input4 = st.columns(
        (1, 0.2, 1, 0.2, 1, 0.2, 1.5)
    )

    with topinput1:
        st.header("Make a prediction")

        model_L = st.selectbox(
            " ",
            ("Choose your model", "XGBoost", "Support Vector Machine"),
            key="lepto_model_select",
            index=["Choose your model", "XGBoost", "Support Vector Machine"].index(
                st.session_state["model_L"]
            ),
        )
        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)

    with input1:
        st.markdown("##### Enter month and period of prediction:")
        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)

        month = st.slider("Month", 1, 12, st.session_state["month"], key="l1")

        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)

        inAdvance = st.slider("Years", 0, 3, st.session_state["Years"], key="l1")

        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)

        st.warning(
            "Prediction will be for "
            + date(1900, month, 1).strftime("%B")
            + " in "
            + str(inAdvance)
            + " year(s) time."
        )

    with input2:
        st.markdown(
            "##### Enter measurements for month of "
            + date(1900, month, 1).strftime("%B")
            + ":"
        )

        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)

        rain = st.number_input(
            "Total rainfall (mm)", value=st.session_state["rain"], min_value=0
        )
        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)

        maxTemp = st.number_input(
            "Average max temperature (C)",
            value=st.session_state["maxTemp"],
            min_value=-20,
        )

        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)
        minTemp = st.number_input(
            "Average min temperature (C)",
            value=st.session_state["minTemp"],
            min_value=-20,
        )

    with input3:
        st.markdown("##### Enter approximate point location:")
        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)
        lat = st.slider(
            "Latitude (South/North)",
            -35.00,
            -23.00,
            st.session_state["lat"],
        )

        st.markdown("""<div><br/></div>""", unsafe_allow_html=True)

        lon = st.slider(
            "Longitude (West/East)",
            19.00,
            33.00,
            st.session_state["lon"],
        )

        st.markdown("---")

        run_l = st.button("Run", key="lepto_run")
        if run_l == True and model_L == "Choose your model":
            st.error("Please select a model")
        elif run_l == True and maxTemp < minTemp:
            st.error("Minimum temperature is greater than maximum temperature")

    with input4:
        mapdf = pd.DataFrame(
            np.random.randn(1, 2) / [50, 50] + [lat, lon],
            columns=["lat", "lon"],
        )
        st.map(mapdf, zoom=5)

    st.markdown("---")
    st.header("Results")

    lower_left, lower_space, lower_right = st.columns((2, 0.8, 2))

    if run_l:

        st.session_state["model_L"] = model_L
        st.session_state["month"] = month
        st.session_state["Years"] = inAdvance
        st.session_state["rain"] = rain
        st.session_state["maxTemp"] = maxTemp
        st.session_state["minTemp"] = minTemp
        st.session_state["lat"] = lat
        st.session_state["lon"] = lon

        with st.spinner("Running model and preparing visualisations..."):

            getParameters = feature_engineering(month, rain, maxTemp, minTemp, lat, lon)
            st.session_state["stationData"] = getParameters[1]
            st.session_state["valuesComb"] = getParameters[2]
            st.session_state["stationLoc"] = getParameters[3]

            timeframe = (4 - inAdvance) * 12 + month

            mapParameterInput = getMap(month, timeframe, rain, maxTemp, minTemp)

            mapPredictResults = getModelResults(mapParameterInput, model_L)
            st.session_state["mapPredictResults"] = mapPredictResults

            getParameters = getParameters[0]
            getParameters.insert(0, timeframe)
            getParameters = [getParameters]
            st.session_state["getParameters"] = getParameters

            ts = datetime.timestamp(datetime.now())
            ts = datetime.fromtimestamp(ts)
            ts = ts.strftime("%d-%m-%Y, %H:%M:%S")
            st.session_state["ts"] = ts

    if st.session_state["getParameters"] == None:
        st.markdown("Click 'Run' to generate results.")

    else:
        if model_L == "XGBoost":
            with lower_left:
                inputs = Lscaler.transform(st.session_state["getParameters"])
                prediction = Lxg.predict(inputs)
                probability = Lxg.predict_proba(inputs)
                data = pd.DataFrame(probability[0:], columns=["Negative", "Positive"])

                if prediction[0] == 1:
                    pred1L = "POSITIVE"
                    pred2L = "positive"
                    probaL = np.round(max(probability[0]) * 100, 1)

                else:
                    pred1L = "NEGATIVE"
                    pred2L = "negative"
                    probaL = np.round(max(probability[0]) * 100, 1)

                st.header("Leptocybe")
                st.markdown("Results generated at " + st.session_state["ts"])
                st.subheader("Prediction:   {} ".format(pred1L))
                st.subheader("Class Probabilities:")
                st.table(data)
                st.subheader("XGBoost ROC-AUC Curve")
                image = Image.open("reports/figures/XGB_AUC_lepto.png")
                st.image(image)
                st.subheader("Model Explanation:")

                st.markdown(
                    """
                - The {} classifier is an ensemble machine learning algorithm based on the gradient boosted trees algorithm.
                - The model predicted a ***{}*** Leptocybe inspection with a ***{}%*** probability
                - The ROC-AUC Curve of the model shows how well the model can predict the correct class
                    - An AUC score of 0.5 indicates the model is no better than taking a random guess
                    - An AUC score closer to 1 indicates the model predicts the correct class more often than not
                """.format(
                        model_L, pred2L, probaL
                    )
                )

            with lower_right:
                inputs = Sscaler.transform(st.session_state["getParameters"])
                prediction = Sxg.predict(inputs)
                probability = Sxg.predict_proba(inputs)
                data = pd.DataFrame(probability[0:], columns=["Negative", "Positive"])

                if prediction[0] == 1:
                    pred1S = "POSITIVE"
                    pred2S = "positive"
                    probaS = np.round(max(probability[0]) * 100, 1)

                else:
                    pred1S = "NEGATIVE"
                    pred2S = "negative"
                    probaS = np.round(max(probability[0]) * 100, 1)

                st.header("Sirex")
                st.markdown("Results generated at " + st.session_state["ts"])
                st.subheader("Prediction:   {} ".format(pred1S))
                st.subheader("Class Probabilities:")
                st.table(data)
                st.subheader("XGBoost ROC-AUC Curve")
                image = Image.open("reports/figures/XGB_AUC_sirex.png")
                st.image(image)
                st.subheader("Model Explanation:")
                st.markdown(
                    """
                - The {} classifier is an ensemble machine learning algorithm based on the gradient boosted trees algorithm.
                - The model predicted a ***{}*** Sirex inspection with a ***{}%*** probability
                - The ROC-AUC Curve of the model shows how well the model can predict the correct class
                    - An AUC score of 0.5 indicates the model is no better than taking a random guess
                    - An AUC score closer to 1 indicates the model predicts the correct class more often than not
                """.format(
                        model_L, pred2S, probaS
                    )
                )

        if model_L == "Support Vector Machine":
            with lower_left:
                inputs = Lscaler.transform(st.session_state["getParameters"])
                prediction = Lsvm.predict(inputs)
                probability = Lsvm.predict_proba(inputs)
                data = pd.DataFrame(probability[0:], columns=["Negative", "Positive"])

                if prediction[0] == 1:
                    pred1L = "POSITIVE"
                    pred2L = "positive"
                    probaL = np.round(max(probability[0]) * 100, 1)

                else:
                    pred1L = "NEGATIVE"
                    pred2L = "negative"
                    probaL = np.round(max(probability[0]) * 100, 1)

                st.header("Leptocybe")
                st.markdown("Results generated at " + st.session_state["ts"])
                st.subheader("Prediction:   {} ".format(pred1L))
                st.subheader("Class Probabilities:")
                st.table(data)
                st.subheader("SVM ROC-AUC Curve")
                image = Image.open("reports/figures/SVM_AUC_lepto.png")
                st.image(image)
                st.subheader("Model Explanation:")
                st.markdown(
                    """
                - The {} classifier is based on the margin maximisation principle and aims to locate the optimal separating hyperplane between classes.
                - The model predicted a ***{}*** Leptocybe inspection with a ***{}%*** probability
                - The ROC-AUC Curve of the model shows how well the model can predict the correct class
                    - An AUC score of 0.5 indicates the model is no better than taking a random guess
                    - An AUC score closer to 1 indicates the model predicts the correct class more often than not
                """.format(
                        model_L, pred2L, probaL
                    )
                )

            with lower_right:
                inputs = Sscaler.transform(st.session_state["getParameters"])
                prediction = Ssvm.predict(inputs)
                probability = Ssvm.predict_proba(inputs)
                data = pd.DataFrame(probability[0:], columns=["Negative", "Positive"])

                if prediction[0] == 1:
                    pred1S = "POSITIVE"
                    pred2S = "positive"
                    probaS = np.round(max(probability[0]) * 100, 1)

                else:
                    pred1S = "NEGATIVE"
                    pred2S = "negative"
                    probaS = np.round(max(probability[0]) * 100, 1)

                st.header("Sirex")
                st.markdown("Results generated at " + st.session_state["ts"])
                st.subheader("Prediction:   {} ".format(pred1S))
                st.subheader("Class Probabilities:")
                st.table(data)
                st.subheader("SVM ROC-AUC Curve")
                image = Image.open("reports/figures/SVM_AUC_sirex.png")
                st.image(image)
                st.subheader("Model Explanation:")
                st.markdown(
                    """
                - The {} classifier is based on the margin maximisation principle and aims to locate the optimal separating hyperplane between classes.
                - The model predicted a ***{}*** Sirex inspection with a ***{}%*** probability
                - The ROC-AUC Curve of the model shows how well the model can predict the correct class
                    - An AUC score of 0.5 indicates the model is no better than taking a random guess
                    - An AUC score closer to 1 indicates the model predicts the correct class more often than not
                """.format(
                        model_L, pred2S, probaS
                    )
                )

        st.session_state["pred2L"] = pred2L
        st.session_state["probaL"] = probaL
        st.session_state["pred2S"] = pred2S
        st.session_state["probaS"] = probaS

    st.markdown("---")
