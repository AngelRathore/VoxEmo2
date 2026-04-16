import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server
    port: int = 8000
    host: str = "0.0.0.0"

    # Model paths
    model_dir: str = "./models"
    model_file: str = "emotion_keras_model_22113034.h5"
    scaler_file: str = "minmax_scaler_22113034.pkl"
    pca_file: str = "pca_transform_22113034.pkl"

    # Audio constraints
    max_audio_size_mb: int = 10
    max_audio_duration_sec: int = 30
    audio_sample_rate: int = 22050
    audio_feature_duration: int = 3

    # Database
    database_url: str = "sqlite:///./voxemo.db"

    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama3-8b-8192"

    @property
    def model_path(self) -> str:
        return os.path.join(self.model_dir, self.model_file)

    @property
    def scaler_path(self) -> str:
        return os.path.join(self.model_dir, self.scaler_file)

    @property
    def pca_path(self) -> str:
        return os.path.join(self.model_dir, self.pca_file)

    @property
    def max_audio_bytes(self) -> int:
        return self.max_audio_size_mb * 1024 * 1024

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
