import sys
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
