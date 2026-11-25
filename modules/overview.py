import plotly.express as px
import streamlit as st
from utils.calculations import compute_core_kpis


def render(df):
    kpis = compute_core_kpis(df)

    r1 = st.columns(4)
    r1[0].metric("Total Sales", f"INR {kpis['total_sales']:,.2f}")
    r1[1].metric("Total Profit", f"INR {kpis['total_profit']:,.2f}")
    r1[2].metric("Total Orders", f"{kpis['total_orders']:,}")
    r1[3].metric("Profit Margin", f"{kpis['profit_margin']:.2f}%")

    r2 = st.columns(4)
    r2[0].metric("Total Units Sold", f"{kpis['total_units']:,}")
    r2[1].metric("Average Order Value", f"INR {kpis['aov']:,.2f}")
    r2[2].metric("Return Rate", f"{kpis['return_rate']:.2f}%")
    r2[3].metric("Cancellation Rate", f"{kpis['cancellation_rate']:.2f}%")

    if df.empty or "Month_Start" not in df.columns:
        st.info("No monthly trend data available for the active filter selection.")
        return

    monthly = (
        df.groupby(["Month_Start", "Month_Year"], as_index=False)[["Total_Sales_INR", "Profit_INR"]]
        .sum()
        .sort_values("Month_Start")
    )
    melted = monthly.melt(
        id_vars=["Month_Start", "Month_Year"],
        value_vars=["Total_Sales_INR", "Profit_INR"],
        var_name="Metric",
        value_name="Amount_INR",
    )
    melted["Metric"] = melted["Metric"].map({"Total_Sales_INR": "Total Sales", "Profit_INR": "Total Profit"})

    fig = px.line(
        melted,
        x="Month_Year",
        y="Amount_INR",
        color="Metric",
        markers=True,
        title="Monthly Sales vs. Profit Trend",
        labels={"Month_Year": "Month", "Amount_INR": "Amount (INR)"},
        color_discrete_map={"Total Sales": "#0F172A", "Total Profit": "#FF9900"},
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"family": "Inter, sans-serif", "color": "#0F172A"},
        legend={"orientation": "h", "y": 1.12, "x": 0},
    )
    st.plotly_chart(fig, use_container_width=True)