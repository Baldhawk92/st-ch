import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from streamlit_folium import folium_static

# ------Streamlit------

st.set_page_config(page_title="Canada Health",
                   page_icon='',
                   layout='wide'
)

# ------Streamlit------

stMainMenu = """
    <style>  
        #MainMenu {
            visibility: hidden;
        }
            
        .stDeployButton {
            display:none;
        }

        div [data-testid="stHeader"] {
            display: none;
        }
    </style>
"""
st.markdown(stMainMenu, unsafe_allow_html=True)


#----This the the deploy container (Main Menu)---------


#-------checkbox selection------



#-------checkbox selection------

#---------CSS for the entire page-------

conatiner_style = """
    <style>
        div [data-testid="stSidebarUserContent"]{
            margin-top: -5em;
        }
    </style>
"""
st.markdown(conatiner_style, unsafe_allow_html=True)

#---------CSS for the entire page-------

#-------The logo and the title-----------------



#-------The logo and the title-----------------

# @st.cache_data(show_spinner="Please wait....")
# def load_data():
sidebar_option = st.sidebar.radio("Select what you want:", ["Hospital Finder", "Data Analysis"])
df = pd.read_excel("hospitaldata.xlsx", engine='openpyxl')
df1 = df.fillna(0) #unknown is the value here
df2 = df1.drop(columns=['index', 'unit', 'source_format_str_address', 'CSDuid', 'Pruid'])
df3 = df2.rename(columns={'facility_name': 'Facility Name', 'source_facility_type': 'Category Type', 'odhf_facility_type': 'Facility Type', 'provider': 'Facility Provider', 'street_no': 'Street Number', 'street_name': 'Street Name', 'postal_code': 'Postal Code', 'city': 'City', 'province': 'Province', 'CSDname': 'Sub City', 'latitude': 'Latitude', 'longitude': 'Longitude'})

# if sidebar_option == "Data Analysis":

#     selected_option = st.radio("Select an option:", ["Type of Facility", "Province or City", "Provider", "Source"], index=None)

#     if selected_option:
#         if selected_option == "Type of Facility":
#             column_to_filter = 'odhf_facility_type'
            

        
#         elif selected_option == "Provider":
#             column_to_filter = 'provider'
#         elif selected_option == "Source":
#             column_to_filter = 'source_facility_type'
#         elif selected_option == "Province or City":
#             sub_option = st.radio("Filter By:", ["Province", "City"], index=0)
#             column_to_filter = 'province' if sub_option == "Province" else "city"      
        
#         unique_values = df1[column_to_filter].unique()
#         selected_value = st.selectbox(f"Select a {column_to_filter.title()}", unique_values)
#         filtered_df = df1[df1[column_to_filter] == selected_value]

#         st.dataframe(filtered_df)

#     grouped = df1.groupby(['province', 'odhf_facility_type']).size()
#     table = grouped.unstack().reset_index()

#     st.subheader("Facility Type Distribution by Province:")
#     st.dataframe(table, use_container_width=True)

if sidebar_option == "Hospital Finder":
    try:
        st.title("Healthcare Facility Proximity Finder (Canada)")

        postal_code = st.text_input("Enter your Postal Code (e.g., V8X 1W3):")
        
                
        if postal_code:
            geolocator = Nominatim(user_agent="health_locator", timeout=10)
            location = geolocator.geocode(postal_code)

            user_coords = None

            if location:
                user_coords = (location.latitude, location.longitude)
                st.success(f"Your coordinates: {user_coords} (from geocoder)")
                radius_km = st.slider("Search Radius (in km):", min_value=1, max_value=30)
            else:
                st.warning("Geocoding failed. Trying to find facilities using partial postal code (FSA)...")

                # Extract FSA (first 3 characters)
                fsa = postal_code.strip().upper().replace(" ", "")[:3]

                # Match dataset postal codes that start with this FSA
                df3['Clean Postal'] = df3['Postal Code'].astype(str).str.replace(" ", "").str.upper().str.strip()
                fsa_matches = df3[df3['Clean Postal'].str.startswith(fsa)]

                if not fsa_matches.empty:
                    st.success(f"Found {len(fsa_matches)} facilities in the same FSA ({fsa}).")
                    nearby_facilities = fsa_matches[
                        (fsa_matches['Latitude'] != 0) &
                        (fsa_matches['Longitude'] != 0) |
                        (fsa_matches['Street Number'].astype(str).str.strip() != '') &
                        (fsa_matches['Street Name'].astype(str).str.strip() != '')
                    ]
                    st.dataframe(nearby_facilities)

                    # Optional: display a rough map with these facilities
                    avg_lat = nearby_facilities['Latitude'].mean()
                    avg_lon = nearby_facilities['Longitude'].mean()
                    m = folium.Map(location=(avg_lat, avg_lon), zoom_start=12)

                    for _, row in nearby_facilities.iterrows():
                        folium.Marker(
                            location=(row['Latitude'], row['Longitude']),
                            popup=row['Facility Name'],
                            icon=folium.Icon(color='green')
                        ).add_to(m)

                    folium_static(m)
                else:
                    st.error(f"No facilities found with postal codes starting with '{fsa}'. Please try a different postal code.")
                    st.stop()
            # If geocoding succeeded earlier, continue to normal radius search:
            if user_coords:
                def is_in_radius(row):
                    facility_coords = (row['Latitude'], row['Longitude'])
                    try:
                        distance = geodesic(user_coords, facility_coords).km
                        return distance <= radius_km
                    except:
                        return False

                nearby_facilities = df3[df3.apply(is_in_radius, axis=1)]

                if not nearby_facilities.empty:
                    st.subheader(f"Facilities within {radius_km} km of {postal_code}:")
                    st.dataframe(nearby_facilities)

                    m = folium.Map(location=user_coords, zoom_start=13)
                    folium.Marker(location=user_coords, popup="Your Location", icon=folium.Icon(color='blue')).add_to(m)

                    for _, row in nearby_facilities.iterrows():
                        folium.Marker(
                            location=(row['Latitude'], row['Longitude']),
                            popup=row['Facility Name'],
                            icon=folium.Icon(color='green')
                        ).add_to(m)

                    folium_static(m)
                else:
                    st.warning(f"No facilities found within {radius_km} km.")
    except Exception as e:
        st.error(f"Error occurred: {e}")
