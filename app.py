import streamlit as st
import time

# Trainingsdaten
training_programs = {
    "30 Minuten": {
        "Regenerationseinheit": [
            {"phase": "Warm-up", "dauer": 5, "intensität": "sehr leicht"},
            {"phase": "Fahrtspiel", "dauer": 20, "intensität": "leicht"},
            {"phase": "Cool-down", "dauer": 5, "intensität": "sehr leicht"}
        ],
        "Jon's Short Mix": [
            {"phase": "Warm-up", "dauer": 5, "intensität": "leicht"},
            {"phase": "3x 1min hart", "dauer": 3, "intensität": "intensiv"},
            {"phase": "Cool-down", "dauer": 5, "intensität": "leicht"}
        ]
    },
    "60 Minuten": {
        "GA1 – Grundlagen moderat": [
            {"phase": "Warm-up", "dauer": 10, "intensität": "leicht"},
            {"phase": "Grundlagenausdauer", "dauer": 40, "intensität": "moderat"},
            {"phase": "Cool-down", "dauer": 10, "intensität": "leicht"}
        ],
        "The McCarthy Special": [
            {"phase": "Warm-up", "dauer": 10, "intensität": "leicht"},
            {"phase": "5x 4min VO2max", "dauer": 20, "intensität": "intensiv"},
            {"phase": "Cool-down", "dauer": 10, "intensität": "leicht"}
        ]
    },
    "90 Minuten": {
        "SST (Med)": [
            {"phase": "Warm-up", "dauer": 15, "intensität": "leicht"},
            {"phase": "2x 20min sweet spot", "dauer": 40, "intensität": "mittel"},
            {"phase": "Cool-down", "dauer": 15, "intensität": "leicht"}
        ],
        "Kombination: GA1 + Regenerationseinheit*": [
            {"phase": "GA1", "dauer": 60, "intensität": "moderat"},
            {"phase": "Regeneration", "dauer": 30, "intensität": "leicht"}
        ]
    }
}

# App-Titel
st.title("🏋️‍♂️ Trainings-Dashboard")

# Auswahl der Dauer
selected_duration = st.selectbox("⏱️ Wähle Trainingsdauer:", list(training_programs.keys()))

# Auswahl des Programms basierend auf Dauer
if selected_duration:
    programs = list(training_programs[selected_duration].keys())
    selected_program = st.selectbox("📋 Wähle Trainingsprogramm:", programs)

    if selected_program:
        training_plan = training_programs[selected_duration][selected_program]

        # Initialisierung des Session State
        if "current_phase" not in st.session_state:
            st.session_state.current_phase = 0
        if "timer_running" not in st.session_state:
            st.session_state.timer_running = False
        if "timer_start_time" not in st.session_state:
            st.session_state.timer_start_time = None

        # Anzeige der aktuellen Phase
        current = training_plan[st.session_state.current_phase]
        st.subheader(f"🔄 Phase {st.session_state.current_phase + 1} von {len(training_plan)}")
        st.markdown(f"**🏷️ Name:** {current['phase']}")
        st.markdown(f"**⏳ Dauer:** {current['dauer']} Minuten")
        st.markdown(f"**🔥 Intensität:** {current['intensität']}")

        # Timer-Logik
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start Timer") and not st.session_state.timer_running:
                st.session_state.timer_running = True
                st.session_state.timer_start_time = time.time()
        with col2:
            if st.button("⏹️ Stop Timer"):
                st.session_state.timer_running = False

        if st.session_state.timer_running and st.session_state.timer_start_time:
            elapsed_time = int(time.time() - st.session_state.timer_start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            st.info(f"⏱️ Laufzeit: {minutes:02d}:{seconds:02d} Minuten")

        # Navigation
        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button("⬅️ Zurück") and st.session_state.current_phase > 0:
                st.session_state.current_phase -= 1
                st.session_state.timer_running = False
        with nav2:
            if st.button("➡️ Weiter") and st.session_state.current_phase < len(training_plan) - 1:
                st.session_state.current_phase += 1
                st.session_state.timer_running = False
