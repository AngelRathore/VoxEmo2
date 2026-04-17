from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    port: int = Field(default=8000)
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"]
    )

    model_dir: str = Field(default="./models")
    model_file: str = Field(default="emotion_keras_model_22113034.h5")
    scaler_file: str = Field(default="minmax_scaler_22113034.pkl")
    pca_file: str = Field(default="pca_transform_22113034.pkl")

    max_audio_size_mb: int = Field(default=10)
    max_audio_duration_sec: int = Field(default=30)

    # ✅ ADD THESE TWO LINES
    audio_sample_rate: int = Field(default=22050)
    audio_feature_duration: int = Field(default=3)

    database_url: str = Field(default="sqlite:///./voxemo.db")

    groq_api_key: str = Field(default="")
    groq_model: str = Field(default="llama3-8b-8192")


settings = Settings()