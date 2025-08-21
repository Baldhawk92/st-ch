# ---------Imports----------
import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import googlemaps
# ---------Imports----------


# ------Streamlit----------
st.set_page_config(page_title="Canada Health", page_icon="", layout="wide")
# ------Streamlit----------


# -----CSS--------
HideMainMenu = """
    <style>
        div [data-testid="stHeader"]{
            display: none
        }
        
    </style>
"""
st.html(HideMainMenu)
# -----CSS--------


# ------Sidebar-----------
sidebar_options = st.sidebar.radio("Select what you want", ['Search Facility', 'Data Analysis (Coming Soon)'])
# ------Sidebar-----------


# --------Main code------------
@st.cache_data
def load_data():
    # ------Dataframe-----------
    df = pd.read_excel('hospitaldata.xlsx', engine='openpyxl')
    df.replace(pd.NA, '', inplace=True)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------

    def full_address(row):
        if row['street_no'] and row['street_name']:
            return f'{str(row['street_no']).title()}, {str(row['street_name']).title()}, {str(row['city']).title()}, {str(row['postal_code']).upper()}'
        else:
            return str(row['postal_code'])

    df['Full Address'] = df.apply(full_address, axis=1)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------


    df = df[['facility_name', 'source_facility_type', 'odhf_facility_type', 'provider', 'Full Address', 'postal_code', 'latitude', 'longitude']]
    df.rename(columns={
        'facility_name' : 'Facility Name',
        'source_facility_type' : 'Facility Type',
        'odhf_facility_type' : 'Service Type',
        'provider' : 'Provider Name',
        'postal_code' : 'Postal Code',
        'latitude' : 'Latitude',
        'longitude' : 'Longitude'
    }, inplace=True)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------


    df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].fillna(0.0)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------


    return df
    # ------Dataframe-----------


@st.cache_resource
def get_geolocator():
    gmaps_api_key = st.secrets["api_keys"]["gmaps"]
    gmaps = googlemaps.Client(key=gmaps_api_key)
    return gmaps
# ------------------------------------------------------------------------------------------------------------------------------------------------------

 
df = load_data()
# geolocator = get_geolocator()
# ------------------------------------------------------------------------------------------------------------------------------------------------------


if sidebar_options == 'Search Facility':
    st.title("Healthcare Facility Locator for Canadian Citizens")
    postal_code = st.text_input("Enter your postal code (e.g. V8X 3R5)")
    # ------------------------------------------------------------------------------------------------------------------------------------------------------


    if postal_code:
        gmaps = get_geolocator()
        
        location = gmaps.geocode(postal_code + ", Canada")
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
        

        
        if location:
            location = location[0]['geometry']['location']
            user_coords = (location['lat'], location['lng'])
            
            facility_distance = st.slider("How far do you want to look for? (in Km)", 1, 10)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
        
      
            def is_in_radius(row):
                facility_coords = (row['Latitude'], row['Longitude'])
                distance = geodesic(user_coords, facility_coords).km
                return distance <= facility_distance
        
            df = df[df.apply(is_in_radius, axis=1)]
            # st.dataframe(df)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------


            m = folium.Map(user_coords, zoom_start=12)
            folium.Marker(
                user_coords,
                popup="Your Location",
                icon=folium.Icon(color='blue')
            ).add_to(m)


            for _, row in df.iterrows():
                func = f'<h4>{row['Facility Name']}</h4><span style="font-size: 14px;">Service Type: <b>{row['Service Type']}</b></span><br /><span style="font-size: 14px;">Provider Name: <b>{row['Provider Name']}</b></span><br /><span style="font-size: 14px;">Full Address: <b>{row['Full Address']}</b></span>'
                popup = folium.Popup(func, max_width=350)
                folium.Marker(
                    location = (row['Latitude'], row['Longitude']),
                    popup = popup,
                    icon=folium.Icon(color='green')
                ).add_to(m)
                    

            st_folium(m, width=700, height=400, returned_objects=[])
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
            
  
    else:
        st.error("Please enter a postal code")
# --------Main code------------






