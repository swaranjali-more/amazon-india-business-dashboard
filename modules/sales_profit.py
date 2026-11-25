import plotly.express as px
import streamlit as st


def render(df):
    if df.empty or "Month_Start" not in df.columns:
        st.info("No sales or profit records match the active filters.")
        return

    monthly = (
        df.groupby(["Month_Start", "Month_Year"], as_index=False)
        .agg(
            Total_Sales_INR=("Total_Sales_INR", "sum"),
            Profit_INR=("Profit_INR", "sum"),
            Total_Orders=("Order_ID", "nunique"),
        )
        .sort_values("Month_Start")
    )
    monthly["Profit_Margin_Pct"] = monthly.apply(
        lambda r: (r["Profit_INR"] / r["Total_Sales_INR"] * 100) if r["Total_Sales_INR"] > 0 else 0.0,
        axis=1,
    )
    monthly["MoM_Sales_Pct"] = monthly["Total_Sales_INR"].pct_change() * 100

    c1, c2 = st.columns(2)
    with c1:
        fig_s = px.bar(
            monthly,
            x="Month_Year",
            y="Total_Sales_INR",
            title="Monthly Sales (INR)",
            labels={"Month_Year": "Month", "Total_Sales_INR": "Sales (INR)"},
            color_discrete_sequence=["#0F172A"],
        )
        fig_s.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        fig_p = px.bar(
            monthly,
            x="Month_Year",
            y="Profit_INR",
            title="Monthly Profit (INR)",
            labels={"Month_Year": "Month", "Profit_INR": "Profit (INR)"},
            color_discrete_sequence=["#FF9900"],
        )
        fig_p.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_p, use_container_width=True)

    fig_m = px.line(
        monthly,
        x="Month_Year",
        y="Profit_Margin_Pct",
        markers=True,
        title="Monthly Profit Margin (%)",
        labels={"Month_Year": "Month", "Profit_Margin_Pct": "Profit Margin (%)"},
        color_discrete_sequence=["#0284C7"],
    )
    fig_m.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
    st.plotly_chart(fig_m, use_container_width=True)