import streamlit as st
import time

HFMAX = 180

def pulsbereich(prozent_min, prozent_max):
    min_bpm = int(HFMAX * prozent_min / 100)
    max_bpm = int(HFMAX * prozent_max / 100)
    return f"{prozent_min:.0f}–{prozent_max:.0f}% HFmax ({min_bpm}–{max_bpm} bpm)"

training_programs = {
    "GA1 – Grundlagen moderat": [
        {"name": "Warm-up", "duration": 5, "intensity": pulsbereich(60, 70), "notes": "lockeres Einrollen"},
        {"name": "Intervall 1", "duration": 10, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Pause", "duration": 5, "intensity": pulsbereich(55, 65), "notes": "Erholung"},
        {"name": "Intervall 2", "duration": 10, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Cooldown", "duration": 5, "intensity": pulsbereich(60, 65), "notes": "austreten"}
    ],
    "GA2 – Grundlage intensiv": [
        {"name": "Warm-up", "duration": 5, "intensity": pulsbereich(60, 70), "notes": "lockeres Einrollen"},
        {"name": "Intervall 1", "duration": 8, "intensity": pulsbereich(75, 80), "notes": "GA2 Belastung"},
        {"name": "Pause", "duration": 4, "intensity": pulsbereich(55, 65), "notes": "Erholung"},
        {"name": "Intervall 2", "duration": 8, "intensity": pulsbereich(75, 80), "notes": "GA2 Belastung"},
        {"name": "Cooldown", "duration": 5, "intensity": pulsbereich(60, 65), "notes": "austreten"}
    ],
    "FTP-Test": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": "lockeres Einrollen"},
        {"name": "All-Out Test", "duration": 20, "intensity": "Maximale Leistung", "notes": "Konstant am Limit"},
        {"name": "Cooldown", "duration": 10, "intensity": pulsbereich(60, 65), "notes": "lockeres Ausrollen"}
    ],
    "VO2max-Intervalle": [
        {"name": "Warm-up", "duration": 5, "intensity": pulsbereich(60, 70), "notes": "locker einrollen"},
        {"name": "VO2max Intervall", "duration": 4, "intensity": pulsbereich(90, 95), "notes": "hochintensive Belastung"},
        {"name": "Pause", "duration": 4, "intensity": pulsbereich(55, 65), "notes": "lockere Erholung"},
        {"name": "VO2max Intervall", "duration": 4, "intensity": pulsbereich(90, 95), "notes": "hochintensive Belastung"},
        {"name": "Cooldown", "duration": 5, "intensity": pulsbereich(60, 65), "notes": "austreten"}
    ],
    "K3-Kraftausdauer": [
        {"name": "Warm-up", "duration": 5, "intensity": pulsbereich(60, 70), "notes": "locker einrollen"},
        {"name": "Berg-Simulation", "duration": 8, "intensity": pulsbereich(80, 85), "notes": "hohe Übersetzung, niedrige Trittfrequenz"},
        {"name": "Pause", "duration": 5, "intensity": pulsbereich(55, 65), "notes": "Erholung"},
        {"name": "Berg-Simulation", "duration": 8, "intensity": pulsbereich(80, 85), "notes": "zweite Runde"},
        {"name": "Cooldown", "duration": 5, "intensity": pulsbereich(60, 65), "notes": "locker ausrollen"}
    ],
    "Regeneration": [
        {"name": "Regeneratives Fahren", "duration": 30, "intensity": pulsbereich(55, 65), "notes": "komplett locker bleiben"},
    ]
}

st.title("🚴‍♂️ Trainings-Dashboard")
selected_program = st.selectbox("Wähle dein Trainingsprogramm:", list(training_programs.keys()))

if "phase_index" not in st.session_state:
    st.session_state.phase_index = 0
if "current_program" not in st.session_state or st.session_state.current_program != selected_program:
    st.session_state.phase_index = 0
    st.session_state.current_program = selected_program
    st.session_state.remaining_seconds = 0
    st.session_state.timer_running = False

training = training_programs[selected_program]

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 0

if st.session_state.phase_index < len(training):
    phase = training[st.session_state.phase_index]
    st.subheader(f"Phase {st.session_state.phase_index + 1}: {phase['name']}")
    st.write(f"🕒 Dauer: {phase['duration']} Minuten")
    st.write(f"❤️‍🔥 Intensität: {phase['intensity']}")
    st.write(f"📌 Hinweis: {phase['notes']}")

    total_seconds = phase['duration'] * 60
    if st.session_state.remaining_seconds == 0:
        st.session_state.remaining_seconds = total_seconds

    mins, secs = divmod(st.session_state.remaining_seconds, 60)
    st.markdown(f"## ⏱️ Zeit: {mins:02d}:{secs:02d}")

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("▶️ Start"):
        st.session_state.timer_running = True
    if col2.button("⏸️ Pause"):
        st.session_state.timer_running = False
    if col3.button("🔁 Reset"):
        st.session_state.remaining_seconds = total_seconds
        st.session_state.timer_running = False
    if col4.button("➡️ Weiter"):
        st.session_state.phase_index += 1
        st.session_state.remaining_seconds = 0
        st.session_state.timer_running = False
        st.rerun()

    if st.session_state.phase_index > 0:
        if st.button("⬅️ Zurück"):
            st.session_state.phase_index -= 1
            st.session_state.remaining_seconds = 0
            st.session_state.timer_running = False
            st.rerun()

    if st.session_state.timer_running and st.session_state.remaining_seconds > 0:
        time.sleep(1)
        st.session_state.remaining_seconds -= 1
        st.rerun()
else:
    st.success("🎉 Training abgeschlossen!")
    if st.button("🔁 Training von vorn starten"):
        st.session_state.phase_index = 0
        st.session_state.remaining_seconds = 0
        st.session_state.timer_running = False
        st.rerun()
