import os
import streamlit as st

from modules import fulfillment, geography, orders_returns, overview, payments, products, sales_profit
from utils.calculations import build_dynamic_insights
from utils.data_cleaning import clean_and_validate
from utils.data_loader import load_dataset
from utils.filters import apply_filters

st.set_page_config(
    page_title="Amazon India Business Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_file = os.path.join("assets", "style.css")
if os.path.exists(css_file):
    with open(css_file, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FILTER_KEYS = ["f_date", "f_cat", "f_prod", "f_status", "f_pay", "f_ful", "f_state"]


def reset_all_filters():
    for k in FILTER_KEYS:
        st.session_state.pop(k, None)


# Sidebar brand, upload & navigation
st.sidebar.markdown('<div class="section-label">Amazon Horizon BI</div>', unsafe_allow_html=True)
st.sidebar.markdown("### Amazon India")
st.sidebar.caption("Prepared for Ravi | Built by Swaranjali")
st.sidebar.divider()

st.sidebar.markdown('<div class="section-label">Dataset Source</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

raw_df, source_label, load_err = load_dataset(uploaded_file=uploaded_file)
df, val_report = clean_and_validate(raw_df)

st.sidebar.caption(source_label)
st.sidebar.divider()

st.sidebar.markdown('<div class="section-label">Modules</div>', unsafe_allow_html=True)
sections = [
    "Overview",
    "Sales & Profit",
    "Products & Categories",
    "Orders & Returns",
    "Payment Analysis",
    "Fulfillment Analysis",
    "Geographic Performance",
    "Data Overview",
]
active_section = st.sidebar.radio("Navigation", sections, label_visibility="collapsed")
st.sidebar.divider()

filtered_df = apply_filters(df)

# Top context header
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown(
        f"""
        <div class="horizon-header">
            <div>
                <div class="horizon-kicker">Amazon India Performance System</div>
                <h1 class="horizon-title">{active_section}</h1>
                <p class="horizon-subtitle">Showing {len(filtered_df):,} of {len(df):,} validated records</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_h2:
    st.markdown("<div style='padding-top: 1.15rem;'></div>", unsafe_allow_html=True)
    st.button("Reset All Filters", on_click=reset_all_filters, use_container_width=True)

if load_err:
    st.error(load_err)
elif val_report["missing_columns"]:
    st.warning("Missing expected columns in dataset: " + ", ".join(val_report["missing_columns"]))

# Module routing
if active_section == "Overview":
    overview.render(filtered_df)
elif active_section == "Sales & Profit":
    sales_profit.render(filtered_df)
elif active_section == "Products & Categories":
    products.render(filtered_df)
elif active_section == "Orders & Returns":
    orders_returns.render(filtered_df)
elif active_section == "Payment Analysis":
    payments.render(filtered_df)
elif active_section == "Fulfillment Analysis":
    fulfillment.render(filtered_df)
elif active_section == "Geographic Performance":
    geography.render(filtered_df)
elif active_section == "Data Overview":
    st.markdown("#### Validation Summary")
    v_cols = st.columns(4)
    v_cols[0].metric("Initial Rows", f"{val_report['initial_rows']:,}")
    v_cols[1].metric("Duplicates Removed", f"{val_report['duplicate_rows_removed']:,}")
    v_cols[2].metric("Invalid Dates Removed", f"{val_report['invalid_dates_removed']:,}")
    v_cols[3].metric("Clean Rows", f"{val_report['final_rows']:,}")

    st.markdown("#### Filtered Records")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Filtered Data (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="amazon_india_filtered.csv",
        mime="text/csv",
    )

# Dynamic business insights
st.markdown("#### Business Insights")
bullets = build_dynamic_insights(filtered_df)
st.markdown(
    '<div class="insight-card">' + "<br>".join(f"- {item}" for item in bullets) + "</div>",
    unsafe_allow_html=True,
)