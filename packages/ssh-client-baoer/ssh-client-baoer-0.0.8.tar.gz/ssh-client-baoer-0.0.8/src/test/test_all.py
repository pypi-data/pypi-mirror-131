import os
import time
import unittest

from ..ssh_client.client import SSHClient


def str_time(fmt="%Y%m%d%H%M%S"):
    return time.strftime(fmt, time.localtime())


class TestClient(unittest.TestCase):

    def test_functions(self):
        ssh = SSHClient(os.getenv('HOST'), os.getenv('USER'), os.getenv('PASSWD'))
        ssh.connect()
        test_file = str_time() + ".log"
        ssh.exec(f"echo \"Hello World\" > /tmp/{test_file}")
        ssh.download_working(f'/tmp/{test_file}')
        ssh.download(f'/tmp/{test_file}', os.path.join(os.path.abspath(os.curdir), f'rename-{test_file}'))
        ssh.upload(os.path.join(os.path.abspath(os.curdir), f'{test_file}'), '/tmp')
        ssh.upload_working(f'rename-{test_file}', '/tmp')
        ssh.close()


if __name__ == '__main__':
    unittest.main()
