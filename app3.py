import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv("india_housing_prices.csv")

st.set_page_config(layout="wide")
st.title("Indian Housing Prices Dashboard")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

state_filter = st.sidebar.multiselect(
    "Select State", 
    df["State"].unique()
)

city_filter = st.sidebar.multiselect(
    "Select City", 
    df["City"].unique()
    
)

bhk_filter = st.sidebar.multiselect(
    "Select BHK", 
    sorted(df["BHK"].unique())
)

owner_filter = st.sidebar.multiselect(
    "Owner Type",
    df["Owner_Type"].unique()
    
)

availability_filter = st.sidebar.multiselect(
    "Availability Status",
    df["Availability_Status"].unique()
)

# Filter data
df_filtered = df.copy()

if state_filter:
    df_filtered = df_filtered[df_filtered["State"].isin(state_filter)]
if city_filter:
    df_filtered = df_filtered[df_filtered["City"].isin(city_filter)]
if bhk_filter:
    df_filtered = df_filtered[df_filtered["BHK"].isin(bhk_filter)]
if owner_filter:
    df_filtered = df_filtered[df_filtered["Owner_Type"].isin(owner_filter)]
if availability_filter:
    df_filtered = df_filtered[df_filtered["Availability_Status"].isin(availability_filter)]


# -------------------------------
# KPI ROW
# -------------------------------
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Average Price (₹)", f"{df_filtered['Price_in_Lakhs'].mean():,.0f}")
kpi2.metric("Median Price (₹)", f"{df_filtered['Price_in_Lakhs'].median():,.0f}")
kpi3.metric("Total Listings", f"{len(df_filtered):,}")

# -------------------------------
# Visualization Dashboard
# ------------------------------------------------------
# ROW 1 — Amenities & Accessibility (3 charts)
# ------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Average Price by State")
    state_data = df_filtered.groupby("State")["Price_in_Lakhs"].mean().reset_index()
    fig_state = px.bar(
        state_data,
        x="State",
        y="Price_in_Lakhs",
        title="Avg Price by State",
        color="Price_in_Lakhs",
        color_continuous_scale="Blugrn"
    )
    st.plotly_chart(fig_state, use_container_width=True)

with c2:
    st.subheader("City Price Distribution (Treemap)")
    city_data = df_filtered.groupby("City")["Price_in_Lakhs"].mean().reset_index()
    fig_city = px.treemap(
        city_data,
        path=["City"],
        values="Price_in_Lakhs",
        color="Price_in_Lakhs",
        color_continuous_scale="Blugrn"
    )
    st.plotly_chart(fig_city, use_container_width=True)

with st.container():
    colA, colB = st.columns([2, 1])

    with colA:
        fig_amenities = make_subplots(
            rows=1, cols=3,
            subplot_titles=(
                "Nearby School Count",
                "Nearby Hospital Count",
                "Public Transport Accessibility"
            )
        )

        # Nearby School
        count_school = df_filtered['Nearby_Schools'].value_counts()
        fig_amenities.add_trace(
            go.Bar(x=count_school.index, y=count_school.values),
            row=1, col=1
        )

        # Nearby Hospital
        count_hospital = df_filtered['Nearby_Hospitals'].value_counts()
        fig_amenities.add_trace(
            go.Bar(x=count_hospital.index, y=count_hospital.values),
            row=1, col=2
        )

        # Public Transport Accessibility
        count_transport = df_filtered['Public_Transport_Accessibility'].value_counts()
        fig_amenities.add_trace(
            go.Bar(x=count_transport.index, y=count_transport.values),
            row=1, col=3
        )

        fig_amenities.update_layout(
            height=350,
            showlegend=False,
            title="Amenities & Accessibility Overview",
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="white"
        )

        st.plotly_chart(fig_amenities, use_container_width=True)

    # ------------------------------------------------------
    # ROW 1 RIGHT — Owner Type & Availability Status (2 pie)
    # ------------------------------------------------------
    with colB:
        # Visualization: Owner Type and Availability Status
        fig_owner = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "domain"}, {"type": "domain"}]],
        subplot_titles=("Owner Type Distribution", "Availability Status")
    )

    # Owner Type Pie Chart
    owner_counts = df_filtered['Owner_Type'].value_counts()
    fig_owner.add_trace(
        go.Pie(labels=owner_counts.index, values=owner_counts.values, hole=0.4),
        row=1, col=1
    )

    # Availability Status Pie Chart
    availability_counts = df_filtered['Availability_Status'].value_counts()
    fig_owner.add_trace(
        go.Pie(labels=availability_counts.index, values=availability_counts.values, hole=0.4),
        row=1, col=2
    )

    fig_owner.update_layout(
        height=350,
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white"
    )

    st.plotly_chart(fig_owner, use_container_width=True)


        # Owner Type Pie
    owner_counts = df_filtered['Owner_Type'].value_counts()
    fig_owner.add_trace(
            go.Pie(labels=owner_counts.index, values=owner_counts.values, hole=0.4),
            row=1, col=1
        )

        # Availability Status Pie
    availability_counts = df_filtered['Availability_Status'].value_counts()
    fig_owner.add_trace(
            go.Pie(labels=availability_counts.index, values=availability_counts.values, hole=0.4),
            row=1, col=2
        )

    fig_owner.update_layout(
            height=350,
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="white"
        )

    st.plotly_chart(fig_owner, use_container_width=True)


# ------------------------------------------------------
# ROW 2 — BHK vs Price Boxplot & Scatter Plot
# ------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### BHK vs Price Distribution")
    fig_bhk = px.box(
        df_filtered,
        x="BHK",
        y="Price_in_Lakhs",
        title="Price Variation by BHK",
        template="plotly_dark"
    )
    st.plotly_chart(fig_bhk, use_container_width=True)

with col2:
    st.markdown("### Size vs Price")
    fig_scatter = px.scatter(
        df_filtered,
        x="Size_in_SqFt",
        y="Price_in_Lakhs",
        color="BHK",
        size="Size_in_SqFt",
        title="Price vs Size",
        template="plotly_dark"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# ------------------------------------------------------
