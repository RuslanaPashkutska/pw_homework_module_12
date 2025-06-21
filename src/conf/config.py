from dotenv import load_dotenv
import os

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path)


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../../.env', extra='ignore')
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_minutes: int = 30
    refresh_token_expire_days: int = 7
    debug: bool = False

settings = Settings()

print("DB URL:", settings.database_url)
print("Debug mode:", settings.debug)