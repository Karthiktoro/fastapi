from pydantic_settings import  BaseSettings

class Settings(BaseSettings):
    database_username : str
    database_name : str
    database_password : str
    database_port: str
    database_hostname : str
    algorithm : str
    ACCESS_TOKEN_EXPIRE_TIME: int
    secrete_key : str 

    class Config :
        env_file = ".env"

settings = Settings()