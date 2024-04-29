import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit.components.v1 as components
import json


# Function to preprocess data
def preprocess_data(df):
    # Fill missing values and remove duplicates
    df.fillna(method='ffill', inplace=True)
    df.drop_duplicates(inplace=True)
    return df

def load_data(data_file):
    if data_file is not None:
        return pd.read_csv(data_file)
    return None

# Function to create plots
def create_plot(df, plot_type, x_axis, y_axis=None):
    if plot_type == 'Bar Chart':
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif plot_type == 'Line Chart':
        fig = px.line(df, x=x_axis, y=y_axis)
    elif plot_type == 'Scatter Plot':
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif plot_type == 'Histogram':
        fig = px.histogram(df, x=x_axis)
    elif plot_type == 'Box Plot':
        fig = px.box(df, x=x_axis, y=y_axis)
    elif plot_type == 'Pie Chart':
        fig = px.pie(df, names=x_axis, values=y_axis)
    elif plot_type == 'Area Chart':
        fig = px.area(df, x=x_axis, y=y_axis)
    return fig

# Inject custom Bootstrap-like CSS
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

#st.markdown("<div style='text-align: center; margin-bottom: 20px;'>Developed by Kumaran R</div>", unsafe_allow_html=True)

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
