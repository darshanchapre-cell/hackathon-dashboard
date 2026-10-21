import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Hospital Management Dashboard")
st.caption("Hospital Overview | Patient Management")

# Sample hospital data
df = pd.DataFrame({
    "Department": [
        "Cardiology",
        "Neurology",
        "Pediatrics",
        "Orthopedics",
        "General Medicine"
    ],
    "Patients": [42, 28, 35, 51, 44],
    "Available Beds": [8, 12, 6, 10, 15],
    "Emergency Cases": [5, 3, 4, 6, 2]
})

# Sidebar
st.sidebar.title("Hospital Menu")
menu = st.sidebar.selectbox(
    "Choose Section",
    ["Dashboard", "Patients", "Departments"]
)

if menu == "Dashboard":

    st.subheader("Hospital Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Patients", int(df["Patients"].sum()))
    c2.metric("Available Beds", int(df["Available Beds"].sum()))
    c3.metric("Departments", len(df))
    c4.metric("Emergency Cases", int(df["Emergency Cases"].sum()))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Patients by Department")
        fig = px.bar(
            df,
            x="Department",
            y="Patients",
            color="Department",
            title="Department-wise Patients"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Available Beds")
        fig2 = px.pie(
            df,
            names="Department",
            values="Available Beds",
            title="Bed Availability"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Department Overview")
    st.dataframe(df, use_container_width=True)

elif menu == "Patients":

    st.subheader("Patient Registration")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, value=18)

    department = st.selectbox(
        "Department",
        df["Department"].tolist()
    )

    if st.button("Register Patient"):
        if name.strip():
            st.success(
                f"Patient {name} registered successfully!"
            )
            st.write("Age:", age)
            st.write("Department:", department)
        else:
            st.warning("Please enter the patient's name.")

elif menu == "Departments":

    st.subheader("Department Details")

    selected = st.selectbox(
        "Select Department",
        df["Department"].tolist()
    )

    details = df[df["Department"] == selected]

    st.dataframe(details, use_container_width=True)

    st.info(
        "This dashboard uses sample data for demonstration."
    )
