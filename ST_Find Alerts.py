import requests
import pandas as pd
import streamlit as st

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="NWS Active Alerts", layout="wide")
st.title("🌩️ National Weather Service: Active Alerts")
st.markdown("By Cameron Wang")
st.markdown(
    "Retrieve realtime weather alerts from the **National Weather Service API**."
)

# Input: choose a state (optional)
state = st.text_input("Enter a 2-letter state code (e.g., CA, TX, NY). Leave blank for all states:", "")

# Fetch alerts
url = "https://api.weather.gov/alerts/active"
headers = {"User-Agent": "streamlit-nws-app (wangcameron@gmail.com)"}

params = {}
if state.strip():
    params["area"] = state.strip().upper()

st.write("🔄 Fetching alerts...")
response = requests.get(url, headers=headers, params=params)
if response.status_code != 200:
    st.error(f"Failed to fetch data: {response.status_code}")
    st.stop()

data = response.json()
alerts = data.get("features", [])

# No alerts
if not alerts:
    st.success("✅ No active alerts found.")
    st.stop()

# Parse into DataFrame
rows = []
for alert in alerts:
    props = alert.get("properties", {})
    rows.append({
        "Event": props.get("event"),
        "Area": props.get("areaDesc"),
        "Severity": props.get("severity"),
        "Certainty": props.get("certainty"),
        "Urgency": props.get("urgency"),
        "Effective": props.get("effective"),
        "Expires": props.get("expires"),
        "Description": props.get("description"),
        "Instruction": props.get("instruction"),
        "NWS Office": props.get("senderName"),
        "Alert ID": props.get("id"),
    })

df = pd.DataFrame(rows)

# Display summary
st.subheader(f"Found {len(df)} active alerts")
st.dataframe(df[["Event", "Area", "Severity", "Effective", "Expires"]], use_container_width=True)

# Expand details for each alert
with st.expander("📋 Full Alert Details"):
    st.dataframe(df, use_container_width=True)

# Download CSV option
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Alerts as CSV", csv, "nws_alerts.csv", "text/csv")

githuburl = "https://github.com/TeaDragonSC/NWS-Experiment/"
linkedinurl = "https://www.linkedin.com/in/cameron-wang-sio/"
st.markdown("[GitHub](https://github.com/TeaDragonSC/NWS-Experiment/) | [LinkedIn](https://www.linkedin.com/in/cameron-wang-sio/)")
