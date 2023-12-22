# sftp_client_manager

import paramiko
import os

class SFTPClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def upload_file(self, local_path, remote_path):
        with paramiko.Transport((self.host, self.port)) as transport:
            transport.connect(username=self.username, password=self.password)
            with paramiko.SFTPClient.from_transport(transport) as sftp:
                sftp.put(local_path, remote_path)
                print(f"File uploaded to {remote_path}")

    def close(self):
        # Close the connection (if applicable)
        pass
