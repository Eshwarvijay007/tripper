from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Naomi-like Travel API"
    environment: str = "dev"
    enable_auth: bool = False  # bypass auth for now
    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]


settings = Settings()

