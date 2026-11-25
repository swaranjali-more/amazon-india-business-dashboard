import pandas as pd

REQUIRED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Category",
    "Product",
    "Quantity",
    "Total_Sales_INR",
    "Profit_INR",
    "Payment_Method",
    "Fulfillment",
    "Order_Status",
    "Ship_State",
]


def clean_and_validate(df: pd.DataFrame):
    report = {
        "initial_rows": len(df),
        "missing_columns": [],
        "duplicate_rows_removed": 0,
        "invalid_dates_removed": 0,
        "final_rows": 0,
    }
    if df is None or df.empty:
        return pd.DataFrame(), report

    cleaned = df.copy()
    cleaned.columns = [str(c).strip() for c in cleaned.columns]
    report["missing_columns"] = [c for c in REQUIRED_COLUMNS if c not in cleaned.columns]

    before_dups = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    report["duplicate_rows_removed"] = before_dups - len(cleaned)

    if "Order_Date" in cleaned.columns:
        parsed_dates = pd.to_datetime(cleaned["Order_Date"], errors="coerce")
        invalid_mask = parsed_dates.isna()
        report["invalid_dates_removed"] = int(invalid_mask.sum())
        cleaned = cleaned.loc[~invalid_mask].copy()
        cleaned["Order_Date"] = parsed_dates.loc[~invalid_mask]
        cleaned["Month_Year"] = cleaned["Order_Date"].dt.to_period("M").astype(str)
        cleaned["Month_Start"] = cleaned["Order_Date"].dt.to_period("M").dt.to_timestamp()

    for col in ["Quantity", "Total_Sales_INR", "Profit_INR", "Unit_Price_INR", "Discount_Pct"]:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    for col in ["Category", "Product", "Payment_Method", "Fulfillment", "Order_Status", "Ship_State", "Order_ID"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()

    cleaned = cleaned.dropna(subset=[c for c in ["Order_ID", "Order_Date", "Total_Sales_INR"] if c in cleaned.columns])
    report["final_rows"] = len(cleaned)
    return cleaned, report