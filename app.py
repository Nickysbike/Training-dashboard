import streamlit as st
import time

HFMAX = 180

def pulsbereich(prozent_min, prozent_max):
    min_bpm = int(HFMAX * prozent_min / 100)
    max_bpm = int(HFMAX * prozent_max / 100)
    return f"{prozent_min:.0f}–{prozent_max:.0f}% HFmax ({min_bpm}–{max_bpm} bpm)"

training_programs = {
    "GA1 – Grundlagen moderat": [
        {"name": "Warm-up", "duration": 1, "intensity": pulsbereich(60, 70), "notes": "lockeres Einrollen"},
        {"name": "Intervall 1", "duration": 1, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Pause", "duration": 1, "intensity": pulsbereich(55, 65), "notes": "Erholung"},
        {"name": "Intervall 2", "duration": 1, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Cooldown", "duration": 1, "intensity": pulsbereich(60, 65), "notes": "austreten"}
    ]
}

st.title("🚴‍♂️ Trainingsdashboard mit manuellem Timer")
st.subheader("Wähle dein Training")

selected_program = st.selectbox("Trainingsvariante", list(training_programs.keys()))

if "phase_index" not in st.session_state:
    st.session_state.phase_index = 0
if "current_program" not in st.session_state or st.session_state.current_program != selected_program:
    st.session_state.phase_index = 0
    st.session_state.current_program = selected_program

training = training_programs[selected_program]

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 0

if st.session_state.phase_index < len(training):
    phase = training[st.session_state.phase_index]
    st.markdown(f"## Phase {st.session_state.phase_index + 1}: {phase['name']}")
    st.write(f"🕒 Dauer: {phase['duration']} Minuten")
    st.write(f"❤️‍🔥 Ziel-HF: {phase['intensity']}")
    st.write(f"📌 Hinweis: {phase['notes']}")

    total_seconds = phase['duration'] * 60
    if st.session_state.remaining_seconds == 0:
        st.session_state.remaining_seconds = total_seconds

    # Countdown anzeigen
    mins, secs = divmod(st.session_state.remaining_seconds, 60)
    st.markdown(f"## ⏱️ Zeit: {mins:02d}:{secs:02d}")

    # Steuerungsbuttons
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

    # Zurück-Button (außer bei erster Phase)
    if st.session_state.phase_index > 0:
        if st.button("⬅️ Zurück"):
            st.session_state.phase_index -= 1
            st.session_state.remaining_seconds = 0
            st.session_state.timer_running = False

    # Automatische Aktualisierung (nur wenn Timer läuft)
    if st.session_state.timer_running and st.session_state.remaining_seconds > 0:
        time.sleep(1)
        st.session_state.remaining_seconds -= 1
        st.experimental_rerun()
else:
    st.success("🎉 Training abgeschlossen!")
    if st.button("🔁 Zurück zum Start"):
        st.session_state.phase_index = 0
        st.session_state.remaining_seconds = 0
        st.session_state.timer_running = False
