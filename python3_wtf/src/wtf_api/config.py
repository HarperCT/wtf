"""API configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    api_title: str = "WheresTheFault API"
    api_version: str = "0.1.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS settings
    cors_origins: list[str] = ["*"]
    
    # Execution settings
    default_timeout: int = 5
    default_output_dir: str = "/tmp"
    max_concurrent_default: int | None = None
    
    class Config:
        env_prefix = "WTF_"
        case_sensitive = False


settings = Settings()
