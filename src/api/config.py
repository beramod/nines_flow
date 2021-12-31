import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    nines_flow_env: str

    class Config:
        env_file = ".env"
config = Settings()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))