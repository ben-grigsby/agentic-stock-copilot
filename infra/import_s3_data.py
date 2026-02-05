import boto3
import os
from dotenv import load_dotenv

def download_from_s3(bucket_name, s3_key, local_path):
    """
    Downloads a file from an S3 bucket.
    """
    load_dotenv()
    
    aws_access_key_id = os.getenv("AWS_S3_KEY")
    aws_secret_access_key = os.getenv("AWS_S3_SECRET_KEY")
    
    if not aws_access_key_id or not aws_secret_access_key:
        print("Error: AWS credentials not found in .env file.")
        return False
        
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        
        print(f"Downloading {s3_key} from bucket {bucket_name} to {local_path}...")
        s3.download_file(bucket_name, s3_key, local_path)
        print("Download successful!")
        return True
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

if __name__ == "__main__":
    bucket = "stock-copilot-data" # just change this to edit which data to pull
    key = "raw/daily_bars.csv" # just change this to edit which data to pull
    destination = "data/raw/daily_bars.csv"
    
    # Ensure local directory exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    download_from_s3(bucket, key, destination)
