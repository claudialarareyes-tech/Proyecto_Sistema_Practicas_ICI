import streamlit as st
from config.settings import APP_TITLE, APP_ICON
from views.dashboard import render_dashboard_view
from views.evaluations import render_evaluations_view
from views.calculator import render_calculator_view
from views.admin import render_admin_view

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

def main():
    st.title(f"{APP_ICON} {APP_TITLE}")

    tab_dash, tab_eval, tab_calc, tab_admin = st.tabs([
        "📊 Dashboard", 
        "📝 Evaluaciones", 
        "🧮 Calculadora de Notas", 
        "⚙️ Administración Backend"
    ])

    with tab_dash:
        render_dashboard_view()
    with tab_eval:
        render_evaluations_view()
    with tab_calc:
        render_calculator_view()
    with tab_admin:
        render_admin_view()

if __name__ == "__main__":
    main()
