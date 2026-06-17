import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Universal Data Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal Data Analyzer")

uploaded_file = st.file_uploader(
    "Upload a CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.success("Dataset Loaded Successfully!")

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Basic Information
    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Column Information
    st.subheader("Column Details")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(info_df, use_container_width=True)

    # Statistics
    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include="all"))

    # Missing Values
    st.subheader("Missing Values Analysis")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_df)

    # Column Selection
    st.subheader("Visualization")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if len(numeric_cols) > 0:

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Histogram", "Box Plot", "Line Chart", "Scatter Plot"]
        )

        if chart_type == "Histogram":

            col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=20)
            ax.set_title(f"Histogram of {col}")
            st.pyplot(fig)

        elif chart_type == "Box Plot":

            col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig, ax = plt.subplots()
            ax.boxplot(df[col].dropna())
            ax.set_title(f"Box Plot of {col}")
            st.pyplot(fig)

        elif chart_type == "Line Chart":

            col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            st.line_chart(df[col])

        elif chart_type == "Scatter Plot":

            x_col = st.selectbox("X Axis", numeric_cols)

            y_col = st.selectbox(
                "Y Axis",
                [c for c in numeric_cols if c != x_col]
            )

            fig, ax = plt.subplots()
            ax.scatter(df[x_col], df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{x_col} vs {y_col}")
            st.pyplot(fig)

    # Correlation Matrix
    if len(numeric_cols) > 1:

        st.subheader("Correlation Matrix")

        corr = df[numeric_cols].corr()

        st.dataframe(corr)

        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(corr)

        ax.set_xticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=90)

        ax.set_yticks(range(len(corr.columns)))
        ax.set_yticklabels(corr.columns)

        plt.colorbar(im)

        st.pyplot(fig)

    # Dataset Download
    st.subheader("Download Cleaned Dataset")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        file_name="processed_dataset.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a CSV file to start analysis.")