import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 1. Crear directorio .streamlit y secrets.toml dummy si no existen
streamlit_dir = BASE_DIR / ".streamlit"
streamlit_dir.mkdir(exist_ok=True)
secrets_file = streamlit_dir / "secrets.toml"

if not secrets_file.exists():
    with open(secrets_file, "w", encoding="utf-8") as f:
        f.write('# Configuración local de secretos\nSUPABASE_URL = "https://your-project.supabase.co"\nSUPABASE_KEY = "your-anon-key"\n')
    print("✓ Creado .streamlit/secrets.toml")

# 2. Configurar config/settings.py completo
settings_content = '''# Configuración general
APP_TITLE = "Sistema de Gestión de Prácticas ICI - UNACH"
APP_ICON = "🎓"

# Reglas institucionales (Escala 1.0 - 100.0)
EXIGENCIA_APROBACION = 51.0
PUNTAJE_MINIMO = 1.0
PUNTAJE_MAXIMO = 100.0

# URLs de formulación Gibbs / Tally
URLS_GIBBS = {
    "evaluacion": "https://tally.so/embed/your_form_id"
}
TALLY_EVALUACION_URL = "https://tally.so/embed/your_form_id"
'''

with open(BASE_DIR / "config" / "settings.py", "w", encoding="utf-8") as f:
    f.write(settings_content)
print("✓ Actualizado config/settings.py")

# 3. Configurar services/grading_service.py con manejo robusto de rutas y alias
grading_content = '''import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from config.settings import EXIGENCIA_APROBACION, PUNTAJE_MINIMO, PUNTAJE_MAXIMO

class GradingService:
    @staticmethod
    def evaluate_score(score: float) -> dict:
        try:
            p = float(score)
            p = max(PUNTAJE_MINIMO, min(PUNTAJE_MAXIMO, p))
            approved = p >= EXIGENCIA_APROBACION
            return {
                "score": round(p, 1),
                "approved": approved,
                "status": "Aprobado" if approved else "Reprobado"
            }
        except (ValueError, TypeError):
            return {"score": PUNTAJE_MINIMO, "approved": False, "status": "Reprobado"}

    @staticmethod
    def calculate_unach_grade(score: float) -> dict:
        return GradingService.evaluate_score(score)
'''

with open(BASE_DIR / "services" / "grading_service.py", "w", encoding="utf-8") as f:
    f.write(grading_content)
print("✓ Actualizado services/grading_service.py")

# 4. Configurar views/calculator.py
calculator_content = '''import sys
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
'''

with open(BASE_DIR / "views" / "calculator.py", "w", encoding="utf-8") as f:
    f.write(calculator_content)
print("✓ Actualizado views/calculator.py")

print("\n¡Proyecto arreglado exitosamente!")