import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from config.config import settings

def upload_file_to_s3(file: UploadFile) -> str:
    bucket_name = settings.BUCKET_NAME
    region = settings.REGION
    access_key = settings.ACCESS_KEY
    secret_key = settings.SECRET_ACCESS

    s3 = boto3.client('s3', region_name=region,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

    try:
        s3.upload_fileobj(file.file, bucket_name, file.filename)
        return f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"
    except NoCredentialsError:
        print('Credentials not available')
        return None
