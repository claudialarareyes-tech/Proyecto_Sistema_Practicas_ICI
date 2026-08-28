import streamlit as st
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
