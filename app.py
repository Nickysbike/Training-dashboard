import streamlit as st
import time

HFMAX = 180  # Beispiel – falls du deine HFmax kennst, kannst du hier anpassen


# -------------------------------------------------
# Hilfsfunktion für Pulsbereiche
# -------------------------------------------------
def pulsbereich(min_pct, max_pct):
    bpm_min = int(HFMAX * min_pct / 100)
    bpm_max = int(HFMAX * max_pct / 100)
    return f"{min_pct:.0f}–{max_pct:.0f}% HFmax ({bpm_min}–{bpm_max} bpm)"


# -------------------------------------------------
# Trainings-Datenbank: nach Dauer gruppiert
# -------------------------------------------------
training_programs = {
    "30 Minuten": {
        "Regenerationseinheit": [
            {"name": "Warm-up", "duration": 5, "intensity": pulsbereich(55, 65), "notes": "lockeres Einrollen"},
            {"name": "Fahrtspiel locker", "duration": 20, "intensity": pulsbereich(60, 70), "notes": "freies Rollen"},
            {"name": "Cool-down", "duration": 5, "intensity": pulsbereich(55, 65), "notes": "austreten"}
        ],
        "Jon's Short Mix": [
            {"name": "Warm-up", "duration": 5, "intensity": pulsbereich(60, 70), "notes": ""},
            {"name": "3× 1 min hart", "duration": 3, "intensity": pulsbereich(90, 95), "notes": "VO₂-Spitzen"},
            {"name": "Fahrtspiel", "duration": 17, "intensity": pulsbereich(70, 85), "notes": "wechselnde Belastung"},
            {"name": "Cool-down", "duration": 5, "intensity": pulsbereich(55, 65), "notes": ""}
        ]
    },
    "60 Minuten": {
        "GA1 – Grundlagen moderat": [
            {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": ""},
            {"name": "GA1-Block 1", "duration": 20, "intensity": pulsbereich(70, 75), "notes": "konstant"},
            {"name": "GA1-Block 2", "duration": 20, "intensity": pulsbereich(70, 75), "notes": "konstant"},
            {"name": "Cool-down", "duration": 10, "intensity": pulsbereich(55, 65), "notes": ""}
        ],
        "The McCarthy Special": [
            {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": ""},
            {"name": "Block 1", "duration": 3, "intensity": pulsbereich(90, 95), "notes": "VO₂-max"},
            {"name": "Erholung", "duration": 9, "intensity": pulsbereich(55, 65), "notes": ""},
            {"name": "Block 2", "duration": 3, "intensity": pulsbereich(90, 95), "notes": ""},
            {"name": "Erholung", "duration": 9, "intensity": pulsbereich(55, 65), "notes": ""},
            {"name": "Block 3", "duration": 3, "intensity": pulsbereich(90, 95), "notes": ""},
            {"name": "Cool-down", "duration": 10, "intensity": pulsbereich(55, 65), "notes": ""}
        ]
    },
    "90 Minuten": {
        "SST (Med)": [
            {"name": "Warm-up", "duration": 15, "intensity": pulsbereich(60, 70), "notes": ""},
            {"name": "Sweet-Spot 1", "duration": 20, "intensity": pulsbereich(88, 94), "notes": ""},
            {"name": "Erholung", "duration": 5, "intensity": pulsbereich(55, 65), "notes": ""},
            {"name": "Sweet-Spot 2", "duration": 20, "intensity": pulsbereich(88, 94), "notes": ""},
            {"name": "Erholung", "duration": 5, "intensity": pulsbereich(55, 65), "notes": ""},
            {"name": "Sweet-Spot 3", "duration": 20, "intensity": pulsbereich(88, 94), "notes": ""},
            {"name": "Cool-down", "duration": 5, "intensity": pulsbereich(55, 65), "notes": ""}
        ],
        "Kombi GA1 + Regeneration *": [  # * = Kombination
            {"name": "GA1", "duration": 60, "intensity": pulsbereich(70, 75), "notes": ""},
            {"name": "Regeneration", "duration": 30, "intensity": pulsbereich(55, 65), "notes": ""}
        ]
    }
}

# -------------------------------------------------
# UI – Auswahl‐Dropdowns
# -------------------------------------------------
st.title("🚴‍♂️ Trainings-Dashboard")

selected_duration = st.selectbox("🔢 Trainings­dauer wählen:", list(training_programs.keys()))
selected_program = st.selectbox(
    "📋 Trainings­programm wählen:",
    list(training_programs[selected_duration].keys())
)

# -------------------------------------------------
# Session-State initialisieren / zurücksetzen
# -------------------------------------------------
if "phase_index" not in st.session_state:
    st.session_state.phase_index = 0
if "current_key" not in st.session_state:
    st.session_state.current_key = (selected_duration, selected_program)
if st.session_state.current_key != (selected_duration, selected_program):
    # Nutzer hat Dauer oder Programm gewechselt → Timer & Phase resetten
    st.session_state.phase_index = 0
    st.session_state.remaining_seconds = 0
    st.session_state.timer_running = False
    st.session_state.current_key = (selected_duration, selected_program)

# Timer-Variablen
if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 0
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

plan = training_programs[selected_duration][selected_program]

# -------------------------------------------------
# Anzeige der aktuellen Phase
# -------------------------------------------------
if st.session_state.phase_index < len(plan):
    phase = plan[st.session_state.phase_index]

    st.subheader(f"📌 Phase {st.session_state.phase_index + 1} / {len(plan)}")
    st.markdown(f"**🏷️ Name:** {phase['name']}")
    st.markdown(f"**⏱️ Dauer:** {phase['duration']} Min")
    st.markdown(f"**🔥 Intensität:** {phase['intensity']}")
    if phase.get("notes"):
        st.markdown(f"**📝 Hinweis:** {phase['notes']}")

    # Timer-Initialisierung
    total_sec = phase["duration"] * 60
    if st.session_state.remaining_seconds == 0:
        st.session_state.remaining_seconds = total_sec

    # Timer-Anzeige
    mins, secs = divmod(st.session_state.remaining_seconds, 60)
    st.markdown(f"## ⏳ Restzeit: {mins:02d}:{secs:02d}")

    # -------------------------------------------------
    # Steuer-Buttons (Start / Pause / Reset / Weiter / Zurück)
    # -------------------------------------------------
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("▶️ Start"):
        st.session_state.timer_running = True
    if col2.button("⏸️ Pause"):
        st.session_state.timer_running = False
    if col3.button("🔁 Reset"):
        st.session_state.remaining_seconds = total_sec
        st.session_state.timer_running = False
    if col4.button("➡️ Weiter") and st.session_state.phase_index < len(plan) - 1:
        st.session_state.phase_index += 1
        st.session_state.remaining_seconds = 0
        st.session_state.timer_running = False
        st.rerun()
    if col5.button("⬅️ Zurück") and st.session_state.phase_index > 0:
        st.session_state.phase_index -= 1
        st.session_state.remaining_seconds = 0
        st.session_state.timer_running = False
        st.rerun()

    # -------------------------------------------------
    # Timer-Mechanismus (unverändert zur funktionierenden Version)
    # -------------------------------------------------
    if st.session_state.timer_running and st.session_state.remaining_seconds > 0:
        time.sleep(1)
        st.session_state.remaining_seconds -= 1
        st.rerun()

else:
    st.success("🎉 Training abgeschlossen!")
    if st.button("🔄 Von vorn starten"):
        st.session_state.phase_index = 0
        st.session_state.remaining_seconds = 0
        st.session_state.timer_running = False
        st.rerun()
