import folium
import streamlit as st
from streamlit_folium import st_folium
import branca
from database import Database

# Page configs
st.set_page_config(
    page_title="Global Power Plants",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOUR_DICT = {
    "Gas" : "lightgray",
    "Solar" : "orange",
    "Coal" : "black",
    "Hydro" : "darkblue",
    "Wind" : "blue",
    "Oil" : "gray",
    "Waste" : "beige",
    "Biomass" : "darkgreen",
    "Nuclear": "white", 
    "Other" : "purple"
}

class App:

    def __init__(self) -> None:    
        
        # SIDE BAR
        "Imput Stock Symbol"
        self.stock = st.sidebar.text_input('Enter Stock Symbol').upper()
        
        # data
        # instantiating database object
        DB = Database()
        
        # extracting info
        df = DB._germany_data()

        # MAP
        "map"
        self.map = folium.Map([50.0918, 8.5311], 
                        zoom_start=7,
                        control_scale=True)
        
        for i, row in df.iterrows():
            # adding markers
            self._markers(row)


        # call to render Folium map in Streamlit
        st_data = st_folium(self.map, width=3000, height = 1500)
    
    def _markers(self, _row):
        
        # Icon
        icon = folium.Icon(
                color=COLOUR_DICT[_row["primary_fuel"]],
                icon = "location_dot"
                                )
        # html
        html = f"""
        <h4> {_row["name"]}</h3><br>
        <b> {_row["primary_fuel"]}</b><br>
        Capacity (mw) : {_row["capacity_mw"]}<br>
        Owner : {_row["owner"]}<br> 
        """
        
        iframe = branca.element.IFrame(html=html, width=500, height=300)
        popup = folium.Popup(iframe, max_width=500)
        
        # Marker 
        folium.Marker(
            location= [_row["latitude"], _row["longitude"]],
            tooltip= _row["name"],
            popup=popup, 
            icon=icon,
            ).add_to(self.map)


def main():
    App()

if __name__ == "__main__":
    main()