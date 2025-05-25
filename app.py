import streamlit as st

training_session = [
    {"name": "Warm-up", "duration": 10, "intensity": "locker", "notes": "3x 20 Sek hohe Frequenz"},
    {"name": "Intervall 1", "duration": 8, "intensity": "GA1", "notes": "90–95 rpm, 70–75% FTP"},
    {"name": "Pause", "duration": 2, "intensity": "sehr locker", "notes": ""},
    {"name": "Intervall 2", "duration": 8, "intensity": "GA1", "notes": "90–95 rpm, 70–75% FTP"},
    {"name": "Pause", "duration": 2, "intensity": "sehr locker", "notes": ""},
    {"name": "Intervall 3", "duration": 8, "intensity": "GA1", "notes": "90–95 rpm, 70–75% FTP"},
    {"name": "Cooldown", "duration": 10, "intensity": "locker", "notes": "progressiv von 80 bis 100 rpm"}
]

st.title("🚴‍♂️ Trainingsdashboard – Rolleinheit")
st.write("Heute: Moderate Einheit (ca. 50 Min)")

for i, step in enumerate(training_session):
    st.markdown(f"### {i+1}. {step['name']} – {step['duration']} Min – *{step['intensity']}*")
    st.caption(step["notes"])
