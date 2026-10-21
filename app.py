import streamlit as st
import pandas as pd
from streamlit_elements import elements, dashboard, mui

st.set_page_config(
    page_title="Exam Vacancy Dashboard",
    layout="wide"
)

st.title("🎯 Competitive Exam Vacancy Dashboard")
st.caption("Demo data — actual vacancies verify karna zaroori hai.")

# Sample vacancy data
df = pd.DataFrame({
    "Exam": [
        "SSC CGL",
        "RRB NTPC",
        "UPSC CSE",
        "IBPS PO",
        "MPSC"
    ],
    "Category": [
        "Central", "Railway", "Central",
        "Banking", "State"
    ],
    "Vacancies": [14500, 8500, 1000, 5200, 500]
})

# Sidebar filter
category = st.sidebar.selectbox(
    "Select exam category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

filtered = df if category == "All" else df[
    df["Category"] == category
]

total = int(filtered["Vacancies"].sum())
exams = len(filtered)

# Dashboard card positions
default_layout = [
    {"i": "total", "x": 0, "y": 0, "w": 4, "h": 2},
    {"i": "exams", "x": 4, "y": 0, "w": 4, "h": 2},
    {"i": "table", "x": 0, "y": 2, "w": 8, "h": 5},
]

if "exam_layout" not in st.session_state:
    st.session_state.exam_layout = default_layout


def save_layout(new_layout):
    st.session_state.exam_layout = new_layout


st.subheader("📊 Move the dashboard cards")
st.caption("Cards ko mouse se drag karo aur apni pasand ki jagah rakho.")
with elements("test_dashboard"):
    with dashboard.Grid(
        [
            {"i": "total", "x": 0, "y": 0, "w": 4, "h": 2},
            {"i": "exams", "x": 4, "y": 0, "w": 4, "h": 2},
        ],
        cols=12,
        rowHeight=80,
    ):
        with mui.Paper(
            key="total",
            sx={"padding": 2, "backgroundColor": "#263238", "color": "white"}
        ):
            mui.Typography("Total Vacancies")
            mui.Typography(str(total), variant="h4")

        with mui.Paper(
            key="exams",
            sx={"padding": 2, "backgroundColor": "#263238", "color": "white"}
        ):
            mui.Typography("Exams Listed")
            mui.Typography(str(exams), variant="h4")
