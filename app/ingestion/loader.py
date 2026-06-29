import boto3
from app.config import settings
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader

def load_document(file_path: str):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.md'):
        loader = UnstructuredMarkdownLoader(file_path)
    else:
        loader = TextLoader(file_path)
    return loader.load()

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

def download_documents_from_s3(prefix: str = "") -> List[str]:
    """Download all files from S3 bucket under a prefix to a temp folder."""
    bucket = settings.AWS_S3_BUCKET
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    local_paths = []
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith('/'):  # skip folders
            continue
        local_file = f"/tmp/{key.split('/')[-1]}"  # simple name
        s3_client.download_file(bucket, key, local_file)
        local_paths.append(local_file)
    return local_paths