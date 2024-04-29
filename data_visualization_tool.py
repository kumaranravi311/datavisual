#=======================================================================
## 0.1 Importing libraries, data

#Import the necessary packages
import streamlit as st
import openpyxl
import pygwalker as pyg
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import sys

#Setting the web app page name
st.set_page_config(page_title='Exploratory Data Analysis App', page_icon=None, layout="wide")

#Injecting custom CSS for assigning theme to app
custom_css = """
body {
  background-color: #FFFFFF;
}

h1, h2, h3, h4, h5, h6 {
  color: #FF4B4B;
}
"""
st.write('<style>' + custom_css + '</style>', unsafe_allow_html=True)

#Setting markdown
st.markdown("<h1 style='text-align: center;'>Exploratory Data Analysis App</h1>", unsafe_allow_html=True)

st.sidebar.write("****A) File upload****")

#User prompt to select file type
ft = st.sidebar.selectbox("*What is the file type?*",["Excel", "csv"])

#Creating dynamic file upload option in sidebar
uploaded_file = st.sidebar.file_uploader("*Upload file here*")

if uploaded_file is not None:
    file_path = uploaded_file

    if ft == 'Excel':
        try:
            #User prompt to select sheet name in uploaded Excel
            sh = st.sidebar.selectbox("*Which sheet name in the file should be read?*",pd.ExcelFile(file_path).sheet_names)
            #User prompt to define row with column names if they aren't in the header row in the uploaded Excel
            h = st.sidebar.number_input("*Which row contains the column names?*",0,100)
        except:
            st.info("File is not recognised as an Excel file")
            sys.exit()
    
    elif ft == 'csv':
        try:
            #No need for sh and h for csv, set them to None
            sh = None
            h = None
        except:
            st.info("File is not recognised as a csv file.")
            sys.exit()

    #Caching function to load data
    @st.cache_data(experimental_allow_widgets=True)
    def load_data(file_path,ft,sh,h):
        
        if ft == 'Excel':
            try:
                #Reading the excel file
                data = pd.read_excel(file_path,header=h,sheet_name=sh,engine='openpyxl')
            except:
                st.info("File is not recognised as an Excel file.")
                sys.exit()
    
        elif ft == 'csv':
            try:
                #Reading the csv file
                data = pd.read_csv(file_path)
            except:
                st.info("File is not recognised as a csv file.")
                sys.exit()
        
        return data

    data = load_data(file_path,ft,sh,h)
#=======================================================================
## 0.2 Pre-processing datasets

    #Replacing underscores in column names with spaces
    data.columns = data.columns.str.replace('_',' ') 

    data = data.reset_index()

    #Converting column names to title case
    data.columns = data.columns.str.title()

    #Horizontal divider
    st.sidebar.divider()
#=====================================================================================================
## 1. Overview of the data
    st.write( '### 1. Dataset Preview ')

    try:
      #View the dataframe in streamlit
      st.dataframe(data, use_container_width=True,hide_index=True)

    except:
      st.info("The file wasn't read properly. Please ensure that the input parameters are correctly defined.")
      sys.exit()

    #Horizontal divider
    st.divider()
#=====================================================================================================
## 2. Understanding the data
    st.write( '### 2. High-Level Overview ')

    #Creating radio button and sidebar simulataneously
    selected = st.sidebar.radio( "**B) What would you like to know about the data?**", 
                                ["Data Dimensions",
                                 "Field Descriptions",
                                "Summary Statistics", 
                                "Value Counts of Fields"])

    #Showing field types
    if selected == 'Field Descriptions':
        fd = data.dtypes.reset_index().rename(columns={'index':'Field Name',0:'Field Type'}).sort_values(by='Field Type',ascending=False).reset_index(drop=True)
        st.dataframe(fd, use_container_width=True,hide_index=True)

    #Showing summary statistics
    elif selected == 'Summary Statistics':
        ss = pd.DataFrame(data.describe(include='all').round(2).fillna(''))
        #Adding null counts to summary statistics
        nc = pd.DataFrame(data.isnull().sum()).rename(columns={0: 'count_null'}).T
        ss = pd.concat([nc,ss]).copy()
        st.dataframe(ss, use_container_width=True)

    #Showing value counts of object fields
    elif selected == 'Value Counts of Fields':
        # creating radio button and sidebar simulataneously if this main selection is made
        sub_selected = st.sidebar.radio( "*Which field should be investigated?*",data.select_dtypes('object').columns)
        vc = data[sub_selected].value_counts().reset_index().rename(columns={'count':'Count'}).reset_index(drop=True)
        st.dataframe(vc, use_container_width=True,hide_index=True)

    #Showing the shape of the dataframe
    else:
        st.write('###### The data has the dimensions :',data.shape)

    #Horizontal divider
    st.divider()

    #Horizontal divider in sidebar
    st.sidebar.divider()
#=====================================================================================================
## 3. Visualisation

    #Selecting whether visualisation is required
    vis_select = st.sidebar.checkbox("**C) Is visualisation required for this dataset (hide sidebar for full view of dashboard) ?**")

    if vis_select:

        st.write( '### 3. Visual Insights ')

        #Creating a PyGWalker Dashboard
        walker = pyg.walk(data, return_html=True)
        st.components.v1.html(walker, width=1500, height=800)  # Adjust width and height as needed)

        #Inject custom Bootstrap-like CSS
        custom_css = """
        <style>
            /* Custom CSS for Streamlit app */
            .reportview-container .main .block-container{
                padding: 2rem;
            }
            .stButton>button {
                border: 1px solid #4CAF50;
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                cursor: pointer;
                width: 100%;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

        highlighted_title = "<div style='background-color: #007bff; color: white; padding: 10px; border-radius: 5px; text-align: center;'>" \
                            "Comprehensive Data Analysis and Visualization Tool" \
                            "</div>"
        st.markdown(highlighted_title, unsafe_allow_html=True)

        uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df = preprocess_data(df)

            st.sidebar.subheader("Data Exploration")
            if st.sidebar.checkbox("View Data Head"):
                st.info("This displays the first 5 rows of the dataset.")
                st.subheader("Data Head (First 5 Rows)")
                st.dataframe(df.head())
            if st.sidebar.checkbox("View Data Description"):
                st.info("This displays the statistical summary of the dataset.")
                st.subheader("Data Description (Statistical Summary)")
                st.dataframe(df.describe())
            if st.sidebar.checkbox("View Data Types"):
                st.info("This displays the data types of each column in the dataset.")
                st.subheader("Data Types")
                st.dataframe(df.dtypes.astype(str).to_frame('Data Type'))
            if st.sidebar.checkbox("View Missing Data"):
                st.info("This displays the missing values in the dataset.")
                st.subheader("Missing Data Report")
                missing_data = df.isnull().sum()
                st.dataframe(missing_data.to_frame('Missing Values'))
            if st.sidebar.checkbox("View Duplicate Data"):
                st.info("This displays the number of duplicate rows in the dataset.")
                st.subheader("Duplicate Data Report")
                duplicate_data = df.duplicated().sum()
                st.write(f"Duplicate Rows: {duplicate_data}")
            if st.sidebar.checkbox("View Dataset Shape"):
                st.info("This displays the shape (number of rows and columns) of the dataset.")
                st.subheader("Dataset Shape")
                st.write(df.shape)
            if st.sidebar.checkbox("View Dataset Info"):
                st.info("This displays information about the dataset, including data types and memory usage.")
                st.subheader("Dataset Info")
                st.write(df.info())
            if st.sidebar.checkbox("View Dataset Columns"):
                st.info("This displays the list of column names in the dataset.")
                st.subheader("Dataset Columns")
                st.write(df.columns.tolist())
            if st.sidebar.checkbox("View unique values"):
                st.info("This displays the number of unique values in each column of the dataset.")
                st.subheader("Check for Duplicate Values")
                st.write(df.nunique())
                # Data Filtering
            if st.sidebar.checkbox("Data Filtering"):
                filter_column = st.sidebar.selectbox('Select Filter Column', df.columns)
                filter_value = st.sidebar.text_input('Enter Filter Value')
                if st.sidebar.button('Apply Filter'):
                    filtered_df = df[df[filter_column] == filter_value]
                    st.subheader("Filtered Data")
                    st.write(filtered_df)


            st.sidebar.subheader("Data Visualization")
            plot_types = ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Histogram', 'Box Plot', 'Pie Chart', 'Area Chart']
            plot_choice = st.sidebar.selectbox("Choose plot type", plot_types)
            x_axis = st.selectbox('Select X-axis', df.columns)
            y_axis = None
            if plot_choice not in ['Histogram', 'Pie Chart', 'Heatmap']:
                y_axis = st.selectbox('Select Y-axis', df.columns)
            if st.button('Generate Plot'):
                fig = create_plot(df, plot_choice, x_axis, y_axis)
                st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please upload a file to proceed.")

#Horizontal divider
st.divider()
