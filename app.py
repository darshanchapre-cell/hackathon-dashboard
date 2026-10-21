import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML

# Sirf demo data; kisi asli patient ki jaankari nahi
df = pd.DataFrame({
    "Department": ["Cardiology", "Pediatrics", "Orthopedics", "General Medicine", "Neurology"],
    "Patients": [42, 35, 28, 51, 19],
    "Available Beds": [8, 12, 6, 10, 5]
})

total_patients = df["Patients"].sum()
total_beds = df["Available Beds"].sum()

display(HTML(f"""
<h2 style="font-family:Arial">🏥 Hospital Overview</h2>
<p style="font-family:Arial;color:#555">Demo dashboard — sample data</p>
<div style="display:flex;gap:15px;font-family:Arial">
  <div style="background:#e8f0fe;padding:18px;border-radius:10px">
    <b>Patients today</b><br><span style="font-size:28px">{total_patients}</span>
  </div>
  <div style="background:#e6f4ea;padding:18px;border-radius:10px">
    <b>Available beds</b><br><span style="font-size:28px">{total_beds}</span>
  </div>
  <div style="background:#fff4e5;padding:18px;border-radius:10px">
    <b>Departments</b><br><span style="font-size:28px">{len(df)}</span>
  </div>
</div>
"""))

plt.figure(figsize=(9, 4))
plt.bar(df["Department"], df["Patients"], color="#4285F4")
plt.title("Patients by Department")
plt.ylabel("Patient count")
plt.xticks(rotation=20, ha="right")
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.show()

display(df)
