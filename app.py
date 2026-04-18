import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Page config
st.set_page_config(page_title="Interactive Dashboard", layout="wide")

# Title and description
st.title("📊 Interactive Dashboard - Module 6")
st.write("This dashboard demonstrates interactive data visualization using Streamlit.")

# Generate sample data
np.random.seed(42)
data = pd.DataFrame({
    "Category": np.random.choice(["A", "B", "C"], size=100),
    "Value1": np.random.randn(100) * 10,
    "Value2": np.random.randn(100) * 5,
    "Date": pd.date_range("2024-01-01", periods=100, freq="D")
})

# Sidebar filters
st.sidebar.header("Filters")

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=data["Category"].unique(),
    default=data["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [data["Date"].min(), data["Date"].max()]
)

# Validate date range
if len(date_range) != 2:
    st.error("Please select a valid date range.")
    st.stop()

# Apply filters
filtered_data = data[
    (data["Category"].isin(selected_category)) &
    (data["Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# Handle empty dataset
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ======================
# KPI Section
# ======================
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Average Value1", f"{filtered_data['Value1'].mean():.2f}")
col2.metric("Average Value2", f"{filtered_data['Value2'].mean():.2f}")
col3.metric("Total Records", len(filtered_data))

# ======================
# Data Table
# ======================
st.subheader("📋 Filtered Data")
st.dataframe(filtered_data, use_container_width=True)

# Download button
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ======================
# Line Chart (Altair)
# ======================
st.subheader("📈 Trends Over Time")

line_chart = alt.Chart(filtered_data).mark_line(point=True).encode(
    x=alt.X("Date:T", title="Date"),
    y=alt.Y("Value1:Q", title="Value1"),
    color=alt.Color("Category:N", title="Category"),
    tooltip=[
        alt.Tooltip("Date:T"),
        alt.Tooltip("Category:N"),
        alt.Tooltip("Value1:Q"),
        alt.Tooltip("Value2:Q")
    ]
).properties(height=400)

st.altair_chart(line_chart, use_container_width=True)

# ======================
# Bar Chart (FIXED)
# ======================
st.subheader("📊 Average Values by Category")

grouped = filtered_data.groupby("Category")[["Value1", "Value2"]].mean().reset_index()

bar_chart = alt.Chart(grouped).transform_fold(
    ["Value1", "Value2"],
    as_=["Metric", "Value"]
).mark_bar().encode(
    x=alt.X("Category:N", title="Category"),
    y=alt.Y("Value:Q", title="Average Value"),
    color=alt.Color("Metric:N", title="Metric"),
    tooltip=[
        alt.Tooltip("Category:N"),
        alt.Tooltip("Metric:N"),
        alt.Tooltip("Value:Q")
    ]
).properties(height=400)

st.altair_chart(bar_chart, use_container_width=True)

# ======================
# Summary Statistics
# ======================
st.subheader("📑 Summary Statistics")
st.write(filtered_data.describe())