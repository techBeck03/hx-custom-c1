'''
Author: Brandon Beck
Purpose: Prompts user for password to encypt then creates an ansible vault string
'''

from getpass import getpass
from os import getenv
from typing import Text, Union
import subprocess
import shlex
import sys
from pathlib import Path

# Globals
PASSWORD_FILE = 'vault_pass'
FILE_TO_ENCRYPT = 'encryptme'

# Get encryption type from environment variable (default is `text` variable.  Supported options are 'text|file')
ENCRYPTION_TYPE = getenv('ENCRYPTION_TYPE', 'text')

# Function to execute shell commands
def run_sys_command(command_string: Text) -> Union[Text, None]:
    process = subprocess.Popen(shlex.split(command_string),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True)
    for line in process.stdout:
        latest_line = line.rstrip()
        print(latest_line)
    process.wait()
    if process.returncode != 0:
        print(f"An error occurred running command: {command_string}")
        sys.exit(1)
    return

def main():
    if ENCRYPTION_TYPE == 'text':
        # Prompt user for password to encrypt
        print("Please enter the password to encrypt")
        password = getpass(prompt='Password: ', stream=None)
        run_sys_command(f'ansible-vault encrypt_string --vault-password-file {PASSWORD_FILE} {password} --name "secret"')
    elif ENCRYPTION_TYPE == 'file':
        source = Path(FILE_TO_ENCRYPT)
        temp = Path('tempfile')
        temp.write_text(source.read_text())
        run_sys_command(f'ansible-vault encrypt --vault-password-file {PASSWORD_FILE} tempfile')
        source.write_text(temp.read_text())
        print('Your file has now been encrypted')

if __name__ == "__main__":
    main()