from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    jwt_token: SecretStr = Field(validation_alias="JWT_TOKEN")
    endpoint_url: str = Field(validation_alias="ENDPOINT_URL")
    region: str = Field(validation_alias="REGION")
    aws_access_key_id: SecretStr = Field(validation_alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: SecretStr = Field(validation_alias="AWS_SECRET_ACCESS_KEY")
