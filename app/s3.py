import boto3
from loguru import logger

from app.config import Config

# TODO move to config
BUCKET_NAME = "pabd25"
FILE_PATH = "../models/model.pkl"
OBJECT_NAME = "pyatikh/models/model.pkl"


class S3Client:

    def __init__(self, config: Config):
        try:
            s3_client = boto3.client(
                "s3",
                endpoint_url=config.endpoint_url,
                aws_access_key_id=config.aws_access_key_id.get_secret_value(),
                aws_secret_access_key=config.aws_secret_access_key.get_secret_value(),
                region_name=config.region,
            )

            self._client = s3_client
            self._config = config
        except Exception:
            logger.exception("Failed to create S3 client")

    def download_model(self):
        try:
            self._client.download_file(
                BUCKET_NAME,
                OBJECT_NAME,
                FILE_PATH,
            )
        except Exception:
            logger.exception("Failed to download file")
