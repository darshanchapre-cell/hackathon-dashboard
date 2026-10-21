import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hackathon Dashboard", layout="wide")
st.title("📊 Hackathon Dashboard")
st.write("Yahan apne challenge ka short summary likho.")

# Demo data — baad mein apne challenge ke data se replace karna
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Users": [120, 180, 150, 240, 310],
    "Category": ["A", "B", "A", "B", "A"]
})

col1, col2 = st.columns(2)
col1.metric("Total users", f"{df['Users'].sum():,}")
col2.metric("Monthly average", f"{df['Users'].mean():.0f}")

st.subheader("Users over time")
fig = px.line(df, x="Month", y="Users", markers=True)
st.plotly_chart(fig, use_container_width=True)

category = st.selectbox("Category choose karo", df["Category"].unique())
st.dataframe(df[df["Category"] == category], use_container_width=True)
