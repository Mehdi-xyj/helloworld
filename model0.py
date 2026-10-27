import streamlit as st

# Define the pages
model1 = st.Page("model1.py", title="黄酒工艺仿真系统", icon="🏺")
model2 = st.Page("model2.py", title="黄酒工艺仿真模型技术说明书", icon="📑")

# Set up navigation
pg = st.navigation([model1, model2])

# Run the selected page
pg.run()