
import pandas as pd
import plotly.express as px
from IPython.display import display, HTML

# Demo data — apna data milne par ise replace karenge
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Users": [120, 180, 150, 240, 310],
    "Category": ["A", "B", "A", "B", "A"]
})

fig = px.bar(df, x="Month", y="Users", color="Category",
             title="Monthly Users", text="Users")
fig.show()

display(HTML(f"""
<div style="display:flex;gap:16px;font-family:Arial">
  <div style="padding:20px;background:#e8f0fe;border-radius:12px">
    <b>Total users</b><br><span style="font-size:28px">{df['Users'].sum():,}</span>
  </div>
  <div style="padding:20px;background:#e6f4ea;border-radius:12px">
    <b>Monthly average</b><br><span style="font-size:28px">{df['Users'].mean():.0f}</span>
  </div>
</div>
"""))

display(df)
