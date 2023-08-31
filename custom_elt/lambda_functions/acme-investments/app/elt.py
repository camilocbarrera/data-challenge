from utils.clients.snowclient import SnowflakeConnection
from utils.clients.sftpclient import SFTPClient
from utils.clients.aws import S3Storage
from datetime import datetime


class Extraction:
    def __init__(self, list_id):
        self.list_id = list_id
        self.snow_connection = SnowflakeConnection()
        self.sftpclient = SFTPClient()
        self.s3storage = S3Storage()
