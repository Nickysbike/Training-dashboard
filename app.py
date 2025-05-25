import streamlit as st

# Beispielhafte HFmax für Nutzer (kann später individuell einstellbar gemacht werden)
HFMAX = 180

def pulsbereich(prozent_min, prozent_max):
    min_bpm = int(HFMAX * prozent_min / 100)
    max_bpm = int(HFMAX * prozent_max / 100)
    return f"{prozent_min:.0f}–{prozent_max:.0f}% HFmax ({min_bpm}–{max_bpm} bpm)"

# Trainingsprogramme
training_programs = {
    "GA1 – Grundlagen moderat": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": "lockeres Einrollen"},
        {"name": "Intervall 1", "duration": 15, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Pause", "duration": 5, "intensity": pulsbereich(55, 65), "notes": "Erholung"},
        {"name": "Intervall 2", "duration": 10, "intensity": pulsbereich(70, 75), "notes": "GA1 konstant"},
        {"name": "Cooldown", "duration": 10, "intensity": pulsbereich(60, 65), "notes": "austreten"}
    ],
    "VO₂max Training": [
        {"name": "Warm-up", "duration": 10, "intensity": pulsbereich(60, 70), "notes": ""},
        {"name": "Intervall 1", "duration": 2, "intensity": pulsbereich(90, 95), "notes": "intensiv"},
        {"name": "Pause", "duration": 2, "intensity": pulsbereich(60, 65), "notes": ""},
        {"name": "Intervall 2", "duration": 2, "intensity": pulsbereich(90, 95), "notes": "intensiv"},
        {"name": "Pause", "duration": 2, "intensity": pulsbereich(60, 65), "notes": ""},
        {"name": "Intervall 3", "duration": 2, "intensity": pulsbereich(90, 95), "notes": "intensiv"},
        {"name": "Pause", "duration": 2, "intensity": pulsbereich(60, 65), "notes": ""},
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
