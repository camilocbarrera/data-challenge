import pandas as pd
import paramiko


class SFTPClient:
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.sftp = self._connect()

    def _connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp

    def read_bytes_to_dataframe(self, remote_path, sep=',', **kwargs):
        remote_file = self.sftp.open(remote_path)
        file_content = remote_file.read()
        remote_file.close()

        # Assuming the content is in CSV format
        data = pd.read_csv(pd.compat.StringIO(file_content.decode()), sep=sep, **kwargs)
        return data

    def close(self):
        self.sftp.close()

