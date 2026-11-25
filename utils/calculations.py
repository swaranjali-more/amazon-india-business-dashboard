import pandas as pd


def compute_core_kpis(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "total_orders": 0,
            "total_units": 0,
            "aov": 0.0,
            "profit_margin": 0.0,
            "delivered_orders": 0,
            "shipped_orders": 0,
            "returned_orders": 0,
            "cancelled_orders": 0,
            "return_rate": 0.0,
            "cancellation_rate": 0.0,
            "non_delivered_sales": 0.0,
        }

    total_sales = float(df["Total_Sales_INR"].sum()) if "Total_Sales_INR" in df.columns else 0.0
    total_profit = float(df["Profit_INR"].sum()) if "Profit_INR" in df.columns else 0.0
    total_orders = int(df["Order_ID"].nunique()) if "Order_ID" in df.columns else len(df)
    total_units = int(df["Quantity"].sum()) if "Quantity" in df.columns else 0

    aov = (total_sales / total_orders) if total_orders > 0 else 0.0
    profit_margin = ((total_profit / total_sales) * 100.0) if total_sales > 0 else 0.0

    status_series = df["Order_Status"] if "Order_Status" in df.columns else pd.Series(dtype=str)
    delivered_orders = int((status_series == "Delivered").sum())
    shipped_orders = int((status_series == "Shipped").sum())
    returned_orders = int((status_series == "Returned").sum())
    cancelled_orders = int((status_series == "Cancelled").sum())

    total_records = len(df)
    return_rate = ((returned_orders / total_records) * 100.0) if total_records > 0 else 0.0
    cancellation_rate = ((cancelled_orders / total_records) * 100.0) if total_records > 0 else 0.0

    non_delivered_sales = (
        float(df.loc[status_series.isin(["Returned", "Cancelled"]), "Total_Sales_INR"].sum())
        if "Total_Sales_INR" in df.columns
        else 0.0
    )

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "total_units": total_units,
        "aov": aov,
        "profit_margin": profit_margin,
        "delivered_orders": delivered_orders,
        "shipped_orders": shipped_orders,
        "returned_orders": returned_orders,
        "cancelled_orders": cancelled_orders,
        "return_rate": return_rate,
        "cancellation_rate": cancellation_rate,
        "non_delivered_sales": non_delivered_sales,
    }


def build_dynamic_insights(df: pd.DataFrame) -> list[str]:
    if df is None or df.empty:
        return ["No records match the current filter selection. Adjust or reset filters to view insights."]

    insights = []
    if "Category" in df.columns and "Total_Sales_INR" in df.columns and df["Total_Sales_INR"].sum() > 0:
        cat_sales = df.groupby("Category")["Total_Sales_INR"].sum().sort_values(ascending=False)
        top_cat = cat_sales.index[0]
        top_share = (cat_sales.iloc[0] / df["Total_Sales_INR"].sum()) * 100
        insights.append(f"{top_cat} leads revenue at {top_share:.1f}% of filtered sales (INR {cat_sales.iloc[0]:,.2f}).")

    if "Ship_State" in df.columns and "Total_Sales_INR" in df.columns and df["Total_Sales_INR"].sum() > 0:
        state_sales = df.groupby("Ship_State")["Total_Sales_INR"].sum().sort_values(ascending=False)
        insights.append(f"{state_sales.index[0]} is the top shipping state with INR {state_sales.iloc[0]:,.2f} in sales.")

    if "Order_Status" in df.columns and len(df) > 0:
        ret_rate = ((df["Order_Status"] == "Returned").sum() / len(df)) * 100
        can_rate = ((df["Order_Status"] == "Cancelled").sum() / len(df)) * 100
        insights.append(f"Return rate is {ret_rate:.2f}% and cancellation rate is {can_rate:.2f}% across active rows.")

    if "Month_Start" in df.columns and "Total_Sales_INR" in df.columns:
        monthly = df.groupby("Month_Start")["Total_Sales_INR"].sum().sort_index()
        if len(monthly) >= 2 and monthly.iloc[-2] > 0:
            mom = ((monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2]) * 100
            direction = "up" if mom >= 0 else "down"
            insights.append(f"Latest month sales in view are {direction} {abs(mom):.1f}% compared to the prior month.")

    return insights