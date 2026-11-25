import plotly.express as px
import streamlit as st


def render(df):
    if df.empty or "Fulfillment" not in df.columns:
        st.info("No fulfillment data available for the active filters.")
        return

    ful_df = (
        df.groupby("Fulfillment", as_index=False)
        .agg(Total_Sales_INR=("Total_Sales_INR", "sum"), Profit_INR=("Profit_INR", "sum"), Orders=("Order_ID", "nunique"))
        .sort_values("Total_Sales_INR", ascending=False)
    )

    c1, c2 = st.columns(2)
    with c1:
        fig_s = px.bar(
            ful_df,
            x="Fulfillment",
            y="Total_Sales_INR",
            title="Sales by Fulfillment Method (INR)",
            color_discrete_sequence=["#0F172A"],
        )
        fig_s.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        fig_p = px.bar(
            ful_df,
            x="Fulfillment",
            y="Profit_INR",
            title="Profit by Fulfillment Method (INR)",
            color_discrete_sequence=["#FF9900"],
        )
        fig_p.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_p, use_container_width=True)

    fig_o = px.bar(
        ful_df,
        x="Fulfillment",
        y="Orders",
        title="Orders by Fulfillment Method",
        color_discrete_sequence=["#0284C7"],
    )
    fig_o.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
    st.plotly_chart(fig_o, use_container_width=True)