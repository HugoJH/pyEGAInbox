""" Module to manage ssl credentials and session """
__author__ = "gelpi"
__date__ = "$08-March-2019 17:32:38$"

import sys
import os
import stat
import pickle
import paramiko
from io import StringIO
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException, RSAKey

class SSHSession():
    """ Class wrapping ssh operations
        Args:
            * ssh_data (**SSHCredentials**): SSHCredentials object
            * credentials_path (**str**): Path to packed credentials file to use
            * debug (**bool**): Prints verbose debug information on connection
    """

    def __init__(self, ssh_data=None, credentials_path=None, debug=False):
        if ssh_data is None:
            self.ssh_data = SSHCredentials(credentials_path is None)
            if credentials_path:
                self.ssh_data.load_from_file(credentials_path)
        else:
            self.ssh_data = ssh_data
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())

        if debug:
            paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

        try:
            self.ssh.connect(
                self.ssh_data.host,
                username=self.ssh_data.userid,
                pkey=self.ssh_data.key,
                look_for_keys=self.ssh_data.look_for_keys
            )
        except AuthenticationException as err:
            sys.exit(err)
        except SSHException as err:
            sys.exit(err)

    def run_command(self, command):
        """ Runs command on remote, produces stdout, stderr tuple
            Args:
                * command (**str**): Command to execute on remote
        """
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(command)
        return ''.join(stdout), ''.join(stderr)


    def run_sftp(self, oper, input_file_path, output_file_path=''):
        """ Runs SFTP session on remote
            Args:
                * oper (**str**): Operation to perform, one of
                    * get (gets a single file from input_file_path (remote) to output_file_path (local) )
                    * put (puts a single file from input_file_path (local) to output_file_path (remote)
                    * create (creates a file in output_file_path (remote) from input_file_path string-
                    * file (opens a remote file in input_file_path for read). Returns a file handle.
                    * listdir (returns a list of files in remote input_file_path
                * input_file_path (**str**): Input file path or input string
                * output_file_path (**str**): Output file path
        """
        sftp = self.ssh.open_sftp()
        try:
            if oper == 'get':
                sftp.get(input_file_path, output_file_path)
            elif oper == 'put':
                sftp.put(input_file_path, output_file_path)
            elif oper == 'create':
                with sftp.file(output_file_path, "w") as remote_fileh:
                    remote_fileh.write(input_file_path)
#            elif oper == 'open':
#                return sftp.open(input_file_path)
            elif oper == 'file':
                with sftp.file(input_file_path, "r") as remote_file:
                    return remote_file.read().decode()
            elif oper == "listdir":
                return sftp.listdir(input_file_path)
#            elif oper == 'rmdir':
#                return sftp.rmdir(input_file_path)
            elif oper == 'lstat':
                return sftp.lstat(input_file_path)
            else:
                print('Unknown sftp command', oper)
                return True
        #TODO check appropriate errors
        except IOError as err:
            sys.exit(err)
        return False

