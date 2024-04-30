import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pygwalk

# Function to preprocess data
def preprocess_data(df):
    # Fill missing values and remove duplicates
    df.fillna(method='ffill', inplace=True)
    df.drop_duplicates(inplace=True)
    return df

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

# Sidebar
st.sidebar.title("Data Analytics Playground")

# Upload file
uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.type == 'text/csv':
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = st.sidebar.selectbox("Select sheet for analysis", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name, engine='openpyxl')
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.stop()

    # Data preprocessing
    df = preprocess_data(df)

    # Data transformation
    if st.sidebar.checkbox("Perform Data Transformation"):
        st.subheader("Data Transformation")
        transform_type = st.selectbox("Select Transformation", ["Filtering", "Sorting", "Grouping"])
        if transform_type == "Filtering":
            filter_column = st.selectbox('Select Column for Filtering', df.columns)
            filter_value = st.text_input('Enter Filter Value')
            df = df[df[filter_column] == filter_value]
        elif transform_type == "Sorting":
            sort_column = st.selectbox('Select Column for Sorting', df.columns)
            df = df.sort_values(by=[sort_column])
        elif transform_type == "Grouping":
            group_column = st.selectbox('Select Column for Grouping', df.columns)
            df = df.groupby(group_column).size().reset_index(name='Count')

    # Statistical analysis
    if st.sidebar.checkbox("Perform Statistical Analysis"):
        st.subheader("Statistical Analysis")
        st.write(df.describe())

    # Data Visualization
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

    # Additional analytics
    st.sidebar.subheader("Additional Analytics")
    if st.sidebar.checkbox("Correlation Matrix"):
        corr = df.corr()
        fig = px.imshow(corr)
        st.plotly_chart(fig, use_container_width=True)

    if st.sidebar.checkbox("Pairplot"):
        fig = px.scatter_matrix(df)
        st.plotly_chart(fig, use_container_width=True)

    if st.sidebar.checkbox("Word Cloud"):
        text = ' '.join(df[df.columns[0]].dropna())
        wordcloud = WordCloud(width=800, height=400).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    if st.sidebar.checkbox("Value Counts"):
        value_counts_column = st.selectbox('Select Column for Value Counts', df.columns)
        st.write(df[value_counts_column].value_counts())

    if st.sidebar.checkbox("Distribution Plot"):
        dist_column = st.selectbox('Select Column for Distribution Plot', df.columns)
        sns.histplot(df[dist_column], kde=True)
        st.pyplot()

    if st.sidebar.checkbox("Boxplot"):
        boxplot_column = st.selectbox('Select Column for Boxplot', df.columns)
        sns.boxplot(y=boxplot_column, data=df)
        st.pyplot()

    # Pygwalk interactive dataframe
    if st.sidebar.checkbox("Pygwalk Interactive DataFrame"):
        walker = pygwalk.PygWalk(df)
        st.subheader("Interactive DataFrame with Pygwalk")
        current_row = walker.run()
        st.write(current_row)

