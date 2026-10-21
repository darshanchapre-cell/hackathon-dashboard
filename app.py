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

with elements("exam_dashboard"):
    with dashboard.Grid(
        st.session_state.exam_layout,
        onLayoutChange=save_layout,
        cols=12,
        rowHeight=60,
        draggableHandle=".drag-handle",
    ):
        with mui.Paper(
            key="total",
            elevation=3,
            sx={"padding": 2, "overflow": "auto"}
        ):
            mui.Typography(
                "Total Vacancies",
                className="drag-handle",
                sx={"cursor": "move"}
            )
            mui.Typography(str(total), variant="h4")

        with mui.Paper(
            key="exams",
            elevation=3,
            sx={"padding": 2, "overflow": "auto"}
        ):
            mui.Typography(
                "Exams Listed",
                className="drag-handle",
                sx={"cursor": "move"}
            )
            mui.Typography(str(exams), variant="h4")

        with mui.Paper(
            key="table",
            elevation=3,
            sx={"padding": 2, "overflow": "auto"}
        ):
            mui.Typography(
                "Vacancy Details",
                className="drag-handle",
                sx={"cursor": "move"}
            )
            mui.TableContainer(
                mui.Table(
                    mui.TableHead(
                        mui.TableRow(
                            mui.TableCell("Exam"),
                            mui.TableCell("Category"),
                            mui.TableCell("Vacancies"),
                        )
                    ),
                    mui.TableBody(*[
                        mui.TableRow(
                            mui.TableCell(row["Exam"]),
                            mui.TableCell(row["Category"]),
                            mui.TableCell(str(row["Vacancies"])),
                            key=row["Exam"],
                        )
                        for _, row in filtered.iterrows()
                    ])
                )
            )

st.info(
    "Sample figures are for demonstration only, "
    "not verified current vacancies."
)
