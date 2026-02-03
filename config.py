from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_Name:str="QuickPay API"
    DATABASE_URL:str="sqlite:///./quick.db"
    SECRET_KEY:str
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int =30
    model_config={
        "env_file":".env",
        "env_file_encoding":"utf-8",
    }

settings=Settings()
