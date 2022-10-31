from turtle import color
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date
import json


def app():
    Proceed = True
    if "valuesComb" in st.session_state:
        valuesCombVis = st.session_state["valuesComb"]
    else:
        st.session_state["valuesComb"] = pd.DataFrame()

    if "stationData" in st.session_state:
        stationDataVis = st.session_state["stationData"]
    else:
        st.session_state["stationData"] = pd.DataFrame()

    if valuesCombVis.empty:
        Proceed = False
        st.markdown("Click 'Run' on the Prediction Tab to generate results.")

    if Proceed:
        st.markdown("---")
        st.header(" Weather :cloud:")

        st.subheader("Measurements")
        st.markdown(
            "Weather measurements are shown per year for ***"
            + date(1900, st.session_state["month"], 1).strftime("%B")
            + "*** at the selected location (Lat: "
            + str(st.session_state["lat"])
            + "  |  Lon: "
            + str(st.session_state["lon"])
            + ")."
        )

        input1, input2 = st.columns(2)
        with input1:
            fig = go.Figure()
            fig.add_scatter(
                x=valuesCombVis["year"],
                y=valuesCombVis["rainValues"],
                mode="lines",
                name="Rainfall Total",
            )

            fig.update_traces(line_color="#25b89a")

            fig.update_layout(
                title="Total rainfall for "
                + date(1900, st.session_state["month"], 1).strftime("%B"),
                title_x=0.5,
                xaxis_title="Year",
                yaxis_title="Rainfall (mm)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FAF9F6"),
            )

            fig.add_scatter(
                x=[1950, 2019],
                y=[st.session_state["rain"], st.session_state["rain"]],
                mode="lines",
                # xaxis="x2",
                # showlegend=False,
                line=dict(dash="dash", color="gold", width=2),
                name="Rainfall Actual",
            )

            fig.update_yaxes(
                showgrid=False,
                mirror=True,
                ticks="outside",
                showline=True,
            )

            fig.update_xaxes(
                showgrid=False,
                mirror=True,
                ticks="outside",
                showline=True,
            )

            st.plotly_chart(fig)

        with input2:
            fig = go.Figure()

            fig.add_scatter(
                x=valuesCombVis["year"],
                y=valuesCombVis["tempMaxValues"],
                mode="lines",
                name="Max Temp Average",
            )
            fig.update_traces(line_color="#25b89a")

            fig.add_scatter(
                x=[1950, 2019],
                y=[st.session_state["maxTemp"], st.session_state["maxTemp"]],
                mode="lines",
                # xaxis="x2",
                # showlegend=False,
                line=dict(dash="dash", color="gold", width=2),
                name="Max Temp Actual",
            )

            fig.add_scatter(
                x=valuesCombVis["year"],
                y=valuesCombVis["tempMinValues"],
                mode="lines",
                name="Min Temp Average",
                marker={"color": "#da4765"},
            )

            fig.add_scatter(
                x=[1950, 2019],
                y=[st.session_state["minTemp"], st.session_state["minTemp"]],
                mode="lines",
                # xaxis="x2",
                # showlegend=False,
                line=dict(dash="dash", color="coral", width=2),
                name="Min Temp Actual",
            )

            fig.update_layout(
                title="Average max and min temps for "
                + date(1900, st.session_state["month"], 1).strftime("%B"),
                title_x=0.5,
                xaxis_title="Year",
                yaxis_title="Temperature (C)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FAF9F6"),
            )

            fig.update_yaxes(
                showgrid=False,
                mirror=True,
                ticks="outside",
                showline=True,
            )

            fig.update_xaxes(
                showgrid=False,
                mirror=True,
                ticks="outside",
                showline=True,
            )

            st.plotly_chart(fig)

        stationLoc = st.session_state["stationLoc"]
        st.subheader("Stations")
        st.markdown(
            "Active stations change from month-to-month, where only stations with valid and complete measurements are used to determine the expected weather conditions at a location."
        )

        uniqueStations = len(stationLoc[["lat", "lon"]].value_counts().index.values)
        totalStations = len(stationLoc["lat"])

        st.markdown(
            "The selected location (at Lat: "
            + str(st.session_state["lat"])
            + "  |  Lon: "
            + str(st.session_state["lon"])
            + ") uses data from a total of ***"
            + str(uniqueStations)
            + "*** unique station locations, with ***"
            + str(totalStations - uniqueStations)
            + "*** station(s) changing names, over the period of consideration."
        )

        input1, space, input2 = st.columns((2, 0.5, 2))

        with input1:

            fig = go.Figure()
            fig.add_scatter(
                x=stationDataVis["year"],
                y=stationDataVis["rainDist"],
                mode="lines",
                name="Rain Station",
                line=dict(color="#25b89a"),
            )

            fig.add_scatter(
                x=stationDataVis["year"],
                y=stationDataVis["tempMaxDist"],
                mode="lines",
                name="Temp Station",
                line=dict(color="#da4765"),
            )

            fig.update_layout(
                title="Distance to nearest active station in "
                + date(1900, st.session_state["month"], 1).strftime("%B")
                + " per year",
                xaxis_title="Year",
                yaxis_title="Distance (km)",
                legend_title="Station type",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FAF9F6"),
            )

            fig.update_yaxes(
                showgrid=False,
                mirror=True,
                ticks="outside",
                showline=True,
            )

            fig.update_xaxes(
                showgrid=False,
                mirror=True,
                ticks="outside",
                showline=True,
            )

            fig.add_trace(
                go.Scatter(
                    x=stationLoc["year"],
                    y=stationLoc["Distance"],
                    mode="markers+text",
                    name="Station ID",
                    text=stationLoc["StationId"],
                    textposition="bottom center",
                    line=dict(color="#FFFFFF"),
                )
            )

            st.plotly_chart(fig)

        with input2:

            stationLoc["colours"] = "black"
            stationLoc["sizes"] = 0.3
            stationLoc["Type"] = "Station"

            stationLoc = stationLoc.append(
                {
                    "StationId": "Inspection",
                    "lat": st.session_state["lat"],
                    "lon": st.session_state["lon"],
                    "colours": "crimson",
                    "sizes": 0.6,
                    "Type": "Inspection",
                    "Distance": 0,
                },
                ignore_index=True,
            )

            fig = px.scatter_mapbox(
                stationLoc,
                lat="lat",
                lon="lon",
                color="Type",
                size="sizes",
                title="All active station locations from 1950",
                center={"lat": st.session_state["lat"], "lon": st.session_state["lon"]},
                hover_name="StationId",
                hover_data={
                    "Distance": True,
                    "Type": False,
                    "sizes": False,
                    "lat": False,
                    "lon": False,
                },
                color_discrete_map={"Inspection": "crimson", "Station": "black"},
                labels={"Distance": "Distance to inspection (km)"},
                width=600,
                zoom=6,
            )
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(
                title_x=0,
                title_y=0.9,
                margin={"l": 0, "r": 0, "b": 20, "t": 80},
            )
            st.plotly_chart(fig)

        st.markdown("---")
        st.header("Pest prediction at selected location")
        st.markdown(
            "Table 1: Input measurements (actuals) provided in the 'Prediction' page vs Average monthly measurements for location (Lat: "
            + str(st.session_state["lat"])
            + "  |  Lon: "
            + str(st.session_state["lon"])
            + ")"
        )
        valAvg = valuesCombVis.mean()

        sessionData = pd.DataFrame()
        sessionData["Description"] = [
            "Input measurements",
            "Average for location",
            "Difference",
        ]
        sessionData["Total Rainfall (mm)"] = [
            st.session_state["rain"],
            valAvg["rainValues"],
            (st.session_state["rain"] - valAvg["rainValues"]),
        ]
        sessionData["Average Maximum Temperature (C)"] = [
            st.session_state["maxTemp"],
            valAvg["tempMaxValues"],
            (st.session_state["maxTemp"] - valAvg["tempMaxValues"]),
        ]
        sessionData["Average Minimum Temperature (C)"] = [
            st.session_state["minTemp"],
            valAvg["tempMinValues"],
            (st.session_state["minTemp"] - valAvg["tempMinValues"]),
        ]

        sessionData = sessionData.set_index("Description")
        st.table(sessionData)

        st.markdown(
            "Results calculated for ***"
            + date(1900, st.session_state["month"], 1).strftime("%B")
            + "*** in ***"
            + str(st.session_state["Years"])
            + "*** year(s) time, using ***"
            + st.session_state["model_L"]
            + "*** and parameters from **Table 1**:"
        )

        lepto1, space, sirex1 = st.columns((2, 0.5, 2))
        with lepto1:
            st.subheader("Leptocybe :ant:")
            if st.session_state["pred2L"] == "positive":
                st.markdown(
                    ":heavy_plus_sign: POSITIVE with "
                    + str(st.session_state["probaL"])
                    + " probability"
                )
            else:
                st.markdown(
                    ":heavy_minus_sign: NEGATIVE with ***"
                    + str(st.session_state["probaL"])
                    + "*** probability"
                )
        with sirex1:
            st.subheader("Sirex :bee:")
            if st.session_state["pred2S"] == "positive":
                st.markdown(
                    ":heavy_plus_sign: POSITIVE with "
                    + str(st.session_state["probaS"])
                    + " probability"
                )
            else:
                st.markdown(
                    ":heavy_minus_sign: NEGATIVE with ***"
                    + str(st.session_state["probaS"])
                    + "*** probability"
                )

        st.markdown("---")
        st.header("Pest prediction across South Africa")
        st.markdown(
            "If the input measurements provided in the 'Prediction' page (and **Table 1**) are experienced across the country, the following prediction probabilities are seen."
        )

        lepto, space, sirex = st.columns((2, 0.5, 2))

        mapPredictResults = st.session_state["mapPredictResults"]

        f = open("data/processed/grid_voronois.geojson")
        pestMap = json.load(f)

        for i in range(0, len(pestMap["features"])):
            pestMap["features"][i]["id"] = pestMap["features"][i]["properties"]["id"]

        df = mapPredictResults

        with lepto:
            st.subheader("Leptocybe :ant:")

            fig = px.choropleth_mapbox(
                df,
                geojson=pestMap,
                color="lepto_prob",
                locations="id",
                center={"lat": -29.46, "lon": 25.32},
                mapbox_style="open-street-map",
                zoom=4.2,
                opacity=0.4,
                width=600,
                title="Positive probability of positive Leptocybe inspection for given measurements",
                labels={"lepto_prob": "Probability"},
                range_color=[0, 1],
            )
            fig.update_traces(marker_line_width=0)

            fig.add_scattermapbox(
                lat=[st.session_state["lat"]],
                lon=[st.session_state["lon"]],
                mode="markers",
                name="Inspection",
                marker={"size": 10, "color": "crimson"},
            )

            fig.update_layout(
                title_x=0,
                title_y=0.9,
                margin={"l": 0, "r": 0, "b": 20, "t": 80},
            )

            st.plotly_chart(fig)

        with sirex:
            st.subheader("Sirex :honeybee:")

            fig = px.choropleth_mapbox(
                df,
                geojson=pestMap,
                color="sirex_prob",
                locations="id",
                center={"lat": -29.46, "lon": 25.32},
                mapbox_style="open-street-map",
                zoom=4.2,
                opacity=0.4,
                width=600,
                title="Probability of positive Sirex inspection for given measurements",
                labels={"sirex_prob": "Probability"},
                range_color=[0, 1],
            )

            fig.update_traces(marker_line_width=0)

            fig.add_scattermapbox(
                lat=[st.session_state["lat"]],
                lon=[st.session_state["lon"]],
                mode="markers",
                name="Inspection",
                marker={"size": 10, "color": "crimson"},
            )

            fig.update_layout(
                title_x=0,
                title_y=0.9,
                margin={"l": 0, "r": 0, "b": 20, "t": 80},
            )

            st.plotly_chart(fig)
        st.markdown("---")
