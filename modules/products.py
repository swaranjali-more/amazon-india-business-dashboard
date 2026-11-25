import plotly.express as px
import streamlit as st


def render(df):
    if df.empty:
        st.info("No category or product records match the active filters.")
        return

    cat_summary = (
        df.groupby("Category", as_index=False)
        .agg(Total_Sales_INR=("Total_Sales_INR", "sum"), Profit_INR=("Profit_INR", "sum"), Quantity=("Quantity", "sum"))
        .sort_values("Total_Sales_INR", ascending=False)
    )

    c1, c2 = st.columns(2)
    with c1:
        fig_cs = px.bar(
            cat_summary,
            x="Category",
            y="Total_Sales_INR",
            title="Category-Wise Sales (INR)",
            labels={"Total_Sales_INR": "Sales (INR)"},
            color_discrete_sequence=["#0F172A"],
        )
        fig_cs.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_cs, use_container_width=True)

    with c2:
        fig_cp = px.bar(
            cat_summary,
            x="Category",
            y="Profit_INR",
            title="Category-Wise Profit (INR)",
            labels={"Profit_INR": "Profit (INR)"},
            color_discrete_sequence=["#FF9900"],
        )
        fig_cp.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_cp, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig_cu = px.bar(
            cat_summary.sort_values("Quantity", ascending=False),
            x="Category",
            y="Quantity",
            title="Category-Wise Units Sold",
            labels={"Quantity": "Units Sold"},
            color_discrete_sequence=["#0284C7"],
        )
        fig_cu.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_cu, use_container_width=True)

    with c4:
        top_prod = (
            df.groupby("Product", as_index=False)["Total_Sales_INR"]
            .sum()
            .sort_values("Total_Sales_INR", ascending=False)
            .head(10)
            .sort_values("Total_Sales_INR", ascending=True)
        )
        fig_tp = px.bar(
            top_prod,
            x="Total_Sales_INR",
            y="Product",
            orientation="h",
            title="Top 10 Products by Sales (INR)",
            labels={"Total_Sales_INR": "Sales (INR)", "Product": ""},
            color_discrete_sequence=["#1E293B"],
        )
        fig_tp.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_tp, use_container_width=True)