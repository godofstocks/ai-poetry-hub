import streamlit as st
import requests
import os

# We will set this variable in Railway later
HUB_URL = os.getenv("HUB_URL", "http://localhost:8000")

st.title("📜 AI Poetry Hub")

# Controls
col1, col2, col3 = st.columns(3)
if col1.button("▶️ Start"): requests.post(f"{HUB_URL}/hub/control?action=start")
if col2.button("🛑 End"): requests.post(f"{HUB_URL}/hub/control?action=end")
if col3.button("🔄 Reset"): requests.post(f"{HUB_URL}/hub/control?action=reset")

# Display
res = requests.get(f"{HUB_URL}/hub").json()
st.write(f"**Status:** {'🟢 Active' if res['is_running'] else '🔴 Paused'}")

for p in res['poem']:
    st.markdown(f"**{p['agent_name']}**: {p['line']}")

if st.button("Refresh Feed"):
    st.rerun()
