import streamlit as st
from config.settings import URLS_GIBBS

def render_evaluations_view():
    st.header("📝 Formulario de Evaluación Empresarial")
    
    col_sel, col_info = st.columns([1, 2])
    with col_sel:
        level = st.selectbox("Seleccione Nivel de Práctica:", list(URLS_GIBBS.keys()))
    with col_info:
        st.info("💡 **Regla de Evaluación:** Puntuación de 1 a 100 puntos. Exigencia del 51% para nota 4.0.")

    url = URLS_GIBBS[level]
    st.components.v1.iframe(url, height=750, scrolling=True)
