import os
import boto3
from config.Connection import prisma_connection
from config.settings import settings
import logging
import asyncio


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


async def migrate_files():
    try:
        await prisma_connection.connect()

        s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        bucket_name = settings.AWS_S3_BUCKET_NAME

        files = await prisma_connection.prisma.file.find_many()
        logger.info(f"Found {len(files)} files to migrate")

        for file_record in files:
            local_file_path = os.path.join(BASE_DIR, file_record.path)
            if os.path.exists(local_file_path):
                try:
                    s3_key = file_record.path
                    file_size = os.path.getsize(local_file_path)

                    with open(local_file_path, "rb") as data:
                        s3_client.upload_fileobj(
                            data,
                            bucket_name,
                            s3_key,
                            ExtraArgs={
                                "ContentType": file_record.mimetype,
                                "ACL": "private",
                            },
                        )

                    logger.info(f"Uploaded file {file_record.path} to S3")

                    await prisma_connection.prisma.file.update(
                        where={"id": file_record.id},
                        data={"size": file_size},
                    )

                except Exception as e:
                    logger.error(f"Error uploading file {file_record.path}: {e}")

            else:
                logger.info(f"File {file_record.path} does not exist locally")

    except Exception as e:
        logger.critical(f"Migration failed: {e}")

    finally:
        await prisma_connection.disconnect()


if __name__ == "__main__":
    asyncio.run(migrate_files())
    print("Migration completed")
