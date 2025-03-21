import requests
import io


def fetch_s3_file(file_url):
    """Fetches a file from S3 and returns it as an in-memory BytesIO object."""
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        return io.BytesIO(response.content)  # Return as an in-memory file object

    except requests.exceptions.RequestException as e:
        print(f"Error fetching file: {e}...")
        return None
