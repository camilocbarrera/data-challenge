from utils.clients.snowclient import SnowflakeConnection
from utils.clients.sftpclient import SFTPClient
from utils.clients.aws import S3Storage
from datetime import datetime
import tempfile
import os


class Extraction:
    def __init__(self, file_name, remote_path):
        self.file_name = file_name
        self.remote_path = remote_path
        self.snow_connection = SnowflakeConnection()
        self.sftpclient = SFTPClient()
        self.s3storage = S3Storage()

    def extract_and_load(self):
        self.sftpclient.connect()
        with tempfile.TemporaryDirectory() as temp_dir:
            local_xlsx_path = os.path.join(temp_dir, "downloaded_file.xlsx")
            local_csv_path = os.path.join(temp_dir, "converted_file.csv")

            # remote_path = '/acme-investments/Loan Tape.xlsx'
            # remote_path = "/acme-investments/Repayments.xlsx"

            self.sftpclient.download_xlsx_to_csv(
                remote_path=self.remote_path,
                local_xlsx_path=local_xlsx_path,
                local_csv_path=local_csv_path
            )

            self.s3storage.put_csv_to_s3(temp_csv_path=local_csv_path, s3_key=f"acme-investments/{self.file_name}")

        self.sftpclient.disconnect()

        return {
            "message:": "success"
        }
