from pydantic import BaseSettings, Field


class OcrSettings(BaseSettings):
    data_path: str = Field(..., env="TESSDATA_PREFIX")

    class Config:
        env_file = ".env"
