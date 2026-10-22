import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Competitive Exam Vacancy Portal",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Competitive Exam Forms & Vacancies")
st.write("Find exams, application deadlines and vacancies.")

# Demo data: replace with verified official notifications
data = {
    "Exam": [
        "SSC CGL",
        "SSC CHSL",
        "RRB NTPC",
        "UPSC Civil Services",
        "IBPS PO",
        "MPSC State Services"
    ],
    "Category": [
        "SSC", "SSC", "Railway",
        "UPSC", "Banking", "State PSC"
    ],
    "Vacancies": [1000, 500, 800, 150, 600, 200],
    "Last Date": [
        "2026-11-10",
        "2026-11-15",
        "2026-11-20",
        "2026-10-30",
        "2026-11-05",
        "2026-11-12"
    ],
    "Status": [
        "Check Official Notice",
        "Check Official Notice",
        "Check Official Notice",
        "Check Official Notice",
        "Check Official Notice",
        "Check Official Notice"
    ]
}

df = pd.DataFrame(data)
df["Last Date"] = pd.to_datetime(df["Last Date"])

# Sidebar filters
st.sidebar.header("Find an Exam")

categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox(
    "Exam Category", categories
)

search = st.sidebar.text_input("Search Exam Name")

filtered = df.copy()

if selected_category != "All":
    filtered = filtered[
        filtered["Category"] == selected_category
    ]

if search:
    filtered = filtered[
        filtered["Exam"].str.contains(
            search, case=False, na=False
        )
    ]

# Summary cards
c1, c2, c3 = st.columns(3)

c1.metric("Exams Listed", len(filtered))
c2.metric(
    "Listed Vacancies",
    f"{filtered['Vacancies'].sum():,}"
)
c3.metric(
    "Categories",
    filtered["Category"].nunique()
)

st.divider()

# Bar chart
st.subheader("📊 Vacancies by Exam")

if not filtered.empty:
    fig = px.bar(
        filtered,
        x="Exam",
        y="Vacancies",
        color="Category",
        title="Advertised Vacancies (Demo Data)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart
    st.subheader("🥧 Vacancy Share by Category")

    category_data = (
        filtered.groupby("Category")["Vacancies"].sum()
        .reset_index()
    )

    fig2 = px.pie(
        category_data,
        names="Category",
        values="Vacancies",
        title="Vacancies by Exam Category"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Table
    st.subheader("📋 Exam & Vacancy List")

    display_df = filtered.copy()
    display_df["Last Date"] = (
        display_df["Last Date"].dt.strftime("%d %b %Y")
    )

    st.dataframe(display_df, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Exam List",
        data=csv,
        file_name="competitive_exam_vacancies.csv",
        mime="text/csv"
    )
else:
    st.warning("No matching exams found.")

st.caption(
    "Important: Sample data for demonstration only. "
    "Verify vacancies, deadlines and application status "
    "on the official recruitment notification before applying."
)
