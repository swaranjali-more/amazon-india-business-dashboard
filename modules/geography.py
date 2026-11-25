import plotly.express as px
import streamlit as st


def render(df):
    if df.empty or "Ship_State" not in df.columns:
        st.info("No state-level shipping data available for the active filters.")
        return

    state_df = (
        df.groupby("Ship_State", as_index=False)
        .agg(
            Total_Sales_INR=("Total_Sales_INR", "sum"),
            Profit_INR=("Profit_INR", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .sort_values("Total_Sales_INR", ascending=False)
    )

    c1, c2 = st.columns(2)
    with c1:
        top_s = state_df.head(12).sort_values("Total_Sales_INR", ascending=True)
        fig_s = px.bar(
            top_s,
            x="Total_Sales_INR",
            y="Ship_State",
            orientation="h",
            title="Top States by Sales (INR)",
            labels={"Total_Sales_INR": "Sales (INR)", "Ship_State": ""},
            color_discrete_sequence=["#0F172A"],
        )
        fig_s.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        top_p = state_df.sort_values("Profit_INR", ascending=False).head(12).sort_values("Profit_INR", ascending=True)
        fig_p = px.bar(
            top_p,
            x="Profit_INR",
            y="Ship_State",
            orientation="h",
            title="Top States by Profit (INR)",
            labels={"Profit_INR": "Profit (INR)", "Ship_State": ""},
            color_discrete_sequence=["#FF9900"],
        )
        fig_p.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_p, use_container_width=True)

    fig_o = px.bar(
        state_df.head(15),
        x="Ship_State",
        y="Orders",
        title="Top 15 States by Order Volume",
        color_discrete_sequence=["#0284C7"],
    )
    fig_o.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
    st.plotly_chart(fig_o, use_container_width=True)

    st.dataframe(state_df, use_container_width=True, hide_index=True)