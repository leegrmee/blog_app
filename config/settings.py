from pydantic import BaseModel


class Settings(BaseModel):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_S3_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"


settings = Settings()
