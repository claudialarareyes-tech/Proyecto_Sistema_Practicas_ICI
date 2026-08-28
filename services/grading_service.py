from config.settings import EXIGENCIA_APROBACION, NOTA_MINIMA, NOTA_APROBACION, NOTA_MAXIMA

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
