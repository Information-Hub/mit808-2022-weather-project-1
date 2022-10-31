from matplotlib import animation
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from pages.functions import *
from PIL import Image
import json
import plotly.express as px


def app():

    st.subheader(
        "Project 13: Weather-based Disease Management in South African Forests :evergreen_tree: :ant:"
    )
    st.markdown("---")
    leftcol, rightcol = st.columns(2)
    with leftcol:

        st.header(":loudspeaker: Project Info: ")
        st.markdown(
            """
        For this project we partnered with the Forestry and Agricultural Biotechnology Institute (FABI) \nto analyse temporal weather patterns across South Africa and determine the characteristics that lead to pest infestations of the Leptocybe invasa and Sirex notilio pests.
        
        """
        )

        st.markdown(
            """
        We were provided with **three** datasets namely:

        1. Temperature and rainfall records of roughly 6000 forestry plantations across South Africa

        2. Leptocybe invasa (Leptocybe) pest inspection samples

        3. Sirex noctilio (Sirex) pest inspection samples
        
        """
        )

    with rightcol:
        with open("src/resources/72436-green-leafs-loader.json") as json_file:
            data = json.load(json_file)
            st_lottie(data, height=300, width=600)

    leftcol2, space, rightcol2 = st.columns((1, 0.1, 1))
    with leftcol2:

        st.header(" Leptocybe :ant:")
        st.markdown(
            """
        - ***Leptocybe invasa*** is a small black wasp around 1mm in length. These wasps create abnormal growths  known as ***galls*** on the leaves, petioles and stems of young Blue Gum trees. Heavily infected trees may experience stunted growth or even death."""
        )

        sirex_image = Image.open("reports/figures/leptocybe_image.jpeg")
        st.image(
            sirex_image, caption="Leptocybe invasa - image supplied by fabinet.up.ac.za"
        )

    with rightcol2:
        st.header(" Sirex :honeybee:")

        st.markdown(
            """
        - ***Sirex noctilio*** is a fairly large wasp (up to 4cm long) which bores into the trunk of Pine trees to lay eggs. The eggs are deposited with a mucoid substance which is toxic to trees, this substance ultimately leads to a decline in the trees health"""
        )

        sirex_image = Image.open("reports/figures/sirex_image.jpeg")
        st.image(
            sirex_image, caption="Sirex noctilio - image supplied by fabinet.up.ac.za"
        )

    st.markdown("""---""")
    st.header("Historical pest presence")
    st.markdown(
        "Toggle the inspection year to identify areas more prone to Leptocybe and Sirex, based on previous inspections. This data, together with historical weather data, was used to build the models on the *Prediction* page."
    )
    leftcol3a, leftcol3b, space, rightcol3a, rightcol3b = st.columns(
        (0.6, 0.4, 0.1, 0.6, 0.4)
    )

    with leftcol3a:
        leptoRange = ["All", 2016, 2017, 2018, 2019, 2020, 2021]
        leptoRangeSelection = st.selectbox(
            "Select year of Leptocybe inspection:",
            leptoRange,
        )

    with rightcol3a:
        sirexRange = ["All", 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
        sirexRangeSelection = st.selectbox(
            "Select year of Sirex inspection:",
            sirexRange,
        )

    leftcol3c, space, rightcol3c = st.columns((1, 0.1, 1))
    leptoData = pd.read_csv("data/processed/Leptocybe_R02.csv")
    sirexData = pd.read_csv("data/processed/Sirex_R02.csv")

    with leftcol3c:
        if leptoRangeSelection == "All":
            leptoDataYear = leptoData
        else:
            leptoDataYear = leptoData[leptoData["Year"] == leptoRangeSelection]

        fig = px.scatter_mapbox(
            leptoDataYear,
            lat="Lat",
            lon="Lon",
            color="Lepto_Y_N",
            title="Leptocybe inspections for " + str(leptoRangeSelection),
            center={"lat": -29.46, "lon": 25.32},
            hover_name="Lepto_Y_N",
            opacity=0.5,
            width=600,
            hover_data={
                "Year": True,
                "Lepto_Y_N": False,
                "Lat": False,
                "Lon": False,
            },
            color_discrete_map={"Leptocybe": "limegreen", "No Leptocybe": "Black"},
            labels={"Lepto_Y_N": "Status"},
            # width=600,
            zoom=4,
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(
            title_x=0,
            title_y=0.9,
            margin={"l": 0, "r": 0, "b": 20, "t": 80},
        )
        st.plotly_chart(fig)

    with rightcol3c:
        if sirexRangeSelection == "All":
            sirexDataYear = sirexData
        else:
            sirexDataYear = sirexData[sirexData["Year"] == sirexRangeSelection]

        fig = px.scatter_mapbox(
            sirexDataYear,
            lat="Lat",
            lon="Lon",
            color="Sirex_Presence",
            title="Sirex inspections for " + str(sirexRangeSelection),
            center={"lat": -29.46, "lon": 25.32},
            hover_name="Sirex_Presence",
            opacity=0.5,
            width=600,
            hover_data={
                "Year": True,
                "Sirex_Presence": False,
                "Lat": False,
                "Lon": False,
            },
            color_discrete_map={"Sirex": "red", "No Sirex": "Black"},
            labels={"Sirex_Presence": "Status"},
            # width=600,
            zoom=4,
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(
            title_x=0,
            title_y=0.9,
            margin={"l": 0, "r": 0, "b": 20, "t": 80},
        )
        st.plotly_chart(fig)

    st.markdown("""---""")

    leftcol4, rightcol4 = st.columns(2)
    with leftcol4:

        st.header(":mag: Want to see the previous projects?")

        with open("reports/MIT808 EDA.pdf", "rb") as file:
            btn = st.download_button(
                label="Download Exploratory Data Analysis",
                data=file,
                file_name="EDA.pdf",
                mime="application/pdf",
            )

        with open("reports/MIT808 Modelling.pdf", "rb") as file:
            btn = st.download_button(
                label="Download Modelling Report",
                data=file,
                file_name="Modelling.pdf",
                mime="application/pdf",
            )

        with open("reports/MIT808 Visualisation.pdf", "rb") as file:
            btn = st.download_button(
                label="Download Visualisation Report",
                data=file,
                file_name="Visualisation.pdf",
                mime="application/pdf",
            )

        st.markdown(
            """
        [FABI website](https://www.fabinet.up.ac.za/)

        [GitHub Repo](https://github.com/up-mitc-ds/mit808-2022-project-significant-outliers-1)
        """
        )

    with rightcol4:
        with open("src/resources/82340-dashboard-bi.json") as json_file:
            data = json.load(json_file)
            st_lottie(data, height=250, width=625)
