import plotly.express as px
import streamlit as st
from utils.calculations import compute_core_kpis


def render(df):
    if df.empty:
        st.info("No order status records match the active filters.")
        return

    kpis = compute_core_kpis(df)
    cols = st.columns(5)
    cols[0].metric("Delivered", f"{kpis['delivered_orders']:,}")
    cols[1].metric("Shipped", f"{kpis['shipped_orders']:,}")
    cols[2].metric("Returned", f"{kpis['returned_orders']:,}")
    cols[3].metric("Cancelled", f"{kpis['cancelled_orders']:,}")
    cols[4].metric("Returned + Cancelled Value", f"INR {kpis['non_delivered_sales']:,.2f}")

    c1, c2 = st.columns(2)
    with c1:
        status_df = df.groupby("Order_Status", as_index=False)["Order_ID"].nunique().rename(columns={"Order_ID": "Orders"})
        fig_st = px.bar(
            status_df,
            x="Order_Status",
            y="Orders",
            title="Order Status Distribution",
            color="Order_Status",
            color_discrete_map={"Delivered": "#0F172A", "Shipped": "#0284C7", "Returned": "#FF9900", "Cancelled": "#64748B"},
        )
        fig_st.update_layout(template="plotly_white", showlegend=False, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
        st.plotly_chart(fig_st, use_container_width=True)

    with c2:
        rc_df = df[df["Order_Status"].isin(["Returned", "Cancelled"])]
        if rc_df.empty:
            st.info("No returned or cancelled orders in the selected view.")
        else:
            cat_rc = rc_df.groupby(["Category", "Order_Status"], as_index=False)["Order_ID"].nunique().rename(columns={"Order_ID": "Orders"})
            fig_rc = px.bar(
                cat_rc,
                x="Category",
                y="Orders",
                color="Order_Status",
                barmode="group",
                title="Category-Wise Returns & Cancellations",
                color_discrete_map={"Returned": "#FF9900", "Cancelled": "#0F172A"},
            )
            fig_rc.update_layout(template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font={"family": "Inter, sans-serif"})
            st.plotly_chart(fig_rc, use_container_width=True)