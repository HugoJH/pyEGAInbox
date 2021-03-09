"""This file contain the pyEGAInbox class"""
import socket
from os.path import join,basename, expanduser
from paramiko import Transport as pm_transport
from paramiko import SSHClient as pm_ssh
from paramiko import RSAKey

class pyEGAInbox:
    """class that handles sftp connection to EGA Inbox Server """
    def __init__(self, host, username, password=None,
                 pkey=RSAKey(filename=join(expanduser("~"),".ssh/id_rsa"))):
        #pm_log("paramiko.log")
        ssh_client = pm_ssh()
        self.get_host_key(host)
        ssh_client.get_host_keys().add(host, 'ssh-rsa', self.k)
        if password is not None:
            ssh_client.connect(hostname=host, username=username, password=password)
        else:
            ssh_client.connect(hostname=host, username=username, pkey=pkey)
        self.sftp = ssh_client.open_sftp()

    def get_host_key(self,host,port=22):
        """This function retrieves public key from remote EGA Inbox Server"""
        sock = socket.socket()
        sock.connect((host, port))
        trans = pm_transport(sock)
        trans.start_client()
        self.k = trans.get_remote_server_key()

    def upload(self, local_path, remote_path):
        """This function gets local path file and uploads via ftp to remote_path"""
        self.sftp.put(local_path, join(remote_path, basename(local_path)))

    def download(self, remote_path, local_path):
        """This function gets a remote_path file and downloads via ftp to a local_path"""
        self.sftp.get(remote_path, local_path)
