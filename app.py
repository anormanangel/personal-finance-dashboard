import pandas as pd
import streamlit as st
from io import BytesIO
import plotly.express as px

st.set_page_config(
    page_title="Income & Expense Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown(
    """
    <style>
    

    .kpi-card:hover {
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }

    .kpi-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 10px;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 8px;
        color: #6b7280;
    }

    .kpi-caption {
        font-size: 0.85rem;
        color: #6b7280;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 0.25rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# HELPERS
# -----------------------------
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Transactions")
    return output.getvalue()


def render_kpi_card(title, value, caption, icon, tooltip):
    st.markdown(
        f"""
        <div class="kpi-card" title="{tooltip}">
            <div class="kpi-title">{icon} {title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


MONTH_ORDER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("income_expense.csv")

    df.columns = [col.strip().upper() for col in df.columns]

    expected_cols = ["DATE", "MONTH", "CATEGORY", "TYPE", "DESCRIPTION", "AMOUNT"]
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Missing columns in CSV: {missing_cols}")
        st.stop()

    df["DATE"] = df["DATE"].astype(str).str.strip()
    df["MONTH"] = df["MONTH"].astype(str).str.strip()
    df["CATEGORY"] = df["CATEGORY"].astype(str).str.strip()
    df["TYPE"] = df["TYPE"].astype(str).str.strip()
    df["DESCRIPTION"] = df["DESCRIPTION"].astype(str).str.strip()

    df["AMOUNT"] = (
        df["AMOUNT"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["AMOUNT"] = pd.to_numeric(df["AMOUNT"], errors="coerce").fillna(0)

    df["MONTH_NUM"] = df["MONTH"].map(MONTH_ORDER)

    return df


df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Finance Dashboard")
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Transactions Summary"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

month_options = ["All"] + [
    m for m in sorted(df["MONTH"].dropna().unique(), key=lambda x: MONTH_ORDER.get(x, 99))
]
type_options = ["All"] + sorted(df["TYPE"].dropna().unique().tolist())
category_options = ["All"] + sorted(df["CATEGORY"].dropna().unique().tolist())

selected_month = st.sidebar.selectbox("Month", month_options)
selected_type = st.sidebar.selectbox("Type", type_options)
selected_category = st.sidebar.selectbox("Category", category_options)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df.copy()

if selected_month != "All":
    filtered_df = filtered_df[filtered_df["MONTH"] == selected_month]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["TYPE"] == selected_type]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["CATEGORY"] == selected_category]

income_df = filtered_df[filtered_df["TYPE"].str.lower() == "income"]
expense_df = filtered_df[filtered_df["TYPE"].str.lower() == "expense"]

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_income = income_df["AMOUNT"].sum()
total_expense = expense_df["AMOUNT"].sum()
net_balance = total_income - total_expense
total_transactions = len(filtered_df)
avg_transaction = filtered_df["AMOUNT"].mean() if total_transactions > 0 else 0

# -----------------------------
# PAGE 1: DASHBOARD
# -----------------------------
if page == "Dashboard":
    st.title("Income & Expense Dashboard")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='section-title'>💼 Financial Overview</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_kpi_card(
            title="Total Income",
            value=f"UGX {total_income:,.0f}",
            caption="All income in current filtered view",
            icon="💰",
            tooltip="Total income amount based on the selected filters."
        )

    with c2:
        render_kpi_card(
            title="Total Expense",
            value=f"UGX {total_expense:,.0f}",
            caption="All expenses in current filtered view",
            icon="💸",
            tooltip="Total expense amount based on the selected filters."
        )

    with c3:
        render_kpi_card(
            title="Net Balance",
            value=f"UGX {net_balance:,.0f}",
            caption="Income minus expenses",
            icon="📊",
            tooltip="Net balance calculated as total income less total expenses."
        )

    with c4:
        render_kpi_card(
            title="Transactions",
            value=f"{total_transactions:,}",
            caption=f"Average amount: UGX {avg_transaction:,.0f}",
            icon="🧾",
            tooltip="Count of all visible transactions in the filtered view."
        )

    st.divider()

    left, right = st.columns(2)
    
    with left:
        st.subheader("Expenses by Category")

        expense_category = (
            expense_df.groupby("CATEGORY", as_index=False)["AMOUNT"]
            .sum()
            .sort_values("AMOUNT", ascending=False)
    )

        st.dataframe(expense_category, use_container_width=True)

        if not expense_category.empty:

            fig_expense = px.bar(
            expense_category,
                x="CATEGORY",
                y="AMOUNT",
                title="Expenses by Category",
                text="AMOUNT"
        )

        fig_expense.update_traces(
            texttemplate="UGX %{text:,.0f}",
            textposition="outside"
        )

        fig_expense.update_layout(
            xaxis_title="Category",
            yaxis_title="Amount (UGX)"
        )

        st.plotly_chart(fig_expense, use_container_width=True)



    with right:
        st.subheader("Income by Category")
        income_category = (
            income_df.groupby("CATEGORY", as_index=False)["AMOUNT"]
            .sum()
            .sort_values("AMOUNT", ascending=False)
        )
        st.dataframe(income_category, use_container_width=True)

        if not income_category.empty:

            # add vertical spacing to align with left chart
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            fig_income = px.pie(
                income_category,
                names="CATEGORY",
                values="AMOUNT",
                title="Income Share by Category"
            )
            fig_income.update_traces(
                texttemplate="UGX %{value:,.0f}",
                textposition="inside"
            )
            st.plotly_chart(fig_income, use_container_width=True)

    st.divider()

    st.subheader("Monthly Totals")
    month_summary = (
        filtered_df.groupby(["MONTH_NUM", "MONTH", "TYPE"], as_index=False)["AMOUNT"]
        .sum()
        .sort_values(["MONTH_NUM", "TYPE"])
    )
    if not month_summary.empty:
        pivot_month = month_summary.pivot(index="MONTH", columns="TYPE", values="AMOUNT").fillna(0)
        month_ordered = [m for m in sorted(pivot_month.index, key=lambda x: MONTH_ORDER.get(x, 99))]
        pivot_month = pivot_month.loc[month_ordered]
        st.dataframe(pivot_month, use_container_width=True)
        st.bar_chart(pivot_month)

# -----------------------------
# PAGE 2: TRANSACTIONS SUMMARY
# -----------------------------
elif page == "Transactions Summary":
    st.title("Transactions Summary")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='section-title'>Summary Indicators</div>",
        unsafe_allow_html=True
    )

    t1, t2, t3 = st.columns(3)

    with t1:
        render_kpi_card(
            title="Income",
            value=f"UGX {total_income:,.0f}",
            caption="Visible income total",
            icon="💰",
            tooltip="Total income in the current filtered summary."
        )

    with t2:
        render_kpi_card(
            title="Expense",
            value=f"UGX {total_expense:,.0f}",
            caption="Visible expense total",
            icon="💸",
            tooltip="Total expenses in the current filtered summary."
        )

    with t3:
        render_kpi_card(
            title="Net Balance",
            value=f"UGX {net_balance:,.0f}",
            caption="Visible balance after expenses",
            icon="📊",
            tooltip="Net balance in the current filtered summary."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    group_by = st.selectbox(
        "Drill down by",
        ["Category", "Type", "Month"]
    )

    if group_by == "Category":
        summary = (
            filtered_df.groupby("CATEGORY")
            .agg(
                NUMBER_OF_TRANSACTIONS=("AMOUNT", "count"),
                TOTAL_AMOUNT=("AMOUNT", "sum")
            )
            .reset_index()
            .sort_values("TOTAL_AMOUNT", ascending=False)
        )
        st.dataframe(summary, use_container_width=True)
        if not summary.empty:
            st.bar_chart(summary.set_index("CATEGORY")["TOTAL_AMOUNT"])

    elif group_by == "Type":
        summary = (
            filtered_df.groupby("TYPE")
            .agg(
                NUMBER_OF_TRANSACTIONS=("AMOUNT", "count"),
                TOTAL_AMOUNT=("AMOUNT", "sum")
            )
            .reset_index()
            .sort_values("TOTAL_AMOUNT", ascending=False)
        )
        st.dataframe(summary, use_container_width=True)
        if not summary.empty:
            st.bar_chart(summary.set_index("TYPE")["TOTAL_AMOUNT"])

    elif group_by == "Month":
        summary = (
            filtered_df.groupby(["MONTH_NUM", "MONTH"])
            .agg(
                NUMBER_OF_TRANSACTIONS=("AMOUNT", "count"),
                TOTAL_AMOUNT=("AMOUNT", "sum")
            )
            .reset_index()
            .sort_values("MONTH_NUM")
        )
        st.dataframe(summary[["MONTH", "NUMBER_OF_TRANSACTIONS", "TOTAL_AMOUNT"]], use_container_width=True)
        if not summary.empty:
            st.bar_chart(summary.set_index("MONTH")["TOTAL_AMOUNT"])