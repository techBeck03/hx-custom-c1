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

# Get Password file if defined
PASSWORD_FILE = '/app/vault_pass'

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
    # Prompt user for password to encrypt
    print("Please enter the password to encrypt")
    password = getpass(prompt='Password: ', stream=None)
    run_sys_command(f'ansible-vault encrypt_string --vault-password-file {PASSWORD_FILE} {password} --name "secret"')

if __name__ == "__main__":
    main()