"""Settings"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    General settings for the service
    """
    project_name: str = "Crypto Alert API"
    api_version: int = 1
    host: str = "0.0.0.0"
    port: int = 7000
    error_topic: str = "Unknown-Crypto-Alert"
    log_level: str = "debug"
    hot_reload: bool = False
