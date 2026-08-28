import os

# Definición de carpetas y archivos a crear
project_structure = {
    "config/__init__.py": "",
    "config/settings.py": '''APP_TITLE = "Sistema de Gestión de Prácticas Profesionales — ICI UNACH"
APP_ICON = "🎓"

URLS_GIBBS = {
    "Práctica Intermedia 1 (174 hrs)": "https://tally.so/r/RGyjWK",
    "Práctica Intermedia 2 (174 hrs)": "https://tally.so/r/0QRkQ9",
    "Práctica Profesional (522 hrs)": "https://tally.so/r/gD6zDP"
}

# Configuración de escala de 1 a 100 con aprobación en 51 pts (4.0)
EXIGENCIA_APROBACION = 51.0
NOTA_MINIMA = 1.0
NOTA_APROBACION = 4.0
NOTA_MAXIMA = 7.0
''',
    "services/__init__.py": "",
    "services/grading_service.py": '''from config.settings import EXIGENCIA_APROBACION, NOTA_MINIMA, NOTA_APROBACION, NOTA_MAXIMA

class GradingService:
    @staticmethod
    def calculate_unach_grade(score: float) -> float:
        """
        Calcula la nota oficial chilena (1.0 - 7.0) a partir de un puntaje de 1 a 100.
        Puntaje 51.0 representa la exigencia mínima para nota 4.0.
        """
        try:
            p = float(score)
            if p <= 1.0:
                return NOTA_MINIMA
            if p >= 100.0:
                return NOTA_MAXIMA
            
            if p < EXIGENCIA_APROBACION:
                # Tramo reprobatorio: 1 a 50 pts -> 1.0 a 3.9
                grade = NOTA_MINIMA + (p / EXIGENCIA_APROBACION) * (3.9 - NOTA_MINIMA)
            else:
                # Tramo aprobatorio: 51 a 100 pts -> 4.0 a 7.0
                grade = NOTA_APROBACION + ((p - EXIGENCIA_APROBACION) / (100.0 - EXIGENCIA_APROBACION)) * (NOTA_MAXIMA - NOTA_APROBACION)
            
            return round(grade, 1)
        except (ValueError, TypeError):
            return NOTA_MINIMA
''',
    "services/supabase_client.py": '''import streamlit as st
from supabase import create_client, Client

class SupabaseService:
    def __init__(self, url: str = None, key: str = None):
        self.url = url or st.secrets.get("SUPABASE_URL", "")
        self.key = key or st.secrets.get("SUPABASE_KEY", "")
        self.client: Client = None
        if self.url and self.key:
            self.client = create_client(self.url, self.key)

    def is_connected(self) -> bool:
        return self.client is not None

    def fetch_evaluations(self, table_name: str = "evaluaciones"):
        if not self.client:
            raise ConnectionError("Cliente Supabase no inicializado.")
        response = self.client.table(table_name).select("*").execute()
        return response.data
''',
    "views/__init__.py": "",
    "views/dashboard.py": '''import streamlit as st

def render_dashboard_view():
    st.header("📊 Panel de Control Académico")
    st.caption("Visión general del estado de los procesos de prácticas ICI.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Estudiantes Activos", "28", delta="+4 este mes")
    m2.metric("Evaluaciones Recibidas", "18", delta="60% completado")
    m3.metric("Promedio General", "5.6", delta="0.2 vs periodo anterior")
    m4.metric("Empresas Vinculadas", "15")
    
    st.divider()
''',
    "views/evaluations.py": '''import streamlit as st
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
''',
    "views/calculator.py": '''import streamlit as st
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
''',
    "views/admin.py": '''import streamlit as st
import pandas as pd
from services.supabase_client import SupabaseService

def render_admin_view():
    st.header("⚙️ Gestión y Auditoría de Datos")
    
    db = SupabaseService()
    if not db.is_connected():
        st.warning("Ingrese credenciales de Supabase en Secrets o configuración para continuar.")
        return

    st.success("✅ Conexión con Supabase establecida.")
    table = st.text_input("Tabla destino:", value="evaluaciones")
    
    if st.button("🔄 Sincronizar Registros"):
        try:
            data = db.fetch_evaluations(table)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                st.download_button("📥 Exportar Reporte CSV", df.to_csv(index=False), "reporte_practicas.csv", "text/csv")
            else:
                st.info("No hay registros almacenados en la tabla especificada.")
        except Exception as e:
            st.error(f"Error al consultar la base de datos: {e}")
''',
    "app.py": '''import streamlit as st
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
''',
    "requirements.txt": '''streamlit
pandas
supabase
'''
}

def create_project():
    for path, content in project_structure.items():
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Creado: {path}")

if __name__ == "__main__":
    create_project()
    print("\n¡Estructura modular creada exitosamente!")