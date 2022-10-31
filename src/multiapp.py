"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st
import hydralit_components as hc

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })


    def run(self):
        with st.sidebar:
            app = st.selectbox(
                'Page',
                self.apps,
                format_func=lambda app: app['title'])
            
            n = st.subheader('Authors')
            n2 = st.write('Gené Fourie: `u20797274@tuks.co.za`')
            n3 = st.write('Connor McDonald: `u16040725@tuks.co.za`')
            

        app['function']()