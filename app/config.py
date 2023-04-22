from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname:str="localhost"
    database_port:str="port"
    database_password:str="password"
    database_name:str="database_name"
    database_username:str="username"
    secret_key:str="secret_key"
    algorithm:str="algorithm"
    access_token_expiry:str="access_token_expiry"

    class Config:
        env_file = ".env"



setting =Settings()