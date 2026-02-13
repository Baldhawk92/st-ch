# ---------Imports----------
import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from streamlit_folium import st_folium
import time
# ---------Imports----------


# ------Streamlit----------
st.set_page_config(page_title="Canada Health", layout="wide")
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
    # Initialize Nominatim geocoder with a custom user agent
    geolocator = Nominatim(user_agent="canada_health_locator_v1")
    # Add rate limiting to be respectful to the free service (1 request per second)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    return geolocator, geocode
# ------------------------------------------------------------------------------------------------------------------------------------------------------

 
df = load_data()
# ------------------------------------------------------------------------------------------------------------------------------------------------------


if sidebar_options == 'Search Facility':
    st.title("Healthcare Facility Locator for Canadian Citizens")
    postal_code = st.text_input("Please enter your address or location name")
    # ------------------------------------------------------------------------------------------------------------------------------------------------------


    if postal_code:
        geolocator, geocode = get_geolocator()
        
        try:
            # Geocode the postal code with Canada specified
            location = geocode(f"{postal_code}, Canada")
        except Exception as e:
            st.error(f"Error geocoding postal code: {e}")
            location = None
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
        

        
        if location:
            user_coords = (location.latitude, location.longitude)
            
            facility_distance = st.slider("How far do you want to look for? (in Km)", 1, 10)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
        
      
            def is_in_radius(row):
                facility_coords = (row['Latitude'], row['Longitude'])
                distance = geodesic(user_coords, facility_coords).km
                return distance <= facility_distance
        
            filtered_df = df[df.apply(is_in_radius, axis=1)]
            # st.dataframe(filtered_df)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------


            m = folium.Map(user_coords, zoom_start=12)
            folium.Marker(
                user_coords,
                popup="Your Location",
                icon=folium.Icon(color='blue')
            ).add_to(m)


            for _, row in filtered_df.iterrows():
                func = f'<h4>{row["Facility Name"]}</h4><span style="font-size: 14px;">Service Type: <b>{row["Service Type"]}</b></span><br /><span style="font-size: 14px;">Provider Name: <b>{row["Provider Name"]}</b></span><br /><span style="font-size: 14px;">Full Address: <b>{row["Full Address"]}</b></span>'
                popup = folium.Popup(func, max_width=350)
                folium.Marker(
                    location = (row['Latitude'], row['Longitude']),
                    popup = popup,
                    icon=folium.Icon(color='green')
                ).add_to(m)
                    

            st_folium(m, width=700, height=400, returned_objects=[])
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
        else:
            st.error("Could not find location for the entered postal code. Please check and try again.")
            
  
    else:
        st.warning("Please enter your address or location name")
# --------Main code------------
