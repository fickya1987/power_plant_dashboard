import folium
import streamlit as st
from streamlit_folium import st_folium

# Page configs
st.set_page_config(
    page_title="Global Power Plants",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class App:

    def __init__(self) -> None:    
        
        # SIDE BAR
        "Imput Stock Symbol"
        self.stock = st.sidebar.text_input('Enter Stock Symbol').upper()
        
        # MAIN
        "map"
        self.map = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
        folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell").add_to(self.map)

        # call to render Folium map in Streamlit
        st_data = st_folium(self.map)


def main():
    App()

if __name__ == "__main__":
    main()