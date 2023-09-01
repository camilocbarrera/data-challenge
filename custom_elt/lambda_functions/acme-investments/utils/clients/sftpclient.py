import pandas as pd
import paramiko
import os
from dotenv import load_dotenv
from utils.utils import standardize_columns

load_dotenv()


class SFTPClient:
    def __init__(self):
        self.hostname = os.getenv("SFTP_HOSTNAME")
        self.username = os.getenv("SFTP_USERNAME")
        self.password = os.getenv("SFTP_PASSWORD")
        self.port = 22
        self.transport = None
        self.sftp = None

    def connect(self):
        self.transport = paramiko.Transport((self.hostname, self.port))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def disconnect(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()

    def download_xlsx_to_csv(self, remote_path, local_xlsx_path, local_csv_path):
        if not self.sftp:
            raise Exception(
                "SFTP connection not established. Call the connect() method first."
            )

        self.sftp.get(remote_path, local_xlsx_path)

        xlsx_df = pd.read_excel(local_xlsx_path, engine="openpyxl")

        cleaned_df = standardize_columns(xlsx_df)

        cleaned_df.to_csv(local_csv_path, index=False)

        meta_response = {
            "shape": cleaned_df.shape,
            "local_csv_path": local_csv_path
        }
        return meta_response
