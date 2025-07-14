import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture

# Set page config FIRST
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Load cleaned dataset

BASE_DIR = os.path.dirname(__file__)  # Folder where app.py is
DATA_PATH = os.path.join(BASE_DIR, "data1.xlsx")

@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH, parse_dates=["InvoiceDate"])

data1 = load_data()

# Calculate revenue
data1['Revenue'] = data1['Quantity'] * data1['UnitPrice']


# Sidebar filters
st.sidebar.title("🔍 Filters")
selected_country = st.sidebar.selectbox("Select Country", options=["All"] + sorted(data1['Country'].unique().tolist()))
min_date, max_date = data1['InvoiceDate'].min(), data1['InvoiceDate'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter data
if selected_country != "All":
    data1 = data1[data1['Country'] == selected_country]

data1 = data1[(data1['InvoiceDate'] >= pd.to_datetime(date_range[0])) & (data1['InvoiceDate'] <= pd.to_datetime(date_range[1]))]

# Title
st.title("📈 E-commerce Sales Dashboard")

# Metrics
total_revenue = data1['Revenue'].sum()
unique_customers = data1['CustomerID'].nunique()
num_orders = data1['InvoiceNo'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("👥 Unique Customers", unique_customers)
col3.metric("🧾 Total Orders", num_orders)

# 1. Raw Data
st.subheader("📄 Raw Dataset Preview")
st.dataframe(data1.head(100))

# 2. Top Products by Revenue
st.subheader("🔝 Top 10 Products by Revenue")
top_products = (
    data1.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig1 = px.bar(top_products, x='Revenue', y='Description', orientation='h', title='Top Products by Revenue')
st.plotly_chart(fig1, use_container_width=True)

# 3. Top Customers by Revenue
st.subheader("💰 Top 10 Customers by Revenue")
top_customers = (
    data1.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_customers["CustomerID"] = top_customers["CustomerID"].astype(str)

fig2 = px.bar(top_customers, x='Revenue', y='CustomerID', orientation='h', title='Top Customers by Revenue')

fig2.update_layout(yaxis=dict(title='CustomerID'), xaxis=dict(title='Revenue'))

st.plotly_chart(fig2, use_container_width=True)

# 4. Top Countries by Number of Transactions
st.subheader("🌍 Top Countries by Transactions")
top_countries = (
    data1.groupby("Country")["InvoiceNo"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig3 = px.bar(top_countries, x='Country', y='InvoiceNo', title='Top Countries by Number of Orders')
st.plotly_chart(fig3, use_container_width=True)

# 5. Monthly Revenue Trend
st.subheader("📅 Monthly Revenue Trend")
data1['YearMonth'] = data1['InvoiceDate'].dt.to_period("M").astype(str)
monthly_rev = data1.groupby("YearMonth")["Revenue"].sum().reset_index()
fig4 = px.line(monthly_rev, x="YearMonth", y="Revenue", markers=True, title='Monthly Revenue')
st.plotly_chart(fig4, use_container_width=True)

# 6. Busiest Transaction Days
st.subheader("📆 Busiest Days of the Week")

# Create 'Weekday' column from InvoiceDate
data1["Weekday"] = data1["InvoiceDate"].dt.day_name()

# Group by weekday and count unique InvoiceNo (i.e. transactions)
weekday_traffic = (
    data1.groupby("Weekday")["InvoiceNo"]
    .nunique()
    .reset_index()
)

# Optional: Order weekdays properly
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_traffic["Weekday"] = pd.Categorical(weekday_traffic["Weekday"], categories=weekday_order, ordered=True)
weekday_traffic = weekday_traffic.sort_values("Weekday")

# Plot line chart
fig5 = px.line(
    weekday_traffic,
    x="Weekday",
    y="InvoiceNo",
    markers=True,
    title="Transactions by Weekday"
)

st.plotly_chart(fig5, use_container_width=True)

# RFM Analysis

st.title("📦 RFM Segmentation Dashboard")

# Load RFM Excel file
RFM_PATH = os.path.join(BASE_DIR, "RFM.xlsx")

@st.cache_data
def load_rfm_excel():
    return pd.read_excel(RFM_PATH)

rfm = load_rfm_excel()

# Define RFM_level assignment
def assign_rfm_level(row):
    if row['RFM_Score'] >= 9:
        return 'Best Customer'
    elif 5 <= row['RFM_Score'] < 9:
        return 'Loyal Customer'
    elif 1 <= row['RFM_Score'] < 5:
        return 'Less Active Customer'
    else:
        return 'Unknown'

# Apply segmentation
rfm['RFM_level'] = rfm.apply(assign_rfm_level, axis=1)

# Sidebar filter
st.sidebar.header("🔍 Filter by RFM Segment")
rfm_levels = ["All"] + sorted(rfm['RFM_level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select RFM Segment", rfm_levels)

# Filter DataFrame by selected RFM level
if selected_level != "All":
    filtered_rfm = rfm[rfm['RFM_level'] == selected_level]
    st.write(f"📂 Showing customers in segment: **{selected_level}**")
else:
    filtered_rfm = rfm

# Show table of customers
st.subheader("🧾 Customer RFM Table")
st.dataframe(filtered_rfm[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'RFM_level']].head(20))

# Segment count chart
st.subheader("📈 RFM Segment Distribution")
segment_counts = rfm['RFM_level'].value_counts().reset_index()
segment_counts.columns = ['RFM_level', 'Count']
fig1 = px.bar(segment_counts, x='RFM_level', y='Count', color='RFM_level', title="Segment Counts")
st.plotly_chart(fig1, use_container_width=True)

# RFM averages
st.subheader("📊 Average RFM Metrics per Segment")
avg_rfm = rfm.groupby('RFM_level')[['Recency', 'Frequency', 'Monetary']].mean().round(2).reset_index()
st.dataframe(avg_rfm)


# GMM Clustering

# GMM-Based Customer Segmentation Section
st.subheader("📦 GMM-Based Customer Segmentation Dashboard")

# Load the pre-clustered Excel file
GMM_PATH = os.path.join(BASE_DIR, "Gmm.xlsx")

@st.cache_data
def load_clustered_data():
    return pd.read_excel(GMM_PATH)

rfm = load_clustered_data()

# Sidebar Filter
st.sidebar.header("🔍 Filter by Segment")
segments = ["All"] + sorted(rfm['GMM_Segment'].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("Select GMM Segment", segments)

# Display cluster counts
st.write("🧮 **Cluster Distribution**")
cluster_counts = rfm['GMM_Cluster'].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Customer Count']
st.dataframe(cluster_counts)

# Filter if a specific segment is selected
if selected_segment != "All":
    filtered_rfm = rfm[rfm['GMM_Segment'] == selected_segment]
    st.write(f"📂 Showing customers in segment: **{selected_segment}**")
else:
    filtered_rfm = rfm

# Display customer segmentation table
st.write("🧩 **Customer Segments**")
filtered_cols = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'GMM_Cluster', 'GMM_Segment', 'GMM_Advice']
st.dataframe(filtered_rfm[filtered_cols].head(20))

# Show cluster-wise RFM averages
st.write("📊 **Cluster Averages (RFM Metrics)**")
cluster_summary = rfm.groupby('GMM_Cluster')[['Recency', 'Frequency', 'Monetary']].mean().round(2).reset_index()
st.dataframe(cluster_summary)

# 3D Scatter plot
fig = px.scatter_3d(
    rfm,
    x='Recency', y='Frequency', z='Monetary',
    color='GMM_Segment',
    symbol='GMM_Cluster',
    hover_data=['CustomerID', 'GMM_Advice'],
    title="🧬 Customer Segments (GMM)"
)
st.plotly_chart(fig, use_container_width=True)

# Display Segment + Advice Legend
st.subheader("💡 Cluster-Based Marketing Advice")
advice_table = rfm[['GMM_Cluster', 'GMM_Segment', 'GMM_Advice']].drop_duplicates().sort_values('GMM_Cluster')

for _, row in advice_table.iterrows():
    st.markdown(f"""
    ### 🧩 Cluster {int(row['GMM_Cluster'])}
    - **Segment:** {row['GMM_Segment']}
    - **Advice:** {row['GMM_Advice']}
    """)

# Optional sidebar legend
st.sidebar.markdown("### 📘 Segment Legend")
for _, row in advice_table.iterrows():
    st.sidebar.markdown(f"- {row['GMM_Segment']}: {row['GMM_Advice']}")
