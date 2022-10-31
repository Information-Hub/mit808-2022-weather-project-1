import streamlit as st
import datetime


def app():
    st.markdown("---")
    st.header(" Manual Data Upload")
    st.write(":information_source: Please enter your records in the appropriate form")

    left, space1, middle, space2, right = st.columns((1, 0.2, 1, 0.2, 1))

    with left:
        st.header("Leptocybe Inspection")
        st.date_input("Date of Inspection", datetime.date(2019, 7, 6), key="ld")
        st.number_input(
            "Longitude",
            min_value=20.0,
            max_value=30.0,
            value=25.0,
            step=0.01,
            key="llo",
        )
        st.number_input(
            "Latitude",
            min_value=-30.0,
            max_value=-20.0,
            value=-23.0,
            step=0.01,
            key="lla",
        )
        st.selectbox("Pest Status", ("positive", "negative"), key="ls")
        Luploadbutton = st.button("Upload Leptocybe inspection")
        if Luploadbutton:
            st.markdown("Leptocybe record uploaded")

    with middle:
        st.header("Sirex Inspection")
        st.date_input("Date of Inspection", datetime.date(2019, 7, 6), key="sd")
        st.number_input(
            "Longitude",
            min_value=20.0,
            max_value=30.0,
            value=25.0,
            step=0.01,
            key="slo",
        )
        st.number_input(
            "Latitude",
            min_value=-30.0,
            max_value=-20.0,
            value=-23.0,
            step=0.01,
            key="sla",
        )
        st.selectbox("Pest Status", ("positive", "negative"), key="ss")
        Suploadbutton = st.button("Upload Sirex inspection")
        if Suploadbutton:
            st.markdown("Sirex record uploaded")

    with right:
        st.header("Weather")
        st.date_input("Date of Inspection", datetime.date(2019, 7, 6), key="wd")
        st.text_input("Site Number")
        st.number_input(
            "Maximum Temperature", min_value=-10, max_value=50, value=25, step=1
        )
        st.number_input(
            "Minimum Temperature", min_value=-20, max_value=30, value=15, step=1
        )
        st.number_input("Rainfall", min_value=0, max_value=1000, value=50, step=1)

        Wuploadbutton = st.button("Upload Weather")
        if Wuploadbutton:
            st.markdown("Weather record uploaded")

    st.markdown("---")
