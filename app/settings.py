import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_OPENAI_KEY: str = os.getenv("AZURE_OPENAI_KEY")
    AZURE_API_VERSION : str = os.getenv("AZURE_API_VERSION")
    AZURE_ENDPOINT : str = os.getenv("AZURE_ENDPOINT")
    AZURE_DEPLOYMENT : str = os.getenv("AZURE_DEPLOYMENT")
    AZURE_DEPLOYMENT_EMBEDDING : str = os.getenv("AZURE_DEPLOYMENT_EMBEDDING")

    POSTGRE_CONNECTION_STR: str = os.getenv("POSTGRE_CONNECTION_STR")

settings = Settings()