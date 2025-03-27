import requests
import io
import boto3
import os


def fetch_s3_file(bucket_name,file_key):
    """Fetches a file from S3 and returns it as an in-memory BytesIO object."""
    try:
        # Create a session using your access keys
        session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        s3 = session.resource('s3')
        obj = s3.Object(bucket_name, file_key)

        # Get the file content
        file_content = obj.get()['Body'].read()

        return io.BytesIO(file_content)  # Return as an in-memory file object

    except Exception as e:
        print(f"Error fetching file: {e}...")
        return None
