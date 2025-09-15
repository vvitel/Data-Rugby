from boto3 import session
from os import getenv

class Bucket:

    SPACES_NAME = "match-spaces"

    def __init__(self):
        if getenv("BUCKET_ENDPOINT") is None:
            raise ValueError("Environment variable 'BUCKET_ENDPOINT' is not set.")

        if getenv("BUCKET_ACCESS_ID") is None:
            raise ValueError("Environment variable 'BUCKET_ACCESS_ID' is not set.")

        if getenv("BUCKET_SECRET_KEY") is None:
            raise ValueError("Environment variable 'BUCKET_SECRET_KEY' is not set.")

        active_session = session.Session()
        self.client = active_session.client(
            "s3",
            endpoint_url=getenv("BUCKET_ENDPOINT"),
            aws_access_key_id=getenv("BUCKET_ACCESS_ID"),
            aws_secret_access_key=getenv("BUCKET_SECRET_KEY"),
        )

    def upload_video(self, path_file, output_name):
        self.client.upload_file(path_file, Bucket.SPACES_NAME, output_name)

    def get_video(self, name):
        response = self.client.get_object(Bucket=Bucket.SPACES_NAME, Key=name)
        return response["Body"].read()