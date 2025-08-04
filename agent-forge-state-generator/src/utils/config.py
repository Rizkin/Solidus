# src/utils/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    direct_database_url: Optional[str] = None
    
    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str
    
    # API Keys
    anthropic_api_key: Optional[str] = None
    
    # App Settings
    api_port: int = 8000
    agent_forge_mode: str = "development"
    
    # Supabase-specific settings
    supabase_project_id: str = "acptpimmuyvhjrsmzltc"
    supabase_project_ref: str = "acptpimmuyvhjrsmzltc"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
