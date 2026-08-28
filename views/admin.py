import streamlit as st
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
