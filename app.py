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

st.markdown(
    """
    <style>
    {% include 'styles.css' %}
    </style>
    """,
    unsafe_allow_html=True
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
    "Other" : "purple",
    "Wave and Tidal" : "purple",
    "Petcoke":"purple",
    "Geothermal":"purple",
    "Storage":"purple",
    "Cogeneration":"purple",
}

class App:

    def __init__(self) -> None:    
        
        # SIDE BAR
        "Imput Stock Symbol"
        self.country = st.sidebar.text_input('Enter country', value="Germany")
        num_of_plants = st.sidebar.selectbox(
                            'Show how many power plants?',
                            (10,100,"all"),
                            index = 0
                            )
        
        # data
        # instantiating database object
        DB = Database()
        
        # extracting info
        df = DB._country_data(self.country)

        if num_of_plants == "all":
            pass
        else:
            df = df.head(num_of_plants)

        # MAP
        "map"
        self.map = folium.Map(
                        [df.loc[0, "latitude"], df.loc[0, "longitude"]], # zooming into the country
                        zoom_start=3,
                        control_scale=True)
        
        for i, row in df.iterrows():
            # adding markers
            self._markers(row)


        # call to render Folium map in Streamlit
        st_data = st_folium(self.map)

        # TABLES
        # top ten
        st.dataframe(df.head(10))

        #CHARTS
        st.bar_chart(
            data=df,
            x = "primary_fuel",
            y = "capacity_mw"
        )
    
    def _markers(self, _row):
        
        # Icon
        icon = folium.Icon(
                color=COLOUR_DICT[_row["primary_fuel"]],
                icon = "location_dot"
                                )
        # html
        html = f"""
        <b> {_row["name"]}</b><br>
        <b> {_row["primary_fuel"]}</b><br>
        Capacity (mw) : {_row["capacity_mw"]}<br>
        Owner : {_row["owner"]}<br> 
        """
        
        iframe = branca.element.IFrame(html=html, width=200, height=100)
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