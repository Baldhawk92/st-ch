import pandas as pd
# import pygwalker as pyg
import streamlit as st
import streamlit.components.v1 as components
from io import BytesIO
import base64
import os
import time
# import plotly.express as px
# from openpyxl import load_workbook
# import xlsxwriter


# ------Streamlit------

st.set_page_config(page_title="CVIEW",
                   page_icon='https://commissionaires.ca/wp-content/uploads/2021/10/index.ico',
                   layout='wide'
)

# ------Streamlit------


#----This the the deploy container (Main Menu)---------

stMainMenu = """
    <style>  
        #MainMenu {
            visibility: hidden;
        }
            
        .stDeployButton {
            display:none;
        }
            
        footer {
            visibility: hidden;
        }
            
        #stDecoration {
            display:none;
        }
            
        div [data-testid="block-container"], div [data-testid="stAppViewBlockContainer"] {
            margin-top: -5em;
        }

        div [data-testid="stHeader"] {
            display: none;
        }

        div [data-testid="stException"] {
            display: none
        }
    </style>
"""
st.markdown(stMainMenu, unsafe_allow_html=True)

#----This the the deploy container (Main Menu)---------


#-------checkbox selection------

st.sidebar.header('Select Type:')

#-------checkbox selection------


#---------CSS for the entire page-------

conatiner_style = """
    <style>
        div [data-testid="stSidebarUserContent"]{
            margin-top: -5em;
        }

        div [data-testid="stSidebarUserContent"] .stHeadingContainer h2{
            color: #F26222;
            font-weight: bold;
        }

        div [data-testid="stSidebarUserContent"] p{
            font-weight: bold;
        }

        div[data-testid="stHorizontalBlock"] div[data-testid="stMarkdownContainer"] h2,h3 {
            # background-color: #36454F;
            text-align: center;
        }

        div[data-testid="stHorizontalBlock"] div[data-testid="stVerticalBlock"] div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdown"] div[data-testid="stMarkdownContainer"] p {
            text-align: center;
        } 

        p.content_titles {
            text-align: center;
        }

        .stButton {
            position: relative;
            text-align: center;
            overflow-wrap: above;
        }

        div [data-testid="stButton"] button{
            background: #003A63;
            color: #f26222;
        }

        div [data-testid="stButton"] button:hover{
            color: white;
            border: 1px solid #f26222;
        }
        
        [data-testid="stDataFrameResizable"] {
            border: 2px solid #000000 !important;
        }

        [id^="total-"], [id^="revenue-"] {
            color: #F26222;
        }
        
        div [data-testid="stFileUploadDropzone"] {
            background: #003A63;
            color: #F26222;
        }

        div [data-testid="stFileUploadDropzone"] button{
            background: #F26222;
            color: black;
        }

        .stMarkdown p a {
            color: #F26222;
        }

        div [data-testid="stSidebarContent"] div[data-testid="stMultiSelect"] span{
            color: black;
            font-weight: bold;
        }

        div[data-testid="stMultiSelect"] span{
            color: black;
        }
    </style>
"""
st.markdown(conatiner_style, unsafe_allow_html=True)

#---------CSS for the entire page-------


#-------The logo and the title-----------------

st.markdown(f'<img src="https://commissionaires.ca/wp-content/uploads/2021/10/index.ico" width=100 style="display: block; margin-left: auto; margin-right: auto;"/>', unsafe_allow_html=True)
st.markdown(f'<p class="sales" style="text-align:center; font-size: 50px; font-weight: 900;">Revenue Dashboard</p>', unsafe_allow_html=True)
st.markdown("##")

#-------The logo and the title-----------------

#-------Add borders to all the downloaded excel files (defined globally)-------

def add_borders(s):
    border = 'border: 0.1px solid black;'
    return border

#-------Add borders to all the downloaded excel files (defined globally)-------


#--------Cache Data----------
#-----------STATIC GUARDING---------------

@st.cache_data(show_spinner="Please wait....")

#-------Upload files 1 and 2 which are billable hours and client master file--------

def read_data(file1, file2):
    # e = time.time()
    if file1 is not None and file2 is not None:
        df1 = pd.read_excel(file1, sheet_name="Source Data", skiprows=3, usecols=['Invoice Date', 'Customer Number', 'Hours', 'Total'], engine='openpyxl')
        df2 = pd.read_excel(file2, engine='openpyxl')
        # print("Cached Static")
        # f = time.time()
        # print(f"Time taken to read files for Static: {f - e} seconds")
        return df1, df2
    elif file1 is not None:
        st.warning("Please upload the Client Master file.")
    elif file2 is not None:
        st.warning("Please upload the first Excel file.")
    else:
        st.warning("Please upload all the Excel files.")
        
    return None, None


# uploaded_file1 = None
# uploaded_file2 = None
df1 = None
df2 = None

selected_option = st.sidebar.radio("Select an option:", ["Static Guarding", "Other Revenue"], index=None)



if selected_option == "Static Guarding":
    
    save_folder = os.path.abspath("Uploads/Static_Guarding_Billable_files")
    os.makedirs(save_folder, exist_ok=True)

    # if os.access(save_folder, os.W_OK):
    #     print(f"User has write permission to {save_folder}")
    # else:
    #     print(f"User does not have write permission to {save_folder}")

    save_folder2 = os.path.abspath("Uploads/Static_Guarding_Client_Master_file")
    os.makedirs(save_folder2, exist_ok=True)

    # with st.expander("Upload the XLSX Files", expanded=False):
    #     uploaded_file1 = st.file_uploader("Upload Static Guarding Billable Hours and Revenue File", type=["xlsx"])
    #     uploaded_file2 = st.file_uploader("Upload Client Master File", type=["xlsx"], key='file2', on_change=None)

    # if 'show_success1' not in st.session_state:
    #     st.session_state.show_success1 = True
    
    # if 'show_success2' not in st.session_state:
    #     st.session_state.show_success2 = True
 
    # if uploaded_file1:
    #     file_path1 = os.path.join(save_folder, uploaded_file1.name)
    #     with open(file_path1, "wb") as file:
    #         file.write(uploaded_file1.read())
    #     if st.session_state.show_success1:
    #         succ = st.success(f"File '{uploaded_file1.name}' saved to {save_folder}")
    #         time.sleep(2)
    #         succ.empty()
    #     st.session_state.show_success1 = False
        

    # if uploaded_file2:
    #         file_path2 = os.path.join(save_folder2, uploaded_file2.name)
    #         with open(file_path2, "wb") as file:
    #             file.write(uploaded_file2.read())
    #         if st.session_state.show_success2:
    #             succ2 = st.success(f"File '{uploaded_file2.name}' saved to {save_folder2}")
    #             time.sleep(2)
    #             succ2.empty() 
    #         st.session_state.show_success2 = False

    saved_files = [f for f in os.listdir(save_folder) if f.endswith((".xlsx"))]
    selected_files = st.sidebar.multiselect("Select file to display", saved_files, default=[])

    saved_file = next((f.name for f in os.scandir(save_folder2) if f.is_file() and f.name.endswith(".xlsx")), None)

    if selected_files:
        if saved_file is not None:
            for selected_file in selected_files:
                file_path = os.path.join(save_folder, selected_file)
                file_path_new = os.path.join(save_folder2, saved_file)
                df1, df2 = read_data(file_path, file_path_new)
        else:
            st.error("Please upload the Static Guarding Client Master file")
        

        if df1 is not None:
            # e = time.time()
            df1.replace(' ', pd.NA, inplace=True)
            df1.rename(columns={'Total': 'Revenue'}, inplace=True)
            df1.dropna(how='all', axis=1, inplace=True)
            # columns_to_drop = ['Category', 'Batch #', 'Invoice #', 'Line #', 'Employee #', 'First Name', 'Middle Name', 'Last Name', 'Classification', 'Rate']
            # df1.drop(columns=columns_to_drop, inplace=True)
            # f = time.time()
            # print('Time taken by df1: ', format(f-e))
            # df1.to_excel("df1.xlsx", index=False)

        if df1 is not None and df2 is not None:
            # a = time.time()
            merged_df = pd.merge(df1, df2, on=['Customer Number'], how="outer")

            cust_no_to_delete = 9200
            merged_df = merged_df[merged_df['Customer Number'] != cust_no_to_delete]

            # b = time.time()
            # print('Time taken by merged_df: ', format(b-a))

            # -------Exporting as Master DB-------

            if st.sidebar.button('Export Static Guarding Merged Database'):
                with st.spinner('Exporting Static Guarding Merged Database....'):
                    save_merged = os.path.abspath("Merged Databases/Static_Guarding_Merged_Databases")
                    filename = "Merged Database " + os.path.basename(file_path)
                    save_path = os.path.join(save_merged, filename)
                    merged_df.to_excel(f"{save_path}.xlsx", index=False)
                succ = st.success(f'Static Guarding Merged Database exported to {save_path} folder')
                time.sleep(5)
                succ.empty()

            # -------Exporting as Master DB-------

# ------Make a folder and save the files in pc------
# -------Upload files 1 and 2 which are billable hours and client master file--------    


    if df1 is not None and df2 is not None:

    # ------Location Sidebar------
        
        st.sidebar.header('Please Filter Here:')

        non_empty_hours_mask = merged_df['Hours'].notna()

        if non_empty_hours_mask.any():

            location = merged_df.loc[non_empty_hours_mask, "Location"].unique()
            select_all_option = "Select All"

            if select_all_option not in location:
                location_options = [select_all_option] + list(location)

            location = st.sidebar.multiselect("Select the Location:", options=location_options)

            if select_all_option in location:
                location = list(merged_df.loc[non_empty_hours_mask, "Location"].unique())

            location_str = [str(item) for item in location]
            

            # ---------Check for locations, add their hours and revenue, round them, make them in descending order, and showing top 10 customers----------  
                
            filtered_by_location = merged_df[merged_df['Location'].isin(location)]
            filtered_by_location2 = filtered_by_location.groupby(['Customer Name', 'Location']).agg({'Hours' : "sum", 'Revenue': 'sum'}).reset_index()
            sorted_by_location = filtered_by_location2.sort_values('Revenue', ascending=False).round(2)
            sorted_by_location2 = sorted_by_location.style.apply(lambda x: ['background-color: #003A63; color: white;' if i < 10 else 'background-color: #00172B; color: white;' for i in range(len(x))], axis=0).format({'Hours': "{:,}", 'Revenue' : "{:,}"})
            
                            
            # ---------Check for locations, add their hours and revenue, round them, make them in descending order, and showing top 10 customers----------


            


            # ------Show the category sidebar only when location is selected--------

            if filtered_by_location.shape[0] > 0:     #check whether the df is empty or not
                
                #---------Category Sidebar--------

                non_empty_cat_mask = merged_df['Hours'].notna()

                if non_empty_cat_mask.any():
                    
                    category = merged_df.loc[non_empty_cat_mask, "Category"].unique()
                    select_all_option = "Select All"

                    if select_all_option not in category:
                        category_options = [select_all_option] + list(category)

                    category = st.sidebar.multiselect("Select the Category:", options=category_options)

                    if select_all_option in category:
                        category = list(merged_df.loc[non_empty_cat_mask, "Category"].unique())

                    category_str = [str(item) for item in category]
                        

                    #---------Category Sidebar--------


                    #-------Filtering the category----------
                        
                    filtered_by_category = filtered_by_location[filtered_by_location['Category'].isin(category)]
                    filtered_by_category2 = filtered_by_category.groupby(['Customer Name', 'Location']).agg({'Category' : 'first', 'Hours' : "sum", 'Revenue': 'sum'}).reset_index()
                    sorted_by_category = filtered_by_category2.sort_values('Revenue', ascending=False).round(2)
                    sorted_by_category2 = sorted_by_category.style.apply(lambda x: ['background-color: #003A63; color: white;' if i < 10 else 'background-color: #00172B; color: white' for i in range(len(x))], axis=0).format({'Hours': "{:,}", 'Revenue' : "{:,}"})
                    
                    #-------Filtering the category----------
                    
                    
                    #--------Totalling the Hours and Revenue--------

                    total_hours_location = int(round(filtered_by_location['Hours'].sum()))
                    total_hours_category = int(round(filtered_by_category['Hours'].sum()))
                    total_revenue_location = int(round(filtered_by_location['Revenue'].sum()))
                    total_revenue_category = int(round(filtered_by_category['Revenue'].sum()))

                    #--------Totalling the Hours and Revenue--------
                    

                    #-------Creating 2 columns and showing data-------
                    
                    left_column,middle_column = st.columns(2)
                    
                    

                    with left_column:
                        st.subheader("Total Billable Hours (By Location)")
                        st.subheader(f"[{', '.join(location_str)}]")
                        st.subheader(f"{total_hours_location:,} Hours")
                        st.markdown("##")
                        st.markdown("##")
                        st.subheader("Total Billable Hours (By Category)")
                        st.subheader(f"[{', '.join(category_str)}]")
                        st.subheader(f"{total_hours_category:,} Hours")
                        st.markdown("##")
                        st.markdown("##")
                        
                        
                        #--------Creating filter (drop-down) for Revenue by Location and also inserting a row with Total Hours and Revenue based on the filter---------

                        st.subheader("Revenue By Location")
                        filter_value = st.multiselect("Filter by Customer Name (Location)", sorted_by_location['Customer Name'].unique(), key=hash("multiselect_1"))
                        if filter_value:
                            filtered_df = sorted_by_location[sorted_by_location['Customer Name'].isin(filter_value)]
                            total_hours = filtered_df['Hours'].sum()
                            total_revenue = filtered_df['Revenue'].sum()
                            total_row = pd.DataFrame({'Customer Name' : ['TOTAL'], 'Hours' : [total_hours], 'Revenue' : [total_revenue], 'Location' : ''})
                            filtered_df = pd.concat([filtered_df, total_row], ignore_index=True)
                            filtered_df['Hours'] = filtered_df['Hours'].round(2).astype(float)
                            filtered_df['Revenue'] = filtered_df['Revenue'].round(2).astype(float)
                            def highlight_last_row(s):
                                if s.name == len(filtered_df) - 1:
                                    return ['background-color: #F26222; color: black' for i in s]
                                else:
                                    return ['' for i in s]
                            filtered_df2 = filtered_df.style.apply(highlight_last_row, axis=1).format({'Hours': "{:,}", 'Revenue' : "{:,}"})
                            st.dataframe(filtered_df2, hide_index=True, use_container_width=True, height=500)
                            st.markdown(f"Total Hours: {int(round(total_hours)):,} Hours")
                            st.markdown(f"Total Revenue: ${int(round(total_revenue)):,}") 
                        else:
                            st.dataframe(sorted_by_location2, hide_index=True, use_container_width=True, height=500)
                            st.markdown(f"Total Hours: {int(round(filtered_by_location['Hours'].sum())):,} Hours")
                            st.markdown(f"Total Revenue: ${int(round(filtered_by_location['Revenue'].sum())):,}")                        


                        #-----------Creating download button for Revenue by Location-----------

                        

                        def download_link(filtered_df, filename, txt):
                            towrite = BytesIO()
                            filtered_df = filtered_df.copy()  
                            filtered_df = filtered_df.style.map(add_borders)
                            filtered_df.to_excel(towrite, index=False, header=True)
                            towrite.seek(0)  
                            b64 = base64.b64encode(towrite.read()).decode()
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                            return href                    
                        

                        def download_link2(sorted_by_location, filename, txt):
                            towrite = BytesIO()
                            sorted_by_location = sorted_by_location.copy()         
                            sorted_by_location = sorted_by_location.style.apply(lambda x: ['background-color: #003A63; color: white;' if i < 10 else 'background-color: white; color: black;' for i in range(len(x))], axis=0).map(add_borders)
                            sorted_by_location.to_excel(towrite, index=False, header=True)
                            towrite.seek(0) 
                            b64 = base64.b64encode(towrite.read()).decode()
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                            return href
                        
                        if filter_value:
                            if st.button('Create Revenue By Location as XLSX'):
                                tmp_download_link = download_link(filtered_df, f'Loc - {location}.xlsx', txt="Click here to download")
                                st.markdown(tmp_download_link, unsafe_allow_html=True)
                        else:
                            if st.button('Create Revenue By Location as XLSX'):
                                tmp_download_link = download_link2(sorted_by_location, f'Loc - {location}.xlsx', txt="Click here to download")
                                st.markdown(tmp_download_link, unsafe_allow_html=True)

                        #-----------Creating download button for Revenue by Location-----------
                                
                        #--------Creating filter (drop-down) for Revenue by Location and also inserting a row with Total Hours and Revenue based on the filter---------


                    with middle_column:
                        st.subheader("Total Revenue (By Location)")
                        st.subheader(f"[{', '.join(location_str)}]")
                        st.subheader(f"${total_revenue_location:,}")
                        st.markdown("##")
                        st.markdown("##")
                        st.subheader("Total Revenue (By Category)")
                        st.subheader(f"[{', '.join(category_str)}]")
                        st.subheader(f"${total_revenue_category:,}")
                        st.markdown("##")
                        st.markdown("##")


                        #--------Creating filter (drop-down) for Revenue by Location & Category and also inserting a row with Total Hours and Revenue based on the filter---------

                        st.subheader("Revenue By Location & Category")
                        filter_value = st.multiselect("Filter by Customer Name (Location & Category)", sorted_by_category['Customer Name'].unique(), key=hash("multiselect_2"))
                        if filter_value:
                            filtered_df = sorted_by_category[sorted_by_category['Customer Name'].isin(filter_value)]
                            total_hours = filtered_df['Hours'].sum()
                            total_revenue = filtered_df['Revenue'].sum()
                            total_row = pd.DataFrame({'Customer Name' : ['TOTAL'], 'Hours' : [total_hours], 'Revenue' : [total_revenue], 'Location' : '', 'Category' : ''})
                            filtered_df = pd.concat([filtered_df, total_row], ignore_index=True)
                            filtered_df['Hours'] = filtered_df['Hours'].round(2).astype(float)
                            filtered_df['Revenue'] = filtered_df['Revenue'].round(2).astype(float)
                            def highlight_last_row(s):
                                if s.name == len(filtered_df) - 1:
                                    return ['background-color: #F26222; color: black;' for i in s]
                                else:
                                    return ['' for i in s]
                            filtered_df2 = filtered_df.style.apply(highlight_last_row, axis=1).format({'Hours': "{:,}", 'Revenue' : "{:,}"})
                            st.dataframe(filtered_df2, hide_index=True, use_container_width=True, height=500)
                            st.markdown(f"Total Hours: {int(round(total_hours)):,} Hours")
                            st.markdown(f"Total Revenue: ${int(round(total_revenue)):,}") 
                        else:
                            st.dataframe(sorted_by_category2, hide_index=True, use_container_width=True, height=500)
                            st.markdown(f"Total Hours: {int(round(filtered_by_category['Hours'].sum())):,} Hours")
                            st.markdown(f"Total Revenue: ${int(round(filtered_by_category['Revenue'].sum())):,}")

                        #--------Creating filter (drop-down) for Revenue by Location & Category and also inserting a row with Total Hours and Revenue based on the filter---------


                        #-----------Creating download button for Revenue by Location & Category-----------
                            
                        def download_link(filtered_df, filename, txt):
                            towrite = BytesIO()
                            filtered_df = filtered_df.copy()
                            filtered_df = filtered_df.style.map(add_borders)   
                            filtered_df.to_excel(towrite, index=False, header=True)
                            towrite.seek(0)
                            b64 = base64.b64encode(towrite.read()).decode()
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                            return href
                        
                        def download_link2(sorted_by_category, filename, txt):
                            towrite = BytesIO()
                            sorted_by_category = sorted_by_category.copy()  
                            sorted_by_category = sorted_by_category.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: white; color: black' for i in range(len(x))], axis=0).map(add_borders)
                            sorted_by_category.to_excel(towrite, index=False, header=True)
                            towrite.seek(0)
                            b64 = base64.b64encode(towrite.read()).decode()
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                            return href
                        
                        if filter_value:
                            if st.button('Create Revenue By Location & Category as XLSX'):
                                tmp_download_link = download_link(filtered_df, f'L&C{location}-{category}.xlsx', txt="Click here to download")
                                st.markdown(tmp_download_link, unsafe_allow_html=True)
                        else:
                            if st.button('Create Revenue By Location & Category as XLSX'):
                                tmp_download_link = download_link2(sorted_by_category, f'L&C{location}-{category}.xlsx', txt="Click here to download")
                                st.markdown(tmp_download_link, unsafe_allow_html=True)

                        #-----------Creating download button for Revenue by Location & Category-----------
                                
                        #--------Creating filter (drop-down) for Revenue by Location & Category---------
                                
                    #-------Creating 2 columns and showing data-------
                    
                    

                    # ------Show the site name only when category is selected---------
                                
                    if filtered_by_category.shape[0] > 0:
                        site_name = filtered_by_category["Site Name"].unique()


                        # ---------Check for locations, add their hours and revenue, round them, make them in descending order, and showing top 10 customers---------- 
                        
                        filtered_by_site_name = filtered_by_category[filtered_by_category['Site Name'].isin(site_name)]
                        filtered_by_site_name2 = filtered_by_site_name.groupby(['Site Name', 'Location']).agg({'Hours' : "sum", 'Revenue': 'sum', 'Category' : 'first', 'Customer Number' : 'first', 'Customer Name' : 'first'}).reset_index()[['Customer Number', 'Customer Name', 'Site Name', 'Location', 'Category', 'Hours', 'Revenue']]
                        sorted_by_site_name = filtered_by_site_name2.sort_values('Revenue', ascending=False).round(2)
                        sorted_by_site_name2 = sorted_by_site_name.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: #00172B; color: white' for i in range(len(x))], axis=0).format({'Hours': "{:,}", 'Revenue' : "{:,}"})
                        st.markdown("##")
                        st.markdown("##")
                        
                        # ---------Check for locations, add their hours and revenue, round them, make them in descending order, and showing top 10 customers----------


                        #-------Creating filter (drop-down) for Revenue by Site Name and also inserting a row with Total Hours and Revenue based on the filter---------

                        st.subheader("Revenue By Site Name")
                        filter_value = st.multiselect("Filter by Customer Name (Location)", sorted_by_site_name['Customer Name'].unique(), key=hash("multiselect_3"))
                        if filter_value:
                            filtered_df = sorted_by_site_name[sorted_by_site_name['Customer Name'].isin(filter_value)]
                            total_hours = filtered_df['Hours'].sum()
                            total_revenue = filtered_df['Revenue'].sum()
                            filtered_df.loc[:, 'Customer Number'] = filtered_df['Customer Number'].astype(str)
                            total_row = pd.DataFrame({'Customer Name' : ['TOTAL'], 'Hours' : [total_hours], 'Revenue' : [total_revenue], 'Location' : '', 'Category' : '', 'Site Name' : '', 'Customer Number' : ''})
                            filtered_df = pd.concat([filtered_df, total_row], ignore_index=True)
                            filtered_df['Hours'] = filtered_df['Hours'].round(2).astype(float)
                            filtered_df['Revenue'] = filtered_df['Revenue'].round(2).astype(float)
                            
                            def highlight_last_row(s):
                                if s.name == len(filtered_df) - 1:
                                    return ['background-color: #F26222; color: black;' for i in s]
                                else:
                                    return ['' for i in s]
                            filtered_df2 = filtered_df.style.apply(highlight_last_row, axis=1).format({'Hours': "{:,}", 'Revenue' : "{:,}"})
                            st.dataframe(filtered_df2, hide_index=True, use_container_width=True, height=500)
                            st.markdown(f"Total Hours: {int(round(total_hours)):,} Hours")
                            st.markdown(f"Total Revenue: ${int(round(total_revenue)):,}") 
                        else:
                            st.dataframe(sorted_by_site_name2, hide_index=True, use_container_width=True, height=500)
                            st.markdown(f"Total Hours: {int(round(filtered_by_site_name['Hours'].sum())):,} Hours")
                            st.markdown(f"Total Revenue: ${int(round(filtered_by_site_name['Revenue'].sum())):,}")
                        
                        #-------Creating filter (drop-down) for Revenue by Site Name and also inserting a row with Total Hours and Revenue based on the filter---------


                        #-----------Creating download button for Revenue by Site Name-----------
                            
                        def download_link(filtered_df, filename, txt):
                            towrite = BytesIO()
                            filtered_df = filtered_df.copy()   
                            filtered_df = filtered_df.style.map(add_borders)
                            filtered_df.to_excel(towrite, index=False, header=True)
                            towrite.seek(0)
                            b64 = base64.b64encode(towrite.read()).decode()
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                            return href
                        
                        def download_link2(sorted_by_site_name, filename, txt):
                            towrite = BytesIO()
                            sorted_by_site_name = sorted_by_site_name.copy()    
                            sorted_by_site_name = sorted_by_site_name.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: white; color: black' for i in range(len(x))], axis=0).map(add_borders)
                            sorted_by_site_name.to_excel(towrite, index=False, header=True)
                            towrite.seek(0)
                            b64 = base64.b64encode(towrite.read()).decode()
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                            return href
                        
                        if filter_value:
                            if st.button('Create Revenue By Site Name as XLSX'):
                                tmp_download_link = download_link(filtered_df, f'Loc - {location}.xlsx', txt="Click here to download")
                                st.markdown(tmp_download_link, unsafe_allow_html=True)
                        else:
                            if st.button('Create Revenue By Site Name as XLSX'):
                                tmp_download_link = download_link2(sorted_by_site_name, f'Loc - {location}.xlsx', txt="Click here to download")
                                st.markdown(tmp_download_link, unsafe_allow_html=True)

                        #-----------Creating download button for Revenue by Site Name-----------
                                
                    #--------Creating filter (drop-down) for Revenue by Site Name---------
                                
                    # ------Show the site name only when category is selected---------

                    #-------PygWalker(Data Visualization - Tables, Graphs, etc.)--------
                                
                        st.markdown("##")
                        st.markdown("##")
                        
                        st.subheader("Revenue & Sales Data Visualisation (Static Guarding)")
                       
                        # pyg_html = pyg.walk(sorted_by_site_name, return_html=True, dark='dark', env="Streamlit")
                        # components.html(pyg_html, height=900, scrolling=False)
                    
                    #-------PygWalker(Data Visualization - Tables, Graphs, etc.)--------

#-------Upload files 3 and 4 which are AR invoices file and Other revenue file--------
   

@st.cache_data(show_spinner="Please Wait....")
def read_data(file3, file4, file5):
    # e = time.time()
    if file3 is not None and file4 is not None and file5 is not None:
      
        df3 = pd.read_excel(file3, skipfooter=4, usecols=['Document Number/Type', 'Order Number'], engine='openpyxl')
        df4 = pd.read_excel(file4, skipfooter=4, engine='openpyxl')
        df5 = pd.read_excel(file5, engine='openpyxl')
        # print("Cached AR")
        # f = time.time()
        # print(f"Time taken to read files: {f - e} seconds")

        return df3, df4, df5

    elif file3 is not None:
        st.warning("Please upload the fourth Excel file.")
    elif file4 is not None:
        st.warning("Please upload the third Excel file.")
    elif file5 is not None:
        st.warning("Please upload the Client Master file.")
    else:
        st.warning("Please upload all the Excel files.")
    return None, None, None


# uploaded_file3 = None
# uploaded_file4 = None
# uploaded_file5 = None
df3 = None
df4 = None
df5 = None



if selected_option == "Other Revenue":
    save_folder3 = os.path.abspath("Uploads/AR_Invoice_files")
    os.makedirs(save_folder3, exist_ok=True)

    save_folder4 = os.path.abspath("Uploads/Other_Revenue_files")
    os.makedirs(save_folder4, exist_ok=True)

    save_folder5 = os.path.abspath("Uploads/Other_Revenue_Client_Master_file")
    os.makedirs(save_folder5, exist_ok=True)

    # with st.expander("Upload the XLSX Files", expanded=False):
    #     uploaded_file3 = st.file_uploader("Upload AR Customer Invoices File", type=["xlsx"])
    #     uploaded_file4 = st.file_uploader("Upload Other Revenue File", type=["xlsx"])
    #     uploaded_file5 = st.file_uploader("Upload Client Master File", type=["xlsx"], key='file5', on_change=None)

    # if 'show_success3' not in st.session_state:
    #     st.session_state.show_success3 = True
    
    # if 'show_success4' not in st.session_state:
    #     st.session_state.show_success4 = True

    # if 'show_success5' not in st.session_state:
    #     st.session_state.show_success5 = True

    # if uploaded_file3:
    #     file_path3 = os.path.join(save_folder3, uploaded_file3.name)
    #     with open(file_path3, "wb") as file:
    #         file.write(uploaded_file3.read())
    #     if st.session_state.show_success3:
    #         succ3 = st.success(f"File '{uploaded_file3.name}' saved to {save_folder3}")
    #         time.sleep(2)
    #         succ3.empty()
    #     st.session_state.show_success3 = False

    # if uploaded_file4:
    #     file_path4 = os.path.join(save_folder4, uploaded_file4.name)
    #     with open(file_path4, "wb") as file:
    #         file.write(uploaded_file4.read())
    #     if st.session_state.show_success4:
    #         succ4 = st.success(f"File '{uploaded_file4.name}' saved to {save_folder4}")
    #         time.sleep(2)
    #         succ4.empty()
    #     st.session_state.show_success4 = False

    # if uploaded_file5:
    #     file_path5 = os.path.join(save_folder5, uploaded_file5.name)
    #     with open(file_path5, "wb") as file:
    #         file.write(uploaded_file5.read())
    #     if st.session_state.show_success5:
    #         succ5 = st.success(f"File '{uploaded_file5.name}' saved to {save_folder5}")
    #         time.sleep(2)
    #         succ5.empty() 
    #     st.session_state.show_success5 = False

    saved_files2 = [f for f in os.listdir(save_folder3) if f.endswith((".xlsx"))]
    selected_files2 = st.sidebar.multiselect("Select AR file to display", saved_files2, default=[])
    
    saved_files3 = [f for f in os.listdir(save_folder4) if f.endswith((".xlsx"))]
    selected_files3 = st.sidebar.multiselect("Select Other Revenue file to display", saved_files3, default=[])

    saved_file5 = next((f.name for f in os.scandir(save_folder5) if f.is_file() and f.name.endswith(".xlsx")), None)


    if selected_files2 and selected_files3:
        if saved_file5 is not None:
            for selected_file, selected_file_new in zip(selected_files2, selected_files3):
                file_path2 = os.path.join(save_folder3, selected_file)
                file_path3 = os.path.join(save_folder4, selected_file_new)
                file_path_new5 = os.path.join(save_folder5, saved_file5)
                df3, df4, df5 = read_data(file_path2, file_path3, file_path_new5)
        else:
            st.error("Please upload the Other Revenue Client Master file")

        
        if df3 is not None:
            # e= time.time()
            # df3.drop(columns=['Amount', 'Balance', 'Entry', 'Over', 'PO Number','Doc. Date', 'Unnamed: 9', 'Due Date or Check/Recpt. No.'], inplace=True)
            mask = df3['Document Number/Type'].astype(str).str.contains(r'^\d')
            df3.loc[mask, 'Customer Number'] = df3.loc[mask, 'Document Number/Type']
            df3['Invoice Number'] = df3['Document Number/Type'][df3['Document Number/Type'].astype(str).str.startswith(('INV', 'RC'))]
            df3['Customer Number'] = pd.to_numeric(df3['Customer Number'])
            df3.drop(columns=['Document Number/Type'], inplace=True)
            result_data = {'Invoice Number': [], 'Customer Number': []}
            current_customer = ''

            def process_row(row):
                global current_customer
                if pd.notna(row['Customer Number']):
                    current_customer = row['Customer Number']
                elif pd.notna(row['Invoice Number']):
                    result_data['Invoice Number'].append(row['Invoice Number'])
                    result_data['Customer Number'].append(current_customer)

            df3.apply(process_row, axis=1)
            # df3.to_excel("df3.xlsx", index=False)
                
            result_df = pd.DataFrame(result_data)

            # result_df.to_excel("result_df.xlsx", index=False)

            merged_df_ar = pd.merge(result_df, df3, on=['Customer Number'], how="outer")
            condition = ~(merged_df_ar['Order Number'].isin(['IN', 'CR']))
            merged_df_ar.rename(columns={'Invoice Number_x': 'Invoice Number', 'Order Number' : 'Customer Name'}, inplace=True)
            merged_df_ar.drop(columns=['Invoice Number_y', 'Customer Name'], inplace=True)
            # f= time.time()
            # print('time taken by df3: ', format(f-e))
            # merged_df_ar.to_excel("merged_df_ar.xlsx", index=False)
        

        # if df4 is not None:
        #     a = time.time()
        #     df4.rename(columns={'Credits' : 'Revenue'}, inplace=True)
        #     pattern = r'\b[A-Z]{2}\s*-\s*[A-Z]{2}\b'
        #     df4['Source'] = df4['Source'].astype(str).str.replace(pattern, '', regex=True)
        #     df4[['Revenue Text', 'Category']] = df4['Source'].str.split(' - ', expand=True)
        #     mask = (df4['Revenue'] == 0)
        #     df4.loc[mask, 'Revenue'] = -df4.loc[mask, 'Debits']
        #     df4.loc[mask, 'Debits'] = 0
        #     df4.drop(columns=['Debits', 'Source'], inplace=True)

        #     df4 = df4[~df4.apply(lambda row: row.astype(str).str.match(r'Totals|Ending Balance').any(), axis=1)]

        #     current_category = None

        #     for index, row in df4.iterrows():
        #         if pd.notna(row['Category']) and row['Category'] != 'nan':
        #             current_category = row['Category']

        #         df4.loc[index, 'Category'] = current_category

        #     df4 = df4[~((df4['Revenue Text'] == 'Revenue') | (df4['Revenue Text'] == 'nan'))]
        #     df4.drop(columns=['Revenue Text', 'Account Number/Year/ Prd.'], inplace=True)
        #     df4.rename(columns={'Reference' : 'Invoice Number'}, inplace=True)
           
            
            

        #     df4 = df4.sort_values(by='Invoice Number', na_position='last')

        #     def convert_to_int(x):
        #         if isinstance(x, str) and x.isdigit():
        #             return int(x)
        #         return x
            
        #     df4['Invoice Number'] = df4['Invoice Number'].apply(convert_to_int)

        #     b = time.time()
        #     print('Time taken by df4: ', format(b-a))
            
        #     # df4.to_excel("df4.xlsx", index=False)
        
            
        if df4 is not None:
            # a = time.time()
            
            df4.rename(columns={'Credits': 'Revenue', 'Reference': 'Invoice Number'}, inplace=True)
            df4['Source'] = df4['Source'].str.replace(r'\b[A-Z]{2}\s*-\s*[A-Z]{2}\b', '', regex=True)
            
            
            df4[['Revenue Text', 'Category']] = df4['Source'].str.split(' - ', n=1, expand=True)
            
            mask = (df4['Revenue'] == 0)
            df4.loc[mask, 'Revenue'] = -df4.loc[mask, 'Debits']
            df4.loc[mask, 'Debits'] = 0
            
            

            df4.drop(columns=['Debits', 'Source', 'Account Number/Year/ Prd.'], inplace=True)
            
            df4 = df4[~df4.astype(str).apply(lambda row: row.str.contains(r'Totals|Ending Balance')).any(axis=1)]
            
            df4['Category'].ffill(inplace=True)
            
            df4 = df4[~df4['Revenue Text'].isin(['Revenue', 'nan'])]
            
            df4.sort_values(by='Invoice Number', na_position='last', inplace=True)
            
            # b = time.time()
            # print('Time taken by df4:', format(b - a))
            
        
        if df3 is not None and df4 is not None and df5 is not None:
            merged_df_final = pd.merge(merged_df_ar, df4, on=['Invoice Number'], how="outer")
            merged_df_final['Customer Number'] = merged_df_final['Customer Number'].fillna(999).astype(int)
            merged_df_final['Invoice Number'].fillna("INV999999999", inplace=True)
            merged_df_final = merged_df_final[~((merged_df_final['Invoice Number'] == 'INV999999999') & merged_df_final.duplicated(subset=['Revenue', 'Invoice Number', 'Description', 'Category', 'Doc. Date'], keep='first'))]
            # merged_df_final.to_excel("merged_df_final.xlsx", index=False)
            merged_df_final = pd.merge(merged_df_final, df5, on=['Customer Number', 'Category'], how="outer")
            merged_df_final = merged_df_final[merged_df_final['Doc. Date'].notna()]
            merged_df_final['Location'].fillna("Combined", inplace=True)
            merged_df_final['Customer Name'].fillna("Other", inplace=True)
            merged_df_final['Site Name'].fillna("Other", inplace=True)
            merged_df_final.drop(columns=['Revenue Text'], inplace=True)

            if st.sidebar.button('Export Other Revenue Merged Database'):
                with st.spinner('Exporting Other Revenue Merged Database....'):
                    save_merged2 = os.path.abspath("Merged Databases/Other_Revenue_Merged_Databases")
                    filename2 = "Merged Database " + os.path.basename(file_path2) + os.path.basename(file_path3)
                    save_path2 = os.path.join(save_merged2, filename2)
                    merged_df_final.to_excel(f"{save_path2}.xlsx", index=False, engine="openpyxl")
                succ2 = st.success(f'Other Revenue Merged Database exported to {save_path2} folder')
                time.sleep(5)
                succ2.empty()

    #-------Upload files 3 and 4 which are AR invoices file and Other revenue file--------  


    if df3 is not None and df4 is not None and df5 is not None:
        
        st.sidebar.header('Please Filter Here:')

        non_empty_hours_mask2 = merged_df_final['Revenue'].notna()

        if non_empty_hours_mask2.any():

            location_ar = merged_df_final.loc[non_empty_hours_mask2, "Location"].unique()
            select_all_option = "Select All"

            if select_all_option not in location_ar:
                location_options = [select_all_option] + list(location_ar)

            location_ar = st.sidebar.multiselect("Select the Location:", options=location_options)

            if select_all_option in location_ar:
                location_ar = list(merged_df_final.loc[non_empty_hours_mask2, "Location"].unique())

            location_ar_str = [str(item) for item in location_ar]

        # ------Location Sidebar------
        
        
        filtered_by_location_ar = merged_df_final[merged_df_final['Location'].isin(location_ar)]
        filtered_by_location2_ar = filtered_by_location_ar.groupby(['Customer Name', 'Location']).agg({'Revenue': 'sum'}).reset_index()
        sorted_by_location_ar = filtered_by_location2_ar.sort_values('Revenue', ascending=False).round(2)
        sorted_by_location2_ar = sorted_by_location_ar.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: #00172B; color: white' for i in range(len(x))], axis=0).format({'Revenue' : "{:,}"})
    

        if filtered_by_location_ar.shape[0] > 0:     #check whether the df is empty or not
                    
            #---------Category Sidebar--------

            non_empty_cat_mask2 = merged_df_final['Revenue'].notna()

            if non_empty_cat_mask2.any():
                
                category_ar = merged_df_final.loc[non_empty_cat_mask2, "Category"].unique()
                select_all_option = "Select All"

                if select_all_option not in category_ar:
                    category_options = [select_all_option] + list(category_ar)

                category_ar = st.sidebar.multiselect("Select the Category:", options=category_options)

                if select_all_option in category_ar:
                    category_ar = list(merged_df_final.loc[non_empty_cat_mask2, "Category"].unique())
                    
            #---------Category Sidebar--------
            
            #-------Filtering the category----------
                            
            filtered_by_category_ar = filtered_by_location_ar[filtered_by_location_ar['Category'].isin(category_ar)]
            filtered_by_category2_ar = filtered_by_category_ar.groupby(['Customer Name', 'Location', 'Category']).agg({'Revenue': 'sum'}).reset_index()
            sorted_by_category_ar = filtered_by_category2_ar.sort_values('Revenue', ascending=False).round(2)
            sorted_by_category2_ar = sorted_by_category_ar.style.apply(lambda x: ['background-color: #003A63; color: white;' if i < 10 else 'background-color: #00172B; color: white' for i in range(len(x))], axis=0).format({'Revenue' : "{:,}"})
            
            #-------Filtering the category----------
            
            
            #--------Totalling the Hours and Revenue--------

            total_revenue_location_ar = int(round(filtered_by_location_ar['Revenue'].sum()))
            total_revenue_category_ar = int(round(filtered_by_category_ar['Revenue'].sum()))

            #--------Totalling the Hours and Revenue--------

            #-------Creating 2 columns and showing data-------
            

            st.subheader("Total Revenue (By Location)")
            st.subheader(f"[{', '.join(location_ar_str)}]")
            st.subheader(f"${total_revenue_location_ar:,}")
            st.markdown("##")
            st.markdown("##")
            st.subheader("Total Revenue (By Category)")
            st.subheader(f"[{', '.join(category_ar)}]")
            st.subheader(f"${total_revenue_category_ar:,}")
            st.markdown("##")
            st.markdown("##")

            left_column2,middle_column2 = st.columns(2)

            #--------Creating filter (drop-down) for Revenue by Location and also inserting a row with Total Hours and Revenue based on the filter---------
            with left_column2:
                st.subheader("Revenue By Location")
                filter_value2 = st.multiselect("Filter by Customer Name (Location)", sorted_by_location_ar['Customer Name'].unique(), key=hash("multiselect_4"))
                if filter_value2:
                    filtered_df = sorted_by_location_ar[sorted_by_location_ar['Customer Name'].isin(filter_value2)]
                    total_revenue = filtered_df['Revenue'].sum()
                    total_row = pd.DataFrame({'Customer Name' : ['TOTAL'], 'Revenue' : [total_revenue], 'Location' : ''})
                    filtered_df = pd.concat([filtered_df, total_row], ignore_index=True)
                    filtered_df['Revenue'] = filtered_df['Revenue'].round(2).astype(float)
                    def highlight_last_row(s):
                        if s.name == len(filtered_df) - 1:
                            return ['background-color: #F26222; color: black' for i in s]
                        else:
                            return ['' for i in s]
                    filtered_df2 = filtered_df.style.apply(highlight_last_row, axis=1).format({'Revenue' : "{:,}"})
                    st.dataframe(filtered_df2, hide_index=True, use_container_width=True, height=500)
                    st.markdown(f"Total Revenue: ${int(round(total_revenue)):,}")
                else:
                    st.dataframe(sorted_by_location2_ar, hide_index=True, use_container_width=True, height=500)
                    st.markdown(f"Total Revenue: ${int(round(filtered_by_location_ar['Revenue'].sum())):,}")                        


                #-----------Creating download button for Revenue by Location-----------
                    
                def download_link3(filtered_df, filename, txt):
                    towrite = BytesIO()
                    filtered_df = filtered_df.copy()     
                    filtered_df = filtered_df.style.map(add_borders)
                    filtered_df.to_excel(towrite, index=False, header=True)
                    towrite.seek(0)  
                    b64 = base64.b64encode(towrite.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                    return href                    
                

                def download_link4(sorted_by_location_ar, filename, txt):
                    towrite = BytesIO()
                    sorted_by_location_ar = sorted_by_location_ar.copy()         
                    sorted_by_location_ar = sorted_by_location_ar.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: white; color: black' for i in range(len(x))], axis=0).format({'Revenue' : "{:,}"})
                    sorted_by_location_ar.to_excel(towrite, index=False, header=True)
                    towrite.seek(0) 
                    b64 = base64.b64encode(towrite.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                    return href
                
                if filter_value2:
                    if st.button('Create Revenue By Location as XLSX'):
                        tmp_download_link = download_link3(filtered_df, f'Loc - {location_ar}.xlsx', txt="Click here to download")
                        st.markdown(tmp_download_link, unsafe_allow_html=True)
                else:
                    if st.button('Create Revenue By Location as XLSX'):
                        tmp_download_link = download_link4(sorted_by_location_ar, f'Loc - {location_ar}.xlsx', txt="Click here to download")
                        st.markdown(tmp_download_link, unsafe_allow_html=True)

                #-----------Creating download button for Revenue by Location-----------
                        
            #--------Creating filter (drop-down) for Revenue by Location and also inserting a row with Total Hours and Revenue based on the filter---------
                        
            
            #--------Creating filter (drop-down) for Revenue by Location & Category and also inserting a row with Total Hours and Revenue based on the filter---------
            with middle_column2:
                st.subheader("Revenue By Location & Category")
                filter_value3 = st.multiselect("Filter by Customer Name (Location & Category)", sorted_by_category_ar['Customer Name'].unique(), key=hash("multiselect_5"))
                if filter_value3:
                    filtered_df = sorted_by_category_ar[sorted_by_category_ar['Customer Name'].isin(filter_value3)]
                    total_revenue = filtered_df['Revenue'].sum()
                    total_row = pd.DataFrame({'Customer Name' : ['TOTAL'], 'Revenue' : [total_revenue], 'Location' : '', 'Category' : ''})
                    filtered_df = pd.concat([filtered_df, total_row], ignore_index=True)
                    filtered_df['Revenue'] = filtered_df['Revenue'].round(2).astype(float)
                    def highlight_last_row(s):
                        if s.name == len(filtered_df) - 1:
                            return ['background-color: #F26222; color: black' for i in s]
                        else:
                            return ['' for i in s]
                    filtered_df2 = filtered_df.style.apply(highlight_last_row, axis=1).format({'Revenue' : "{:,}"})
                    st.dataframe(filtered_df2, hide_index=True, use_container_width=True, height=500)
                    st.markdown(f"Total Revenue: ${int(round(total_revenue)):,}")
                else:
                    st.dataframe(sorted_by_category2_ar, hide_index=True, use_container_width=True, height=500)
                    st.markdown(f"Total Revenue: ${int(round(filtered_by_category_ar['Revenue'].sum())):,}")

                #--------Creating filter (drop-down) for Revenue by Location & Category and also inserting a row with Total Hours and Revenue based on the filter---------


                #-----------Creating download button for Revenue by Location & Category-----------
                    
                def download_link5(filtered_df, filename, txt):
                    towrite = BytesIO()
                    filtered_df = filtered_df.copy()   
                    filtered_df = filtered_df.style.map(add_borders)    
                    filtered_df.to_excel(towrite, index=False, header=True)
                    towrite.seek(0)
                    b64 = base64.b64encode(towrite.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                    return href
                
                def download_link6(sorted_by_category_ar, filename, txt):
                    towrite = BytesIO()
                    sorted_by_category_ar = sorted_by_category_ar.copy()   
                    sorted_by_category_ar['Revenue'] = sorted_by_category_ar['Revenue'].apply(lambda x: "{:,}".format(x) if isinstance(x, int) else x)    
                    sorted_by_category3_ar = sorted_by_category_ar.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: white; color: black' for i in range(len(x))], axis=0).format({'Revenue' : "{:,}"})
                    sorted_by_category3_ar.to_excel(towrite, index=False, header=True)
                    towrite.seek(0)
                    b64 = base64.b64encode(towrite.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                    return href
                
                if filter_value3:
                    if st.button('Create Revenue By Location & Category as XLSX'):
                        tmp_download_link = download_link5(filtered_df, f'L&C{location_ar}-{category_ar}.xlsx', txt="Click here to download")
                        st.markdown(tmp_download_link, unsafe_allow_html=True)
                else:
                    if st.button('Create Revenue By Location & Category as XLSX'):
                        tmp_download_link = download_link6(sorted_by_category_ar, f'L&C{location_ar}-{category_ar}.xlsx', txt="Click here to download")
                        st.markdown(tmp_download_link, unsafe_allow_html=True)

                #-----------Creating download button for Revenue by Location & Category-----------
                        
                #--------Creating filter (drop-down) for Revenue by Location & Category---------
                        
            #-------Creating 2 columns and showing data-------            
            

            # ------Show the site name only when category is selected---------
                        
            if filtered_by_category_ar.shape[0] > 0:
                site_name_ar = filtered_by_category_ar["Site Name"].unique()


                # ---------Check for locations, add their hours and revenue, round them, make them in descending order, and showing top 10 customers---------- 
                
                filtered_by_site_name_ar = filtered_by_category_ar[filtered_by_category_ar['Site Name'].isin(site_name_ar)]
                filtered_by_site_name2_ar = filtered_by_site_name_ar.groupby(['Site Name', 'Location', 'Category']).agg({'Revenue': 'sum', 'Customer Name' : 'first', 'Customer Number' : 'first'}).reset_index()[['Customer Number', 'Customer Name', 'Site Name', 'Location', 'Category', 'Revenue']]
                sorted_by_site_name_ar = filtered_by_site_name2_ar.sort_values('Revenue', ascending=False).round(2)
                sorted_by_site_name2_ar = sorted_by_site_name_ar.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: #00172B; color: white' for i in range(len(x))], axis=0).format({'Revenue' : "{:,}"})
                st.markdown("##")
                st.markdown("##")
                
                # ---------Check for locations, add their hours and revenue, round them, make them in descending order, and showing top 10 customers----------


                #-------Creating filter (drop-down) for Revenue by Site Name and also inserting a row with Total Hours and Revenue based on the filter---------

                st.subheader("Revenue By Site Name")
                filter_value4 = st.multiselect("Filter by Customer Name (Location)", sorted_by_site_name_ar['Customer Name'].unique(), key=hash("multiselect_6"))
                if filter_value4:
                    filtered_df = sorted_by_site_name_ar[sorted_by_site_name_ar['Customer Name'].isin(filter_value4)]
                    total_revenue = filtered_df['Revenue'].sum()
                    filtered_df.loc[:, 'Customer Number'] = filtered_df['Customer Number'].astype(str)
                    total_row = pd.DataFrame({'Site Name' : ['TOTAL'], 'Revenue' : [total_revenue], 'Location' : '', 'Category' : '', 'Customer Name' : '', 'Customer Number' : ''})
                    filtered_df = pd.concat([filtered_df, total_row], ignore_index=True)
                    filtered_df['Revenue'] = filtered_df['Revenue'].round(2).astype(float)
                    
                    
                    def highlight_last_row(s):
                        if s.name == len(filtered_df) - 1:
                            return ['background-color: #F26222; color: black' for i in s]
                        else:
                            return ['' for i in s]
                    filtered_df2 = filtered_df.style.apply(highlight_last_row, axis=1).format({'Revenue' : "{:,}"})
                    st.dataframe(filtered_df2, hide_index=True, use_container_width=True, height=500)
                    st.markdown(f"Total Revenue: ${int(round(total_revenue)):,}")
                else:
                    st.dataframe(sorted_by_site_name2_ar, hide_index=True, use_container_width=True, height=500)
                    st.markdown(f"Total Revenue: ${int(round(sorted_by_site_name_ar['Revenue'].sum())):,}")
                
                #-------Creating filter (drop-down) for Revenue by Site Name and also inserting a row with Total Hours and Revenue based on the filter---------


                #-----------Creating download button for Revenue by Site Name-----------
                    
                def download_link7(filtered_df, filename, txt):
                    towrite = BytesIO()
                    filtered_df = filtered_df.copy()   
                    filtered_df = filtered_df.style.map(add_borders) 
                    filtered_df.to_excel(towrite, index=False, header=True)
                    towrite.seek(0)
                    b64 = base64.b64encode(towrite.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                    return href
                
                def download_link8(sorted_by_site_name_ar, filename, txt):
                    towrite = BytesIO()
                    sorted_by_site_name_ar = sorted_by_site_name_ar.copy()  
                    sorted_by_site_name_ar = sorted_by_site_name_ar.style.apply(lambda x: ['background-color: #003A63; color: white' if i < 10 else 'background-color: white; color: black' for i in range(len(x))], axis=0).map(add_borders)
                    sorted_by_site_name_ar.to_excel(towrite, index=False, header=True)
                    towrite.seek(0)
                    b64 = base64.b64encode(towrite.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> {txt}'
                    return href
                
                if filter_value4:
                    if st.button('Create Revenue By Site Name as XLSX'):
                        tmp_download_link = download_link7(filtered_df, f'Loc - {location_ar}.xlsx', txt="Click here to download")
                        st.markdown(tmp_download_link, unsafe_allow_html=True)
                else:
                    if st.button('Create Revenue By Site Name as XLSX'):
                        tmp_download_link = download_link8(sorted_by_site_name_ar, f'Loc - {location_ar}.xlsx', txt="Click here to download")
                        st.markdown(tmp_download_link, unsafe_allow_html=True)

                #-----------Creating download button for Revenue by Site Name-----------
                        
            #--------Creating filter (drop-down) for Revenue by Site Name---------
                        
            # ------Show the site name only when category is selected---------

            #-------PygWalker(Data Visualization - Tables, Graphs, etc.)--------
                                    
                st.markdown("##")
                st.markdown("##")
                
                st.subheader("Revenue & Sales Data Visualisation (Other Revenue)")
                         
                # pyg_html2 = pyg.walk(sorted_by_site_name_ar, return_html=True, dark="dark", env="Streamlit")
                # components.html(pyg_html2, height=900, scrolling=False)
            
            # -------PygWalker(Data Visualization - Tables, Graphs, etc.)--------
        
