import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import f_oneway, ttest_ind, zscore, chi2_contingency

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

# Main function
def main():
    st.title("Comprehensive Data Analysis and Visualization Tool")

    # Upload file
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = preprocess_data(df)

        st.sidebar.subheader("Data Exploration")
        # Existing code for data exploration...

        st.sidebar.subheader("Statistical Analysis")
        stat_choice = st.sidebar.selectbox("Select Statistical Analysis", ["Mean", "Median", "Standard Deviation", "ANOVA", "T-Test", "Z-Test", "Chi-Square Test"])
        if stat_choice == "Mean":
            st.write("Mean Values")
            st.write(df.mean())
        elif stat_choice == "Median":
            st.write("Median Values")
            st.write(df.median())
        elif stat_choice == "Standard Deviation":
            st.write("Standard Deviation Values")
            st.write(df.std())
        elif stat_choice == "ANOVA":
            st.write("Performing ANOVA")
            anova_col = st.selectbox("Select column for ANOVA", df.columns)
            group_col = st.selectbox("Select grouping column for ANOVA", df.columns)
            anova_result = f_oneway(*[group[1][anova_col] for group in df.groupby(group_col)])
            st.write("ANOVA Result:")
            st.write(anova_result)
        elif stat_choice == "T-Test":
            st.write("Performing T-Test")
            ttest_col = st.selectbox("Select column for T-Test", df.columns)
            group_col = st.selectbox("Select grouping column for T-Test", df.columns)
            group1 = df[df[group_col] == df[group_col].unique()[0]][ttest_col]
            group2 = df[df[group_col] == df[group_col].unique()[1]][ttest_col]
            ttest_result = ttest_ind(group1, group2)
            st.write("T-Test Result:")
            st.write(ttest_result)
        elif stat_choice == "Z-Test":
            st.write("Performing Z-Test")
            ztest_col = st.selectbox("Select column for Z-Test", df.columns)
            ztest_result = zscore(df[ztest_col])
            st.write("Z-Test Result:")
            st.write(ztest_result)
        elif stat_choice == "Chi-Square Test":
            st.write("Performing Chi-Square Test")
            # Provide a contingency table for Chi-Square test
            # Example:
            # chi_square_table = pd.crosstab(df['column1'], df['column2'])
            # chi2, p, dof, expected = chi2_contingency(chi_square_table)
            # st.write("Chi-Square Test Result:")
            # st.write(f"Chi2: {chi2}, p: {p}, dof: {dof}, expected: {expected}")

        # Univariate Analysis
        st.sidebar.subheader("Univariate Analysis")
        column = st.sidebar.selectbox("Select a column", df.columns)
        if st.sidebar.button("Generate Univariate Analysis"):
            st.subheader(f"Univariate Analysis of {column}")
            st.write("Value Counts:")
            st.write(df[column].value_counts())
            st.write("Summary Statistics:")
            st.write(df[column].describe())
            st.write("Histogram:")
            fig = px.histogram(df, x=column)
            st.plotly_chart(fig)

        # Bivariate Analysis
        st.sidebar.subheader("Bivariate Analysis")
        column1 = st.sidebar.selectbox("Select first column", df.columns)
        column2 = st.sidebar.selectbox("Select second column", df.columns)
        if st.sidebar.button("Generate Bivariate Analysis"):
            st.subheader(f"Bivariate Analysis of {column1} and {column2}")
            st.write("Scatter Plot:")
            fig = px.scatter(df, x=column1, y=column2)
            st.plotly_chart(fig)

        # Multivariate Analysis
        st.sidebar.subheader("Multivariate Analysis")
        columns = st.sidebar.multiselect("Select columns", df.columns)
        if st.sidebar.button("Generate Multivariate Analysis"):
            st.subheader("Multivariate Analysis")
            st.write("Pairplot:")
            fig = px.scatter_matrix(df[columns])
            st.plotly_chart(fig)

        # Data Filtering
        st.sidebar.subheader("Data Filtering")
        filter_col = st.sidebar.selectbox("Filter data by column", df.columns)
        filter_val = st.sidebar.text_input(f"Filter {filter_col} by value")
        if st.sidebar.button("Apply Filter"):
            filtered_df = df[df[filter_col] == filter_val]
            st.subheader("Filtered Data")
            st.write(filtered_df)

        # Data Sorting
        st.sidebar.subheader("Data Sorting")
        sort_col = st.sidebar.selectbox("Sort data by column", df.columns)
        sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
        if st.sidebar.button("Apply Sort"):
            if sort_order == "Ascending":
                sorted_df = df.sort_values(by=sort_col, ascending=True)
            else:
                sorted_df = df.sort_values(by=sort_col, ascending=False)
            st.subheader("Sorted Data")
            st.write(sorted_df)

        # Data Visualization
        st.sidebar.subheader("Data Visualization")
        plot_types = ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Histogram', 'Box Plot', 'Pie Chart', 'Area Chart']
        plot_choice = st.sidebar.selectbox("Choose plot type", plot_types)
        x_axis = st.selectbox('Select X-axis', df.columns)
        y_axis = None
        if plot_choice not in ['Histogram', 'Pie Chart', 'Heatmap']:
            y_axis = st.selectbox('Select Y-axis', df.columns)
        if st.sidebar.button('Generate Plot'):
            fig = create_plot(df, plot_choice, x_axis, y_axis)
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
