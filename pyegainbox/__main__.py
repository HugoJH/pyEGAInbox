import plac
from pyegainbox.pyegainbox import pyEGAInbox

if __name__ == '__main__':
    @plac.pos('host', help="remote EGA host address")
    @plac.pos('username', help="EGA Inbox username")
    @plac.pos('op', help="pyEGAInbox operation", choices=[ "upload", "download", "list" ])
    @plac.pos('remote_path', help="Remote dataset path")
    @plac.opt('local_path', help="Local dataset path")
    def main(host, username, op, remote_path, local_path=None):
        inbox = pyEGAInbox(host, username)
        if op == "upload":
            inbox.upload(local_path,remote_path)
        elif op == "download":
            inbox.download(remote_path,local_path)
        elif op == "list":
            inbox.list_dir(remote_path)
        else:
            print("Unknown operation ", op)

    plac.call(main)

