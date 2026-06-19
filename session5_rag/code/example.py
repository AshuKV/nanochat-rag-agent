import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 1️⃣  Prepare the data (copy/paste from your context)
# ------------------------------------------------------------------
data = {
    "Year": [2019, 2020, 2021, 2022, 2023, 2024],
    "Total Revenue (M$)": [
        11_171,  # 2019
        12_868,  # 2020
        15_785,  # 2021
        17_606,  # 2022
        19_409,  # 2023
        21_505  # 2024 (latest)
    ]
}

df = pd.DataFrame(data)

# ------------------------------------------------------------------
# 2️⃣  Compute YoY growth %
# ------------------------------------------------------------------
df["YoY Growth (%)"] = df["Total Revenue (M$)"].pct_change() * 100

# ------------------------------------------------------------------
# 3️⃣  Streamlit UI
# ------------------------------------------------------------------
st.set_page_config(page_title="Adobe Revenue Growth", layout="wide")

st.title("📈 Adobe Inc. – Total Revenue & YoY Growth")
st.markdown(
    """
    This simple dashboard shows Adobe’s **Total Revenue** (in millions of dollars) and the corresponding year‑over‑year growth rate.

    Data source: Adobe Consolidated Statements of Income (latest 6 quarters).
    """
)

# ------------------------------------------------------------------
# 4️⃣  Plotting
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5), tight_layout=True)

# Revenue bar chart
axes[0].bar(df["Year"], df["Total Revenue (M$)"], color="#0073e6")
axes[0].set_title("Total Revenue (Millions USD)")
axes[0].set_xlabel("Fiscal Year")
axes[0].set_ylabel("Revenue ($M)")
axes[0].grid(axis="y", linestyle="--", alpha=0.4)

# YoY growth line chart
axes[1].plot(df["Year"], df["YoY Growth (%)"], marker="o", color="#e60000")
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].set_title("Year‑over‑Year Revenue Growth")
axes[1].set_xlabel("Fiscal Year")
axes[1].set_ylabel("Growth (%)")
axes[1].grid(True, linestyle="--", alpha=0.4)

# Render the figure in Streamlit
st.pyplot(fig)

# ------------------------------------------------------------------
# 5️⃣  Optional: Show raw data table
# ------------------------------------------------------------------
if st.checkbox("Show raw data"):
    st.dataframe(df.style.format({"Total Revenue (M$)": "{:,}", "YoY Growth (%)": "{:.2f}%"}))
