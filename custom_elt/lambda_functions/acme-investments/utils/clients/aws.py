import json
import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class S3Storage:
    def __init__(self, bucket_name="raw-clickup-bucket"):
        self.access_key = os.getenv("S3_ACCESS_KEY")
        self.secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY")
        self.bucket_name = bucket_name

    def put_json_to_s3(self, json_data, s3_key):
        try:
            json_string = json.dumps(json_data)
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
            )
            s3_client.put_object(Body=json_string, Bucket=self.bucket_name, Key=s3_key)
        except Exception as e:
            print("An error occurred while connecting to S3:", str(e))
            raise e  # Optionally, you may want to re-raise the exception to handle it at a higher level

    def format_datetime_with_seconds(self, dt, date_separator, time_separator):
        return dt.strftime(
            f"%Y{date_separator}%m{date_separator}%d{date_separator}%H{time_separator}%M{time_separator}%S"
        )
