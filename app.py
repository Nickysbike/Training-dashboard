import streamlit as st

HFMAX = 180

def pulsbereich(prozent_min, prozent_max):
    min_bpm = int(HFMAX * prozent_min / 100)
    max_bpm = int(HFMAX * prozent_max / 100)
    return f"{prozent_min:.0f}–{prozent_max:.0f}% HFmax ({min_bpm}–{max_bpm} bpm)"

training_programs = {
    "GA1 – Grundlagen moderat": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": "lockeres Einrollen"},
        {"name": "Intervall 1", "duration": 15, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Pause", "duration": 5, "intensity": pulsbereich(55, 65), "notes": "Erholung"},
        {"name": "Intervall 2", "duration": 10, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Cooldown", "duration": 10, "intensity": pulsbereich(60, 65), "notes": "austreten"}
    ],
    "Fahrtspiel": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": ""},
        {"name": "4x Tempowechsel", "duration": 20, "intensity": pulsbereich(75, 85), "notes": "Wechsel zwischen zügig (3 Min) & locker (2 Min)"},
        {"name": "2x Sprint", "duration": 2, "intensity": pulsbereich(90, 95), "notes": "2x 1 Min Sprint mit 1 Min Pause"},
        {"name": "Cooldown", "duration": 10, "intensity": pulsbereich(60, 65), "notes": ""}
    ],
    "Schwellentraining – FTP-orientiert": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": "inkl. 3x 30 Sek. hohe Trittfrequenz"},
        {"name": "Schwelle 1", "duration": 10, "intensity": pulsbereich(85, 90), "notes": ""},
        {"name": "Pause", "duration": 4, "intensity": pulsbereich(60, 65), "notes": ""},
        {"name": "Schwelle 2", "duration": 10, "intensity": pulsbereich(85, 90), "notes": ""},
        {"name": "Cooldown", "duration": 10, "intensity": pulsbereich(60, 65), "notes": ""}
    ],
    "VO₂max Training": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": ""},
        {"name": "6x 2 Min intensiv", "duration": 12, "intensity": pulsbereich(90, 95), "notes": "Mit je 2 Min Pause"},
        {"name": "Cooldown", "duration": 10, "intensity": pulsbereich(60, 65), "notes": ""}
    ],
    "Recovery Ride": [
        {"name": "Recovery", "duration": 30, "intensity": pulsbereich(55, 65), "notes": "Erholungstraining, locker"}
    ],
    "Kombi GA1 + VO₂max": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": ""},
        {"name": "GA1 Teil 1", "duration": 15, "intensity": pulsbereich(70, 75), "notes": ""},
        {"name": "VO₂max Blöcke", "duration": 12, "intensity": pulsbereich(90, 95), "notes": "3x 2 Min mit Pause"},
        {"name": "GA1 Teil 2", "duration": 10, "intensity": pulsbereich(70, 75), "notes": ""},
        {"name": "Cooldown", "duration": 10, "intensity": pulsbereich(60, 65), "notes": ""}
    ]
}

st.title("🚴‍♂️ Interaktives Trainingsdashboard")
st.subheader("Wähle dein Training")

selected_program = st.selectbox("Trainingsvariante", list(training_programs.keys()))

if "phase_index" not in st.session_state:
    st.session_state.phase_index = 0
if "current_program" not in st.session_state or st.session_state.current_program != selected_program:
    st.session_state.phase_index = 0
    st.session_state.current_program = selected_program

training = training_programs[selected_program]

if st.session_state.phase_index < len(training):
    phase = training[st.session_state.phase_index]
    st.markdown(f"## Phase {st.session_state.phase_index + 1}: {phase['name']}")
    st.write(f"🕒 Dauer: {phase['duration']} Minuten")
    st.write(f"❤️‍🔥 Ziel-HF: {phase['intensity']}")
    st.write(f"📌 Hinweis: {phase['notes']}")
    if st.button("✅ Nächste Phase starten"):
        st.session_state.phase_index += 1
else:
    st.success("🎉 Training abgeschlossen!")
    if st.button("🔁 Zurück zum Start"):
        st.session_state.phase_index = 0
