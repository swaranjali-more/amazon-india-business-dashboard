import pandas as pd
import streamlit as st


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()

    st.sidebar.markdown('<div class="section-label">Filter Controls</div>', unsafe_allow_html=True)

    filtered = df.copy()

    if "Order_Date" in filtered.columns and not filtered["Order_Date"].dropna().empty:
        min_d = filtered["Order_Date"].min().date()
        max_d = filtered["Order_Date"].max().date()
        date_val = st.sidebar.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d, key="f_date")
        if isinstance(date_val, (list, tuple)) and len(date_val) == 2:
            start_d, end_d = date_val
            filtered = filtered[(filtered["Order_Date"].dt.date >= start_d) & (filtered["Order_Date"].dt.date <= end_d)]

    filter_specs = [
        ("Category", "Category", "f_cat"),
        ("Product", "Product", "f_prod"),
        ("Order_Status", "Order Status", "f_status"),
        ("Payment_Method", "Payment Method", "f_pay"),
        ("Fulfillment", "Fulfillment Method", "f_ful"),
        ("Ship_State", "State", "f_state"),
    ]

    for col, label, key in filter_specs:
        if col in filtered.columns:
            options = sorted(filtered[col].dropna().unique().tolist())
            selected = st.sidebar.multiselect(label, options=options, default=options, key=key)
            if selected:
                filtered = filtered[filtered[col].isin(selected)]

    return filtered