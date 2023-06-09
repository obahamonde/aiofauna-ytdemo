from typing import Optional

from pydantic import BaseConfig, BaseSettings, Field


class Env(BaseSettings):
    """Environment Variables"""

    env_str: Optional[str]

    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"

    FAUNA_SECRET: str = Field(..., env="FAUNA_SECRET")
    OAUTH2_DOMAIN: str = Field(..., env="AUTH0_DOMAIN")
    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: str = Field(..., env="AWS_S3_BUCKET")
    AWS_S3_ENDPOINT: str = Field(..., env="AWS_S3_ENDPOINT")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    IP_ADDR: str = Field(..., env="IP_ADDR")
    CF_ZONE_ID: str = Field(..., env="CF_ZONE_ID")
    CF_EMAIL: str = Field(..., env="CF_EMAIL")
    CF_API_KEY: str = Field(..., env="CF_API_KEY")
    CF_ACCOUNT_ID: str = Field(..., env="CF_ACCOUNT_ID")

env = Env()