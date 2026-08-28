import streamlit as st
from services.grading_service import GradingService

def render_calculator_view():
    st.header("🧮 Simulador de Calificación UNACH")
    st.write("Verifique la conversión entre el puntaje asignado por la empresa (1-100 pts) y la nota oficial.")

    score = st.number_input("Puntaje Obtenido (1 a 100 pts):", min_value=1.0, max_value=100.0, value=51.0, step=1.0)
    grade = GradingService.calculate_unach_grade(score)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Puntaje Evaluación", f"{score} pts")
    with c2:
        status = "Aprobado" if grade >= 4.0 else "Reprobado"
        st.metric("Nota Final UNACH", f"{grade}", delta=status, delta_color="normal" if grade >= 4.0 else "inverse")
