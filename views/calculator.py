import sys
from pathlib import Path
import streamlit as st

root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from services.grading_service import GradingService

def render_calculator_view():
    st.header("📊 Simulador de Calificación UNACH")
    st.write("Verifique el resultado en la escala institucional (1-100 pts, Aprobación >= 51 pts).")

    score = st.number_input(
        "Puntaje Obtenido (1 a 100 pts):",
        min_value=1.0,
        max_value=100.0,
        value=51.0,
        step=1.0
    )

    grade = GradingService.evaluate_score(score)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Puntaje Evaluación", f"{grade['score']} pts")
    with c2:
        st.metric("Estado Final", grade["status"])
