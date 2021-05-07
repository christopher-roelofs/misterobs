import paramiko
from paramiko import SSHException
import config
import logger

SETTINGS = config.get_config()
client = None


def send_command(command):
    stdout = []
    try:
        stdin, stdout, stderr = client.exec_command(command)
        stdout=stdout.readlines()
        return stdout
    except SSHException as e:
        logger.error(repr(e))
        quit()

try:
    logger.info("Attempting to connect to Mister ...")
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SETTINGS['main']['mister_ip'],22, username=SETTINGS['main']['mister_username'], password=SETTINGS['main']['mister_password'])
except Exception as e:
    logger.error(repr(e))
    quit()

if __name__ == "__main__":
    pass