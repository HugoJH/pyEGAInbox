"""This file contain the pyEGAInbox class"""
import socket
from os.path import join,basename, expanduser
from pyegainbox.ssh_credentials import SSHCredentials
from pyegainbox.ssh_session import SSHSession

class pyEGAInbox:
    """class that handles sftp connection to EGA Inbox Server """
    def __init__(self, host, username):
        self.private_key_path = expanduser("~" + username) + "/.ssh/" + username + ".egakeys"
        self.public_key_path = self.private_key_path + "pub"
        self.packed_keys_path = self.private_key_path + ".packed"

        try:
            self._load_credentials(username)
        except SystemExit as se:
            print ("File", self.packed_keys_path, " not found")
            print ("Creating new credentials in ", self.packed_keys_path)
            self._create_credentials(host, username)
        self._create_session(self.credentials)



    def _load_credentials(self, username):
        self.credentials = SSHCredentials(host='', userid='', generate_key=False, look_for_keys=True)
        self.credentials.load_from_file(self.packed_keys_path)

    def _create_credentials(self, host, username):
        self.credentials = SSHCredentials(host=host, userid=username, generate_key=False, look_for_keys=True)
        self.credentials.generate_key()
        self.credentials.save(output_path=self.packed_keys_path, public_key_path=self.public_key_path,
                              private_key_path=self.private_key_path)

    def _create_session(self, credentials):
        self.session = SSHSession(credentials,credentials_path=self.packed_keys_path)

    def upload(self, local_path, remote_path):
        """This function gets local path file and uploads via ftp to remote_path"""
        self.session.run_sftp("put", input_file_path=local_path,
                              output_file_path=remote_path)

    def download(self, remote_path, local_path):
        """This function gets a remote_path file and downloads via ftp to a local_path"""
        self.session.run_sftp("get", input_file_path=remote_path,
                              output_file_path=local_path)

    def list_dir(self, remote_path):
        """This function gets a remote_path file and downloads via ftp to a local_path"""
        print(self.session.run_sftp("listdir", input_file_path=remote_path))
