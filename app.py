import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Transport Passenger Analysis",
    page_icon="🚌",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("dataset/transport_passenger_analysis_6000.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# ---------------- TITLE ----------------
st.title("🚌 Transport Passenger Analysis Dashboard")
st.markdown("### Interactive Transport Data Analysis")

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

routes = ["All"] + sorted(df["Route"].unique().tolist())
vehicles = ["All"] + sorted(df["vehicle_Type"].unique().tolist())
payments = ["All"] + sorted(df["Payment_Method"].unique().tolist())

selected_route = st.sidebar.selectbox("Select Route", routes)
selected_vehicle = st.sidebar.selectbox("Select Vehicle Type", vehicles)
selected_payment = st.sidebar.selectbox("Select Payment Method", payments)

filtered_df = df.copy()

if selected_route != "All":
    filtered_df = filtered_df[filtered_df["Route"] == selected_route]

if selected_vehicle != "All":
    filtered_df = filtered_df[filtered_df["vehicle_Type"] == selected_vehicle]

if selected_payment != "All":
    filtered_df = filtered_df[filtered_df["Payment_Method"] == selected_payment]

# ---------------- KPI METRICS ----------------
total_passengers = filtered_df["Passenger_Count"].sum()
total_revenue = filtered_df["Total_revenue"].sum()
average_passengers = filtered_df["Passenger_Count"].mean()
average_ticket = filtered_df["Ticket_Price"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Passengers", f"{total_passengers:,.0f}")

with col2:
    st.metric("💰 Total Revenue", f"Rs. {total_revenue:,.2f}")

with col3:
    st.metric("📊 Average Passengers", f"{average_passengers:.2f}")

with col4:
    st.metric("🎫 Average Ticket Price", f"Rs. {average_ticket:.2f}")

st.divider()

# ---------------- ROUTE ANALYSIS ----------------
st.header("🛣️ Passenger Count by Route")

route_data = (
    filtered_df.groupby("Route")["Passenger_Count"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(route_data)

# ---------------- TWO COLUMN CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚍 Vehicle Type Distribution")

    vehicle_data = filtered_df["vehicle_Type"].value_counts()

    st.bar_chart(vehicle_data)

with col2:
    st.subheader("💳 Payment Method Distribution")

    payment_data = filtered_df["Payment_Method"].value_counts()

    st.bar_chart(payment_data)

st.divider()

# ---------------- MONTHLY ANALYSIS ----------------
st.header("📈 Monthly Passenger Trend")

monthly_passengers = (
    filtered_df.groupby("Month")["Passenger_Count"]
    .sum()
)

st.line_chart(monthly_passengers)

st.header("💰 Monthly Revenue Trend")

monthly_revenue = (
    filtered_df.groupby("Month")["Total_revenue"]
    .sum()
)

st.line_chart(monthly_revenue)

st.divider()

# ---------------- CORRELATION ----------------
st.header("🔗 Correlation Analysis")

corr = filtered_df[
    ["Passenger_Count", "Ticket_Price", "Total_revenue"]
].corr()

st.dataframe(corr.round(4), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    passenger_revenue_corr = corr.loc[
        "Passenger_Count", "Total_revenue"
    ]

    st.metric(
        "Passenger Count vs Revenue",
        f"{passenger_revenue_corr:.4f}"
    )

with col2:
    ticket_passenger_corr = corr.loc[
        "Ticket_Price", "Passenger_Count"
    ]

    st.metric(
        "Ticket Price vs Passengers",
        f"{ticket_passenger_corr:.4f}"
    )

st.divider()

# ---------------- OUTLIER ANALYSIS ----------------
st.header("📦 Passenger Count Outlier Analysis")

Q1 = filtered_df["Passenger_Count"].quantile(0.25)
Q3 = filtered_df["Passenger_Count"].quantile(0.75)
IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = filtered_df[
    (filtered_df["Passenger_Count"] < lower_limit) |
    (filtered_df["Passenger_Count"] > upper_limit)
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Q1", f"{Q1:.2f}")

with col2:
    st.metric("Q3", f"{Q3:.2f}")

with col3:
    st.metric("Upper Limit", f"{upper_limit:.2f}")

with col4:
    st.metric("Number of Outliers", len(outliers))

# ---------------- KEY FINDINGS ----------------
st.divider()

st.header("⭐ Key Findings")

if len(filtered_df) > 0:

    highest_route = (
        filtered_df.groupby("Route")["Passenger_Count"]
        .sum()
        .idxmax()
    )

    highest_revenue_route = (
        filtered_df.groupby("Route")["Total_revenue"]
        .sum()
        .idxmax()
    )

    common_vehicle = (
        filtered_df["vehicle_Type"]
        .value_counts()
        .idxmax()
    )

    common_payment = (
        filtered_df["Payment_Method"]
        .value_counts()
        .idxmax()
    )

    st.write(f"• Highest passenger route: **{highest_route}**")
    st.write(f"• Highest revenue route: **{highest_revenue_route}**")
    st.write(f"• Most common vehicle type: **{common_vehicle}**")
    st.write(f"• Most common payment method: **{common_payment}**")
    st.write(f"• Number of detected outliers: **{len(outliers)}**")

else:
    st.warning("No data available for the selected filters.")

# ---------------- FOOTER ----------------
st.divider()

st.success("✅ Transport Passenger Analysis Dashboard Completed")
st.caption("Developed using Python, Pandas, Matplotlib and Streamlit")