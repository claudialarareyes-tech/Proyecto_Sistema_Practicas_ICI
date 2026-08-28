import streamlit as st

def render_dashboard_view():
    st.header("📊 Panel de Control Académico")
    st.caption("Visión general del estado de los procesos de prácticas ICI.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Estudiantes Activos", "28", delta="+4 este mes")
    m2.metric("Evaluaciones Recibidas", "18", delta="60% completado")
    m3.metric("Promedio General", "5.6", delta="0.2 vs periodo anterior")
    m4.metric("Empresas Vinculadas", "15")
    
    st.divider()
