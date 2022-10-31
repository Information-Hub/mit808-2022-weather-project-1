import streamlit as st
import hydralit_components as hc
from multiapp import MultiApp
from pages import upload, visualisation, prediction, home
import time

st.set_page_config(page_title='FABI App', page_icon=':evergreen_tree:', layout='wide',initial_sidebar_state='collapsed')

# specify the primary menu definition
menu_data = [
    {'id': 'home','icon': "home", 'label':"Home"},
    {'id': 'prediction','icon':"bug",'label':"Prediction"},
    {'id': 'visualisation','icon': "graph", 'label':"Visualisation"},
    {'id': 'upload','icon': "graph", 'label':"Upload"}]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=False,
    sticky_nav=True, 
    sticky_mode='pinned')


app = MultiApp()



#pages
if menu_id == 'home':
    app.add_app("Home", home.app)

if menu_id == 'prediction':
    app.add_app("Prediction", prediction.app)

if menu_id == 'visualisation':
    app.add_app("Visualisaton", visualisation.app)

if menu_id == 'upload':
    app.add_app("Upload", upload.app)
# The main app
app.run()







