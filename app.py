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

if "phase_index" not in st.session_state:
    st.session_state.phase_index = 0

st.title("🚴‍♂️ Interaktives Trainingsdashboard")
st.subheader("🎯 Einheit: ca. 50 Minuten – Intervallbasiert")

if st.session_state.phase_index < len(training_session):
    phase = training_session[st.session_state.phase_index]
    st.markdown(f"## Phase {st.session_state.phase_index + 1}: {phase['name']}")
    st.write(f"🕒 Dauer: {phase['duration']} Minuten")
    st.write(f"🔥 Intensität: *{phase['intensity']}*")
    st.write(f"📌 Hinweis: {phase['notes']}")

    if st.button("✅ Phase abschließen & nächste starten"):
        st.session_state.phase_index += 1
        st.experimental_rerun()
else:
    st.success("🎉 Alle Phasen abgeschlossen! Gut gemacht!")
    if st.button("🔄 Zurück zum Anfang"):
        st.session_state.phase_index = 0
        st.experimental_rerun()
